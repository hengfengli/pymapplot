#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import glob
import pickle
import math

class StaticMap:
    
    @staticmethod
    def download(filename, boundary, zoom=15):
        
        width = glob.PIC_WIDTH
        height = glob.PIC_WIDTH/boundary.ratio
        
        # # resolution 1024x493 = openstreetmap
        # url = "http://staticmap.openstreetmap.de/staticmap.php?"
        # url += "center=%.6f,%.6f&zoom=14&size=%dx%d&maptype=mapnik" \
        #     % (b.center_y, b.center_x, width, height)
        
        scale = 2
        # # resolution 1000 × 986
        print "requested width:%d height:%d" % (width, height)
        # center: lat, lon
        url = "http://maps.googleapis.com/maps/api/staticmap?"
        url += "center=%.6f,%.6f&size=%dx%d&zoom=%d&scale=%d&sensor=false" \
            % (boundary.center_y, boundary.center_x, width, height, zoom, scale)
        
        print url
        
        r = requests.get(url)
        
        with open(filename, 'wb') as test:
            test.write(r.content)
        
        # return Boundary(min_lon,max_lon,min_lat,max_lat)
    
    @staticmethod
    def xy2latlon(my_map, X, Y):
        """
        :type my_map: map info
        :type X: longitude value
        :type Y: latitude value
        :rtype: None
        """
        lat_center = my_map['center']['lat']
        lon_center = my_map['center']['lon']
        zoom = my_map['zoom']
        
        mycenter = StaticMap.latlon2xy_tile(lat_center, lon_center, zoom)
        
        x = mycenter['tile']['X'] + (X + mycenter['coords']['x'])/256
        y = mycenter['tile']['Y'] - (Y - mycenter['coords']['y'])/256
        
        ytilde = 1 - y / 2**(zoom-1)
        yy = (math.exp(2*math.pi*ytilde) - 1) / (math.exp(2*math.pi*ytilde) + 1)
        
        def shift_lat(yy):
            n = [-1,0,1]
            lat = map(lambda x: 2 * math.pi * x + math.asin(yy), n)
            lat = filter(lambda x: x <= math.pi/2 and x > -math.pi/2, lat)[0]
            lat = 180 * lat / math.pi
            return lat
        
        lat = shift_lat(yy)
        lon = 180 * (x/2**(zoom-1) - 1)
        
        return {'lat':lat, 'lon':lon}
    
    @staticmethod
    def tile2coord(point, center):
        X =  256 * (point['tile']['X']-center['tile']['X']) + (point['coords']['x']-center['coords']['x'])
        Y = -256 * (point['tile']['Y']-center['tile']['Y']) - (point['coords']['y']-center['coords']['y'])
        return {'X':X, 'Y':Y}
    
    @staticmethod
    def latlon2xy_centered(my_map, lat, lon):
        
        lat_center = my_map['center']['lat']
        lon_center = my_map['center']['lon']
        zoom = my_map['zoom']
        
        point = StaticMap.latlon2xy_tile(lat, lon, zoom)
        center = StaticMap.latlon2xy_tile(lat_center, lon_center, zoom)
        
        return StaticMap.tile2coord(point, center)
    
    @staticmethod
    def latlon2xy_tile(lat, lon, zoom):
        """
        :type lat: latitude value
        :type lon: longitude value
        :type zoom: zoom level
        :rtype: {'tile': (tile_coords), 'coords': (coords_in_tile)}
        
        'tile' is a coordinate of the tile in the world map. 
        'coords' is a coordinate of a point in that tile. 
        """
        
        sin_phi = math.sin(lat * math.pi / 180)
        normX = lon / 180
        normY = (0.5 * math.log((1+sin_phi) / (1-sin_phi))) / math.pi
        
        Y = (2**zoom) * ((1-normY)/2)
        X = (2**zoom) * ((normX+1)/2)
        
        x = 256 * (X - math.floor(X))
        y = 256 * (Y - math.floor(Y))
        
        return {'tile': {'X':math.floor(X), 'Y':math.floor(Y)}, \
                'coords': {'x':x, 'y':y} }
    
    @staticmethod
    def get_map(destfile,                       \
            center={'lat':42,'lon':-76},        \
            size={'width':640,'height':640},    \
            zoom=12,                            \
            sensor=True,                        \
            maptype="roadmap",                  \
            fmt="png32",                        \
            scale=1                             \
        ):
        """
        maptype:
        "roadmap","mobile","satellite","terrain","hybrid","mapmaker-roadmap","mapmaker-hybrid"

        format:
        "gif","jpg","jpg-baseline","png8","png32"

        """
        
        url = "http://maps.googleapis.com/maps/api/staticmap?"
        url += "center=%.6f,%.6f" % (center['lat'], center['lon'])
        url += "&zoom=%d" % zoom
        url += "&size=%dx%d" % (size['width'], size['height'])
        url += "&maptype=%s" % maptype
        url += "&format=%s" % fmt
        url += "&sensor=%s" % "true" if sensor else "false"
        url += "&scale=%d" % scale
        
        # print out the requested url
        print url
        
        my_map = {'center':center, 'zoom':zoom, 'scale':scale}
        # BBOX <- list(ll = XY2LatLon(MyMap, -size[1]/2 + 0.5, -size[2]/2 - 0.5), ur = XY2LatLon(MyMap, size[1]/2 + 0.5, size[2]/2 - 0.5) );
        
        bbox = {'low_left': StaticMap.xy2latlon(my_map, -size['width']/2.0, \
                                                        -size['height']/2.0), \
                'upper_right': StaticMap.xy2latlon(my_map, size['width']/2.0, \
                                                           size['height']/2.0)}
        
        metainfo = {'center':center, 'zoom':zoom, 'scale':scale, \
                    'url':"google", 'bbox':bbox, 'size':size}
        
        # save(MetaInfo, file = paste(destfile,"rda",sep="."));
        
        # write meta info into a dictionary and 
        # pickle.dump(metainfo, open(destfile+".pkl", "wb"))
        
        # make the request
        r = requests.get(url)
        with open(destfile, 'wb') as open_file:
            open_file.write(r.content)
        
        return metainfo
