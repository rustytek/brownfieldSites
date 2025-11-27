import requests
import pandas as pd
import io

url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/2023_WA/csv"
print(f"Fetching from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status()
    print("Download successful.")
    
    # Print first 500 chars to see raw content
    print("\n--- Raw Content Start ---")
    print(response.text[:500])
    print("--- Raw Content End ---\n")
    
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Columns found: {list(df.columns)}")
    print(f"Total rows: {len(df)}")
    
    # Check for latitude/longitude columns
    print(f"LATITUDE column exists: {'LATITUDE' in df.columns}")
    print(f"LONGITUDE column exists: {'LONGITUDE' in df.columns}")
    
    if 'LATITUDE' in df.columns:
        print(f"First 5 rows of LATITUDE:\n{df['LATITUDE'].head()}")

except Exception as e:
    print(f"Error: {e}")
