import urllib.request
import json
import time

# Use the 'previous' endpoint with descending order to get newest first
API_URL = "https://lldev.thespacedevs.com/2.2.0/launch/previous/?limit=100&lsp__name=SpaceX&ordering=-net"

def fetch_page(url):
    print(f"  Fetching URL: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            print(f"Error: {e}, retrying...")
            time.sleep(2)
    return {}

def main():
    print("Fetching SpaceX launches from SpaceDevs LL2 API...")
    url = API_URL
    all_results = []
    
    # Just fetch the first 4 pages (400 results) to cover 2024, 2023, 2022
    for _ in range(4):
        if not url: break
        data = fetch_page(url)
        results = data.get("results", [])
        if not results: break
        all_results.extend(results)
        print(f"  -> Got {len(results)} items. Earliest in batch: {results[-1]['net']}")
        url = data.get("next")
        time.sleep(1)
        
    print(f"Total SpaceX flights fetched: {len(all_results)}")
    
    launches = []
    for r in all_results:
        date_str = r.get("net", "")[:10]
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
        
    print(f"Filtered to {len(launches)} SpaceX missions in 2023/2024.")
    if not launches: return
    
    with open("src/app/data/missions.json", "r") as f:
        existing = json.load(f)

    # Clean out any partial/broken records
    filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and (m["date"].startswith("2023") or m["date"].startswith("2024")))]

    combined = filtered + launches
    combined.sort(key=lambda x: x["date"], reverse=True)

    with open("src/app/data/missions.json", "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Restored SpaceX missions to database. Total: {len(combined)}")

if __name__ == "__main__":
    main()
