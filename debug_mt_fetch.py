import logging
from src.data_fetchers import fetch_all_data, get_location_details

logging.basicConfig(level=logging.INFO)

def debug_mt_fetch():
    zipcode = "59601"
    print(f"--- Debugging Fetch for {zipcode} ---")
    
    # 1. Check Location Details
    details = get_location_details(zipcode)
    print(f"Location Details: {details}")
    
    if not details:
        print("Failed to get location details.")
        return

    state = details['state']
    print(f"Detected State: {state}")

    # 2. Fetch All Data
    sites, towers, mines, inactive_mines, hazardous_minerals = fetch_all_data(zipcode, is_zip=True, state=state)
    
    print(f"\n--- Results ---")
    print(f"Toxic Sites: {len(sites)}")
    for s in sites:
        print(f"  - Name: '{s.get('name')}' | Source: '{s.get('source')}' | Lat/Lon: {s.get('lat')}, {s.get('lon')}")
        
    print(f"Mines: {len(mines)}")
    for m in mines:
        print(f"  - Name: '{m.get('name')}' | Source: '{m.get('source')}' | Lat/Lon: {m.get('lat')}, {m.get('lon')}")

if __name__ == "__main__":
    debug_mt_fetch()
