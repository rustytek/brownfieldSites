import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def probe_services():
    base_url = "https://mapcase.deq.idaho.gov/arcgis/rest/services"
    services_to_check = [
        "SWA_PCI_WMS",
        "SWA_ADMIN_WMS",
        "GWQ"
    ]
    
    params = {'f': 'json'}
    
    for service in services_to_check:
        url = f"{base_url}/{service}/MapServer"
        print(f"\n--- Probing {service} ---")
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("Layers:")
                for layer in data.get('layers', []):
                    print(f" - {layer['id']}: {layer['name']}")
                    
                    # Probe layer fields for the first layer to see content
                    if layer['id'] == 0:
                        layer_url = f"{url}/0"
                        l_resp = requests.get(layer_url, params=params, timeout=10)
                        if l_resp.status_code == 200:
                            l_data = l_resp.json()
                            print(f"   Fields for Layer 0:")
                            for field in l_data.get('fields', [])[:5]: # First 5 fields
                                print(f"    - {field['name']} ({field['type']})")
        except Exception as e:
            print(f"Error probing {service}: {e}")

if __name__ == "__main__":
    probe_services()
