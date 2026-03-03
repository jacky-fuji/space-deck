import json
import re

with open("src/app/data/missions.json", "r") as f:
    missions = json.load(f)

def determine_category(m):
    text_to_search = f"{m.get('rocketName', '')} {m.get('missionName', '')} {m.get('location', '')} {m.get('provider', '')}".lower()
    
    # Missile keywords
    if any(k in text_to_search for k in ["missile", "icbm", "irbm", "srbm", "mrbm", "target", "warhead", "abm target", "kpa strategic"]):
        return "Missile"
        
    # Suborbital keywords
    if "(suborbital)" in text_to_search or "sub-orbital" in text_to_search or "suborbital" in text_to_search:
        return "Suborbital"
    
    # Specific providers/rockets that only do suborbital (unless it's a known orbital)
    if any(k in m.get("provider", "").lower() for k in ["blue origin", "space transportation", "virgin galactic", "sandia", "drdo"]):
        if "missile" not in text_to_search:
            return "Suborbital"
            
    # Default
    return "Orbital"

for m in missions:
    # 1. Fix the 2022 parsed SpaceX flights
    # The structure of the bug is: provider ended up as the Launch Site, location ended up as the Orbit/Remarks, and siteId ended up as "unknown"
    if m.get("date", "").startswith("2022") and m.get("rocketName", "").startswith("Falcon 9"):
        prov = m.get("provider", "")
        if "Kennedy" in prov or "Cape Canaveral" in prov or "Vandenberg" in prov:
            # We found a swapped record
            actual_location = m.get("provider", "")
            actual_orbit = m.get("location", "")
            m["provider"] = "SpaceX"
            m["location"] = actual_location
            m["missionName"] = f"{m.get('missionName')} ({actual_orbit.replace('(', '').replace(')', '').strip()})"
            m["siteId"] = "usa"
            
    # 2. Assign Category
    category = determine_category(m)
    m["flightCategory"] = category

with open("src/app/data/missions.json", "w", encoding="utf-8") as f:
    json.dump(missions, f, ensure_ascii=False, indent=2)

print("Data categorization and SpaceX 2022 fixes complete.")
