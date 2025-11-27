import requests

# Test Ecology Zip Filter
zipcode = '99021'
url_ecology = f"https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json&Zip={zipcode}"
print(f"Testing Ecology URL: {url_ecology}")
try:
    response = requests.get(url_ecology)
    data = response.json()
    print(f"Ecology Records: {len(data)}")
    if len(data) > 0:
        print(f"Sample Zip: {data[0].get('ZipCode')}")
except Exception as e:
    print(f"Ecology Error: {e}")

# Test Towers URL with headers
url_towers = "https://opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0.geojson"
print(f"\nTesting Towers URL: {url_towers}")
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    response = requests.get(url_towers, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        # It might be a redirect or direct file
        # Check content type
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        # data = response.json() # This might fail if it's large or not json
        # print(f"Towers found: {len(data.get('features', []))}")
except Exception as e:
    print(f"Towers Error: {e}")
