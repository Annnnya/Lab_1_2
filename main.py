"""
program that shows the closest locations of films' shootings
"""

import argparse
import ssl
import re
import folium
import certifi
import haversine as hs
import geopy.geocoders
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

def location_finder(line):
    """
    Processes the line of the file to find the substring that contains the location
    and finds its coordinates
    >>> location_finder('"26 Men" (1957)						Phoenix, Arizona, USA')
    (33.4484367, -112.0741417)
    """
    if '}' in line:
        line = line[line.index('}')+1:].strip()
    else:
        line = line[(re.search(r'\([1-2][0-9][0-9][0-9]\)', line).end()+1):].strip()
    if line[0]=='(':
        line = line[line.find(')')+1:].strip()
    if '(' in line:
        line = line[:line.find('(')].strip()
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(user_agent="main.py", scheme = 'http')
    location = geolocator.geocode(line, timeout=None)
    def corrector(loc):
        try:
            loc = loc[loc.index(',') + 1:]
        except ValueError:
            return None
        # print(loc)
        location = geolocator.geocode(loc, timeout=None)
        if location is not None:
            return location.latitude, location.longitude
        else:
            return corrector(loc)
    if location is not None:
        return location.latitude, location.longitude
    else:
        return corrector(line)

def reading_from_file(path, year, us_loc):
    """
    This function reads from the file and forms a list of
    names, distances from givem location and locations of the films

    Note: the doctest is with the full path to file on my computer
    >>> print(reading_from_file\
('C:/Users/asus/progrexp/lab_2_1/locations_for_documentation.list', 2016, (28.426846,77.088834)))
    [('Emerald City', 5333.275543922748, (47.1817585, 19.5060937)), \
('Girl Unburdened', 13051.682503244176, (32.7174202, -117.1627728)), \
('Jazz y chistes Show', 6770.824381160194, (41.3828939, 2.1774322)), \
('Dan Bell Cutting/Room/Floor #22: Final Night in the Meat Factory', \
12007.03879384452, (39.2908816, -76.610759))]
    """
    res = []
    date_pat = '\('+str(year)+'\)'
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if re.search(date_pat, line):
                    name = line[:(re.search(date_pat, line).start() - 1)].strip('"').strip("'")
                    # print(location_finder(line))
                    # print((name, hs.haversine(location_finder(line), us_loc)))
                    loc = location_finder(line)
                    if loc is not None:
                        res.append((name, hs.haversine(loc, us_loc), loc))
        return res
    except FileNotFoundError:
        print('Something wrong with your file path')
        quit()

def map_creation(films, my_loc):
    """
    This function creates a map from list of films and their locations
    """
    films = sorted(films, key=lambda x:x[1])[:10]
    # print(films)
    mapp = folium.Map(location = my_loc, zoom_start = 3, control_scale = True)
    markers_group = folium.FeatureGroup(name = "Film Markers")
    my_marker = folium.FeatureGroup(name = "My marker")
    marker_cluster = MarkerCluster([i[2] for i in films], name = "Markers of distanse")
    mapp.add_child(markers_group)
    mapp.add_child(my_marker)
    mapp.add_child(marker_cluster)
    iframe0 = folium.IFrame("my location", width = 100, height = 100)
    my_marker.add_child(folium.Marker(location=my_loc, popup=folium.Popup(iframe0)))
    for film in films:
        iframe = folium.IFrame(film[0], width = 200, height = 100)
        markers_group.add_child(folium.Marker(location=film[2], popup=folium.Popup(iframe)))
    mapp.add_child(folium.LayerControl())
    mapp.save('map_of_films.html')

def main():
    """
    This function takes arguments from the user and
    calls all necessary functions to create a map
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="the year of the films ypu want to find", type=str)
    parser.add_argument("latitude", help="the latitude of your location", type=str)
    parser.add_argument("longitude", help="the longitude of your location", type=str)
    parser.add_argument("path_to_file", help="path to the file with info aboit films", type=str)
    args = parser.parse_args()
    if re.search('[1-2][0-9][0-9][0-9]', args.year):
        try:
            latitude = float(args.latitude)
            longitude = float(args.longitude)
            assert -90 <= latitude <= 90 and -180 <= longitude <=180
            the_location = (latitude, longitude)
            map_creation(reading_from_file(args.path_to_file, args.year, the_location),\
                 the_location)
        except AssertionError:
            print('please enter valid coordinates')
        except  ValueError:
            print('please enter valid coordinates')
    else:
        print('please enter a valid year')

if __name__ == "__main__":
    main()

# import doctest
# doctest.testmod()
