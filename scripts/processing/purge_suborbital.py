import json
import os

MISSIONS_FILE = "src/app/data/missions.json"

def purge_suborbital():
    if not os.path.exists(MISSIONS_FILE):
        return

    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        missions = json.load(f)

    orbital_missions = []
    removed_count = 0

    for m in missions:
        loc = m.get("location", "").lower()
        rocket = m.get("rocketName", "").lower()
        payload = m.get("missionName", "").lower()
        
        # Identify suborbital or atmospheric tests
        is_suborbital = any(x in loc for x in ["suborbital", "transatmospheric", "atmospheric", "sounding"])
        is_test_flight = "test flight" in payload and "suborbital" in loc
        
        # Additional cleanup: Mislabeled sites that shouldn't be here
        is_misc = "unknown site" in loc and ("jenna" in payload or "that's not a knife" in payload)
        
        if is_suborbital or is_test_flight or is_misc:
            removed_count += 1
        else:
            orbital_missions.append(m)

    print(f"Removed {removed_count} suborbital/non-standard missions.")
    print(f"Total remaining orbital missions: {len(orbital_missions)}")

    with open(MISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(orbital_missions, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    purge_suborbital()
