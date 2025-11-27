import simplekml
import logging
import math

def generate_kml(sites, broadcast_towers, mines, inactive_mines, hazardous_minerals, search_term, output_file):
    """
    Generates a KML file with folders for Toxic Sites, Towers, Active Mines, Inactive Mines, and Hazardous Minerals.
    """
    kml = simplekml.Kml()
    
    logging.info(f"Generating KML for {len(sites)} sites, {len(broadcast_towers)} towers, {len(mines)} active mines, {len(inactive_mines)} inactive mines, {len(hazardous_minerals)} hazardous sites...")

    # Create Folders
    toxic_folder = kml.newfolder(name="Toxic Sites")
    # Dynamic folders based on content would be better, but for now let's make them generic or check sources
    # We'll create a dictionary to hold folder references
    folders = {}
    
    tri_folder = toxic_folder.newfolder(name="EPA TRI Facilities")
    folders['EPA TRI'] = tri_folder
    
    other_folder = toxic_folder.newfolder(name="Other Toxic Sites")
    folders['Other'] = other_folder
    
    towers_folder = kml.newfolder(name="Broadcast Towers")
    mines_folder = kml.newfolder(name="Mines") # Combined for simplicity, or split if needed
    haz_folder = kml.newfolder(name="Hazardous Minerals")

    # Add Toxic Sites
    for site in sites:
        # Determine folder and style based on source
        source = site.get('source', 'Unknown')
        
        if 'Ecology' in source:
            if 'WA Ecology' not in folders:
                folders['WA Ecology'] = toxic_folder.newfolder(name="WA Ecology Cleanup Sites")
            target_folder = folders['WA Ecology']
            
            # Rank coloring for Ecology
            rank = str(site.get('rank', ''))
            if rank == '6': color = simplekml.Color.pink
            elif rank in ['4', '5']: color = simplekml.Color.green
            elif rank == '3': color = simplekml.Color.yellow
            elif rank in ['0', '1', '2']: color = simplekml.Color.red
            else: color = simplekml.Color.blue
            
        elif 'TRI' in source:
            target_folder = tri_folder
            color = simplekml.Color.purple
            
        else:
            # Generic State Cleanup or Other
            if source not in folders:
                folders[source] = toxic_folder.newfolder(name=f"{source} Sites")
            target_folder = folders[source]
            color = simplekml.Color.brown

        # Ensure Name exists
        name = site.get('name') or "Unknown Site"
        
        pnt = target_folder.newpoint(name=name)
        pnt.coords = [(site['lon'], site['lat'])]
        pnt.description = f"Source: {source}<br/>Details: {site.get('details', '')}"
        pnt.style.iconstyle.color = color
        
        # Add Ring for Toxic Sites
        circle = target_folder.newpolygon(name=f"1 Mile Radius - {site['name']}")
        circle.outerboundaryis = create_circle(site['lat'], site['lon'], 1609.34) # 1 mile in meters
        circle.style.polystyle.color = simplekml.Color.changealphaint(100, color)
        circle.style.linestyle.color = color
        circle.style.linestyle.width = 2

    # Add Broadcast Towers
    for tower in broadcast_towers:
        pnt = towers_folder.newpoint(name=tower['name'])
        pnt.coords = [(tower['lon'], tower['lat'])]
        pnt.description = f"Source: {tower['source']}<br/>Details: {tower['details']}"
        # Use a Flag icon for towers
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
        pnt.style.iconstyle.color = simplekml.Color.cyan # Tinted Cyan

    # Add Active Mines
    for mine in mines:
        name = mine.get('name') or "Unknown Mine"
        pnt = mines_folder.newpoint(name=name)
        pnt.coords = [(mine['lon'], mine['lat'])]
        pnt.description = f"Source: {mine.get('source', 'Unknown')}<br/>Details: {mine.get('details', '')}"
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png'
        pnt.style.iconstyle.scale = 0.8
        pnt.style.iconstyle.color = simplekml.Color.orange
        
        # Add Ring for Mines (Orange)
        circle = mines_folder.newpolygon(name=f"1 Mile Radius - {name}")
        circle.outerboundaryis = create_circle(mine['lat'], mine['lon'], 1609.34)
        circle.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.orange)
        circle.style.linestyle.color = simplekml.Color.orange
        circle.style.linestyle.width = 2

    # Add Inactive Mines
    for mine in inactive_mines:
        name = mine.get('name') or "Unknown Inactive Mine"
        # If we want to separate them in the KML structure, we can create a subfolder or just add to mines_folder
        # Let's add to mines_folder but with different icon/color
        pnt = mines_folder.newpoint(name=name)
        pnt.coords = [(mine['lon'], mine['lat'])]
        pnt.description = f"Source: {mine.get('source', 'Unknown')}<br/>Details: {mine.get('details', '')}"
        # Use a shaded dot or similar for inactive
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
        pnt.style.iconstyle.scale = 0.8
        pnt.style.iconstyle.color = simplekml.Color.grey

    # Add Hazardous Minerals
    for site in hazardous_minerals:
        if site.get('geom_type') == 'Point':
            pnt = haz_folder.newpoint(name=site['name'])
            pnt.coords = [(site['lon'], site['lat'])]
            pnt.description = f"Source: {site['source']}<br/>Details: {site['details']}"
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/caution.png'
            pnt.style.iconstyle.color = simplekml.Color.brown
        elif site.get('geom_type') == 'Polygon':
            poly = haz_folder.newpolygon(name=site['name'])
            poly.outerboundaryis = site['rings'][0] # Use first ring
            poly.description = f"Source: {site['source']}<br/>Details: {site['details']}"
            poly.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.brown)
            poly.style.linestyle.color = simplekml.Color.brown
            poly.style.linestyle.width = 2

    kml.save(output_file)
    return True

def create_circle(lat, lon, radius_meters):
    """
    Returns a list of coordinates forming a circle around the point.
    """
    coords = []
    R = 6378137 # Earth's radius in meters
    
    for i in range(0, 361, 10): # 36 steps
        angle = math.radians(i)
        
        lat1 = math.radians(lat)
        lon1 = math.radians(lon)
        
        lat2 = math.asin(math.sin(lat1)*math.cos(radius_meters/R) + 
                         math.cos(lat1)*math.sin(radius_meters/R)*math.cos(angle))
        lon2 = lon1 + math.atan2(math.sin(angle)*math.sin(radius_meters/R)*math.cos(lat1), 
                                 math.cos(radius_meters/R)-math.sin(lat1)*math.sin(lat2))
        
        coords.append((math.degrees(lon2), math.degrees(lat2)))
        
    return coords
