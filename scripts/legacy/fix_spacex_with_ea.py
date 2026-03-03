import json
import urllib.request

EA_URL = "https://lldev.thespacedevs.com/2.2.0/launch/previous/?limit=100&lsp__name=SpaceX&ordering=-net"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode('utf-8'))

def get_spacex():
    print("Fetching SpaceX from EA dev API...")
    try:
        data = fetch_json(EA_URL)
        results = data.get("results", [])
    except Exception as e:
        print(f"Error fetching: {e}")
        return []

    print(f"Got {len(results)} total historical SpaceX launches.")
        
    launches = []
    for r in results:
        date_str = r.get("net", "")[:10]
        # Only interested in the gap years 2023 and 2024
        if not (date_str.startswith("2023") or date_str.startswith("2024")):
            continue
            
        m_name = r.get("mission", {}).get("name", "Unknown Payload") if r.get("mission") else "Unknown Payload"
        m_type = "Satellite" if "Starlink" in m_name else "Commercial"
        rocket = r.get("rocket", {}).get("configuration", {}).get("name", "Falcon 9")
        pad = r.get("pad", {}).get("name", "")
        
        site_id = "usa"
        if "Cape" in pad or "Kennedy" in pad or "CCSFS" in pad:
            location = "Cape Canaveral SFS, FL, USA"
        elif "Vandenberg" in pad or "VAFB" in pad:
            location = "Vandenberg SFB, CA, USA"
        elif "Boca Chica" in pad or "Starbase" in pad:
            location = "Starbase, TX, USA"
        else:
            location = "USA"
            
        status_name = r.get("status", {}).get("name", "Success")
        if "Success" in status_name:
            outcome = "Success"
        elif "Failure" in status_name:
            outcome = "Failure"
        else:
            outcome = "Success"
            
        launches.append({
            "id": f"sxea-{r.get('id', '')}",
            "date": date_str,
            "missionName": m_name,
            "missionType": m_type,
            "rocketName": rocket,
            "provider": "SpaceX",
            "location": location,
            "siteId": site_id,
            "status": outcome
        })
    return launches

def main():
    launches = get_spacex()
    print(f"Extracted {len(launches)} SpaceX missions for 2023/2024 from EA API.")

    if not launches:
        print("No launches to add.")
        return

    with open("src/app/data/missions.json", "r") as f:
        existing = json.load(f)

    # Clean out any old broken ones for 23/24 if they exist
    filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and (m["date"].startswith("2023") or m["date"].startswith("2024")))]

    combined = filtered + launches
    combined.sort(key=lambda x: x["date"], reverse=True)

    with open("src/app/data/missions.json", "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Restored SpaceX missions to database. Total: {len(combined)}")

if __name__ == "__main__":
    main()
