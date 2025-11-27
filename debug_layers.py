import requests
import json

url = "https://gis.dnr.wa.gov/site1/rest/services/Public_Geology/Mines_and_Minerals/MapServer/18/query"
params = {
    'where': "1=1",
    'outFields': '*',
    'f': 'json',
    'resultRecordCount': 1,
    'outSR': '4326'
}

print(f"Testing WA DNR IAML Sites URL: {url}")
try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Features found: {len(data.get('features', []))}")
        if len(data.get('features', [])) > 0:
            print("Sample Feature:")
            print(json.dumps(data['features'][0], indent=2))
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
