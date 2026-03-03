import json
from collections import Counter

with open("src/app/data/missions.json", "r") as f:
    missions = json.load(f)

russia_terms = ["russia", "plesetsk", "baikonur", "kapustin-yar", "vostochny", "yasny", "svobodny", "kazakhstan", "ussr"]
usa_terms = ["usa", "canaveral", "vandenberg", "kennedy"]

soviet_cold_war = []
usa_cold_war = []

for m in missions:
    year = m.get("date", "")[:4]
    if "1960" <= year <= "1989":
        # Check normalized country if possible, or fallback to location string
        site = str(m.get("siteId", "")).lower()
        loc = str(m.get("location", "")).lower()
        
        # In our react UI, we mapped these to "russia" or "kazakhstan" but the raw JSON might have the original IDs
        if site in ["russia", "kazakhstan"] or any(term in loc for term in russia_terms) or site in russia_terms:
            soviet_cold_war.append(m)
        elif site == "usa" or any(term in loc for term in usa_terms) or site in usa_terms:
            usa_cold_war.append(m)

print(f"--- 1960-1989 OVERVIEW ---")
print(f"Total Soviet (Russia/Kazakhstan) launches: {len(soviet_cold_war)}")
print(f"Total US launches: {len(usa_cold_war)}")

# Check for duplicates in Soviet data Date+Rocket is a good proxy for identical launches
soviet_keys = [f"{m['date'][:10]}_{m['rocketName']}" for m in soviet_cold_war]
counter = Counter(soviet_keys)
duplicates = {k: v for k, v in counter.items() if v > 1}

print(f"\nPotential duplicate Date+Rocket combinations: {len(duplicates)}")
if duplicates:
    print("Sample of multi-payload / duplicate launches:")
    for k, v in list(duplicates.items())[:15]:
        # Print the actual payloads to see if they are distinct satellites or true duplicates
        payloads = [m['missionName'] for m in soviet_cold_war if f"{m['date'][:10]}_{m['rocketName']}" == k]
        print(f"  {k} ({v} times) -> Payloads: {', '.join(payloads[:3])}{'...' if len(payloads)>3 else ''}")

years = Counter([m['date'][:4] for m in soviet_cold_war])
print("\nSoviet launches by year (1960-1989):")
for y in sorted(years.keys()):
    print(f"  {y}: {years[y]} launches")

print("\nTop Soviet Rockets (1960-1989):")
rockets = Counter([m['rocketName'] for m in soviet_cold_war])
for r, c in rockets.most_common(10):
    print(f"  {r}: {c}")

