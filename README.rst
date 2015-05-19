Geodesic Lines to GIS
=====================

.. image:: https://travis-ci.org/GeographicaGS/GeodesicLinesToGIS.svg?branch=master
    :target: https://travis-ci.org/GeographicaGS/GeodesicLinesToGIS

Computes geodesic lines from start point to end point and stores them in
a GIS file (Shapefile and GeoJSON). A geodesic is the shortest path
between two points on a curved surface, like an ellipsoid of revolution
(`Read more on
Wikipedia <http://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid>`__).

This code is builded on top of three libraries: Pyproj, Fiona and
Shapely.

There are several libraries to compute geodesic distances solving the geodesic 
inverse problem (to find the shortest path between two given points). 
I chose Pyproj because it works fine for this purpose and is an interface to a 
widely used library in the geospatial industry (Proj4 C library). Actually Proj4 C 
library (>= v.4.9.0) routines used to compute geodesic distance are a simple transcription 
from excellent Geographiclib C++ Library developed by Charles Karney. Proj4 C library < v.4.9.0 
uses Paul D. Thomas algorithms. You can see more about this here:
`GeodeticMusings: a little benchmark of three Python libraries to
compute geodesic
distances <https://github.com/cayetanobv/GeodeticMusings>`__.

All computations are performed with WGS84 ellipsoid and the CRS
(Coordinate Reference System) of GIS file outputs are EPSG:4326.

In the examples section you can see the problem of calculating lines
crossing antimeridian is solved.

Geodesic lines examples
-----------------------

Below are shown different geodesic lines computed with this library on
several map projections. Also you can see the relation with rhumb lines
(loxodromic) and straight lines between the same points:

https://github.com/GeographicaGS/GeodesicLinesToGIS


Requirements
------------

-  Pyproj, https://github.com/jswhit/pyproj
-  Fiona, https://github.com/Toblerity/Fiona
-  Shapely, https://github.com/Toblerity/Shapely

Usage
-----

Usage is very simple. There are two modes: 
- Single input (one
start/end). 
- Multiple input (more than one start/end).

Single input
~~~~~~~~~~~~

Single input usage.

.. code:: python

    from geodesiclinestogis import GeodesicLine2Gisfile

lons\_lats: input coordinates. (start longitude, start latitude, end
longitude, end latitude)

.. code:: python

    lons_lats = (-3.6,40.5,-118.4,33.9)

Folder path to store output file and filename:

.. code:: python

    folderpath = '/tmp'

    layername = "geodesicline"

Create object. You can pass two parameters: - antimeridian: [True \|
False] to solve antimeridian problem (default is True). - prints: [True
\| False] print output messages (default is True).

.. code:: python

    gtg = GeodesicLine2Gisfile()

Launch computations. You can pass two parameter: - lons\_lats: input
coords returned by gcComp. - km\_pts: compute one point each n km
(default is 20 km)

.. code:: python

    cd = gtg.gdlComp(lons_lats, km_pts=30)

Dump geodetic line coords to Linestring Feature and store in a GIS file.

Output formats: "ESRI Shapefile" (default), "GeoJSON"

.. code:: python

    # shapefile output
    gtg.gdlToGisFile(cd, folderpath, layername)

    # geojson output
    gtg.gdlToGisFile(cd, folderpath, layername, fmt="GeoJSON")

Multiple input
~~~~~~~~~~~~~~

Multiple input usage.

.. code:: python

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

About author
------------

Developed by Cayetano Benavent. GIS Analyst at Geographica.

http://www.geographica.gs

License
-------

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

Third-Party licenses
--------------------

You can read Pyproj, Fiona and Shapely licenses in the next links:
https://raw.githubusercontent.com/jswhit/pyproj/master/LICENSE
https://raw.githubusercontent.com/Toblerity/Shapely/master/LICENSE.txt
https://raw.githubusercontent.com/Toblerity/Fiona/master/LICENSE.txt

.. |Mercator1| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_merc.png
.. |Gnomonic| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_gnom.png
.. |Azimuthal Equidistant| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_azim.png
.. |Lambert Azimuthal Equal Area| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/KLAX_LEMD_laea.png
.. |Mercator2| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/Antimeridian.png
.. |Mercator3| image:: https://github.com/GeographicaGS/GeodesicLinesToGIS/blob/master/data/img/Antimeridian_2.png
