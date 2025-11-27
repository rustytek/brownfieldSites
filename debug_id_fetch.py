import logging
from src.data_fetchers import fetch_all_data, get_location_details

logging.basicConfig(level=logging.INFO)

def debug_id_fetch():
    zipcode = "83814"
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
    
    print(f"\n--- Raw Results ---")
    print(f"Toxic Sites (Total Fetched): {len(sites)}")
    
    # Check EPA TRI Zip Codes
    tri_matches = 0
    for s in sites:
        if s.get('source') == 'EPA TRI':
            if str(s.get('zip')) == zipcode:
                tri_matches += 1
            # print sample zips
            # print(f"  TRI Site Zip: {s.get('zip')}")
            
    print(f"EPA TRI Sites exactly matching {zipcode}: {tri_matches}")

    print(f"Mines (Total Fetched): {len(mines)}")
    
    # Check Mine Coordinates vs Zip Center
    center_lat = details['lat']
    center_lon = details['lon']
    lat_range = 0.15
    lon_range = 0.15
    
    mines_in_range = 0
    for m in mines:
        if (center_lat - lat_range <= m['lat'] <= center_lat + lat_range) and \
           (center_lon - lon_range <= m['lon'] <= center_lon + lon_range):
            mines_in_range += 1
            
    print(f"Mines in range of {center_lat}, {center_lon}: {mines_in_range}")

if __name__ == "__main__":
    debug_id_fetch()
