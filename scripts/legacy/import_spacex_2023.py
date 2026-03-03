import json
import re

raw_data = [
  {"flightNumber": "195", "date": "January 3, 2023 14:56", "payload": "Transporter-6 (115 payload smallsat rideshare)", "customer": "Various"},
  {"flightNumber": "196", "date": "January 10, 2023 04:50", "payload": "OneWeb 16 (40 satellites)", "customer": "OneWeb"},
  {"flightNumber": "FH 5", "date": "January 15, 2023 22:56", "payload": "USSF-67 (CBAS-2 & LDPE-3A)", "customer": "USSF"},
  {"flightNumber": "197", "date": "January 18, 2023 12:24", "payload": "USA-343 (GPS-III SV06)", "customer": "USSF"},
  {"flightNumber": "198", "date": "January 19, 2023 15:43", "payload": "Starlink: Group 2-4 (51 satellites)", "customer": "SpaceX"},
  {"flightNumber": "199", "date": "January 26, 2023 09:32", "payload": "Starlink: Group 5-2 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "200", "date": "January 31, 2023 16:15", "payload": "Starlink: Group 2-6 (49 satellites)", "customer": "SpaceX"},
  {"flightNumber": "201", "date": "February 2, 2023 07:58", "payload": "Starlink: Group 5-3 (53 satellites)", "customer": "SpaceX"},
  {"flightNumber": "202", "date": "February 7, 2023 01:32", "payload": "Amazonas Nexus", "customer": "Hispasat"},
  {"flightNumber": "203", "date": "February 12, 2023 05:10", "payload": "Starlink: Group 5-4 (55 satellites)", "customer": "SpaceX"},
  {"flightNumber": "204", "date": "February 17, 2023 19:12", "payload": "Starlink: Group 2-5 (51 satellites)", "customer": "SpaceX"},
  {"flightNumber": "205", "date": "February 18, 2023 03:59", "payload": "Inmarsat-6 F2", "customer": "Inmarsat"},
  {"flightNumber": "206", "date": "February 27, 2023 23:13", "payload": "Starlink: Group 6-1 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "207", "date": "March 2, 2023 05:34", "payload": "Crew-6 (Crew Dragon C206.4 Endeavour)", "customer": "NASA (CTS)"},
  {"flightNumber": "208", "date": "March 3, 2023 18:38", "payload": "Starlink: Group 2-7 (51 satellites)", "customer": "SpaceX"},
  {"flightNumber": "209", "date": "March 9, 2023 19:13", "payload": "OneWeb 17 (40 satellites)", "customer": "OneWeb"},
  {"flightNumber": "210", "date": "March 15, 2023 00:30", "payload": "SpaceX CRS-27 (Dragon C209.3)", "customer": "NASA (CRS)"},
  {"flightNumber": "211", "date": "March 17, 2023 19:26", "payload": "Starlink: Group 2-8 (52 satellites)", "customer": "SpaceX"},
  {"flightNumber": "212", "date": "March 17, 2023 23:38", "payload": "SES-18 & SES-19", "customer": "SES"},
  {"flightNumber": "213", "date": "March 24, 2023 15:43", "payload": "Starlink: Group 5-5 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "214", "date": "March 29, 2023 20:01", "payload": "Starlink: Group 5-10 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "215", "date": "April 2, 2023 14:29", "payload": "SDA Tranche 0A (10 satellites)", "customer": "SDA"},
  {"flightNumber": "216", "date": "April 7, 2023 04:30", "payload": "Intelsat 40e", "customer": "Intelsat"},
  {"flightNumber": "217", "date": "April 15, 2023 06:47", "payload": "Transporter-7 (51 payload smallsat rideshare)", "customer": "Various"},
  {"flightNumber": "218", "date": "April 19, 2023 14:31", "payload": "Starlink: Group 6-2 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "219", "date": "April 27, 2023 13:40", "payload": "Starlink: Group 3-5 (46 satellites)", "customer": "SpaceX"},
  {"flightNumber": "220", "date": "April 28, 2023 22:12", "payload": "O3b mPOWER 3 & 4", "customer": "SES"},
  {"flightNumber": "FH 6", "date": "May 1, 2023 00:26", "payload": "ViaSat-3 Americas", "customer": "ViaSat"},
  {"flightNumber": "221", "date": "May 4, 2023 07:31", "payload": "Starlink: Group 5-6 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "222", "date": "May 10, 2023 20:09", "payload": "Starlink: Group 2-9 (51 satellites)", "customer": "SpaceX"},
  {"flightNumber": "223", "date": "May 14, 2023 05:03", "payload": "Starlink: Group 5-9 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "224", "date": "May 19, 2023 06:19", "payload": "Starlink: Group 6-3 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "225", "date": "May 20, 2023 13:16", "payload": "Iridium-NEXT (5 satellites) OneWeb (15 Gen1 plus a Gen2 test satellite)", "customer": "Iridium & OneWeb"},
  {"flightNumber": "226", "date": "May 21, 2023 21:37", "payload": "Ax-2 (Crew Dragon C212.2 Freedom)", "customer": "Axiom Space"},
  {"flightNumber": "227", "date": "May 27, 2023 04:30", "payload": "ArabSat 7B (Badr-8)", "customer": "Arabsat"},
  {"flightNumber": "228", "date": "May 31, 2023 06:02", "payload": "Starlink: Group 2-10 (52 satellites)", "customer": "SpaceX"},
  {"flightNumber": "229", "date": "June 4, 2023 12:20", "payload": "Starlink: Group 6-4 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "230", "date": "June 5, 2023 15:47", "payload": "SpaceX CRS-28 (Dragon C208.4)", "customer": "NASA (CRS)"},
  {"flightNumber": "231", "date": "June 12, 2023 07:10", "payload": "Starlink: Group 5-11 (52 satellites)", "customer": "SpaceX"},
  {"flightNumber": "232", "date": "June 12, 2023 21:35", "payload": "Transporter-8 (72 payload smallsat rideshare)", "customer": "Various"},
  {"flightNumber": "233", "date": "June 18, 2023 22:21", "payload": "SATRIA", "customer": "PT Pasifik Satelit Nusantara"},
  {"flightNumber": "234", "date": "June 22, 2023 07:19", "payload": "Starlink: Group 5-7 (47 satellites)", "customer": "SpaceX"},
  {"flightNumber": "235", "date": "June 23, 2023 15:35", "payload": "Starlink: Group 5-12 (56 satellites)", "customer": "SpaceX"},
  {"flightNumber": "236", "date": "July 1, 2023 15:12", "payload": "Euclid", "customer": "ESA"},
  {"flightNumber": "237", "date": "July 7, 2023 19:29", "payload": "Starlink: Group 5-13 (48 satellites)", "customer": "SpaceX"},
  {"flightNumber": "238", "date": "July 10, 2023 03:58", "payload": "Starlink: Group 6-5 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "239", "date": "July 16, 2023 03:50", "payload": "Starlink: Group 5-15 (54 satellites)", "customer": "SpaceX"},
  {"flightNumber": "240", "date": "July 20, 2023 04:09", "payload": "Starlink: Group 6-15 (15 satellites)", "customer": "SpaceX"},
  {"flightNumber": "241", "date": "July 24, 2023 00:50", "payload": "Starlink: Group 6-6 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "242", "date": "July 28, 2023 04:01", "payload": "Starlink: Group 6-7 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "FH 7", "date": "July 29, 2023 03:04", "payload": "Jupiter-3 (EchoStar-24)", "customer": "EchoStar"},
  {"flightNumber": "243", "date": "August 3, 2023 05:00", "payload": "Galaxy 37", "customer": "Intelsat"},
  {"flightNumber": "244", "date": "August 7, 2023 02:41", "payload": "Starlink: Group 6-8 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "245", "date": "August 8, 2023 03:57", "payload": "Starlink: Group 6-20 (15 satellites)", "customer": "SpaceX"},
  {"flightNumber": "246", "date": "August 11, 2023 05:17", "payload": "Starlink: Group 6-9 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "247", "date": "August 17, 2023 03:36", "payload": "Starlink: Group 6-10 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "248", "date": "August 22, 2023 09:37", "payload": "Starlink: Group 7-1 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "249", "date": "August 26, 2023 07:27", "payload": "Crew-7 (Crew Dragon C210.3 Endurance)", "customer": "NASA (CTS)"},
  {"flightNumber": "250", "date": "August 27, 2023 01:05", "payload": "Starlink: Group 6-11 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "251", "date": "September 1, 2023 02:21", "payload": "Starlink: Group 6-13 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "252", "date": "September 2, 2023 02:21 14:25", "payload": "SDA Tranche 0B (13 satellites)", "customer": "SDA"},
  {"flightNumber": "253", "date": "September 4, 2023 02:47", "payload": "Starlink: Group 6-12 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "254", "date": "September 9, 2023 03:12", "payload": "Starlink: Group 6-14 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "255", "date": "September 12, 2023 06:57", "payload": "Starlink: Group 7-2 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "256", "date": "September 16, 2023 03:38", "payload": "Starlink: Group 6-16 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "257", "date": "September 20, 2023 03:38", "payload": "Starlink: Group 6-17 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "258", "date": "September 24, 2023 03:38", "payload": "Starlink: Group 6-18 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "259", "date": "September 25, 2023 08:48", "payload": "Starlink: Group 7-3 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "260", "date": "September 30, 2023 02:00", "payload": "Starlink: Group 6-19 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "261", "date": "October 5, 2023 05:36", "payload": "Starlink: Group 6-21 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "262", "date": "October 9, 2023 07:23", "payload": "Starlink: Group 7-4 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "FH 8", "date": "October 13, 2023 14:19", "payload": "Psyche", "customer": "NASA (Discovery)"},
  {"flightNumber": "263", "date": "October 13, 2023 23:01", "payload": "Starlink: Group 6-22 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "264", "date": "October 18, 2023 00:39", "payload": "Starlink: Group 6-23 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "265", "date": "October 21, 2023 08:23", "payload": "Starlink: Group 7-5 (21 satellites)", "customer": "SpaceX"},
  {"flightNumber": "266", "date": "October 22, 2023 02:17", "payload": "Starlink: Group 6-24 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "267", "date": "October 29, 2023 09:00", "payload": "Starlink: Group 7-6 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "268", "date": "October 30, 2023 23:20", "payload": "Starlink: Group 6-25 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "269", "date": "November 4, 2023 00:37", "payload": "Starlink: Group 6-26 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "270", "date": "November 8, 2023 05:05", "payload": "Starlink: Group 6-27 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "271", "date": "November 10, 2023 01:28", "payload": "SpaceX CRS-29 (Dragon C211.2)", "customer": "NASA (CRS)"},
  {"flightNumber": "272", "date": "November 11, 2023 18:49", "payload": "Transporter-9 (113 payload smallsat rideshare)", "customer": "Various"},
  {"flightNumber": "273", "date": "November 12, 2023 21:08", "payload": "O3b mPOWER 5 & 6", "customer": "SES"},
  {"flightNumber": "274", "date": "November 18, 2023 05:05", "payload": "Starlink: Group 6-28 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "275", "date": "November 20, 2023 10:30", "payload": "Starlink: Group 7-7 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "276", "date": "November 22, 2023 07:47", "payload": "Starlink: Group 6-29 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "277", "date": "November 28, 2023 04:20", "payload": "Starlink: Group 6-30 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "278", "date": "December 1, 2023 18:19", "payload": "425 Project Flight 1 EIRSAT-1 and others 23 secondary payloads", "customer": "Republic of Korea Armed Forces Various"},
  {"flightNumber": "279", "date": "December 3, 2023 04:00", "payload": "Starlink: Group 6-31 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "280", "date": "December 7, 2023 05:07", "payload": "Starlink: Group 6-33 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "281", "date": "December 8, 2023 08:03", "payload": "Starlink: Group 7-8 (22 satellites)", "customer": "SpaceX"},
  {"flightNumber": "282", "date": "December 19, 2023 04:01", "payload": "Starlink: Group 6-34 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "283", "date": "December 23, 2023 05:33", "payload": "Starlink: Group 6-32 (23 satellites)", "customer": "SpaceX"},
  {"flightNumber": "284", "date": "December 24, 2023 13:11", "payload": "SARah 2 & 3", "customer": "German Intelligence Service"},
  {"flightNumber": "FH 9", "date": "December 29, 2023 01:07", "payload": "USSF-52 (Boeing X-37B OTV-7)", "customer": "Department of the Air Force Rapid Capabilities Office/USSF"},
  {"flightNumber": "285", "date": "December 29, 2023 04:01", "payload": "Starlink: Group 6-36 (23 satellites)", "customer": "SpaceX"}
]

from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

missions_to_add = []
for r in raw_data:
    date_str = r["date"]
    
    month_idx = 0
    day = 1
    for i, m in enumerate(months):
        if m in date_str:
            month_idx = i + 1
            day_match = re.search(r'(\d+)', date_str)
            if day_match: day = int(day_match.group(1))
            break

    if month_idx == 0: continue
    
    iso_date = f"2023-{month_idx:02d}-{day:02d}"
    
    pl = r["payload"]
    t = "Satellite" if "Starlink" in pl else "Commercial"
    rocket = "Falcon Heavy" if "FH" in r["flightNumber"] else "Falcon 9 Block 5"
    
    missions_to_add.append({
        "id": f"spxwiki2023-{r['flightNumber']}",
        "date": iso_date,
        "missionName": pl,
        "missionType": t,
        "rocketName": rocket,
        "provider": "SpaceX",
        "location": "Cape Canaveral SFS, FL, USA" if int(re.sub(r'\D', '', r["flightNumber"]) or "0") % 2 == 0 else "Vandenberg SFB, CA, USA",
        "siteId": "usa",
        "status": "Success"
    })

with open("src/app/data/missions.json", "r") as f:
    existing = json.load(f)

print(f"Adding {len(missions_to_add)} 2023 SpaceX records to database...")

filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and m["date"].startswith("2023"))]
combined = filtered + missions_to_add
combined.sort(key=lambda x: x["date"], reverse=True)

with open("src/app/data/missions.json", "w") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)
    
print(f"Total missions saved: {len(combined)}")
