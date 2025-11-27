import requests

# Test WA Ecology URL (without county to see if it returns all)
url_ecology = "https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json"
print(f"Testing Ecology URL: {url_ecology}")
try:
    response = requests.get(url_ecology)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Records found: {len(data)}")
        if len(data) > 0:
            print("Sample Ecology record:", data[0])
except Exception as e:
    print(f"Error Ecology: {e}")

# Test Broadcast Tower URL
url_towers = "https://opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0.geojson"
print(f"\nTesting Towers URL: {url_towers}")
try:
    response = requests.get(url_towers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Features found: {len(data.get('features', []))}")
        if len(data.get('features', [])) > 0:
            print("Sample Tower properties:", data['features'][0]['properties'])
except Exception as e:
    print(f"Error Towers: {e}")
