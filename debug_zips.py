import requests
import pandas as pd
import io

url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/2023_WA/csv"
print(f"Fetching from: {url}")

try:
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    # Clean columns
    df.columns = [c.split('.', 1)[-1].strip() if '.' in c else c.strip() for c in df.columns]
    
    # Extract zips
    zips = df['ZIP'].astype(str).apply(lambda x: x.split('-')[0]).unique()
    print(f"Total unique zips: {len(zips)}")
    print(f"First 20 zips: {zips[:20]}")
    
    target = '99021'
    if target in zips:
        print(f"SUCCESS: {target} found in data!")
    else:
        print(f"FAILURE: {target} NOT found in data.")
        
except Exception as e:
    print(f"Error: {e}")
