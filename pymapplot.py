from plot import Plot
from staticmap import StaticMap
from boundary import Boundary, Range, LatLon
import pickle
import pprint
import glob

from fileio import Fileio

x_range = Range(-87.69215,-87.634896)
y_range = Range(41.858952,41.886565)
boundary = Boundary(x_range, y_range)

center = boundary.center()
center_latlon = LatLon(lon=center[0], lat=center[1])

print StaticMap.latlon2xy_tile(center_latlon.lat, center_latlon.lon, 12)


print center_latlon
metainfo = StaticMap.get_map("chicago.png", \
    center={'lat':center_latlon.lat, 'lon':center_latlon.lon}, \
    zoom=14, scale=2, maptype="roadmap")

pprint.pprint(metainfo)

print StaticMap.xy2latlon(metainfo, 0, 0)
print StaticMap.latlon2xy_centered(metainfo, center_latlon.lat, center_latlon.lon)


ll = metainfo['bbox']['low_left']
ur = metainfo['bbox']['upper_right']
x_range = Range(ll['lon'], ur['lon'])
y_range = Range(ll['lat'], ur['lat'])
boundary = Boundary(x_range, y_range)

map_dir = "test_data/shrink-road-maps/"
map_g = Fileio.load_map(map_dir)

print len(map_g.edges)

lines = []
for edge in map_g.edges.values():
    # in_node  = StaticMap.latlon2xy_centered(metainfo, edge.in_node.lat, edge.in_node.lon)
    # out_node = StaticMap.latlon2xy_centered(metainfo, edge.out_node.lat, edge.out_node.lon)
    #
    # offset = glob.PIC_WIDTH / 2.0
    #
    # in_node  = [in_node['X'] + offset, in_node['Y']+offset]
    # out_node = [out_node['X'] + offset, out_node['Y']+offset]
    
    in_node = [edge.in_node.lon, edge.in_node.lat]
    out_node = [edge.out_node.lon, edge.out_node.lat]
    
    lines.append([in_node, out_node])
    
print lines[0]

Plot.plot_graph_with_bgmap(lines, "chicago.png", boundary, "pymapplot.png")

# metainfo = pickle.load(open("chicago.png.pkl", "rb"))
# pprint.pprint(metainfo)