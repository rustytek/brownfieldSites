import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_wa_dnr_inactive_mines():
    """
    Fetches Inactive and Abandoned Mine Lands (IAML) from WA DNR.
    Layer 8: IAML Sites (Points)
    """
    logging.info("Fetching WA DNR Inactive Mines (IAML)...")
    mines = []
    url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Mines_and_Minerals/MapServer/8/query"
    params = {
        'where': "1=1",
        'outFields': '*',
        'f': 'json',
        'outSR': '4326'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        logging.info(f"Raw features count: {len(features)}")
        
        if len(features) > 0:
            logging.info(f"Sample Feature: {json.dumps(features[0], indent=2)}")
        
        for feature in features:
            attrs = feature.get('attributes', {})
            geom = feature.get('geometry', {})
            
            # IAML Sites are points
            lat = attrs.get('LATITUDE')
            lon = attrs.get('LONGITUDE')
            
            # Fallback to geometry if attributes missing
            if not lat or not lon:
                if 'y' in geom and 'x' in geom:
                    lat = geom['y']
                    lon = geom['x']
            
            if not lat or not lon:
                continue
                
            mine = {
                'name': attrs.get('SITE_NAME', 'Unknown Inactive Mine'),
                'lat': lat,
                'lon': lon,
                'county': str(attrs.get('COUNTY', '')).upper(),
                'source': 'WA DNR Inactive Mines',
                'details': f"Commodity: {attrs.get('COMMODITY', 'Unknown')}; Comments: {attrs.get('COMMENT', 'None')}",
                'type': 'Inactive Mine'
            }
            mines.append(mine)
            
        logging.info(f"Parsed {len(mines)} Inactive Mines.")
        return mines
        
    except Exception as e:
        logging.error(f"Error fetching Inactive Mines: {e}")
        return []

def fetch_wa_dnr_hazardous_minerals():
    logging.info("Fetching WA DNR Hazardous Minerals...")
    haz_sites = []
    layers = {14: "Hazardous Minerals", 15: "Mercury", 16: "Asbestos", 17: "Arsenic", 18: "Asbestos Rocks", 20: "Radon", 21: "Uranium Rocks"}
    base_url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Mines_and_Minerals/MapServer"
    
    for layer_id, layer_name in layers.items():
        url = f"{base_url}/{layer_id}/query"
        params = {'where': "1=1", 'outFields': '*', 'f': 'json', 'outSR': '4326'}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            features = data.get('features', [])
            logging.info(f"Layer {layer_id} ({layer_name}): Found {len(features)} features.")
            
            for feature in features:
                attrs = feature.get('attributes', {})
                site = {
                    'name': attrs.get('SITE_NAME', 'Unknown'),
                    'county': str(attrs.get('COUNTY', '')).upper()
                }
                haz_sites.append(site)
        except Exception as e:
            logging.error(f"Error layer {layer_id}: {e}")
    return haz_sites

if __name__ == "__main__":
    mines = fetch_wa_dnr_inactive_mines()
    print(f"Total Inactive Mines: {len(mines)}")
    mine_counties = set(m['county'] for m in mines)
    print(f"Inactive Mines Counties: {sorted(list(mine_counties))}")
    
    haz = fetch_wa_dnr_hazardous_minerals()
    print(f"Total Hazardous Sites: {len(haz)}")
    haz_counties = set(h['county'] for h in haz)
    print(f"Hazardous Sites Counties: {sorted(list(haz_counties))}")
    
    if 'SPOKANE' in mine_counties:
        print(f"Inactive Mines in Spokane: {len([m for m in mines if m['county'] == 'SPOKANE'])}")
    else:
        print("Inactive Mines in Spokane: 0")
        
    if 'SPOKANE' in haz_counties:
        print(f"Hazardous Minerals in Spokane: {len([h for h in haz if h['county'] == 'SPOKANE'])}")
    else:
        print("Hazardous Minerals in Spokane: 0")
