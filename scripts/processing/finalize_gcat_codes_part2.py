import json
import os

MISSIONS_FILE = "src/app/data/missions.json"

FINAL_GCAT_MAP = {
    # Japan
    "F3": "japan", "M4": "japan", "USC": "japan",
    
    # India (PSLV launches from Satish Dhawan)
    "C56": "india", 
    
    # France/ESA (Ariane launches from Kourou)
    "VA261": "france", "VV21": "france",
    
    # USA 
    "SPFLA": "usa", "KLC": "usa",
    
    # Russia (Submarines / Obscure locations)
    "BLA": "russia",
    
    # Spain
    "GANC": "spain",
    
    # South Korea
    "KAU": "south-korea"
}

def finalize():
    if not os.path.exists(MISSIONS_FILE):
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    updated = 0
    removed = 0
    cleaned = []

    for m in missions:
        loc = m.get("location", "").strip()
        site_id = m.get("siteId", "").lower()
        payload = m.get("missionName", "").lower()
        
        # 1. Map known acronyms
        if site_id in ["unknown", ""]:
            if loc in FINAL_GCAT_MAP:
                m["siteId"] = FINAL_GCAT_MAP[loc]
                updated += 1
            # 2. Cleanup last dregs of junk (sounding rockets masquerading as orbital, BB-I, Scout's Arrow)
            elif any(junk in payload for junk in ["bb-i", "scout's arrow", "stronger together", "24 december 2025"]):
                removed += 1
                continue
                
        cleaned.append(m)

    print(f"Mapped {updated} obscure GCAT site codes to countries.")
    print(f"Removed {removed} lingering junk payloads masquerading as locations.")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    finalize()
