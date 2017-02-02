from plot import Plot
from staticmap import StaticMap
from boundary import Boundary, Range, LatLon
from traj import Trajectory
import pickle
import pprint
import glob
from database import DB

from fileio import Fileio

import cv2


def read_clustered_gps_points():
    gps_points, labels = [], []
    with open(glob.CLUSTERED_POINTS_FILE) as reader:
        for line in reader.readlines():
            line = line.strip()
            if line != "":
                lon, lat, label = line.split()
                gps_points.append([float(lon), float(lat)])
                labels.append(int(label))
    return gps_points, labels


def convert_trips_to_lines(trips):
    trip_segs = []

    for trip_id, trip in enumerate(trips):
        n = len(trip.nodes)
        for in_node, out_node in zip(trip.nodes[:-1], trip.nodes[1:]):
            p1 = [in_node.lon, in_node.lat]
            p2 = [out_node.lon, out_node.lat]
            trip_segs.append([p1, p2])

    return trip_segs


def plot_maps(methods=[]):

    # ================ download the map ==================
    x_range = Range(*glob.X_RANGE)
    y_range = Range(*glob.Y_RANGE)
    boundary = Boundary(x_range, y_range)

    center = boundary.center()
    center_latlon = LatLon(lon=center[0], lat=center[1])

    print StaticMap.latlon2xy_tile(center_latlon.lat, center_latlon.lon, 12)

    print center_latlon
    #"roadmap","mobile","satellite","terrain","hybrid","mapmaker-roadmap","mapmaker-hybrid"
    metainfo = StaticMap.get_map("chicago.png", \
        center={'lat':center_latlon.lat, 'lon':center_latlon.lon}, \
        zoom=17, scale=1, maptype="mobile")

    pprint.pprint(metainfo)

    print StaticMap.xy2latlon(metainfo, 0, 0)
    print StaticMap.latlon2xy_centered(metainfo, center_latlon.lat,
                                       center_latlon.lon)

    ll = metainfo['bbox']['low_left']
    ur = metainfo['bbox']['upper_right']
    x_range = Range(ll['lon'], ur['lon'])
    y_range = Range(ll['lat'], ur['lat'])
    boundary = Boundary(x_range, y_range)

    print "Boundary:", boundary

    # ================ download the map ==================

    # x_range = Range(*glob.X_RANGE)
    # y_range = Range(*glob.Y_RANGE)
    # boundary = Boundary(x_range, y_range)

    # ================ load the gpspoints ==================
    gps_points, labels = read_clustered_gps_points()
    print "gps_points:", len(gps_points), "labels:", len(labels)

    Plot.plot_graph(
        [],
        boundary,
        "points_plot_map.png",
        points=gps_points,
        labels=labels,
        pt_size=10,
        bg_filename="chicago.png")

    # =============== underlying road network ==============
    map_g = Fileio.load_map(glob.MAP_DIR)

    print len(map_g.edges)

    # plot the ground truth
    ground_truth_lines = []
    for edge in map_g.edges.values():

        in_node = [edge.in_node.lon, edge.in_node.lat]
        out_node = [edge.out_node.lon, edge.out_node.lat]

        ground_truth_lines.append([in_node, out_node])
    # =============== underlying road network ==============

    start_index, end_index = glob.TRAJ_FILE_RANGE
    gps_trips = Trajectory.load_all_trips(glob.TRAJ_PATH, \
        start_index=start_index, end_index=end_index)
    print "load %d trips" % len(gps_trips)

    trip_points = [[node.lon, node.lat] for node in gps_trips[0].nodes]

    trip_segs = convert_trips_to_lines(gps_trips)
    print "load %d trip segments" % len(trip_segs)

    Plot.plot_graph(
        trip_segs,
        boundary,
        "trips_plot_map.png",
        line_color='black',
        # bg_lines=trip_segs,
        # bg_line_color="black",
        points=trip_points,
        pt_color="red",
        bg_filename="chicago.png")

    # ================ load trips =================

    Plot.plot_graph(
        ground_truth_lines,
        boundary,
        "truth_plot_map.png",
        line_color='red',
        linewidth=glob.LINEWIDTH,
        bg_filename="chicago.png")

    # plot for each method

    methods_graphs = []
    for method in methods:
        use_db_file = glob.DATA_DIR + "%s_graph.db" % method
        g = DB.load_map(use_db_file)
        print "method:", method
        methods_graphs.append(g)

        lines = []
        for edge in g.edges.values():
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

        Plot.plot_graph(
            lines,
            boundary,
            "%s_plot_map.png" % method,
            line_color='red',
            # bg_lines=lines, bg_line_color="red",
            # bg_lines=ground_truth_lines, bg_line_color="#C8C8C8",
            linewidth=glob.LINEWIDTH,
            bg_filename="chicago.png")

        # Plot.plot_graph(lines, boundary, "points_plot_map.png",
        #     line_color='red', linewidth=glob.LINEWIDTH,
        #     points=gps_points, labels=labels, pt_size=10,
        #     bg_filename="chicago.png")

    # metainfo = pickle.load(open("chicago.png.pkl", "rb"))
    # pprint.pprint(metainfo)


def crop_maps(methods):
    for method in methods + ["trips", "truth"]:
        img = cv2.imread("%s_plot_map.png" % method)

        # 850, 509
        pos_x = glob.POS_X
        pos_y = glob.POS_Y
        x_span = glob.X_SPAN
        y_span = glob.Y_SPAN

        crop_img = img[pos_y:pos_y + y_span, pos_x:pos_x + x_span]
        # crop_img = img[:, :]
        # cv2.imshow("cropped", crop_img)
        # cv2.waitKey(0)
        cv2.imwrite('%s_crop_map.png' % method, crop_img)


# def main():
#     # methods = ['cao', 'davies', 'edelkamp', 'biagioni', 'li']
#     # methods = ['li', 'davies', 'biagioni']
#     methods = ['li']
#     plot_maps(methods)
#     # crop_maps(methods)
#     # crop_maps(['truth'])
# 
# if __name__ == '__main__':
#     main()
