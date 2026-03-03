import json
import urllib.request
import re

def clean_html(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&#160;', ' ')
    return ' '.join(text.split())

def fetch_spacex_launches(year):
    if year >= 2023:
        url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2023%E2%80%93present)"
    else:
        url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2020%E2%80%932022)"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    launches = []
    
    # Extract tables
    tables = re.findall(r'<table[^>]*class="wikitable"[^>]*>.*?</table>', html, re.DOTALL)
    
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
              
    for table in tables:
        rows = re.findall(r'<tr[^>]*>.*?</tr>', table, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', row, re.DOTALL)
            if len(cells) < 5: continue
            
            # Flight number is usually first column
            flight_num = clean_html(cells[0])
            if not flight_num.isdigit(): continue
            
            date_str = clean_html(cells[1])
            if str(year) not in date_str: continue
            
            month_idx = 0
            day = 1
            for i, m in enumerate(months):
                if m in date_str:
                    month_idx = i + 1
                    try:
                        day_match = re.search(r'(\d+)\s+' + m, date_str)
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
                "id": f"spxwiki-{year}-{flight_num}",
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
    print("Scraping SpaceX 2023 launches...")
    m_2023 = fetch_spacex_launches(2023)
    print("Scraping SpaceX 2024 launches...")
    m_2024 = fetch_spacex_launches(2024)
    
    missions = m_2023 + m_2024
    print(f"Extracted {len(missions)} SpaceX missions for 2023/2024.")

    if not missions:
        print("Failed to extract missions.")
        return

    with open("src/app/data/missions.json", "r") as f:
        existing = json.load(f)

    # Filter out API records or wiki dupes
    filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and (m["date"].startswith("2023") or m["date"].startswith("2024")))]

    combined = filtered + missions
    combined.sort(key=lambda x: x["date"], reverse=True)

    with open("src/app/data/missions.json", "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Restored SpaceX missions to database. Total: {len(combined)}")

if __name__ == "__main__":
    main()
