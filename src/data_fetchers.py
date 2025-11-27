import requests
import pandas as pd
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_epa_tri_data(year=2023, state='WA'):
    """
    Fetches EPA TRI Basic Data for a specific year and state.
    Returns a list of dictionaries with site details.
    """
    logging.info(f"Fetching EPA TRI data for {state} {year}...")
    # Updated URL pattern found via browser investigation
    url = f"https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/{year}_{state}/csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse CSV
        df = pd.read_csv(io.StringIO(response.text))
        
        # Clean column names (remove "1. ", "2. ", etc.)
        df.columns = [c.split('.', 1)[-1].strip() if '.' in c else c.strip() for c in df.columns]
        
        sites = []
        for _, row in df.iterrows():
            # Filter out rows without coordinates
            if pd.isna(row.get('LATITUDE')) or pd.isna(row.get('LONGITUDE')):
                continue
                
            site = {
                'name': row.get('FACILITY_NAME', 'Unknown Facility'),
                'address': row.get('STREET_ADDRESS', ''),
                'city': row.get('CITY', ''),
                'county': str(row.get('COUNTY', '')).upper(), # Added County
                'zip': str(row.get('ZIP', '')).split('-')[0], # Handle zip+4
                'lat': row.get('LATITUDE'),
                'lon': row.get('LONGITUDE'),
                'source': 'EPA TRI',
                'url': url,
                'details': f"Chemicals: {row.get('CHEMICAL', 'N/A')}; Carcinogen: {row.get('CARCINOGEN', 'N/A')}",
                'rank': 'N/A' # TRI doesn't have a simple rank, default to N/A
            }
            sites.append(site)
            
        logging.info(f"Found {len(sites)} sites from EPA TRI.")
        return sites
        
    except Exception as e:
        logging.error(f"Error fetching EPA TRI data: {e}")
        return []

def fetch_transmission_lines():
    """
    Fetches High Voltage Transmission Lines.
    DISABLED per user request.
    """
    logging.info("Fetching Transmission Lines... (DISABLED)")
    return []

def fetch_broadcast_towers():
    """
    Fetches Broadcast Towers from ArcGIS Open Data.
    Returns a list of dictionaries with tower details.
    """
    logging.info("Fetching Broadcast Towers...")
    url = "https://opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0.geojson"
    
    # Add User-Agent to avoid 400 Bad Request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        towers = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geom = feature.get('geometry', {})
            
            if geom.get('type') == 'Point':
                coords = geom.get('coordinates', [])
                if len(coords) >= 2:
                    lon, lat = coords[0], coords[1]
                    
                    tower = {
                        'name': props.get('CALLSIGN', 'Unknown Tower'),
                        'lat': lat,
                        'lon': lon,
                        'source': 'Broadcast Towers',
                        'url': 'https://hifld-geoplatform.opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0',
                        'details': f"Licensee: {props.get('LICENSEE', 'Unknown')}; ERP: {props.get('ERP', 'Unknown')}",
                        'type': 'Tower'
                    }
                    towers.append(tower)
                    
        logging.info(f"Found {len(towers)} broadcast towers.")
        return towers
        
    except Exception as e:
        logging.error(f"Error fetching Broadcast Towers: {e}")
        return []

