import json
import urllib.request
import re
from datetime import datetime

# Wikipedia URLs for recent years
YEAR_URLS = {
    "2024": "https://en.wikipedia.org/wiki/2024_in_spaceflight",
    "2023": "https://en.wikipedia.org/wiki/2023_in_spaceflight",
    "2022": "https://en.wikipedia.org/wiki/2022_in_spaceflight"
}

MISSIONS_FILE = "src/app/data/missions.json"

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def clean_html(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    return ' '.join(text.split())

def parse_sublist(url, year):
    print(f"  Fetching sub-list: {url}...")
    html = fetch_html(url)
    
    # Extract all tables
    tables = re.findall(r'<table[^>]*class="wikitable"[^>]*>.*?</table>', html, re.DOTALL)
    
    missions = []
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    current_date = None
    current_rocket = None
    current_site = None
    current_provider = None
    
    for table in tables:
        if "Payload" not in table or "Outcome" not in table:
            continue
            
        rows = re.findall(r'<tr[^>]*>.*?</tr>', table, re.DOTALL)
        for row in rows:
            # 1. Date check
            date_match = re.search(rf'(\d+\s+)?({"|".join(months)})( \d+)?', row)
            if date_match and 'rowspan' in row:
                day = date_match.group(1).strip() if date_match.group(1) else "1"
                month_name = date_match.group(2)
                m_num = months.index(month_name) + 1
                current_date = f"{year}-{m_num:02d}-{int(day):02d}"
                
                tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(tds) >= 4:
                    current_rocket = clean_html(tds[1]).strip()
                    current_site = clean_html(tds[2]).strip()
                    current_provider = clean_html(tds[3]).strip()

            # 2. Outcome check
            if "Successful" in row or "Operational" in row or "En route" in row:
                outcome = "Success"
            elif "Failure" in row or "Partial failure" in row:
                outcome = "Failure"
            else:
                continue
                
            if current_date and current_rocket:
                tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                payload = clean_html(tds[0]).strip() if tds else "Unknown"
                
                missions.append({
                    "date": current_date,
                    "missionName": payload,
                    "rocketName": current_rocket,
                    "location": current_site,
                    "status": outcome,
                    "provider": current_provider
                })
    return missions

def main():
    print("Loading local missions...")
    with open(MISSIONS_FILE, "r") as f:
        local_data = json.load(f)

    local_index = set()
    for m in local_data:
        local_index.add((m["date"], m["rocketName"][:5].lower()))

    all_missing = []
    for year, url in YEAR_URLS.items():
        print(f"Scraping {year}...")
        html = fetch_html(url)
        
        # Find links like "/wiki/List_of_spaceflight_launches_in_January–June_2024"
        sublist_links = re.findall(r'href="(/wiki/List_of_spaceflight_launches_in_[^"]+)"', html)
        # Filter and unique
        sublist_links = list(set([f"https://en.wikipedia.org{l}" for l in sublist_links if year in l]))
        
        year_wiki_missions = []
        if not sublist_links:
            # Try parsing the main page if no sublists found
            year_wiki_missions = parse_sublist(url, year)
        else:
            for link in sublist_links:
                year_wiki_missions.extend(parse_sublist(link, year))
                
        print(f"Found {len(year_wiki_missions)} missions for {year} in Wiki.")
        for m in year_wiki_missions:
            if (m["date"], m["rocketName"][:5].lower()) not in local_index:
                all_missing.append(m)

    print(f"\nDiscovered {len(all_missing)} missing missions.")
    if all_missing:
        # Save to missions_to_add.json for final confirmation
        with open("/tmp/missions_to_add.json", "w") as f:
            json.dump(all_missing, f, indent=2, ensure_ascii=False)
        print("Missing missions saved to /tmp/missions_to_add.json")

if __name__ == "__main__":
    main()
