import requests

# Test WA Ecology URL with Zip
zipcode = '99021'
url_ecology = f"https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json&Zip={zipcode}"
print(f"Testing Ecology URL with Zip {zipcode}: {url_ecology}")
try:
    response = requests.get(url_ecology, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Records found: {len(data)}")
        if len(data) > 0:
            print("Sample Ecology record:", data[0])
            # Check for SiteRank
            print("SiteRank:", data[0].get('SiteRank'))
except Exception as e:
    print(f"Error Ecology: {e}")
