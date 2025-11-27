import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def probe_id_deq():
    # Potential server URL from search results
    base_url = "https://mapcase.deq.idaho.gov/arcgis/rest/services"
    
    print(f"Probing {base_url}...")
    
    params = {'f': 'json'}
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Folders:")
            for folder in data.get('folders', []):
                print(f" - {folder}")
                
            print("\nServices:")
            for service in data.get('services', []):
                print(f" - {service['name']} ({service['type']})")
                
            # Check for specific folders like 'Waste' or 'Remediation'
            # If folders exist, we should probe them too
            for folder in data.get('folders', []):
                folder_url = f"{base_url}/{folder}"
                print(f"\nProbing Folder: {folder}...")
                try:
                    f_resp = requests.get(folder_url, params=params, timeout=10)
                    if f_resp.status_code == 200:
                        f_data = f_resp.json()
                        for service in f_data.get('services', []):
                            print(f"   - {service['name']} ({service['type']})")
                except Exception as e:
                    print(f"   Error probing folder {folder}: {e}")

    except Exception as e:
        print(f"Error probing root: {e}")

if __name__ == "__main__":
    probe_id_deq()
