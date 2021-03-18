import webbrowser
browser_location = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
url_desired = 'https://earth.google.com/web/@{},{},572.0950501a,{}d,30y,-0h,0t,0r'
elevation_map = "400" # represents zoom

lon = -79.16225205
lat = -0.24856393

# upleft
webbrowser.get(browser_location).open_new_tab(url_desired.format(str(lat),str(lon), elevation_map))

lat = -0.25031801
lon = -79.15883064
# downright
webbrowser.get(browser_location).open_new_tab(url_desired.format(str(lat),str(lon), elevation_map))