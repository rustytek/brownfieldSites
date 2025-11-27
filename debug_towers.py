import requests

# Test Broadcast Tower URL
url_towers = "https://opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0.geojson"
print(f"Testing Towers URL: {url_towers}")
try:
    response = requests.get(url_towers, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Features found: {len(data.get('features', []))}")
        if len(data.get('features', [])) > 0:
            print("Sample Tower properties:", data['features'][0]['properties'])
except Exception as e:
    print(f"Error Towers: {e}")
