import requests
import json

url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Active_Surface_Mine_Permit_Sites/MapServer/0/query"
params = {
    'where': "1=1", # Select all (or filter by county if needed)
    'outFields': '*',
    'f': 'json',
    'resultRecordCount': 5
}

print(f"Testing WA DNR Mines URL: {url}")
try:
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if 'json' in response.headers.get('Content-Type', '') or 'text/plain' in response.headers.get('Content-Type', ''):
        # ArcGIS sometimes returns text/plain for json
        try:
            data = response.json()
            print(f"Features found: {len(data.get('features', []))}")
            if len(data.get('features', [])) > 0:
                print("Sample Feature:")
                print(json.dumps(data['features'][0], indent=2))
        except:
            print("Failed to parse JSON from text/plain response.")
            print(response.text[:500])
    else:
        print("Response is not JSON. Text:")
        print(response.text[:1000])
except Exception as e:
    print(f"Error: {e}")
