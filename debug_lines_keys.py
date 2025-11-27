import requests

url = "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Electric_Power_Transmission_Lines/FeatureServer/0/query?where=1=1&outFields=*&resultRecordCount=1&f=geojson"
try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data.get('features', [])) > 0:
            props = data['features'][0]['properties']
            print("Keys:", list(props.keys()))
except Exception as e:
    print(f"Error: {e}")
