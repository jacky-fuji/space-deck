import json
import re

raw_table = """
| Flight Number | Date | Launch Site | Payload | Customer |
| :--- | :--- | :--- | :--- | :--- |
| 583 | Jan 3, 2026 | Vandenberg, SLC-4E | CSG-3 | ASI |
| 584 | Jan 4, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-88 | SpaceX |
| 585 | Jan 9, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-96 | SpaceX |
| 586 | Jan 11, 2026 | Vandenberg, SLC-4E | Twilight (Pandora and 39 others) | NASA & Various |
| 587 | Jan 12, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-97 | SpaceX |
| 588 | Jan 14, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-98 | SpaceX |
| 589 | Jan 17, 2026 | Vandenberg, SLC-4E | NROL-105 (2 Starshield satellites) | NRO |
| 590 | Jan 18, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-100 | SpaceX |
| 591 | Jan 22, 2026 | Vandenberg, SLC-4E | Starlink Group 17-30 | SpaceX |
| 592 | Jan 25, 2026 | Vandenberg, SLC-4E | Starlink Group 17-20 | SpaceX |
| 593 | Jan 28, 2026 | Cape Canaveral, SLC-40 | GPS III-9 | USSF |
| 594 | Jan 29, 2026 | Vandenberg, SLC-4E | Starlink Group 17-19 | SpaceX |
| 595 | Jan 30, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-101 | SpaceX |
| 596 | Feb 2, 2026 | Vandenberg, SLC-4E | Starlink Group 17-32 | SpaceX |
| 597 | Feb 7, 2026 | Vandenberg, SLC-4E | Starlink Group 17-33 | SpaceX |
| 598 | Feb 11, 2026 | Vandenberg, SLC-4E | Starlink Group 17-34 | SpaceX |
| 599 | Feb 13, 2026 | Cape Canaveral, SLC-40 | Crew-12 (Freedom) | NASA (CTS) |
| 600 | Feb 15, 2026 | Vandenberg, SLC-4E | Starlink Group 17-13 | SpaceX |
| 601 | Feb 16, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-103 | SpaceX |
| 602 | Feb 20, 2026 | Cape Canaveral, SLC-40 | Starlink Group 10-36 | SpaceX |
| 603 | Feb 21, 2026 | Vandenberg, SLC-4E | Starlink Group 17-25 | SpaceX |
| 604 | Feb 22, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-104 | SpaceX |
| 605 | Feb 24, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-110 | SpaceX |
| 606 | Feb 25, 2026 | Vandenberg, SLC-4E | Starlink Group 17-26 | SpaceX |
| 607 | Feb 27, 2026 | Cape Canaveral, SLC-40 | Starlink Group 6-108 | SpaceX |
| 608 | Mar 1, 2026 | Vandenberg, SLC-4E | Starlink Group 17-23 | SpaceX |
| 609 | Mar 2, 2026 | Cape Canaveral, SLC-40 | Starlink Group 10-41 | SpaceX |
"""

from datetime import datetime

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

missions_to_add = []
for line in raw_table.strip().split('\n'):
    line = line.strip()
    if not line.startswith('|') or 'Flight Number' in line or ':---' in line:
        continue
    
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 5:
        continue
        
    flight_num = parts[0]
    date_str = parts[1]
    site = parts[2]
    pl = parts[3]
    customer = parts[4]
    
    month_idx = 0
    day = 1
    for i, m in enumerate(months):
        if m in date_str:
            month_idx = i + 1
            day_match = re.search(r'(\d+)', date_str)
            if day_match: day = int(day_match.group(1))
            break

    if month_idx == 0: continue
    
    iso_date = f"2026-{month_idx:02d}-{day:02d}"
    
    t = "Satellite" if "Starlink" in pl else "Commercial"
    rocket = "Falcon Heavy" if "FH" in flight_num else "Falcon 9 Block 5"
    
    loc = "USA"
    if "Cape Canaveral" in site or "Kennedy" in site:
        loc = "Cape Canaveral SFS, FL, USA"
    elif "Vandenberg" in site:
        loc = "Vandenberg SFB, CA, USA"
    
    missions_to_add.append({
        "id": f"spxwiki2026-{flight_num}",
        "date": iso_date,
        "missionName": pl,
        "missionType": t,
        "rocketName": rocket,
        "provider": "SpaceX",
        "location": loc,
        "siteId": "usa",
        "status": "Success"
    })

with open("src/app/data/missions.json", "r") as f:
    existing = json.load(f)

print(f"Parsed {len(missions_to_add)} 2026 SpaceX records to database...")

# Filter out old 2026 SpaceX flights that have already occurred (Jan/Feb/early March) 
# to avoid duplicating with the accurately parsed ones we just generated.
# Keep 2026 SpaceX flights if they are scheduled *after* March 3rd (upcoming).
filtered = []
for m in existing:
    if m["provider"].lower() == "spacex" and m["date"].startswith("2026"):
        # If it's earlier than or equal to March 3rd
        if m["date"] <= "2026-03-03":
            continue # drop it, replacing with our new dataset
    filtered.append(m)

combined = filtered + missions_to_add
combined.sort(key=lambda x: x["date"], reverse=True)

with open("src/app/data/missions.json", "w") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)
    
print(f"Total missions saved: {len(combined)}")
