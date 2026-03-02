import json
import os
import re

MISSIONS_FILE = "src/app/data/missions.json"

SITE_TO_COUNTRY = {
    # Abbreviated dictionary for lookup
    "Cape Canaveral": "USA", "Kennedy": "USA", "Vandenberg": "USA", "Boca Chica": "USA", "Wallops": "USA", "Kodiak": "USA", "Omelek": "USA", "Point Arguello": "USA", "Starbase": "USA", "CC": "USA", "VSFB": "USA", "MARS": "USA",
    "Wenchang": "China", "Jiuquan": "China", "Xichang": "China", "Taiyuan": "China", "Hainan": "China", "Yellow Sea": "China", "Haiyang": "China", "JQ": "China", "XSC": "China", "TYSC": "China", "WEN": "China", "HCSLS": "China", "HHAI": "China",
    "Baikonur": "Russia", "Plesetsk": "Russia", "Vostochny": "Russia", "Kapustin Yar": "Russia", "Svobodny": "Russia", "Dombarovsky": "Russia", "Yasny": "Russia", "VOST": "Russia", "NIIP-5": "Russia", "GIK-5": "Russia",
    "Tanegashima": "Japan", "Uchinoura": "Japan", "Kagoshima": "Japan", "Kii": "Japan", "Taiki": "Japan", "Kushimoto": "Japan", "TNSC": "Japan",
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
    for site, country in SITE_TO_COUNTRY.items():
        if site.lower() in location:
            return country
    return "Unknown"

def fix_data():
    if not os.path.exists(MISSIONS_FILE):
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    fixed_misaligned = 0
    removed_payloads = 0
    
    cleaned_missions = []
    
    known_sites = [k.lower() for k in SITE_TO_COUNTRY.keys()]

    for m in missions:
        rocket = str(m.get("rocketName", "")).lower()
        provider = str(m.get("provider", ""))
        loc = str(m.get("location", ""))
        
        # 1. Drop bad 'payload as rocket' records
        # These are usually Wikipedia scraped lists that grabbed the description cell.
        if "launch of" in rocket or len(rocket) > 40 or "will be the first" in rocket:
            removed_payloads += 1
            continue # Drop this record entirely as it's junk data
            
        # 2. Fix misaligned provider/location
        # Provider field accidentally got the Launch Site
        # Location field accidentally got the Payload or Mission ID
        provider_lower = provider.lower()
        
        is_provider_a_site = any(site in provider_lower for site in known_sites)
        is_loc_a_payload = "starlink" in loc.lower() or "f9-" in loc.lower() or "four of a kind" in loc.lower() or "y3" == loc.lower()
        
        if is_provider_a_site and (is_loc_a_payload or m.get("missionName") == "Unknown" or len(m.get("missionName", "")) < 2):
            # Swap them around
            real_location = provider
            real_payload = loc if loc and loc != "Unknown" else "Unknown Payload"
            
            # If missionName was empty, put the payload there
            if m.get("missionName") in ["", "Unknown"]:
                m["missionName"] = real_payload
            
            m["location"] = real_location
            m["provider"] = "Unknown" # Since we don't know the real provider now
            
            # Calculate new siteId
            new_country = get_country(real_location)
            if new_country != "Unknown":
                m["siteId"] = new_country.lower().replace(" ", "-")
                
            fixed_misaligned += 1
            cleaned_missions.append(m)
            continue
            
        cleaned_missions.append(m)

    print(f"Removed {removed_payloads} junk payloads misidentified as rockets.")
    print(f"Fixed {fixed_misaligned} misaligned location/provider fields.")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_missions, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(cleaned_missions)} cleaned missions.")

if __name__ == "__main__":
    fix_data()