def fetch_wa_dnr_mines():
    """
    Fetches Active Surface Mine Permits from WA DNR.
    Returns a list of dictionaries with mine details.
    """
    logging.info("Fetching WA DNR Active Surface Mines...")
    url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Active_Surface_Mine_Permit_Sites/MapServer/0/query"
    params = {
        'where': "1=1",
        'outFields': '*',
        'f': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Handle text/plain response from ArcGIS
        try:
            data = response.json()
        except:
            if 'json' in response.headers.get('Content-Type', '') or 'text/plain' in response.headers.get('Content-Type', ''):
                 data = json.loads(response.text)
            else:
                raise ValueError("Invalid response format")

        mines = []
        for feature in data.get('features', []):
            attrs = feature.get('attributes', {})
            geom = feature.get('geometry', {})
            
            if geom.get('x') and geom.get('y'):
                # ArcGIS REST API returns x/y in the spatial reference of the map service.
                # We need to check if it's lat/lon (4326) or Web Mercator (3857).
                # The debug output showed "LATITUDE": 47.61127832, "LONGITUDE": -117.71024752 in attributes.
                # We should use those if available, as x/y might need projection.
                
                lat = attrs.get('LATITUDE')
                lon = attrs.get('LONGITUDE')
                
                if not lat or not lon:
                    # Fallback to geometry if attributes missing (unlikely based on debug)
                    # Assuming geometry is already lat/lon or we'd need to project.
                    # Debug output showed x: 2328464, y: 842918 which looks like State Plane or similar.
                    # Safest to use LATITUDE/LONGITUDE attributes.
                    continue

                mine = {
                    'name': attrs.get('MINE_NAME', 'Unknown Mine'),
                    'lat': lat,
                    'lon': lon,
                    'county': str(attrs.get('COUNTY_NAME', '')).upper(),
                    'source': 'WA DNR Mines',
                    'url': 'https://fortress.wa.gov/dnr/protectiongis/geology/?theme=surface_mining',
                    'details': f"Applicant: {attrs.get('APPLICANT_NAME', 'Unknown')}; Commodity: {attrs.get('COMMODITY_DESC', 'Unknown')}; Permit: {attrs.get('MINE_PERMIT_NUMBER', 'Unknown')}",
                    'type': 'Mine'
                }
                mines.append(mine)
                    
        logging.info(f"Found {len(mines)} mines.")
        return mines
        
    except Exception as e:
        logging.error(f"Error fetching WA DNR Mines: {e}")
        return []

def fetch_wa_ecology_data(search_term, is_zip=True):
    """
    Fetches WA Ecology Cleanup Sites using the user-provided API.
    Supports filtering by Zip or County.
    """
    logging.info(f"Fetching WA Ecology Cleanup Sites for {'Zip' if is_zip else 'County'} {search_term}...")
    
    base_url = "https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json"
    if is_zip:
        url = f"{base_url}&Zip={search_term}"
    else:
        url = f"{base_url}&County={search_term}"
        
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        sites = []
        for item in data:
            # Client-side filtering to be safe (API might ignore params)
            item_zip = str(item.get('ZipCode', ''))
            item_county = str(item.get('County', '')).upper()
            
            if is_zip:
                # Strict Zip filtering
                if search_term not in item_zip:
                     continue
            else:
                # Strict County filtering
                if search_term.upper() not in item_county:
                    continue

            # Extract contaminants
            contaminants = []
            if item.get('Contaminants'):
                for c in item['Contaminants']:
                    c_name = c.get('ContaminantName', 'Unknown')
                    media = []
                    if c.get('GroundWater'): media.append('GroundWater')
                    if c.get('SurfaceWater'): media.append('SurfaceWater')
                    if c.get('Soil'): media.append('Soil')
                    if c.get('Air'): media.append('Air')
                    contaminants.append(f"{c_name} ({', '.join(media)})")
            
            details = f"Status: {item.get('SiteStatus')}; Rank: {item.get('SiteRank')}; Contaminants: {'; '.join(contaminants)}"
            
            site = {
                'name': item.get('SiteName', 'Unknown Site'),
                'address': item.get('Address', ''),
                'city': item.get('City', ''),
                'county': item.get('County', ''),
                'zip': str(item.get('ZipCode', '')),
                'lat': item.get('Latitude'),
                'lon': item.get('Longitude'),
                'source': 'WA Ecology',
                'url': f"https://apps.ecology.wa.gov/gsp/Sitepage.aspx?csid={item.get('CleanupSiteID')}",
                'details': details,
                'rank': str(item.get('SiteRank', 'N/A'))
            }
            sites.append(site)
            
        logging.info(f"Found {len(sites)} sites from WA Ecology (after filtering).")
        return sites
        
    except Exception as e:
        logging.error(f"Error fetching WA Ecology data: {e}")
        return []

def fetch_epa_superfund_data():
    return []

def fetch_epa_rcra_data():
    return []

def fetch_all_data(search_term, is_zip=True, state='WA', lat=None, lon=None):
    """
    Orchestrates fetching data from all sources based on state.
    """
    sites = []
    towers = []
    mines = []
    inactive_mines = []
    hazardous_minerals = []
    
    # 1. Toxic Sites
    # WA Ecology (Only for WA)
    if state == 'WA':
        sites.extend(fetch_wa_ecology_data(search_term, is_zip))
    
    # EPA TRI (All States)
    sites.extend(fetch_epa_tri_data(state=state))
    
    # 2. Broadcast Towers (All States - HIFLD is national)
    towers = fetch_broadcast_towers()
    
    # 3. Mines & Minerals (State Specific)
    if state == 'WA':
        mines = fetch_wa_dnr_mines()
        inactive_mines = fetch_wa_dnr_inactive_mines()
        hazardous_minerals = fetch_wa_dnr_hazardous_minerals()
    elif state == 'MT':
        mines = fetch_mt_mines(lat=lat, lon=lon)
        # MT MBMG includes inactive/abandoned in the same layer, so we put them in 'mines'
    elif state == 'ID':
        mines = fetch_id_mines(lat=lat, lon=lon)
    
    return sites, towers, mines, inactive_mines, hazardous_minerals

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
        
        for feature in data.get('features', []):
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
                'url': 'https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Mines_and_Minerals/MapServer/8',
                'details': f"Commodity: {attrs.get('COMMODITY', 'Unknown')}; Comments: {attrs.get('COMMENT', 'None')}",
                'type': 'Inactive Mine'
            }
            mines.append(mine)
            
        logging.info(f"Found {len(mines)} Inactive Mines.")
        
    except Exception as e:
        logging.error(f"Error fetching Inactive Mines: {e}")
        
    return mines

