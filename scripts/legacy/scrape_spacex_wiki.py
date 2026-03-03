import json
import urllib.request
import re

def clean_html(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&#160;', ' ')
    return ' '.join(text.split())

def fetch_wiki_spacex(url, year):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return []
    
    launches = []
    
    # Extract tables
    tables = re.findall(r'<table[^>]*class="wikitable"[^>]*>.*?</table>', html, re.DOTALL)
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    full_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
              
    for table in tables:
        rows = re.findall(r'<tr[^>]*>.*?</tr>', table, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', row, re.DOTALL)
            if len(cells) < 5: continue
            
            flight_num = clean_html(cells[0])
            if not flight_num.isdigit(): continue
            
            date_str = clean_html(cells[1])
            if str(year) not in date_str: continue
            
            month_idx = 0
            day = 1
            for i, (sm, fm) in enumerate(zip(months, full_months)):
                if sm in date_str or fm in date_str:
                    month_idx = i + 1
                    try:
                        day_match = re.search(r'(\d+)\s+' + sm, date_str) or re.search(r'(\d+)\s+' + fm, date_str)
                        if day_match: day = int(day_match.group(1))
                    except:
                        pass
                    break
            
            if month_idx == 0: continue
            iso_date = f"{year}-{month_idx:02d}-{day:02d}"
            
            rocket = clean_html(cells[2])
            site = clean_html(cells[3])
            payload = clean_html(cells[4])
            
            if "Starlink" in payload: payload = "Starlink"
            elif len(payload) > 50: payload = payload[:50] + "..."
            
            rocket_name = "Falcon Heavy" if "Heavy" in rocket else "Falcon 9 Block 5"
            site_id = "usa"
            if "KSC" in site or "Cape" in site or "CCSFS" in site:
                location = "Cape Canaveral SFS, FL, USA"
            elif "VAFB" in site or "VSFB" in site or "Vandenberg" in site:
                location = "Vandenberg SFB, CA, USA"
            else:
                location = "USA"

            outcome = "Success"
            for c in cells:
                if "Failure" in clean_html(c): outcome = "Failure"
            
            launches.append({
                "id": f"spxw-{year}-{flight_num}",
                "date": iso_date,
                "missionName": payload,
                "missionType": "Satellite" if "Starlink" in payload else "Commercial",
                "rocketName": rocket_name,
                "provider": "SpaceX",
                "location": location,
                "siteId": site_id,
                "status": outcome
            })
            
    return launches

def main():
    urls = [
        ("https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2023)", 2023),
        ("https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2024)", 2024)
    ]
    
    all_spx = []
    for u, y in urls:
        print(f"Scraping Wikipedia SpaceX {y}...")
        results = fetch_wiki_spacex(u, y)
        print(f"  Got {len(results)} flights.")
        all_spx.extend(results)
    
    print(f"Extracted {len(all_spx)} SpaceX missions for 2023/2024.")

    if not all_spx: return

    with open("src/app/data/missions.json", "r") as f:
        existing = json.load(f)

    # Clean out any old broken ones for 23/24
    filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and (m["date"].startswith("2023") or m["date"].startswith("2024")))]

    combined = filtered + all_spx
    combined.sort(key=lambda x: x["date"], reverse=True)

    with open("src/app/data/missions.json", "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Restored SpaceX missions to database. Total: {len(combined)}")

if __name__ == "__main__":
    main()
