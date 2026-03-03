import json

MISSIONS_FILE = "src/app/data/missions.json"

def analyze():
    with open(MISSIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Look for payloads mistaken as rockets (e.g., long sentences, "Launch of...")
    bad_rockets = []
    
    # 2. Look for location data in rocket or provider fields
    misaligned = []
    
    # Known site names that might appear in the wrong columns
    sites = ["canaveral", "kennedy", "vandenberg", "plesetsk", "vostochny", "jiuquan", "xichang", "kourou", "mahia"]

    for m in data:
        rocket = str(m.get("rocketName", "")).lower()
        provider = str(m.get("provider", "")).lower()
        
        # Check for bad rockets (likely payloads)
        if "launch of" in rocket or len(rocket) > 40:
            bad_rockets.append(m)
            
        # Check for misaligned location data
        for site in sites:
            if site in rocket or site in provider:
                misaligned.append(m)
                break

    print(f"--- Suspect Rockets (Payloads captured as rockets) ({len(bad_rockets)} found) ---")
    for m in bad_rockets[:10]:
         print(f"ID: {m.get('id')}\n  Date: {m.get('date')}\n  Rocket Field: {m.get('rocketName')}\n  Payload Field: {m.get('missionName')}\n")

    print(f"\n--- Misaligned Location Data ({len(misaligned)} found) ---")
    for m in misaligned[:10]:
         print(f"ID: {m.get('id')}\n  Rocket: {m.get('rocketName')}\n  Provider: {m.get('provider')}\n  Location: {m.get('location')}\n")

if __name__ == "__main__":
    analyze()
