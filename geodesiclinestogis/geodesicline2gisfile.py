# -*- coding: utf-8 -*-
#  
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

import os
import math
from pyproj import Geod
from shapely.geometry import LineString, mapping
from fiona import collection
from fiona.transform import transform_geom


class GeodesicLine2Gisfile(object):
    """
    Compute geodesic line from start start lon/lat to
    end lon/lat and dumps to a gis file (Shapefile
    and GeoJSON).
    
    """
    
    
    def __init__(self, antimeridian=True, prints=True):
        """
        antimeridian: solving antimeridian problem [True/False].
        
        prints: print output messages [True/False].
        
        """
        self.__antimeridian = antimeridian
        self.__prints = prints
        
        
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
            
            if self.__prints:
                print "\nGeodesic line succesfully created!"
                print "Total points = {:,}".format(pts)
                print "{:,.4f} km\n".format(dist / 1000.)
            
            return coords_se
        
        except Exception as e:
            print "Error: {0}".format(e.message)
        
    
    def gdlToGisFile(self, coords, folderpath, layername, fmt="ESRI Shapefile"):
        """
        Dump geodesic line coords to ESRI Shapefile 
        and GeoJSON Linestring Feature
        
        coords: input coords returned by gcComp.
        
        folderpath: folder to store output file.
        
        layername: output filename.
        
        fmt: output format ("ESRI Shapefile" (default), "GeoJSON").
        
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
                    print "Output folder does not exist. Set a valid folder path to store file."
                    return
                
                if fmt == "GeoJSON" and os.path.isfile(filepath):
                    os.remove(filepath)
            
                with collection(filepath, "w", fmt, schema) as output:
                    
                    line = LineString(coords)
                    
                    geom = mapping(line)
                
                    if self.__antimeridian:
                        line_t = self.__antiMeridianCut(geom)
                    else:
                        line_t = geom
                    
                    output.write({
                        'properties': {
                            'prop': ''
                        },
                        'geometry': line_t
                    })
                
                if self.__prints:
                    print "{0} succesfully created!\n".format(fmt)
                
            else:
                print "No format to store output..."
                return
        
        except Exception as e:
            print "Error: {0}".format(e.message)
    
    
    def gdlToGisFileMulti(self, data, folderpath, layername, gjs=True):
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
            
            map(self.__multiGeodesicLineCreation, data, fp_lst, lyrnm_lst, gjs_lst)
        
        except Exception as e:
            print "Error: {0}".format(e.message)
        
        
    def __multiGeodesicLineCreation(self, lons_lats, folderpath, layername, gjs):
        """
        Creating geodesic lines in batch mode
        
        """
        
        cd = self.gdlComp(lons_lats)
        
        self.gdlToGisFile(cd, folderpath, layername)
        
        if gjs:
            self.gdlToGisFile(cd, folderpath, layername, fmt="GeoJSON")
        
    
    def __antiMeridianCut(self, geom):
        """
        Solving antimeridian problem...
        
        """
        
        src_crs = '+proj=longlat +datum=WGS84 +no_defs'
        dst_crs = '+proj=longlat +datum=WGS84 +no_defs'
        
        am_offset = 360.0
        
        line_t = transform_geom(src_crs, dst_crs, geom, 
                                antimeridian_cutting=self.__antimeridian,
                                antimeridian_offset=am_offset, 
                                precision=-1)
        
        return line_t
    
    
