import json
import os

MISSIONS_FILE = "src/app/data/missions.json"

SITE_TO_COUNTRY = {
    # ... previous mappings
    "Cape Canaveral": "USA", "Kennedy": "USA", "Vandenberg": "USA", "Boca Chica": "USA", "Wallops": "USA", "Kodiak": "USA", "Omelek": "USA", "Point Arguello": "USA", "Starbase": "USA",
    "Wenchang": "China", "Jiuquan": "China", "Xichang": "China", "Taiyuan": "China", "Hainan": "China", "Yellow Sea": "China", "Haiyang": "China",
    "Baikonur": "Russia", "Plesetsk": "Russia", "Vostochny": "Russia", "Kapustin Yar": "Russia", "Svobodny": "Russia", "Dombarovsky": "Russia", "Yasny": "Russia",
    "Tanegashima": "Japan", "Uchinoura": "Japan", "Kagoshima": "Japan", "Kii": "Japan", "Taiki": "Japan", "Kushimoto": "Japan",
    "Kourou": "France", "Guiana": "France", "CSG": "France",
    "Satish Dhawan": "India", "Sriharikota": "India", "SDSC": "India", "SHAR": "India",
    "Mahia": "New Zealand", "Rocket Lab": "New Zealand",
    "Palmachim": "Israel", "Palmachim Airbase": "Israel",
    "Sohae": "North Korea", "Tonghae": "North Korea", "Sohae Satellite Launching Station": "North Korea",
    "Naro": "South Korea", "Jeju": "South Korea", "Kwangmyongsong": "North Korea",
    "Semnan": "Iran", "Shahroud": "Iran", "Shahrud": "Iran",
    "Woomera": "Australia", "Bowen": "Australia", "Abbot Point": "Australia",
    "Alcantara": "Brazil",
    "Andøya": "Norway", "Andoya": "Norway",
    "Esrange": "Sweden"
}

def get_country(location):
    location = (location or "").lower()
    for site, country in SITE_TO_COUNTRY.items():
        if site.lower() in location:
            return country
    return "Unknown"

def scrub():
    if not os.path.exists(MISSIONS_FILE):
        print("File not found.")
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    # 1. Deduplicate by ID
    unique_ids = set()
    deduped = []
    dup_count = 0
    for m in missions:
        if m["id"] not in unique_ids:
            unique_ids.add(m["id"])
            deduped.append(m)
        else:
            dup_count += 1
    
    print(f"Removed {dup_count} duplicate missions.")
    
    # 2. Scrub siteIds
    updated_count = 0
    for m in deduped:
        original_site_id = m.get("siteId", "")
        loc = m.get("location", "")
        
        # Keyword-based fix
        new_country = get_country(loc)
        if new_country != "Unknown":
            suggested_site_id = new_country.lower().replace(" ", "-")
            
            # If current is generic or wrong, update it
            is_generic = original_site_id.lower() in ["usa", "unknown", "unknown site", ""]
            
            # Special case: if loc contains non-USA keyword but siteId is usa
            loc_lower = loc.lower()
            is_mislabeled_usa = (original_site_id.lower() == "usa") and (new_country != "USA")
            
            if is_generic or is_mislabeled_usa:
                m["siteId"] = suggested_site_id
                updated_count += 1

    print(f"Updated {updated_count} mission records for country attribution.")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(deduped)} total missions.")

if __name__ == "__main__":
    scrub()
