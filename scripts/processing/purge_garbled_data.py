import json
import os
import re

MISSIONS_FILE = "src/app/data/missions.json"

def deep_clean_edge_cases():
    if not os.path.exists(MISSIONS_FILE):
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    cleaned = []
    removed = 0

    for m in missions:
        loc = m.get("location", "").strip().lower()
        payload = m.get("missionName", "").strip().lower()
        rocket = m.get("rocketName", "").strip().lower()
        
        # 1. Drop rows where location is an orbit type, a date, or a mission name
        is_bad_loc = any(x in loc for x in ["low earth", "sso", "transporter", "fh-", "suborbital", "geosynchronous", "geostationary", "leo ", "gto "])
        
        # 2. Drop rows where payload is a date or raw HTML artifacts
        is_bad_payload = any(char.isdigit() for char in payload) and ("-" in payload or "20" in payload) and len(payload) < 20
        # If the payload looks like a garbled date or HTML entity (e.g. "&#91;" )
        is_garbled_payload = "&#9" in payload or payload == "-" or payload == "" or "tba" == payload
        
        # If the payload is just a date string "1 July 2013"
        date_pattern = re.compile(r'^\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}')
        is_date_payload = bool(date_pattern.search(payload))

        if is_bad_loc or is_garbled_payload or is_date_payload:
            removed += 1
            continue
            
        cleaned.append(m)

    print(f"Removed {removed} garbled edge-case records.")
    print(f"Total pristine orbital missions remaining: {len(cleaned)}")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    deep_clean_edge_cases()
