#!/opt/local/bin/python3

"""
    wiki-geosearch.py

    Return the Wikipedia pages within the specified distance.

    Usage:
    Update the lat, lon and distance values below.

    Based on geosearch.py from MediaWiki API Demos, which has a MIT License
    spiralPrint is from https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/, license unknown

    MIT License
"""

import requests
import geolocation

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

# Gerlach, Nevada
lat=40.651389
lon=-119.356667

# Temagami, ON
lat=47.066667
lon=-79.783333

# X,Y dimensions of the area in km.  Must be greater than
# 10km. Multiples of 10 may get "Bounding box is too big", so try
# numbers that end in 9.
distance = 19 

headers = {
    'User-Agent': 'WikiGeoSearch/0.1 (User:Cxbrx)',
    'From': 'cxbrooks@gmail.com'
}

# Given a bounding box in (lat, lon) query the database for pages within that bounding box.
def geosearch(top, left, bottom, right):
    # print("geosearch: ", top, left, bottom, right);
    PARAMS = {
        "format": "json",
        "list": "geosearch",
        #"gscoord": "40.651389|-119.356667",
        #"gsradius": "10000",
        "gsbbox": "%s|%s|%s|%s" %(top, left, bottom, right),
        "action": "query"
    }

    R = S.get(url=URL, params=PARAMS, headers=headers)
    DATA = R.json()
    # print(DATA)

    if 'error' in DATA:
        raise Exception(DATA['error'])

    PLACES = DATA['query']['geosearch']
    # for place in PLACES:
    #    print(place['title'])

    return PLACES


# The maximum number of places in a reading list.  See https://www.mediawiki.org/wiki/Extension:ReadingLists
MAX_PLACES = 1000 

# Get the places in the bounding box and add them to the all_places list
# If all_places is full return false.
def geoplaces(sw, ne, all_places):
    PLACES = geosearch(ne.deg_lat, sw.deg_lon, sw.deg_lat, ne.deg_lon)
    for place in PLACES:
        all_places[place[key]] = place
        # print(place['title'])
        if len(all_places) >= MAX_PLACES:
            return False
    return True

# The geolocation api limits us to 10,000m radius (see
# https://www.mediawiki.org/wiki/Extension:ReadingLists), so we make
# multiple calls.  We get the bounding box for the area and then
# divide the box in to 10km patches starting at the center patch, we
# work our way outwards in a spiral collecting pages until we finish or we get to
# 1000, which is the maximum number of entries per list.

ALL_PLACES = {}  # All of the places collected thus far
key='pageid'

# Bounding box of the entire area.
#
# Test data:
# SW_all = geolocation.GeoLocation.from_degrees(40, -120)
# NE_all = geolocation.GeoLocation.from_degrees(43, -117)
# lat_step = 1
# lon_step = 1
center = geolocation.GeoLocation.from_degrees(lat,lon)
SW_all, NE_all = center.bounding_locations(distance)
# print("center: ", center.deg_lat, center.deg_lon)
# print("SW_all: ", SW_all.deg_lat, SW_all.deg_lon)
# print("NE_all: ", NE_all.deg_lat, NE_all.deg_lon)

# Each patch cannot be more than 10km x 10km.
steps = round(distance/10)
lat_step = (NE_all.deg_lat - SW_all.deg_lat)/steps
lon_step = (NE_all.deg_lon - SW_all.deg_lon)/steps
# print("steps: ", steps, lat_step, lon_step)

# Populate the patches array with SW, NE points.
patches = [[0 for x in range(steps)] for y in range(steps)] 
for x in range(0, steps):
    for y in range(0, steps):
        SW = geolocation.GeoLocation.from_degrees(SW_all.deg_lat + y * lat_step,
                                                  SW_all.deg_lon + x * lon_step)
        NE = geolocation.GeoLocation.from_degrees(SW_all.deg_lat + (y+1) * lat_step,
                                                  SW_all.deg_lon + (x+1) * lon_step)
        # print("patches: ", x, y, SW.deg_lat, SW.deg_lon, NE.deg_lat, NE.deg_lon)
        patches[x][y] = {'SW': SW, 'NE': NE}

# Python3 program to print  
# given matrix in spiral form 
# From https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/  License unknown.
def spiralPrint(m, n, a) : 
    k = 0; l = 0
  
    ''' k - starting row index 
        m - ending row index 
        l - starting column index 
        n - ending column index 
        i - iterator '''
      
  
    while (k < m and l < n) : 
          
        # Print the first row from 
        # the remaining rows  
        for i in range(l, n) : 
            place = a[k][i]
            sw = place['SW']
            ne = place['NE']
            #print("A: ", k, i, sw, sw.deg_lat, sw.deg_lon, a[k][i], end = " ") 
            # print("(", sw.deg_lat, sw.deg_lon, " ", ne.deg_lat, ne.deg_lon, ")", end = " ")
            if not geoplaces(sw, ne, ALL_PLACES):
                return False

        k += 1
  
        # Print the last column from 
        # the remaining columns  
        for i in range(k, m) : 
            place = a[i][n - 1]
            sw = place['SW']
            ne = place['NE']
            #print("B: ", i, n - 1, a[i][n - 1], end = " ") 
            if not geoplaces(sw, ne, ALL_PLACES):
                return False
              
        n -= 1

        # Print the last row from 
        # the remaining rows  
        if ( k < m) : 
              
            for i in range(n - 1, (l - 1), -1) : 
                place = a[m - 1][i]
                sw = place['SW']
                ne = place['NE']
                #print("C: ", m - 1, i, a[m - 1][i], end = " ") 
                if not geoplaces(sw, ne, ALL_PLACES):
                    return False
              
            m -= 1
          
        # Print the first column from 
        # the remaining columns  
        if (l < n) : 
            for i in range(m - 1, k - 1, -1) : 
                place = a[i][l]
                sw = place['SW']
                ne = place['NE']
                #print("D: ", i, l, a[i][l], end = " ") 
                if not geoplaces(sw, ne, ALL_PLACES):
                    return False

            l += 1

spiralPrint(steps, steps, patches)

for place in ALL_PLACES:
    print(ALL_PLACES[place]['title'])