def fetch_wa_dnr_hazardous_minerals():
    """
    Fetches Hazardous Minerals from WA DNR.
    Layers: 14-18, 20-21.
    """
    logging.info("Fetching WA DNR Hazardous Minerals...")
    haz_sites = []
    
    # Layer IDs and Names
    layers = {
        14: "Hazardous Minerals", # Likely Group, but we check
        15: "Mercury Locations",
        16: "Asbestos Locations",
        17: "Arsenic Locations",
        18: "Asbestos Bearing Rocks", # Polygon
        20: "Radon Hazard--Radon Locations",
        21: "Radon Hazard--Uranium Bearing Rocks" # Polygon
    }
    
    base_url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Mines_and_Minerals/MapServer"
    
    for layer_id, layer_name in layers.items():
        logging.info(f"Fetching Layer {layer_id}: {layer_name}...")
        url = f"{base_url}/{layer_id}/query"
        params = {
            'where': "1=1",
            'outFields': '*',
            'f': 'json',
            'outSR': '4326' # Request Lat/Lon for all
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                continue
                
            data = response.json()
            features = data.get('features', [])
            
            for feature in features:
                attrs = feature.get('attributes', {})
                geom = feature.get('geometry', {})
                
                site = {
                    'name': attrs.get('SITE_NAME', attrs.get('NAMED_UNITS', layer_name)),
                    'source': f"WA DNR {layer_name}",
                    'url': f"{base_url}/{layer_id}",
                    'details': f"Layer: {layer_name}; Lithology: {attrs.get('LITHOLOGY', 'N/A')}; Commodity: {attrs.get('COMMODITY', 'N/A')}",
                    'type': 'Hazardous Mineral',
                    'layer_id': layer_id,
                    'county': str(attrs.get('COUNTY', '')).upper()
                }
                
                # Handle Geometry
                if 'x' in geom and 'y' in geom:
                    # Point
                    site['lat'] = geom['y']
                    site['lon'] = geom['x']
                    site['geom_type'] = 'Point'
                elif 'rings' in geom:
                    # Polygon
                    site['rings'] = geom['rings']
                    site['geom_type'] = 'Polygon'
                    # Calculate centroid for filtering
                    # Simple average of first ring
                    ring = geom['rings'][0]
                    avg_lon = sum(p[0] for p in ring) / len(ring)
                    avg_lat = sum(p[1] for p in ring) / len(ring)
                    site['lat'] = avg_lat
                    site['lon'] = avg_lon
                else:
                    continue
                
                haz_sites.append(site)
                
        except Exception as e:
            logging.error(f"Error fetching layer {layer_id}: {e}")
            
    logging.info(f"Found {len(haz_sites)} Hazardous Mineral sites/areas.")
    return haz_sites

def get_county_for_zip(zipcode):
    """
    Determines the county for a given zip code using the WA Ecology API.
    Returns the county name (string) or None if not found.
    """
    logging.info(f"Looking up County for Zip {zipcode}...")
    url = f"https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json&Zip={zipcode}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data:
            # Iterate to find the specific zip match
            # API might return all sites if filter fails, so we must check zip
            for item in data:
                item_zip = str(item.get('ZipCode', ''))
                if str(zipcode) in item_zip:
                    county = item.get('County')
                    if county:
                        logging.info(f"Found County: {county}")
                        return county
    except Exception as e:
        logging.error(f"Error looking up county: {e}")
    
    return None

def get_location_details(zipcode):
    """
    Determines State, County, and City from Zip Code using Zippopotam.us.
    Returns a dict with details or None.
    """
    url = f"http://api.zippopotam.us/us/{zipcode}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            place = data['places'][0]
            return {
                'zip': zipcode,
                'state': place['state abbreviation'],
                'county': place['place name'], # Zippopotam returns City as place name, need to check if it has county
                'city': place['place name'],
                'lat': float(place['latitude']),
                'lon': float(place['longitude'])
            }
    except Exception as e:
        logging.error(f"Error looking up zip {zipcode}: {e}")
    return None

def fetch_mt_mines(lat=None, lon=None, radius_miles=10):
    """
    Fetches mines from Montana Bureau of Mines and Geology (MBMG).
    Service: Mine_MBMG2006_shp
    If lat/lon provided, filters by bounding box in API query.
    """
    logging.info("Fetching Montana Mines (MBMG)...")
    mines = []
    url = "https://services9.arcgis.com/QjBb6o7pu37CDH58/arcgis/rest/services/Mine_MBMG2006_shp/FeatureServer/0/query"
    
    params = {
        'where': "1=1",
        'outFields': '*',
        'f': 'json',
        'outSR': '4326'
    }
    
    if lat and lon:
        # Create bounding box
        offset = radius_miles * 0.02 # Approx conversion
        xmin, ymin = lon - offset, lat - offset
        xmax, ymax = lon + offset, lat + offset
        params['geometry'] = f"{xmin},{ymin},{xmax},{ymax}"
        params['geometryType'] = 'esriGeometryEnvelope'
        params['spatialRel'] = 'esriSpatialRelIntersects'
        params['inSR'] = '4326'
        logging.info(f"Querying MT Mines in bbox: {params['geometry']}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for feature in data.get('features', []):
            attrs = feature.get('attributes', {})
            geom = feature.get('geometry', {})
            
            lat_val = attrs.get('DLAT') or geom.get('y')
            lon_val = attrs.get('DLONG') or geom.get('x')
            
            if not lat_val or not lon_val:
                continue
                
            mine = {
                'name': attrs.get('Name', 'Unknown Mine'),
                'lat': lat_val,
                'lon': lon_val,
                'county': str(attrs.get('County', '')).upper(),
                'source': 'MT MBMG Mines',
                'url': 'https://services9.arcgis.com/QjBb6o7pu37CDH58/arcgis/rest/services/Mine_MBMG2006_shp/FeatureServer/0',
                'details': f"Type: {attrs.get('Prop_Type', 'Unknown')}; Status: {attrs.get('Status', 'Unknown')}; Commodity: {attrs.get('Com', 'Unknown')}",
                'type': 'Mine'
            }
            mines.append(mine)
            
        logging.info(f"Parsed {len(mines)} MT Mines.")
        return mines
    except Exception as e:
        logging.error(f"Error fetching MT Mines: {e}")
        return []

def fetch_id_mines(lat=None, lon=None, radius_miles=10):
    """
    Fetches mines from Idaho Geological Survey (IGS).
    Service: Mines and Prospects
    If lat/lon provided, filters by bounding box in API query.
    """
    logging.info("Fetching Idaho Mines (IGS)...")
    mines = []
    url = "https://services.arcgis.com/WLhB60Nqwp4NnHz3/arcgis/rest/services/Mines/FeatureServer/0/query"
    
    params = {
        'where': "1=1",
        'outFields': '*',
        'f': 'json',
        'outSR': '4326'
    }
    
    if lat and lon:
        # Create bounding box
        offset = radius_miles * 0.02
        xmin, ymin = lon - offset, lat - offset
        xmax, ymax = lon + offset, lat + offset
        params['geometry'] = f"{xmin},{ymin},{xmax},{ymax}"
        params['geometryType'] = 'esriGeometryEnvelope'
        params['spatialRel'] = 'esriSpatialRelIntersects'
        params['inSR'] = '4326'
        logging.info(f"Querying ID Mines in bbox: {params['geometry']}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for feature in data.get('features', []):
            attrs = feature.get('attributes', {})
            geom = feature.get('geometry', {})
            
            # IGS attributes might differ
            lat_val = attrs.get('NAD27lat') or geom.get('y')
            lon_val = attrs.get('NAD27long') or geom.get('x')
            
            if not lat_val or not lon_val:
                continue
                
            mine = {
                'name': attrs.get('PropName', 'Unknown Mine'),
                'lat': lat_val,
                'lon': lon_val,
                'county': str(attrs.get('County', '')).upper(),
                'source': 'ID IGS Mines',
                'url': 'https://services.arcgis.com/WLhB60Nqwp4NnHz3/arcgis/rest/services/Mines/FeatureServer/0',
                'details': f"Commodity: {attrs.get('Commod1', 'Unknown')}; Type: {attrs.get('PropType', 'Unknown')}",
                'type': 'Mine'
            }
            mines.append(mine)
            
        logging.info(f"Parsed {len(mines)} ID Mines.")
        return mines
    except Exception as e:
        logging.error(f"Error fetching ID Mines: {e}")
        return []
