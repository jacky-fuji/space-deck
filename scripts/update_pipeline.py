import json
import logging
import os
from datetime import datetime, timezone
import subprocess

# Set up logging
os.makedirs("scripts/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scripts/logs/update_pipeline.log"),
        logging.StreamHandler()
    ]
)

MISSIONS_FILE = "src/app/data/missions.json"
EA_DATA_FILE = "scripts/data/everyday_astronaut_missions.json"

def run_scraper():
    logging.info("Running Everyday Astronaut scraper...")
    result = subprocess.run(["python3", "scripts/processing/scrape_everyday_astronaut.py"], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Scraper failed: {result.stderr}")
        return False
    return True

def merge_data():
    logging.info("Merging new data into missions.json...")
    
    with open(MISSIONS_FILE, "r") as f:
        existing_missions = json.load(f)
        
    try:
        with open(EA_DATA_FILE, "r") as f:
            new_missions = json.load(f)
    except FileNotFoundError:
        logging.error(f"Scraped data file not found: {EA_DATA_FILE}")
        return False

    existing_map = {m["id"]: m for m in existing_missions}
    
    updated_count = 0
    added_count = 0
    status_changed_count = 0
    
    current_time = datetime.now(timezone.utc)

    for nm in new_missions:
        m_id = nm["id"]
        if m_id in existing_map:
            # Check for status updates (e.g., Scheduled -> Success)
            old_status = existing_map[m_id]["status"]
            new_status = nm["status"]
            
            # Update the existing record completely to get new dates/times or payload names
            # But preserve flightCategory if we set it manually
            old_category = existing_map[m_id].get("flightCategory")
            
            existing_map[m_id].update(nm)
            
            if old_category:
                existing_map[m_id]["flightCategory"] = old_category
                
            updated_count += 1
            if old_status != new_status:
                logging.info(f"Status changed for {m_id}: {old_status} -> {new_status}")
                status_changed_count += 1
        else:
            # It's a brand new upcoming or past mission
            existing_missions.append(nm)
            added_count += 1
            logging.info(f"Added new mission: {nm['missionName']} ({nm['date']})")

    # Time-based Fallback: If a Scheduled mission is 2 days past its launch date and hasn't been updated 
    # to Success/Failure by the scraper, we flag it in logs (it might be delayed but the scraper missed it)
    for m in existing_missions:
        if m["status"] == "Scheduled":
            try:
                m_date = datetime.strptime(m["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if (current_time - m_date).days > 2:
                    logging.warning(f"Mission {m['id']} is Scheduled but 2 days past launch time. Needs review.")
            except ValueError:
                pass # ignore poorly formatted dates

    # Re-sort by date descending
    existing_missions.sort(key=lambda x: x["date"], reverse=True)

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_missions, f, ensure_ascii=False, indent=2)

    logging.info(f"Merge complete. Added: {added_count}, Updated: {updated_count}, Status Swaps: {status_changed_count}")
    return added_count > 0 or status_changed_count > 0 or updated_count > 0

if __name__ == "__main__":
    logging.info("Starting Daily Space-Deck Data Pipeline")
    if run_scraper():
        changed = merge_data()
        if changed:
            logging.info("Data was modified. Ready for commit.")
        else:
            logging.info("No meaningful changes detected. Exiting.")
