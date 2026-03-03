import json
import urllib.request
from datetime import datetime

# URLs
LAUNCHES_URL = "https://api.spacexdata.com/v4/launches/past"
ROCKETS_URL = "https://api.spacexdata.com/v4/rockets"
LAUNCHPADS_URL = "https://api.spacexdata.com/v4/launchpads"

MISSIONS_FILE = "src/app/data/missions.json"

# Local mapping for launchpads to match dashboard siteIds or names
PAD_MAPPING = {
    "5e9e4501f509094ba4566f84": "cape-canaveral", # CCSFS SLC 40
    "5e9e4502f509094188566f88": "ksc",            # KSC LC 39A
    "5e9e4502f509092b78566f87": "vandenberg",     # VAFB SLC 4E
    "5e9e4502f5090995de566f86": "kwajalein",      # Kwajalein
    "5e9e4502f5090927f8566f85": "boca-chica",     # Starbase (STLS)
}

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

def resolve_mission_type(name, details):
    name_l = name.lower()
    details_l = (details or "").lower()
    if "starlink" in name_l:
        return "Satellite"
    if "dragon" in name_l or "crs" in name_l:
        return "Cargo"
    if "demo" in name_l or "test" in name_l:
        return "Test Flight"
    if "crew" in name_l:
        return "Crew"
    return "Satellite"

def main():
    print("Fetching rockets and launchpads...")
    try:
        rockets_data = fetch_json(ROCKETS_URL)
        pads_data = fetch_json(LAUNCHPADS_URL)
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return

    rockets = {r["id"]: r["name"] for r in rockets_data}
    pads = {p["id"]: p for p in pads_data}

    print("Fetching all past SpaceX launches...")
    try:
        spacex_launches = fetch_json(LAUNCHES_URL)
    except Exception as e:
        print(f"Error fetching launches: {e}")
        return

    print(f"Found {len(spacex_launches)} SpaceX launches.")

    new_missions = []
    for sx in spacex_launches:
        m_type = resolve_mission_type(sx["name"], sx["details"])
        
        # Site ID and Location name
        pad = pads.get(sx["launchpad"])
        site_id = PAD_MAPPING.get(sx["launchpad"], "usa")
        location = pad["name"] if pad else "USA"

        mission = {
            "id": f"sx{sx['flight_number']}",
            "date": sx["date_utc"][:10],
            "missionName": sx["name"],
            "missionType": m_type,
            "rocketName": rockets.get(sx["rocket"], "Falcon 9"),
            "provider": "SpaceX",
            "location": location,
            "siteId": site_id,
            "status": "Success" if sx.get("success") else "Failure"
        }
        new_missions.append(mission)

    print("Loading existing missions...")
    try:
        with open(MISSIONS_FILE, "r") as f:
            existing = json.load(f)
    except Exception as e:
        print(f"Error reading missions file: {e}")
        return

    # Filter out old SPX or SpaceX records
    filtered = [m for m in existing if m.get("provider") not in ["SPX", "SpaceX"]]
    print(f"Removed {len(existing) - len(filtered)} existing SpaceX records from GCAT.")

    # Merge
    combined = filtered + new_missions
    
    # Sort by date (descending)
    combined.sort(key=lambda x: x["date"], reverse=True)

    print(f"Saving {len(combined)} total missions to {MISSIONS_FILE}...")
    with open(MISSIONS_FILE, "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    
    print("Done!")

if __name__ == "__main__":
    main()
