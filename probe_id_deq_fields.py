import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def probe_layer_fields():
    base_url = "https://mapcase.deq.idaho.gov/arcgis/rest/services/SWA_PCI_WMS/MapServer"
    layers_to_check = [12, 28] # 12: PCI Locations, 28: Landfill
    
    params = {'f': 'json'}
    
    for layer_id in layers_to_check:
        url = f"{base_url}/{layer_id}"
        print(f"\n--- Probing Layer {layer_id} ---")
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Name: {data.get('name')}")
                print("Fields:")
                for field in data.get('fields', []):
                    print(f" - {field['name']} ({field['type']})")
        except Exception as e:
            print(f"Error probing layer {layer_id}: {e}")

if __name__ == "__main__":
    probe_layer_fields()
