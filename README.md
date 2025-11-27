# Brownfield Sites & ToxMap Scraper

A Python tool to scrape, aggregate, and visualize toxic sites, mines, and broadcast towers for Washington, Montana, and Idaho. The tool generates a KML file for visualization in Google Earth.

## Features

*   **Multi-State Support**: Fetches data for Washington (WA), Montana (MT), and Idaho (ID).
*   **Data Aggregation**: Combines data from multiple sources:
    *   **Toxic Sites**: WA Department of Ecology, EPA TRI (Toxic Release Inventory).
    *   **Mines**: WA DNR (Active & Inactive), Montana Bureau of Mines and Geology (MBMG), Idaho Geological Survey (IGS).
    *   **Broadcast Towers**: HIFLD Open Data.
    *   **Hazardous Minerals**: WA DNR (Mercury, Asbestos, Arsenic, Radon, etc.).
*   **Smart Filtering**:
    *   **Zip Code Search**: Automatically detects state and county from Zip Code.
    *   **County Search**: Fetches all data for a specific county.
    *   **Proximity Filtering**: Filters mines and towers within a configurable radius (default 10 miles) of toxic sites when searching by Zip.
*   **KML Generation**:
    *   Color-coded icons based on site rank or type.
    *   Distinct folders for different data types (Toxic Sites, Mines, Towers).
    *   Proximity rings around sites.
    *   Polygon support for hazardous mineral zones.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/rustytek/brownfieldSites.git
    cd brownfieldSites
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script:

```bash
python main.py
```

Enter a **Zip Code** (e.g., `99021`, `59601`) or a **County Name** (e.g., `Spokane`, `Lewis and Clark`).

The script will:
1.  Identify the location and state.
2.  Fetch data from relevant state and federal APIs.
3.  Generate a `toxic_sites_combined.kml` file in the project directory.
4.  Open the KML file automatically (if Google Earth is installed).

## Data Sources

*   **Washington**: WA Dept of Ecology, WA DNR.
*   **Montana**: Montana Bureau of Mines and Geology (MBMG), EPA.
*   **Idaho**: Idaho Geological Survey (IGS), EPA.
*   **Federal**: EPA TRI, HIFLD (Broadcast Towers).

## License

[MIT License](LICENSE)
