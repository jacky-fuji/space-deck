import json
import urllib.request

LAUNCHES_URL = "https://api.spacexdata.com/v4/launches/past"
ROCKETS_URL = "https://api.spacexdata.com/v4/rockets"
LAUNCHPADS_URL = "https://api.spacexdata.com/v4/launchpads"

PAD_MAPPING = {
    "5e9e4501f509094ba4566f84": "usa", # CCSFS SLC 40 (Will get localized in UI via string match, but 'usa' is safe fallback)
    "5e9e4502f509094188566f88": "usa", # KSC LC 39A
    "5e9e4502f509092b78566f87": "usa", # VAFB SLC 4E
    "5e9e4502f5090995de566f86": "mhl", # Kwajalein
    "5e9e4502f5090927f8566f85": "usa", # Starbase
}

def resolve_mission_type(name, details):
    name_l = name.lower()
    if "starlink" in name_l: return "Satellite"
    if "dragon" in name_l or "crs" in name_l: return "Cargo"
    if "demo" in name_l or "test" in name_l: return "Test Flight"
    if "crew" in name_l: return "Crew"
    return "Satellite"

def main():
    print("Fetching rockets, launchpads, and past launches from SpaceX v4 API...")
    rockets_data = json.loads(urllib.request.urlopen(ROCKETS_URL).read().decode('utf-8'))
    pads_data = json.loads(urllib.request.urlopen(LAUNCHPADS_URL).read().decode('utf-8'))
    spacex_launches = json.loads(urllib.request.urlopen(LAUNCHES_URL).read().decode('utf-8'))
    
    rockets = {r["id"]: r["name"] for r in rockets_data}
    pads = {p["id"]: p for p in pads_data}
    
    new_missions = []
    for sx in spacex_launches:
        date_str = sx["date_utc"][:10]
        # Ignore any stray data 2023 or later since our Wikipedia data is better there
        if date_str >= "2023-01-01":
            continue
            
        m_type = resolve_mission_type(sx["name"], sx["details"])
        pad = pads.get(sx["launchpad"])
        site_id = PAD_MAPPING.get(sx["launchpad"], "usa")
        location = pad["name"] if pad else "USA"
        
        # Normalize the location strings so they map cleanly to countries in Next.js
        if "Cape" in location or "Kennedy" in location or "KSC" in location or "CCSFS" in location:
            location = "Cape Canaveral SFS, FL, USA"
        elif "Vandenberg" in location or "VAFB" in location:
            location = "Vandenberg SFB, CA, USA"
        elif "Kwaj" in location or "Omelek" in location:
            location = "Omelek Island, Marshall Islands"
        elif "Boca Chica" in location or "Starbase" in location:
            location = "Starbase, TX, USA"
        
        new_missions.append({
            "id": f"sx_pre2023_{sx['flight_number']}",
            "date": date_str,
            "missionName": sx["name"],
            "missionType": m_type,
            "rocketName": rockets.get(sx["rocket"], "Falcon 9"),
            "provider": "SpaceX",
            "location": location,
            "siteId": site_id,
            "status": "Success" if sx.get("success") else "Failure"
        })
        
    print(f"Prepared {len(new_missions)} pre-2023 SpaceX missions.")
    
    with open("src/app/data/missions.json", "r") as f:
        existing = json.load(f)
        
    # Strictly filter out pre-2023 SpaceX flights just in case any slipped through
    filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and m["date"] < "2023-01-01")]
    
    combined = filtered + new_missions
    combined.sort(key=lambda x: x["date"], reverse=True)
    
    with open("src/app/data/missions.json", "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
        
    print(f"Total missions saved: {len(combined)}")

if __name__ == "__main__":
    main()
