import json
import os

MISSING_FILE = "/tmp/missions_to_add.json"
MISSIONS_FILE = "src/app/data/missions.json"

# SITE_TO_COUNTRY mapping
SITE_TO_COUNTRY = {
    "Cape Canaveral": "USA", "Kennedy": "USA", "Vandenberg": "USA", "Boca Chica": "USA", "Wallops": "USA",
    "Wenchang": "China", "Jiuquan": "China", "Xichang": "China", "Taiyuan": "China",
    "Baikonur": "Russia", "Plesetsk": "Russia", "Vostochny": "Russia",
    "Tanegashima": "Japan", "Uchinoura": "Japan",
    "Kourou": "France", "Guiana": "France",
    "Satish Dhawan": "India", "Sriharikota": "India",
    "Mahia": "New Zealand", "Rocket Lab": "New Zealand",
    "Kwajalein": "USA", "Omelek": "USA",
    "Palmachim": "Israel",
    "Sohae": "North Korea", "Tonghae": "North Korea",
    "Naro": "South Korea",
    "Semnan": "Iran", "Shahroud": "Iran"
}

def get_country(location):
    location = (location or "").lower()
    for site, country in SITE_TO_COUNTRY.items():
        if site.lower() in location:
            return country
    return "Unknown"

def main():
    if not os.path.exists(MISSING_FILE):
        print("No missing missions file found.")
        return

    with open(MISSING_FILE, "r") as f:
        new_raw = json.load(f)

    with open(MISSIONS_FILE, "r") as f:
        existing = json.load(f)

    existing_index = set()
    for m in existing:
        existing_index.add((m["date"], m["rocketName"][:10].lower()))

    unique_new = []
    seen_this_pass = set()

    for m in new_raw:
        # Use first 10 chars of rocket name for more precise uniqueness
        rocket_prefix = m["rocketName"][:10].lower()
        key = (m["date"], rocket_prefix)
        
        if key not in existing_index and key not in seen_this_pass:
            if m["status"] == "Success": # Focus on successful orbital missions for now
                m["id"] = f"wiki-{m['date'].replace('-', '')}-{len(unique_new)}"
                m["siteId"] = "usa" if get_country(m["location"]) == "USA" else "unknown"
                # Country resolution check
                country = get_country(m["location"])
                
                unique_new.append(m)
                seen_this_pass.add(key)

    print(f"Filtered {len(new_raw)} raw missions down to {len(unique_new)} unique successful missing missions.")
    
    # Merge and sort
    final_list = existing + unique_new
    final_list.sort(key=lambda x: x["date"], reverse=True)

    print(f"Total missions after merge: {len(final_list)}")
    
    with open(MISSIONS_FILE, "w") as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
    
    print("Missions file updated.")

if __name__ == "__main__":
    main()
