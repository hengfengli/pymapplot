#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import glob

class StaticMap:
    
    @staticmethod
    def download(filename, boundary, zoom=15):
        
        width = glob.PIC_WIDTH
        height = glob.PIC_WIDTH/boundary.ratio
        
        # url += "%s/%.6f,%.6f,%d/%dx%d.%s?access_token=%s" \
        #     % (mapid, boundary.center_x, boundary.center_y, zoom, width, height, \
        #     img_format, access_token)
        
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
    def get_map(destfile,                       \
            center={'lat':42,'lon':-76},        \
            size={'width':640,'height':640},    \
            zoom=12,                            \
            sensor=True,                      \
            maptype="roadmap",                  \
            fmt="png32",                     \
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
        
        # make the request
        r = requests.get(url)
        with open(destfile, 'wb') as open_file:
            open_file.write(r.content)
