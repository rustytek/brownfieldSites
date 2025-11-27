import requests
import json

def get_county_from_ecology(zipcode):
    # Use the Ecology API which we know has Zip and County data
    url = f"https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json&Zip={zipcode}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Iterate to find the specific zip match, as API might return all
                for item in data:
                    item_zip = str(item.get('ZipCode', ''))
                    if str(zipcode) in item_zip:
                        county = item.get('County')
                        if county:
                            return county
    except Exception as e:
        print(f"Error: {e}")
    return None

zips = ['99021', '98108']
for z in zips:
    county = get_county_from_ecology(z)
    print(f"Zip {z} -> County: {county}")
