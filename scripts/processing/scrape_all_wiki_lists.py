import json
import urllib.request
import re
import os
from datetime import datetime

MISSIONS_FILE = "src/app/data/missions.json"
MISSING_FILE = "/tmp/all_missing_missions.json"

SITE_TO_COUNTRY = {
    "Cape Canaveral": "USA", "Kennedy": "USA", "Vandenberg": "USA", "Boca Chica": "USA", "Wallops": "USA", "Kodiak": "USA", "Omelek": "USA",
    "Wenchang": "China", "Jiuquan": "China", "Xichang": "China", "Taiyuan": "China", "Jielong": "China", "Yellow Sea": "China",
    "Baikonur": "Russia", "Plesetsk": "Russia", "Vostochny": "Russia", "Kapustin Yar": "Russia", "Svobodny": "Russia", "Dombarovsky": "Russia",
    "Tanegashima": "Japan", "Uchinoura": "Japan", "Kagoshima": "Japan",
    "Kourou": "France", "Guiana": "France",
    "Satish Dhawan": "India", "Sriharikota": "India",
    "Mahia": "New Zealand", "Rocket Lab": "New Zealand",
    "Palmachim": "Israel",
    "Sohae": "North Korea", "Tonghae": "North Korea",
    "Naro": "South Korea",
    "Semnan": "Iran", "Shahroud": "Iran",
    "Woomera": "Australia",
    "San Marco": "Kenya",
    "Hammaguir": "Algeria"
}

def get_country(location):
    location = (location or "").lower()
    # Check SITE_TO_COUNTRY first
    for site, country in SITE_TO_COUNTRY.items():
        if site.lower() in location:
            return country
    
    # Keyword fallback
    if "japan" in location or "kii" in location or "tanegashima" in location or "uchinoura" in location: return "Japan"
    if "russia" in location or "plesetsk" in location or "vostochny" in location or "baikonur" in location or "kazakhstan" in location: return "Russia"
    if "china" in location or "jiuquan" in location or "xichang" in location or "taiyuan" in location or "wenchang" in location or "hainan" in location: return "China"
    if "usa" in location or "canaveral" in location or "vandenberg" in location or "kennedy" in location or "wallops" in location or "boca chica" in location or "starbase" in location: return "USA"
    if "france" in location or "guiana" in location or "kourou" in location or "csg" in location: return "France"
    if "india" in location or "sriharikota" in location or "sdsc" in location or "shar" in location: return "India"
    if "new zealand" in location or "mahia" in location or "rocket lab" in location: return "New Zealand"
    if "australia" in location or "woomera" in location or "bowen" in location: return "Australia"
    if "brazil" in location or "alcantara" in location: return "Brazil"
    if "israel" in location or "palmachim" in location: return "Israel"
    if "n. korea" in location or "sohae" in location: return "North Korea"
    if "s. korea" in location or "naro" in location or "jeju" in location: return "South Korea"
    
    return "Unknown"

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def clean_html(text):
    text = re.sub(r'<sup[^>]*>.*?</sup>', '', text)  # remove citations
    text = re.sub(r'<[^>]+>', ' ', text)  # remove tags
    text = text.replace('&#160;', ' ').replace('&amp;', '&').replace('\\n', ' ')
    return ' '.join(text.split())

months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]

