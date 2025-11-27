import requests

urls = [
    "https://data.epa.gov/efservice/frs_interest/state_code/WA/interest_type/SUPERFUND%20NPL/JSON",
    "https://data.epa.gov/efservice/frs_interest/state_code/WA/interest_type/RCRAINFO/JSON"
]

for url in urls:
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Records found: {len(data)}")
            if len(data) > 0:
                print("Sample record:", data[0])
    except Exception as e:
        print(f"Error: {e}")
