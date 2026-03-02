import json
import os
from collections import Counter

MISSIONS_FILE = "src/app/data/missions.json"

SITE_TO_COUNTRY = {
    "Cape Canaveral": "USA", "Kennedy": "USA", "Vandenberg": "USA", "Boca Chica": "USA", "Wallops": "USA", "Kodiak": "USA", "Omelek": "USA", "Point Arguello": "USA", "Starbase": "USA", "CC": "USA", "VSFB": "USA", "MARS": "USA",
    "Wenchang": "China", "Jiuquan": "China", "Xichang": "China", "Taiyuan": "China", "Hainan": "China", "Yellow Sea": "China", "Haiyang": "China", "JQ": "China", "XSC": "China", "TYSC": "China", "WEN": "China", "HCSLS": "China", "HHAI": "China", "SLA": "China",
    "Baikonur": "Russia", "Plesetsk": "Russia", "Vostochny": "Russia", "Kapustin Yar": "Russia", "Svobodny": "Russia", "Dombarovsky": "Russia", "Yasny": "Russia", "VOST": "Russia", "NIIP-5": "Russia", "GIK-5": "Russia", "GIK-1": "Russia",
    "Tanegashima": "Japan", "Uchinoura": "Japan", "Kagoshima": "Japan", "Kii": "Japan", "Taiki": "Japan", "Kushimoto": "Japan", "TNSC": "Japan", "KSC": "Japan", # Need to be careful with KSC
    "Kourou": "France", "Guiana": "France", "CSG": "France",
    "Satish Dhawan": "India", "Sriharikota": "India", "SDSC": "India", "SHAR": "India",
    "Mahia": "New Zealand", "Rocket Lab": "New Zealand",
    "Palmachim": "Israel", "Palmachim Airbase": "Israel", "PALB": "Israel",
    "Sohae": "North Korea", "Tonghae": "North Korea",
    "Naro": "South Korea", "Jeju": "South Korea",
    "Semnan": "Iran", "Shahroud": "Iran",
    "Woomera": "Australia", "Bowen": "Australia", "Abbot Point": "Australia",
    "Alcantara": "Brazil", "ALCA": "Brazil",
    "Andøya": "Norway", "Andoya": "Norway",
    "Esrange": "Sweden"
}

def get_country(location):
    location = (location or "").lower()
    
    # KSC conflict resolution (Kennedy vs Kagoshima)
    if "ksc" in location and "japan" not in location:
        return "USA"
        
    for site, country in SITE_TO_COUNTRY.items():
        if site.lower() in location:
            return country
    return "Unknown"

def deep_clean():
    if not os.path.exists(MISSIONS_FILE):
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    cleaned = []
    removed = []
    updated_sites = 0

    known_sites_lower = [k.lower() for k in SITE_TO_COUNTRY.keys()]

    for m in missions:
        rocket = str(m.get("rocketName", "")).strip()
        provider = str(m.get("provider", "")).strip()
        loc = str(m.get("location", "")).strip()
        payload = str(m.get("missionName", "")).strip()
        
        # 1. Catch more payloads disguised as rockets
        if any(bad in rocket.lower() for bad in [" satellites", " launch to", "first crewed", " space centre", "space center", "december ", "january ", "february ", "march ", "april ", "may ", "june ", "july ", "august ", "september ", "october ", "november "]):
            removed.append(m)
            continue
            
        if len(rocket) > 30 and ("." in rocket or "," in rocket or " and " in rocket or " to " in rocket):
           removed.append(m)
           continue
           
        # 2. Fix Provider holding Location
        is_provider_location = any(s in provider.lower() for s in known_sites_lower) and len(provider) > 3
        if is_provider_location and loc in ["", "Unknown", "Unknown Site"]:
            loc = provider
            provider = "Unknown"
            m["location"] = loc
            m["provider"] = provider
            m["siteId"] = get_country(loc).lower().replace(" ", "-")
            updated_sites += 1
            
        # 3. Force update all siteIds based on the robust logic
        new_country = get_country(loc)
        current_site_id = str(m.get("siteId", "")).lower()
        if new_country != "Unknown" and current_site_id in ["usa", "unknown", "unknown site", ""]:
            m["siteId"] = new_country.lower().replace(" ", "-")
            updated_sites += 1

        cleaned.append(m)

    print(f"Removed {len(removed)} records with fundamentally broken text (dates/paragraphs as rockets).")
    print(f"Updated country/site mappings for {updated_sites} records.")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
        
    print(f"Total remaining standard missions: {len(cleaned)}")

if __name__ == "__main__":
    deep_clean()
