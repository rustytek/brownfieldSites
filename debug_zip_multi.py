import requests
import json

def check_zip(zipcode):
    url = f"http://api.zippopotam.us/us/{zipcode}"
    print(f"Checking {zipcode}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_zip("99021") # WA
    check_zip("59601") # MT
    check_zip("83702") # ID
