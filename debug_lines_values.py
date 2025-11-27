import requests

url = "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Electric_Power_Transmission_Lines/FeatureServer/0/query?where=1=1&outFields=SUB_1,SUB_2,OWNER,ID&resultRecordCount=5&f=geojson"
try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for f in data.get('features', []):
            print(f['properties'])
except Exception as e:
    print(f"Error: {e}")
