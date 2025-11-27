import os
import sys
from src.data_fetchers import fetch_all_data, get_county_for_zip, get_location_details
from src.kml_generator import generate_kml

def main():
    print("--- ToxMap Scraper ---")
    user_input = input("Enter Zip Code or County Name (e.g., 99021 or Spokane): ").strip()
    
    is_zip = user_input.isdigit()
    search_term = user_input
    state = 'WA' # Default
    
    print(f"Fetching data for {search_term} ({'Zip' if is_zip else 'County'})...")
    
    # Zip-to-Location Expansion
    if is_zip:
        print("Looking up Location details...")
        details = get_location_details(search_term)
        if details:
            state = details['state']
            county = details['county'] # Note: Zippopotam might return City name as Place Name. 
            # For Zippopotam, 'place name' is usually city. 'county' is not always direct.
            # Let's rely on the state at least.
            # Actually, let's use get_county_for_zip for WA as fallback if Zippopotam is vague, 
            # but Zippopotam is good for State.
            
            print(f"--> Zip {search_term} is in {details['city']}, {state}.")
            
            # For WA, we still want the County expansion behavior
            if state == 'WA':
                wa_county = get_county_for_zip(search_term)
                if wa_county:
                    print(f"--> WA County identified: {wa_county}")
                    print(f"--> Switching to full County search for {wa_county} to include all data.")
                    search_term = wa_county
                    is_zip = False
            else:
                # For MT/ID, we might stick to Zip or try to find County.
                # Since we don't have a reliable Zip->County API for MT/ID implemented yet (Zippopotam 'place name' is city),
                # we will proceed with Zip search for now, OR fetch all for state and filter by proximity.
                # Fetching all for state is safer.
                print(f"--> Detected State: {state}")
        else:
            print("--> Could not determine location. Defaulting to WA.")

    # Fetch Data
    # sites contains Ecology (filtered) + TRI (all State) + others
    # towers contains all towers
    # mines contains all mines for State
    # inactive_mines contains all inactive mines (WA only)
    # hazardous_minerals contains all hazardous minerals (WA only)
    sites, towers, mines, inactive_mines, hazardous_minerals = fetch_all_data(search_term, is_zip, state)
    
    # Filter Data
    filtered_sites = []
    filtered_towers = []
    filtered_mines = []
    filtered_inactive_mines = []
    filtered_haz_minerals = []
    
    # Filter Sites
    for site in sites:
        if site['source'] == 'WA Ecology':
            # Already filtered by API
            filtered_sites.append(site)
        elif site['source'] == 'EPA TRI':
            # Filter by Zip or County
            if is_zip:
                if site['zip'] == search_term:
                    filtered_sites.append(site)
            else:
                # Filter by County (TRI county is usually UPPERCASE)
                if search_term.upper() in site['county']:
                    filtered_sites.append(site)
        else:
            # Other sources (placeholders)
            filtered_sites.append(site)
            
    # Filter Towers, Mines, Inactive Mines, Hazardous Minerals
    if not is_zip:
        # County Search - Filter by County Name
        target_county = search_term.upper()
        
        for mine in mines:
            if target_county in mine['county'].upper():
                filtered_mines.append(mine)
                
        for mine in inactive_mines:
            if target_county in mine['county'].upper():
                filtered_inactive_mines.append(mine)
                
        for site in hazardous_minerals:
            if site.get('county') and target_county in site['county'].upper():
                filtered_haz_minerals.append(site)
            elif not site.get('county'):
                 # Fallback to proximity for items without county
                 if filtered_sites:
                     # Calculate centroid for filtering
                     lats = [s['lat'] for s in filtered_sites]
                     lons = [s['lon'] for s in filtered_sites]
                     avg_lat = sum(lats) / len(lats)
                     avg_lon = sum(lons) / len(lons)
                     lat_range = 0.1
                     lon_range = 0.1
                     
                     if (avg_lat - lat_range <= site['lat'] <= avg_lat + lat_range) and \
                        (avg_lon - lon_range <= site['lon'] <= avg_lon + lon_range):
                         filtered_haz_minerals.append(site)
    
    # Spatial Filtering (Fallback or Zip)
    if filtered_sites:
        lats = [s['lat'] for s in filtered_sites]
        lons = [s['lon'] for s in filtered_sites]
        avg_lat = sum(lats) / len(lats)
        avg_lon = sum(lons) / len(lons)
        lat_range = 0.1
        lon_range = 0.1
        
        # Filter Towers (Always proximity)
        for tower in towers:
            if (avg_lat - lat_range <= tower['lat'] <= avg_lat + lat_range) and \
               (avg_lon - lon_range <= tower['lon'] <= avg_lon + lon_range):
                filtered_towers.append(tower)
                
        # Filter others if Zip search
        if is_zip:
             for mine in mines:
                if (avg_lat - lat_range <= mine['lat'] <= avg_lat + lat_range) and \
                   (avg_lon - lon_range <= mine['lon'] <= avg_lon + lon_range):
                    filtered_mines.append(mine)
             for mine in inactive_mines:
                if (avg_lat - lat_range <= mine['lat'] <= avg_lat + lat_range) and \
                   (avg_lon - lon_range <= mine['lon'] <= avg_lon + lon_range):
                    filtered_inactive_mines.append(mine)
             for site in hazardous_minerals:
                if (avg_lat - lat_range <= site['lat'] <= avg_lat + lat_range) and \
                   (avg_lon - lon_range <= site['lon'] <= avg_lon + lon_range):
                    filtered_haz_minerals.append(site)

    print(f"Found {len(filtered_sites)} Toxic Sites.")
    print(f"Found {len(filtered_towers)} Broadcast Towers (in range).")
    print(f"Found {len(filtered_mines)} Active Mines.")
    print(f"Found {len(filtered_inactive_mines)} Inactive Mines.")
    print(f"Found {len(filtered_haz_minerals)} Hazardous Mineral Sites.")
    
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    safe_term = "".join([c for c in search_term if c.isalnum() or c in (' ', '_')]).strip()
    output_file = os.path.join(output_dir, f"toxMap[{safe_term}].kml")
    
    print(f"Generating KML...")
    success = generate_kml(filtered_sites, filtered_towers, filtered_mines, filtered_inactive_mines, filtered_haz_minerals, search_term, output_file)
    
    if success:
        print(f"Successfully created: {output_file}")
    else:
        print("Failed to generate KML.")

if __name__ == "__main__":
    main()
