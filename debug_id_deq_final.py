import logging
from src.data_fetchers import fetch_id_deq_data, get_location_details

logging.basicConfig(level=logging.INFO)

def test_id_deq():
    zipcode = "83814"
    print(f"Testing ID DEQ Fetch for {zipcode}...")
    
    details = get_location_details(zipcode)
    lat = details['lat']
    lon = details['lon']
    
    sites = fetch_id_deq_data(zipcode, is_zip=True, lat=lat, lon=lon)
    
    print(f"Found {len(sites)} ID DEQ sites.")
    for s in sites[:5]:
        print(f" - {s['name']} ({s['type']}): {s['url']}")

if __name__ == "__main__":
    test_id_deq()
