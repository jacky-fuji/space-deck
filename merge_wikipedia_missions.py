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
    
    # Keyword fallback
    if "japan" in location or "kii" in location or "tanegashima" in location or "uchinoura" in location: return "Japan"
    if "russia" in location or "plesetsk" in location or "vostochny" in location or "baikonur" in location or "kazakhstan" in location: return "Russia"
    if "china" in location or "jiuquan" in location or "xichang" in location or "taiyuan" in location or "wenchang" in location or "hainan" in location: return "China"
    if "usa" in location or "canaveral" in location or "vandenberg" in location or "kennedy" in location or "wallops" in location or "boca chica" in location or "starbase" in location: return "USA"
    if "france" in location or "guiana" in location or "kourou" in location or "csg" in location: return "France"
    if "india" in location or "sriharikota" in location or "sdsc" in location or "shar" in location: return "India"
    if "new zealand" in location or "mahia" in location or "rocket lab" in location: return "New Zealand"
    if "australia" in location or "woomera" in location or "bowen" in location: return "Australia"
    if "brazil" in location or "alcantara" in location: return "Brazil"
    if "israel" in location or "palmachim" in location: return "Israel"
    if "n. korea" in location or "sohae" in location: return "North Korea"
    if "s. korea" in location or "naro" in location or "jeju" in location: return "South Korea"
    
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
                m["siteId"] = get_country(m["location"]).lower().replace(" ", "-")
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
