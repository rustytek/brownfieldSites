import requests

url = "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Electric_Power_Transmission_Lines/FeatureServer/0/query?where=SUB_1='WA'&outFields=*&resultRecordCount=5&f=geojson"
print(f"Testing URL: {url}")
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Features found: {len(data.get('features', []))}")
        if len(data.get('features', [])) > 0:
            print("Sample feature properties:", data['features'][0]['properties'])
except Exception as e:
    print(f"Error: {e}")
