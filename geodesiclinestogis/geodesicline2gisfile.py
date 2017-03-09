# -*- coding: utf-8 -*-
#
#  Compute geodesic line from start point to
#  end point and dumps to a gis file (Shapefile
#  and GeoJSON). This code is builded on top of
#  three libraries: Pyproj, Fiona and Shapely
#
#  Author: Cayetano Benavent, 2015-2017.
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

import os
import math
import logging
from pyproj import Geod
from shapely.geometry import LineString, mapping
from fiona import collection
from fiona.transform import transform_geom
from fiona.crs import from_epsg


class GeodesicLine2Gisfile(object):
    """
    Compute geodesic line from start start lon/lat to
    end lon/lat and dumps to a gis file (Shapefile
    and GeoJSON). The problem of geodesic lines crossing
    antimeridian is solved.

    Author: Cayetano Benavent, 2015.
    https://github.com/GeographicaGS/GeodesicLinesToGIS

    Usage is very simple. There are two modes:
        - Single input (one start/end).
        - Multiple input (more than one start/end).

    Single input example:
        >>> from geodesiclinestogis import GeodesicLine2Gisfile
        >>> lons_lats = (-3.6,40.5,-118.4,33.9)
        >>> folderpath = '/tmp'
        >>> layername = "geodesicline"
        >>> gtg = GeodesicLine2Gisfile()
        >>> cd = gtg.gdlComp(lons_lats, km_pts=30)
        #shapefile output
        >>> gtg.gdlToGisFile(cd, folderpath, layername)
        #geojson output
        >>> gtg.gdlToGisFile(cd, folderpath, layername, fmt="GeoJSON")

    Multiple input example:
        >>> from geodesiclinestogis import GeodesicLine2Gisfile
        >>> data = [
                (-6.,37.,-145.,11.),
                (-150.,37.,140.,11.),
                (-6.,37.,120.,50.),
                (-3.6,40.5,-118.4,33.9),
                (-118.4,33.9,139.8,35.5),
                (-118.4,33.9,104.,1.35),
                (-118.4,33.9,151.,-33.9),
                (-20.4,33.9,178.,-33.9)
            ]
        >>> folderpath = "/tmp/geod_line"
        >>> layername = "geodesicline"
        >>> gtg = GeodesicLine2Gisfile()
        >>> gtg.gdlToGisFileMulti(data, folderpath, layername)

    """


    def __init__(self, antimeridian=True, loglevel="INFO"):
        """
            antimeridian: solving antimeridian problem [True/False].

            prints: print output messages [True/False].

        """
        self.__antimeridian = antimeridian
        self.__logger = self.__loggerInit(loglevel)


    def __loggerInit(self, loglevel):
        """
        Logger init...
        """
        if loglevel=="INFO":
            __log_level=logging.INFO
        elif loglevel=="DEBUG":
            __log_level=logging.DEBUG
        elif loglevel=="ERROR":
            __log_level=logging.ERROR
        else:
            __log_level=logging.NOTSET

        logfmt = "[%(asctime)s - %(levelname)s] - %(message)s"
        dtfmt = "%Y-%m-%d %I:%M:%S"

        logging.basicConfig(level=__log_level, format=logfmt, datefmt=dtfmt)

        return logging.getLogger()


    def gdlComp(self, lons_lats, km_pts=20):
        """
        Compute geodesic line

            lons_lats: input coordinates.
            (start longitude, start latitude, end longitude, end latitude)

            km_pts: compute one point each 20 km (default).

        """

        try:
            lon_1, lat_1, lon_2, lat_2 = lons_lats

            pygd = Geod(ellps='WGS84')

            res = pygd.inv(lon_1, lat_1, lon_2, lat_2)
            dist = res[2]

            pts  = int(math.ceil(dist) / (km_pts * 1000))

            coords = pygd.npts(lon_1, lat_1, lon_2, lat_2, pts)

            coords_se = [(lon_1, lat_1)] + coords
            coords_se.append((lon_2, lat_2))

            self.__logger.info("Geodesic line succesfully created!")
            self.__logger.info("Total points = {:,}".format(pts))
            self.__logger.info("{:,.4f} km".format(dist / 1000.))

            return coords_se

        except Exception as e:
            self.__logger.error("Error: {0}".format(e.message))


    def gdlToGisFile(self, coords, folderpath, layername, fmt="ESRI Shapefile",
                     epsg_cd=4326, prop=None):
        """
        Dump geodesic line coords to ESRI Shapefile
        and GeoJSON Linestring Feature

            coords: input coords returned by gcComp.

            folderpath: folder to store output file.

            layername: output filename.

            fmt: output format ("ESRI Shapefile" (default), "GeoJSON").

            epsg_cd: Coordinate Reference System, EPSG code (default: 4326)

            prop: property

        """

        schema = { 'geometry': 'LineString',
                   'properties': { 'prop': 'str' }
                   }

        try:

            if fmt in ["ESRI Shapefile", "GeoJSON"]:
                ext = ".shp"
                if fmt == "GeoJSON":
                    ext = ".geojson"

                filepath = os.path.join(folderpath, "{0}{1}".format(layername, ext))

                if not os.path.exists(folderpath):
                    self.__logger.error("Output folder does not exist. Set a valid folder path to store file.")
                    return

                if fmt == "GeoJSON" and os.path.isfile(filepath):
                    os.remove(filepath)

                out_crs = from_epsg(epsg_cd)

                with collection(filepath, "w", fmt, schema, crs=out_crs) as output:

                    line = LineString(coords)

                    geom = mapping(line)

                    if self.__antimeridian:
                        line_t = self.__antiMeridianCut(geom)
                    else:
                        line_t = geom

                    output.write({
                        'properties': {
                            'prop': prop
                        },
                        'geometry': line_t
                    })

                self.__logger.info("{0} succesfully created!".format(fmt))

            else:
                self.__logger.error("No format to store output...")
                return

        except Exception as e:
            self.__logger.error("Error: {0}".format(e.message))


    def gdlToGisFileMulti(self, data, folderpath, layername, prop=[], gjs=True):
        """
        Run creation for a multi input: a list of lat/lon.

            data: a list with input coordinates.

            [
              (start longitude, start latitude, end longitude, end latitude),
              (start longitude, start latitude, end longitude, end latitude),
              (start longitude, start latitude, end longitude, end latitude),
              (start longitude, start latitude, end longitude, end latitude),
              ...
            ]

            folderpath: folder to store output files.

            layername: output base filename (an ordinal integer is added at the end).

            gfs: GeoJSON output format [True (default)|False], in addition to Shapefile.

        """

        try:
            lendata = len(data)

            lyrnm_lst = ["{0}{1}".format(layername, i) for i in range(lendata)]

            fp_lst = [folderpath] * lendata

            gjs_lst = [gjs] * lendata

            map(self.__multiGeodesicLineCreation, data, fp_lst, lyrnm_lst, gjs_lst, prop)

        except Exception as e:
            self.__logger.error()


    def __multiGeodesicLineCreation(self, lons_lats, folderpath, layername, gjs, prop):
        """
        Creating geodesic lines in batch mode

        """

        cd = self.gdlComp(lons_lats)

        self.gdlToGisFile(cd, folderpath, layername, prop=prop)

        if gjs:
            self.gdlToGisFile(cd, folderpath, layername, fmt="GeoJSON")


    def __antiMeridianCut(self, geom):
        """
        Solving antimeridian problem.

        """

        src_crs = '+proj=longlat +datum=WGS84 +no_defs'
        dst_crs = '+proj=longlat +datum=WGS84 +no_defs'

        am_offset = 360.0

        line_t = transform_geom(src_crs, dst_crs, geom,
                                antimeridian_cutting=self.__antimeridian,
                                antimeridian_offset=am_offset,
                                precision=-1)

        return line_t
