import urllib.request
import re
import json
from datetime import datetime

def get_html(url):
    print(f"Fetching {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def clean_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def parse_entries(html, source_type):
    missions = []
    # Find all entry wrappers
    entries = re.findall(r"<div class='cs-entry__wrapper'>(.*?)<!-- .cs-entry__inner -->\s*</div>\s*</div>", html, re.DOTALL)
    if not entries:
        # Fallback for different quote style or slightly different closing
        entries = re.findall(r"<div class='cs-entry__wrapper'>(.*?)</div>\s*</div>\s*</div>", html, re.DOTALL)

    for entry in entries:
        # Title/Rocket
        title_match = re.search(r"<h2 class='cs-entry__title[^>]*>.*?<span>(.*?)</span>", entry, re.DOTALL)
        if not title_match:
            # Try without span or h4
            title_match = re.search(r"<h[24][^>]*class='cs-entry__title'[^>]*>.*?<a[^>]*>(.*?)</a>", entry, re.DOTALL)
        
        if not title_match: continue
        
        launch_info = title_match.group(1).strip()
        if " | " in launch_info:
            rocket, mission = launch_info.split(" | ", 1)
        else:
            rocket = "Unknown"
            mission = launch_info
        
        # Meta categories (Provider, Location, Date)
        meta_categories = re.findall(r"<div class='cs-meta-category[^>]*>(.*?)</div>", entry, re.DOTALL)
        
        provider = "Unknown"
        location = "Unknown"
        date_str = "TBD"
        
        # Look for data-launch-time attribute first
        date_attr_match = re.search(r"data-launch-time='(\d{2})-(\d{2})-(\d{4})", entry)
        if date_attr_match:
            month, day, year = date_attr_match.groups()
            date_str = f"{year}-{month}-{day}"
        
        # Map meta categories
        # Meta 0 is usually Provider, Meta 1 is Location, Meta 2 is Date
        cleaned_metas = [clean_html(m) for m in meta_categories if clean_html(m)]
        
        if len(cleaned_metas) >= 1:
            provider = cleaned_metas[0].title()
        if len(cleaned_metas) >= 2:
            location = cleaned_metas[1]
        
        # Status (based on typical EA colors)
        status = "Success"
        if source_type == "upcoming":
            status = "Scheduled"
        else:
            if 'border-left: 10px solid #ff0000' in entry or 'color: #ff0000' in entry:
                status = "Failure"
            elif 'border-left: 10px solid #ffff00' in entry:
                status = "Partial Failure"

        missions.append({
            "id": f"ea-{source_type}-{hash(launch_info + date_str)}",
            "date": date_str,
            "missionName": mission,
            "missionType": "Commercial",
            "rocketName": rocket,
            "provider": provider,
            "location": location,
            "siteId": "usa", # Placeholder
            "status": status
        })
    return missions

if __name__ == "__main__":
    all_ea_missions = []
    
    # Upcoming
    try:
        html = get_html("https://everydayastronaut.com/upcoming-launches/")
        upcoming = parse_entries(html, "upcoming")
        print(f"Found {len(upcoming)} upcoming missions.")
        all_ea_missions.extend(upcoming)
    except Exception as e:
        print(f"Error scraping upcoming: {e}")

    # Previous (Page 1 & 2)
    try:
        for page in range(1, 3):
            url = "https://everydayastronaut.com/previous-launches/"
            if page > 1:
                url += f"page/{page}/"
            
            html = get_html(url)
            prev = parse_entries(html, "previous")
            print(f"Found {len(prev)} previous missions on page {page}.")
            all_ea_missions.extend(prev)
    except Exception as e:
        print(f"Error scraping previous: {e}")

    # Save
    with open("everyday_astronaut_missions.json", "w", encoding="utf-8") as f:
        json.dump(all_ea_missions, f, ensure_ascii=False, indent=2)
    print(f"Total missions saved: {len(all_ea_missions)}")
