import json
import os

MISSIONS_FILE = "src/app/data/missions.json"

FINAL_GCAT_MAP = {
    # USA
    "VS": "usa", "V": "usa", "PA": "usa", "WI": "usa", "EAFB": "usa", 
    
    # Russia / USSR
    "GTsP-4": "russia", "GNIIPV": "russia", "KLA": "russia", "YAS": "russia", 
    "GIK-2": "russia", "GTsMP-4": "russia", "GNIIP": "russia",
    
    # Iran
    "SEM": "iran",
    
    # Japan
    "KASC": "japan",
     
    # San Marco / Kenya (Italy/USA operated launch platform off coast of Kenya)
    "SMLC": "kenya",
    
    # Hammaguir, Algeria (French tests)
    "HMG": "algeria",
        
    # Australia
    "WOO": "australia",
    
    # Marshall Islands (US operated)
    "KMR": "marshall-is",
    
    # India
    "PSCA": "india",
    
    # China
    "Y1": "china", "Y24": "china", "Y28": "china", "YJ": "china", "Y6": "china", "Y22": "china", "Y5": "china",
    
    # UK / Australia
    "WIMB": "australia" 
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
            elif loc.upper() in FINAL_GCAT_MAP:
                m["siteId"] = FINAL_GCAT_MAP[loc.upper()]
                updated += 1
            # 2. Cleanup last dregs of junk (payload names scraped into Location field)
            elif any(junk in loc.lower() for junk in ["baby come back", "virginia is for", "wise one", "selenocentric"]):
                removed += 1
                continue
                
        cleaned.append(m)

    print(f"Mapped {updated} obscure GCAT site codes to countries.")
    print(f"Removed {removed} lingering junk payloads masquerading as locations.")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    finalize()
