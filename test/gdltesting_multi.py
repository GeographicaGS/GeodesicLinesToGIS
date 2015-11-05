# -*- coding: utf-8 -*-
#
#  TESTING FILE
#  Compute geodesic line from start point to
#  end point and dumps to a gis file (Shapefile
#  and GeoJSON). This code is builded on top of
#  three libraries: Pyproj, Fiona and Shapely
#
#  Author: Cayetano Benavent, 2015.
#  https://github.com/GeographicaGS/GeodesicLinesToGIS
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


from geodesiclinestogis.geodesicline2gisfile import GeodesicLine2Gisfile

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


def main():

    gtg = GeodesicLine2Gisfile()

    gtg.gdlToGisFileMulti(data, folderpath, layername)

if __name__ == '__main__':
    main()
