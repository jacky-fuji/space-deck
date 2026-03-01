import json
import os

def merge():
    base_file = "src/app/data/missions.json"
    ea_file = "everyday_astronaut_missions.json"
    
    if not os.path.exists(base_file):
        print(f"Error: {base_file} not found")
        return
    if not os.path.exists(ea_file):
        print(f"Error: {ea_file} not found")
        return

    with open(base_file, "r", encoding="utf-8") as f:
        all_missions = json.load(f)
    
    with open(ea_file, "r", encoding="utf-8") as f:
        ea_missions = json.load(f)

    print(f"Base missions: {len(all_missions)}")
    print(f"Everyday Astronaut missions to merge: {len(ea_missions)}")

    added_count = 0
    updated_count = 0
    
    # Create a lookup key
    # (Date, Provider, Rocket - shortened)
    def get_key(m):
        # Normalize rocket name (e.g. "Falcon 9 Block 5" -> "Falcon 9")
        rocket = m.get("rocketName", "").lower()
        if "falcon 9" in rocket: rocket = "falcon 9"
        elif "falcon heavy" in rocket: rocket = "falcon heavy"
        elif "electron" in rocket: rocket = "electron"
        
        # Normalize date
        date = m.get("date", "TBD")
        
        return (date, rocket)

    mission_lookup = {}
    for i, m in enumerate(all_missions):
        key = get_key(m)
        if key not in mission_lookup:
            mission_lookup[key] = []
        mission_lookup[key].append(i)

    new_missions = []
    
    for ea_m in ea_missions:
        key = get_key(ea_m)
        match_idx = -1
        
        if key in mission_lookup:
            # Check mission name similarity
            best_score = 0
            for idx in mission_lookup[key]:
                existing = all_missions[idx]
                ea_name = ea_m.get("missionName", "").lower()
                ex_name = existing.get("missionName", "").lower()
                
                # Simple check
                if ea_name in ex_name or ex_name in ea_name:
                    match_idx = idx
                    break
        
        if match_idx != -1:
            # Update existing if EA has more info
            existing = all_missions[match_idx]
            # If status is "Success" but EA says "Failure", update it (unlikely but possible)
            if ea_m["status"] != "Scheduled" and existing["status"] != ea_m["status"]:
                existing["status"] = ea_m["status"]
                updated_count += 1
            
            # If EA has more specific mission name
            if len(ea_m["missionName"]) > len(existing["missionName"]):
                existing["missionName"] = ea_m["missionName"]
            
            # Update provider if EA is not Unknown
            if ea_m["provider"] != "Unknown" and existing.get("provider") == "Unknown":
                existing["provider"] = ea_m["provider"]
        else:
            # Add new
            all_missions.append(ea_m)
            added_count += 1

    print(f"Added {added_count} new missions.")
    print(f"Updated {updated_count} existing missions.")
    print(f"Total missions after merge: {len(all_missions)}")

    with open(base_file, "w", encoding="utf-8") as f:
        json.dump(all_missions, f, ensure_ascii=False, indent=2)
    print("Saved to missions.json")

if __name__ == "__main__":
    merge()
