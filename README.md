# Geodesic Lines to GIS

[![Build Status](https://travis-ci.org/GeographicaGS/GeodesicLinesToGIS.svg?branch=master)](https://travis-ci.org/GeographicaGS/GeodesicLinesToGIS)
[![PyPI version](https://badge.fury.io/py/GeodesicLinesToGIS.svg)](http://badge.fury.io/py/GeodesicLinesToGIS)

Computes geodesic lines from start point to end point and stores them in a GIS 
file (Shapefile and GeoJSON). A geodesic is the shortest path between two 
points on a curved surface, like an ellipsoid of revolution ([Read more on Wikipedia](http://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid)).

This code is builded on top of three libraries: Pyproj, Fiona and Shapely.

There are several libraries to compute geodesic distances solving the geodesic 
inverse problem (to find the shortest path between two given points). 
I chose Pyproj because it works fine for this purpose and is an interface to a 
widely used library in the geospatial industry (Proj4 C library). Actually Proj4 C 
library (>= v.4.9.0) routines used to compute geodesic distance are a simple transcription 
from excellent Geographiclib C++ Library developed by Charles Karney. Proj4 C library < v.4.9.0 
uses Paul D. Thomas algorithms. You can see more about this here: 
[GeodeticMusings: a little benchmark of three Python libraries to compute geodesic distances](https://github.com/cayetanobv/GeodeticMusings).

All computations are performed with WGS84 ellipsoid and the CRS (Coordinate 
Reference System) of GIS file outputs are EPSG:4326.

In the examples section you can see the problem of calculating lines crossing 
antimeridian is solved.

## Installing
You can install this package from PYPI:
https://pypi.python.org/pypi/GeodesicLinesToGIS

```bash
$ pip install GeodesicLinesToGIS
```

## Geodesic lines examples
Below are shown different geodesic lines computed with this library on several 
map projections. Also you can see the relation with rhumb lines (loxodromic) 
and straight lines between the same points.

- Geodesic line (computed): green.
- Loxodromic: red.
- Straight line: dashed black.

Maximun differences occur between Mercator (loxodromic is a straight line) 
and Gnomonic projection (geodesic is a straight line).

[Data and maps are here] (https://github.com/GeographicaGS/GeodesicLinesToGIS/tree/master/data)
 
![Mercator1](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_merc.png)
__Mercator projection__ - Proj4 string:
_'+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



![Gnomonic](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_gnom.png)
__Gnomonic projection__ (centered: 50W and 60N)
Proj4 string:
_'+proj=gnom +lat_0=60 +lon_0=-50 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



![Azimuthal Equidistant](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_azim.png)
__Azimuthal Equidistant projection__ (centered: 50W and 30N) - Proj4 string:
_'+proj=aeqd +lat_0=30 +lon_0=-50 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



![Lambert Azimuthal Equal Area](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_laea.png)
__Lambert Azimuthal Equal Area projection__ (centered: 50W and 60N)
Proj4 string:
_'+proj=laea +lat_0=60 +lon_0=-50 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



## Antimeridian problem solved
You can see the problem of calculating lines crossing antimeridian is solved.

![Mercator2](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/Antimeridian.png)
__Mercator projection__ - Proj4 string:
_'+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



![Mercator3](https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/Antimeridian_2.png)
__Mercator projection__ (centered: 150E) - Proj4 string:
_'+proj=merc +lon_0=150 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'_



## Requirements
- Pyproj, https://github.com/jswhit/pyproj
- Fiona, https://github.com/Toblerity/Fiona
- Shapely, https://github.com/Toblerity/Shapely

## Usage
Usage is very simple. There are two modes:
- Single input (one start/end).
- Multiple input (more than one start/end).

### Single input
Single input usage.
```python
from geodesiclinestogis import GeodesicLine2Gisfile
```
lons_lats: input coordinates.
(start longitude, start latitude, end longitude, end latitude) 
```python
lons_lats = (-3.6,40.5,-118.4,33.9)
```

Folder path to store output file and filename:
```python
folderpath = '/tmp'

layername = "geodesicline"
```

Create object. You can pass two parameters:
- antimeridian: [True | False] to solve antimeridian problem (default is True).
- prints: [True | False] print output messages (default is True).

```python
gtg = GeodesicLine2Gisfile()
```
Launch computations. You can pass two parameter:
- lons_lats: input coords returned by gcComp.
- km_pts: compute one point each n km (default is 20 km)

```python
cd = gtg.gdlComp(lons_lats, km_pts=30)
```

Dump geodetic line coords to Linestring Feature and store in a GIS file.

Output formats: "ESRI Shapefile" (default), "GeoJSON"

```python
# shapefile output
gtg.gdlToGisFile(cd, folderpath, layername)

# geojson output
gtg.gdlToGisFile(cd, folderpath, layername, fmt="GeoJSON")
```

### Multiple input
Multiple input usage.
```python
from geodesiclinestogis import GeodesicLine2Gisfile

data = [
        (-6.,37.,-145.,11.),
        (-150.,37.,140.,11.),
        (-6.,37.,120.,50.),
        (-3.6,40.5,-118.4,33.9),
        (-118.4,33.9,139.8,35.5),
        (-118.4,33.9,104.,1.35),
        (-118.4,33.9,151.,-33.9),
        (-20.4,33.9,178.,-33.9)
    ]

folderpath = "/tmp/geod_line"

layername = "geodesicline"
    
gtg = GeodesicLine2Gisfile()
    
gtg.gdlToGisFileMulti(data, folderpath, layername)
```


## About author
Developed by Cayetano Benavent.
GIS Analyst at Geographica.

http://www.geographica.gs

## License
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

## Third-Party licenses
You can read Pyproj, Fiona and Shapely licenses in the next links:
https://raw.githubusercontent.com/jswhit/pyproj/master/LICENSE
https://raw.githubusercontent.com/Toblerity/Shapely/master/LICENSE.txt
https://raw.githubusercontent.com/Toblerity/Fiona/master/LICENSE.txt
