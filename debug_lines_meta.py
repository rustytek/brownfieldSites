import requests

url = "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Electric_Power_Transmission_Lines/FeatureServer/0?f=json"
try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Fields:")
        for field in data.get('fields', []):
            print(f"{field['name']} ({field['alias']})")
except Exception as e:
    print(f"Error: {e}")
