import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import glob

# Function to generate the current time with a step of one second for each point
def generate_time(index):
    base_time = datetime(2023, 11, 28, 12, 42, 50)
    return (base_time + timedelta(seconds=index)).isoformat() + "Z"

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

# Process all GPX files in the input folder
input_files = glob.glob('input/*.gpx')

for input_filename in input_files:
    # Derive the output filename
    base_name = os.path.basename(input_filename)
    output_filename = os.path.join('output', base_name.replace('.gpx', '_new.gpx'))

    # Parse the input GPX file
    tree = ET.parse(input_filename)
    root = tree.getroot()

    # Create the new GPX structure
    gpx = ET.Element('gpx', {
        'xmlns': "http://www.topografix.com/GPX/1/1",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd",
        'version': "1.1",
        'creator': "murbit GPX Tracker"
    })

    trk = ET.SubElement(gpx, 'trk')
    trkseg = ET.SubElement(trk, 'trkseg')

    # Add each waypoint as a track point
    for index, wpt in enumerate(root.findall('wpt')):
        lon = wpt.get('lon')
        lat = wpt.get('lat')
        ele = wpt.find('ele').text
        magvar = wpt.find('magvar').text
        hdop = wpt.find('hdop').text
        vdop = wpt.find('vdop').text
        speed = wpt.find('speed').text
        time = generate_time(index)

        trkpt = ET.SubElement(trkseg, 'trkpt', {'lon': lon, 'lat': lat})
        ET.SubElement(trkpt, 'ele').text = ele
        ET.SubElement(trkpt, 'time').text = time
        ET.SubElement(trkpt, 'magvar').text = magvar
        ET.SubElement(trkpt, 'hdop').text = hdop
        ET.SubElement(trkpt, 'vdop').text = vdop
        ET.SubElement(trkpt, 'speed').text = speed

    # Write the resulting GPX to the output file
    tree = ET.ElementTree(gpx)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)

    print(f"Converted GPX saved to {output_filename}")