import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def fetch_sample(url, name):
    print(f"\n--- Fetching Sample for {name} ---")
    print(f"URL: {url}")
    try:
        response = requests.get(url + "/query", params={'where': '1=1', 'outFields': '*', 'f': 'json', 'resultRecordCount': 1}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            if features:
                print(f"Found {len(features)} features.")
                print(json.dumps(features[0], indent=2))
            else:
                print("No features found.")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def search_arcgis_online(query):
    print(f"\n--- Searching ArcGIS Online for: {query} ---")
    url = "https://www.arcgis.com/sharing/rest/search"
    params = {
        'q': query,
        'f': 'json',
        'num': 5,
        'type': 'Feature Service'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"Found {len(results)} results:")
            for r in results:
                print(f"  - Title: {r['title']}")
                print(f"    URL: {r['url']}")
                print(f"    Owner: {r['owner']}")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Refined URLs
urls = [
    # Montana MBMG - Candidate Service
    ("https://services9.arcgis.com/QjBb6o7pu37CDH58/arcgis/rest/services/Mine_MBMG2006_shp/FeatureServer", "MT MBMG Mine_MBMG2006"),
    
    # Idaho DEQ - Try Waste Folder directly
    ("https://mapcase.deq.idaho.gov/arcgis/rest/services/Waste", "ID DEQ Waste Folder"),
    
    # MT DEQ - Try a different server found in search results
    ("https://gis.deq.mt.gov/arcgis/rest/services", "MT DEQ GIS Root (Alternative)"),
]

if __name__ == "__main__":
    # Verify MT DEQ URL (Constructed)
    fetch_sample("https://services3.arcgis.com/W9iqPyJhy06cNrrs/arcgis/rest/services/Montana_State_Superfund_(SSU)_Facility_Areas/FeatureServer/0", "MT DEQ State Superfund (Candidate)")
