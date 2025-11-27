import simplekml
import json
import math
import urllib.request
from urllib.parse import quote
from math import sin, cos, sqrt, atan2
from simplekml import Types

def generate_circle(kml, lat_deg, lon_deg, radius_km, siteRank):
    scaled_radius_km = radius_km
    # Mean Earth radius (needed for calculation).
    earth_radius_km = 6371
    earth_radius_m = earth_radius_km * 1000
    # Distance is entered in km, convert to meters.
    radius_m = scaled_radius_km * 1000
    angular_distance = radius_m/earth_radius_m
    # Convert coordinates from degrees to radians.
    lat_rad = math.radians(lat_deg)
    lon_rad = math.radians(lon_deg)
    # Create a list of angles at which to create points (how many points will the circle consist of).
    numPoints = range(0, 360, 10)
    angles = []
    for x in numPoints:
        angles.append(float(x))
    angles.append(float(0))
    
    tuppleLatLongsInner = []
    # Calculate and file.write out the list of coordinates.
    for angle in angles:
        # Convert bearing to radians and calculates new lat/lon values
        bearing = math.radians(angle)
        new_lat = math.asin(math.sin(lat_rad) * math.cos(angular_distance) + math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing))
        new_lon = lon_rad + math.atan2(math.sin(bearing) * math.sin(angular_distance) * math.cos(lat_rad), math.cos(angular_distance) - math.sin(lat_rad) * math.sin(new_lat))
        # Convert new lat and lon to degrees
        new_lat_deg = math.degrees(new_lat)
        new_lon_deg = math.degrees(new_lon)
        # Print them out
        tuppleLatLongsInner.append((new_lon_deg, new_lat_deg))
        
    pol = kml.newlinestring(name="Risk zone", coords=tuppleLatLongsInner)
    pol.extrude = 1
    pol.altitudemode = simplekml.AltitudeMode.relativetoground
    pol.style.linestyle.width = 2
    
    if( siteRank  == '6'):
        pol.style.linestyle.color = simplekml.Color.pink
        pol.style.linestyle.width = 2
    elif( siteRank  == '4'):
        pol.style.linestyle.color = simplekml.Color.green
        pol.style.linestyle.width = 2
    elif( siteRank  == '3'):
        pol.style.linestyle.color = simplekml.Color.yellow
    elif( siteRank  == '2'):
        pol.style.linestyle.color = simplekml.Color.red
    elif( siteRank  == '1'):
        pol.style.linestyle.color = simplekml.Color.red
    elif( siteRank  == '0'):
        pol.style.linestyle.color = simplekml.Color.red
    else:
        print("NO Site hazard rank")
        pol.style.linestyle.color = simplekml.Color.blue

def rangeToPoint(lat_deg, lon_deg):
    R = 6373.0
    lat1 = 47.64782919095977
    lon1 = -117.36023898827709
    lat2 = lat_deg
    lon2 = lon_deg
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    print(distance)
    return distance

# countyName = input("Enter name of county: ")
# print("Processing " + countyName + " county data")
# countyURLLookup = "https://apps.ecology.wa.gov/cleanupsearch/reports/cleanup/all/export?format=json&County=" + quote(countyName)
# with urllib.request.urlopen(countyURLLookup) as url:
#    brownFieldData = json.loads(url.read().decode())

# with urllib.request.urlopen("https://opendata.arcgis.com/datasets/2bfd434d9263401eadae464a9c26104f_0.geojson") as url:
#    broadcastTowerData = json.loads(url.read().decode())
