from fastkml import  kml, geometry
import os
import webbrowser
import pyautogui
import time

url_default_format = 'https://earth.google.com/web/@-0.24961457,-79.16049739,572.0950501a,625.87477459d,30y,-0h,0t,0r'
# here is lon, lat, dunno, elevation map, and defaults from 30y (also dunno)
url_desired = 'https://earth.google.com/web/@{},{},572.0950501a,{}d,30y,-0h,0t,0r'
browser_location = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
elevation_map = "400" # represents zoom

# one : kml.Document = None
take_off_lat = 0
take_off_lon = 0
land_lat = 0
land_lon = 0

def print_child_features(element):
    """ Prints the name of every child node of the given element,   recursively """
    if not getattr(element, 'features', None):
        return
    for feature in element.features():
        print(feature.name, end=" ")
        if isinstance(feature, kml.Placemark):  
            placemark : kml.Placemark = feature
            # print("This is a placemark", end=" ")
            if isinstance(placemark.geometry, geometry.Point):
                print(" longitude:", placemark.geometry.x, "latitude:", placemark.geometry.y)
                if(feature.name == "Take off"):
                    take_off_lat = placemark.geometry.x
                    take_off_lon = placemark.geometry.y
                    print("Opening Google Earth coordinates in Chrome browser")
                    webbrowser.get(browser_location).open_new_tab(url_desired.format(str(take_off_lon),str(take_off_lat), elevation_map))
                    
                    time.sleep(10) # wait 10 seconds to let the map load
                    im = pyautogui.screenshot(region=(57, 72, 1700, 873))
                    # im.   
                    im.save("take_off.png") # take the screenshot of the map
                elif(feature.name == "Land"):
                    land_lat = placemark.geometry.x
                    land_lon = placemark.geometry.y

                    
            elif isinstance(placemark.geometry, geometry.LineString):
                print("is a linestring")
            else:
                print("It's geometry:", placemark.geometry())
        print()

        # parse_placemarks(feature)
        print_child_features(feature)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    """
    Taken from https://stackoverflow.com/a/1969274/11326330
    This maps a range of values to another range for a specific value
    """
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


with open("square.kml") as f:
    doc = f.read()
    k = kml.KML()
    k.from_string(doc)
    print_child_features(k)
    
    