def parse_generic_list(url):
    print(f"  Fetching: {url}")
    html = fetch_html(url)
    tables = re.findall(r'<table[^>]*class="wikitable[^>]*>.*?</table>', html, re.DOTALL)
    
    missions = []
    current_year = "Unknown"
    
    # Simple regex to find years in headers or captions before tables
    parts = re.split(r'<table', html)
    
    for table in tables:
        # A very generic heuristic: try to find rows with Dates, payloads, and outcomes
        rows = re.findall(r'<tr[^>]*>.*?</tr>', table, re.DOTALL)
        
        current_date = None
        current_rocket = "Unknown Rocket"
        current_site = "Unknown Site"
        
        for row in rows:
            tds = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', row, re.DOTALL)
            if not tds: continue
            
            cleaned_tds = [clean_html(td) for td in tds]
            
            # 1. Date check
            date_match = None
            for idx, text in enumerate(cleaned_tds):
                match = re.search(rf'\b(?:(\d{{1,2}})\s+)?({"|".join(months)})\s*(?:(\d{{4}}))?\b', text)
                if match:
                    day = match.group(1) or "1"
                    month_name = match.group(2)
                    year = match.group(3) or current_year
                    if year != "Unknown":
                        m_num = months.index(month_name) + 1
                        try:
                            # Avoid matching random text, ensure year is realistic
                            if 1950 <= int(year) <= 2030:
                                current_date = f"{year}-{m_num:02d}-{int(day):02d}"
                                current_year = year
                                date_match_idx = idx
                                break
                        except ValueError:
                            pass

            # 2. Outcome check
            outcome = None
            if re.search(r'\b(Success|Successful|Operational|En route)\b', row, re.IGNORECASE):
                outcome = "Success"
            elif re.search(r'\b(Failure|Partial failure)\b', row, re.IGNORECASE):
                outcome = "Failure"
            else:
                # If there's no outcome string but it's a past date, sometimes tables just assume success
                pass
                
            if current_date and outcome == "Success":
                # Heuristics to find payload, rocket, site
                # Payload is usually column 2, 3 or 4. Rocket is sometimes 1 or 2.
                # Just join everything and it can be cleaned later, but let's try to grab distinct columns
                
                payload = cleaned_tds[1] if len(cleaned_tds) > 1 else "Unknown Payload"
                
                # If we have a generic list by rocket family, the list title implies the rocket
                rocket_title_match = re.search(r'List_of_(.*)_launches', url)
                if rocket_title_match:
                    family = rocket_title_match.group(1).replace('_', ' ')
                    # Look for variants in the row, e.g. "Falcon 9 Block 5"
                    potential_rocket = next((td for td in cleaned_tds if family.split()[0] in td), family)
                    current_rocket = potential_rocket
                else:
                    current_rocket = cleaned_tds[2] if len(cleaned_tds) > 2 else "Unknown Rocket"

                # Look for a known site in the text
                for t in cleaned_tds:
                    for site in SITE_TO_COUNTRY.keys():
                        if site.lower() in t.lower():
                            current_site = site
                            break
                            
                # If we found enough info, record it
                if len(payload) > 2 and len(current_rocket) > 2:
                    m = {
                        "date": current_date,
                        "missionName": payload[:50],  # trim long descriptions
                        "rocketName": current_rocket[:50],
                        "location": current_site,
                        "status": outcome,
                        "provider": "Unknown"
                    }
                    missions.append(m)
                    
    return missions

def main():
    print("Loading local missions...")
    if not os.path.exists(MISSIONS_FILE):
        return
        
    with open(MISSIONS_FILE, "r") as f:
        existing = json.load(f)

    existing_index = set()
    for m in existing:
        # fuzzy key to prevent duplicates: Year-Month, and first 5 chars of rocket
        try:
            ym = m["date"][:7] 
            existing_index.add((ym, m["rocketName"][:5].lower()))
        except Exception:
            pass

    # Fetch main index
    main_url = "https://en.wikipedia.org/wiki/Lists_of_rocket_launches"
    html = fetch_html(main_url)
    list_links = list(set(re.findall(r'href="(/wiki/List_of_[^"]+launches[^"]*)"', html)))
    # filter to only main lists, ignore anchor links within the same page if possible, but keep distinct pages
    valid_links = []
    for l in list_links:
        if "Timeline" not in l and "failed" not in l:
            valid_links.append(f"https://en.wikipedia.org{l}")

    valid_links = list(set(valid_links))
    print(f"Found {len(valid_links)} specific rocket/country lists.")

    all_scraped = []
    for link in sorted(valid_links):
        missions = parse_generic_list(link)
        all_scraped.extend(missions)
        print(f"  -> Extracted {len(missions)} potential successes.")

    unique_new = []
    seen = set()
    
    for m in all_scraped:
        ym = m["date"][:7]
        rocket_prefix = m["rocketName"][:5].lower()
        key = (ym, rocket_prefix)
        
        if key not in existing_index and key not in seen:
            # We found a gap
            m["id"] = f"wiki-ext-{ym.replace('-','')}-{len(unique_new)}"
            m["siteId"] = get_country(m["location"]).lower().replace(" ", "-")
            unique_new.append(m)
            seen.add(key)

    print(f"\nDiscovered {len(unique_new)} new unique missions across all specific lists.")
    
    if unique_new:
        final_list = existing + unique_new
        final_list.sort(key=lambda x: x["date"], reverse=True)
        with open(MISSIONS_FILE, "w") as f:
            json.dump(final_list, f, indent=2, ensure_ascii=False)
        print(f"Updated {MISSIONS_FILE}. Total is now {len(final_list)}.")

if __name__ == "__main__":
    main()
