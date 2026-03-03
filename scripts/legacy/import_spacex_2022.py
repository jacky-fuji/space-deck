import json
import re

raw_table = """
| Flight Number | Date | Launch Site | Payload | Customer |
| :--- | :--- | :--- | :--- | :--- |
| 135 | 6 January 2022 | Kennedy, LC‑39A | Starlink: Group 4-5 (49 satellites) | SpaceX |
| 136 | 13 January 2022 | Cape Canaveral, SLC‑40 | Transporter-3 (105 payload smallsat rideshare) | Various |
| 137 | 19 January 2022 | Kennedy, LC‑39A | Starlink: Group 4-6 (49 satellites) | SpaceX |
| 138 | 31 January 2022 | Cape Canaveral, SLC‑40 | CSG-2 | ASI |
| 139 | 2 February 2022 | Vandenberg, SLC‑4E | NROL-87 | NRO |
| 140 | 3 February 2022 | Kennedy, LC‑39A | Starlink: Group 4-7 (49 satellites) | SpaceX |
| 141 | 21 February 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-8 (46 satellites) | SpaceX |
| 142 | 25 February 2022 | Vandenberg, SLC‑4E | Starlink: Group 4-11 (50 satellites) | SpaceX |
| 143 | 3 March 2022 | Kennedy, LC‑39A | Starlink: Group 4-9 (47 satellites) | SpaceX |
| 144 | 9 March 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-10 (48 satellites) | SpaceX |
| 145 | 19 March 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-12 (53 satellites) | SpaceX |
| 146 | 1 April 2022 | Cape Canaveral, SLC‑40 | Transporter-4 (40 payload smallsat rideshare) | Various |
| 147 | 8 April 2022 | Kennedy, LC‑39A | Axiom-1 (Crew Dragon C206.3 Endeavour) | Axiom Space |
| 148 | 17 April 2022 | Vandenberg, SLC‑4E | NROL-85 (Intruder 13A [NOSS-3 9A] and Intruder 13B [(NOSS-3 9B]) | NRO |
| 149 | 21 April 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-14 (53 satellites) | SpaceX |
| 150 | 27 April 2022 | Kennedy, LC‑39A | Crew-4 (Crew Dragon C212.1 Freedom) | NASA (CTS) |
| 151 | 29 April 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-16 (53 satellites) | SpaceX |
| 152 | 6 May 2022 | Kennedy, LC‑39A | Starlink: Group 4-17 (53 satellites) | SpaceX |
| 153 | 13 May 2022 | Vandenberg, SLC‑4E | Starlink: Group 4-13 (53 satellites) | SpaceX |
| 154 | 14 May 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-15 (53 satellites) | SpaceX |
| 155 | 18 May 2022 | Kennedy, LC‑39A | Starlink: Group 4-18 (53 satellites) | SpaceX |
| 156 | 25 May 2022 | Cape Canaveral, SLC‑40 | Transporter-5 (59 payload smallsat rideshare) | Various |
| 157 | 8 June 2022 | Cape Canaveral, SLC‑40 | Nilesat-301 | Nilesat |
| 158 | 17 June 2022 | Kennedy, LC‑39A | Starlink: Group 4-19 (53 satellites) | SpaceX |
| 159 | 18 June 2022 | Vandenberg, SLC‑4E | SARah 1 | German Intelligence Service |
| 160 | 19 June 2022 | Cape Canaveral, SLC‑40 | Globalstar-2 M087 (FM15) USA 328-331 | Globalstar, Unknown US government agency |
| 161 | 29 June 2022 | Cape Canaveral, SLC‑40 | SES-22 | SES |
| 162 | 7 July 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-21 (53 satellites) | SpaceX |
| 163 | 11 July 2022 | Vandenberg, SLC‑4E | Starlink: Group 3-1 (46 satellites) | SpaceX |
| 164 | 15 July 2022 | Kennedy, LC‑39A | SpaceX CRS-25 (Dragon C208.3) | NASA (CRS) |
| 165 | 17 July 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-22 (53 satellites) | SpaceX |
| 166 | 22 July 2022 | Vandenberg, SLC‑4E | Starlink: Group 3-2 (46 satellites) | SpaceX |
| 167 | 24 July 2022 | Kennedy, LC‑39A | Starlink: Group 4-25 (53 satellites) | SpaceX |
| 168 | 4 August 2022 | Cape Canaveral, SLC‑40 | Danuri (Korea Pathfinder Lunar Orbiter) | KARI |
| 169 | 10 August 2022 | Kennedy, LC‑39A | Starlink: Group 4-26 (52 satellites) | SpaceX |
| 170 | 12 August 2022 | Vandenberg, SLC‑4E | Starlink: Group 3-3 (46 satellites) | SpaceX |
| 171 | 19 August 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-27 (53 satellites) | SpaceX |
| 172 | 28 August 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-23 (54 satellites) | SpaceX |
| 173 | 31 August 2022 | Vandenberg, SLC‑4E | Starlink: Group 3-4 (46 satellites) | SpaceX |
| 174 | 5 September 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-20 (51 satellites) Sherpa-LTC2 | SpaceX, Spaceflight Industries |
| 175 | 11 September 2022 | Kennedy, LC‑39A | Starlink: Group 4-2 (34 satellites) BlueWalker-3 | SpaceX, AST SpaceMobile |
| 176 | 19 September 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-34 (54 satellites) | SpaceX |
| 177 | 24 September 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-35 (52 satellites) | SpaceX |
| 178 | 5 October 2022 | Kennedy, LC‑39A | Crew-5 (Crew Dragon C210.2 Endurance) | NASA (CTS) |
| 179 | 5 October 2022 | Vandenberg, SLC‑4E | Starlink: Group 4-29 (52 satellites) | SpaceX |
| 180 | 8 October 2022 | Cape Canaveral, SLC‑40 | Galaxy 33 & 34 | Intelsat |
| 181 | 15 October 2022 | Cape Canaveral, SLC‑40 | Hotbird 13F | Eutelsat |
| 182 | 20 October 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 4-36 (54 satellites) | SpaceX |
| 183 | 28 October 2022 | Vandenberg, SLC‑4E | Starlink: Group 4-31 (53 satellites) | SpaceX |
| FH 4 | 1 November 2022 | Kennedy, LC‑39A | USSF-44 (Shepherd Demonstration & LDPE-2) | USSF, Millennium Space Systems and Lockheed Martin Space |
| 184 | 3 November 2022 | Cape Canaveral, SLC‑40 | Hotbird 13G | Eutelsat |
| 185 | 12 November 2022 | Cape Canaveral, SLC‑40 | Galaxy 31 and Galaxy 32 (2 satellites) | Intelsat |
| 186 | 23 November 2022 | Cape Canaveral, SLC‑40 | Eutelsat 10B | Eutelsat |
| 187 | 26 November 2022 | Kennedy, LC‑39A | SpaceX CRS-26 (Dragon C211.1) | NASA (CRS) |
| 188 | 8 December 2022 | Kennedy, LC‑39A | OneWeb Flight #15 / SpaceX Flight 1 (40 satellites) | OneWeb |
| 189 | 11 December 2022 | Cape Canaveral, SLC‑40 | Hakuto-R Mission 1 Emirates Lunar Mission Lunar Flashlight | ispace, MBRSC, JAXA, NASA |
| 190 | 16 December 2022 | Vandenberg, SLC‑4E | Surface Water and Ocean Topography (SWOT) | NASA/CNES |
| 191 | 16 December 2022 | Cape Canaveral, SLC‑40 | O3b mPOWER 1 & 2 | SES |
| 192 | 17 December 2022 | Kennedy, LC‑39A | Starlink: Group 4-37 (54 satellites) | SpaceX |
| 193 | 28 December 2022 | Cape Canaveral, SLC‑40 | Starlink: Group 5-1 (54 satellites) | SpaceX |
| 194 | 30 December 2022 | Vandenberg, SLC‑4E | EROS-C3 | ImageSat International |
"""

from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

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
    
    iso_date = f"2022-{month_idx:02d}-{day:02d}"
    
    t = "Satellite" if "Starlink" in pl else "Commercial"
    rocket = "Falcon Heavy" if "FH" in flight_num else "Falcon 9 Block 5"
    
    loc = "USA"
    if "Cape Canaveral" in site or "Kennedy" in site:
        loc = "Cape Canaveral SFS, FL, USA"
    elif "Vandenberg" in site:
        loc = "Vandenberg SFB, CA, USA"
    
    missions_to_add.append({
        "id": f"spxwiki2022-{flight_num}",
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

print(f"Parsed {len(missions_to_add)} 2022 SpaceX records to database...")

filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and m["date"].startswith("2022"))]
combined = filtered + missions_to_add
combined.sort(key=lambda x: x["date"], reverse=True)

with open("src/app/data/missions.json", "w") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)
    
print(f"Total missions saved: {len(combined)}")
