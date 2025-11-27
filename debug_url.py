import requests

urls = [
    "https://data.epa.gov/efservice/downloads/tri/basic/2022/WA/csv",
    "https://data.epa.gov/efservice/downloads/tri/basic/2023/wa/csv",
    "https://data.epa.gov/efservice/downloads/tri/basic/2021/WA/csv"
]

for url in urls:
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS!")
            break
    except Exception as e:
        print(f"Error: {e}")
