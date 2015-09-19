import math
# from graph import *

METERS_PER_DEGREE_LATITUDE = 111070.34306591158
METERS_PER_DEGREE_LONGITUDE = 83044.98918812413
EARTH_RADIUS = 6371000.0 # meters
METERS_PER_DEGREE_LONLAT = 0.000011 # 1 meter

class Spatial:
    @staticmethod
    def dist(p1x, p1y, p2x, p2y):
        return math.sqrt((p1x-p2x)**2 + (p1y-p2y)**2)
    
    @staticmethod
    def dist_nodes(node1, node2):
        return Spatial.dist(node1.lon, node1.lat, node2.lon, node2.lat)
    
    @staticmethod
    def dist_arrays(p1, p2):
        p1x, p1y = p1[:2]
        p2x, p2y = p2[:2]
        return Spatial.dist(p1x, p1y, p2x, p2y)
    
    @staticmethod
    def dist_line(line):
        return Spatial.dist_arrays(*line)
    
    @staticmethod
    def same_coords(p1x, p1y, p2x, p2y):
        return p1x == p2x and p1y == p2y
    
    @staticmethod
    def calc_angle_raw(p1x, p1y, p2x, p2y):
        angle = math.degrees(math.atan2(p2y - p1y, p2x - p1x))
        if angle < 0: angle += 360
        return angle
    
    @staticmethod
    def calc_angle_point(pt1, pt2):
        p1x, p1y = pt1
        p2x, p2y = pt2
        angle = math.degrees(math.atan2(p2y - p1y, p2x - p1x))
        if angle < 0: angle += 360
        return angle
    
    @staticmethod
    def calc_angle(p1, p2):
        angle = math.degrees(math.atan2(p2.lat - p1.lat, p2.lon - p1.lon))
        if angle < 0: angle += 360
        return angle
    
    @staticmethod
    def diff_angle180(a, b):
        c = abs(a - b)
        return min(c, 360 - c)
    
    @staticmethod
    def generatePoint(position, p1, p2, edge_dist):
        """ Generate points along with an edge. 
        Args:
            position: A float, the position from the start node (it should
                      be consistent to edge_dist).
            p1: A Node, the start node of this edge.
            p2: A Node, the end node of this edge.
            edge_dist: A float, the distance between p1 and p2 (it should
                      be consistent to position).
        
        Returns:
            A list, a list of generated nodes.
        """
        ratio = position/edge_dist
        
        p1x, p1y = p1.lon, p1.lat
        p2x, p2y = p2.lon, p2.lat
        
        x = p1x - (p1x - p2x) * ratio;
        y = p1y - (p1y - p2y) * ratio;
        
        return [x, y]
    
    @staticmethod
    def calc_real_dist(A, B):
        EPSILON = 0.000001
        Ax, Ay = A
        Bx, By = B
        theta     = Ax - Bx
        theta_lat = Ay - By
        
        if (Ax == Bx and Ay == By) or \
            (abs(theta) < EPSILON and abs(theta_lat) < EPSILON):
            return 0.0
        
        radians_theta = math.radians(theta)
        radians_lat1  = math.radians(Ay)
        radians_lat2  = math.radians(By)
        
        dist = (math.sin(radians_lat1) * math.sin(radians_lat2))    \
             + (math.cos(radians_lat1) * math.cos(radians_lat2)     \
                * math.cos(radians_theta))
        
        # Throw Error => ValueError: math domain error
        # because 'dist' is a slight bigger than 1.0 or less than -1.0
        dist = round(dist, 12)
        
        dist = math.acos(dist)
        dist = math.degrees(dist)
        dist = dist * 60 * 1.1515
        dist = dist * 1609.344
        return dist
    
    @staticmethod
    def raw_fast_distance(node1_lon, node1_lat, node2_lon, node2_lat):
        # Returns the distance in meters between two points specified in 
        # degrees, using an approximation method.
        if (Spatial.same_coords(node1_lon, node2_lat, node2_lon, node2_lat)):
            return 0.0
        
        y_dist = METERS_PER_DEGREE_LATITUDE * (node1_lat - node2_lat)
        x_dist = METERS_PER_DEGREE_LONGITUDE * (node1_lon - node2_lon)
        
        return math.sqrt((y_dist * y_dist) + (x_dist * x_dist))

    
    @staticmethod
    def fast_distance(node1, node2):
        return Spatial.raw_fast_distance(node1.lon, node1.lat, node2.lon, node2.lat)
    
    @staticmethod
    def calculateBounds(center, zoom_level, width, height):
        zoom_to_scale = {
            10:500000,
            11:250000,
            12:150000,
            13:70000,
            14:35000,
            15:15000,
            16:8000,
            17:4000,
            18:2000,
            19:1000
        }
        scaleDenominator = zoom_to_scale[zoom_level]
        
        print "zoom:",zoom_level, "scale:",scaleDenominator
        
        resolution = 1 / ((1. / scaleDenominator) * 4374754 * 72)
        halfWDeg = (width * resolution) / 2
        halfHDeg = (height * resolution) / 2
        
        return Boundary(
            center.lon - halfWDeg,
            center.lon + halfWDeg,
            center.lat - halfHDeg,
            center.lat + halfHDeg
        )
    
    @staticmethod
    def is_in_line_bounds(C, A, B):
        min_x = min(A[0], B[0])
        min_y = min(A[1], B[1])
        max_x = max(A[0], B[0])
        max_y = max(A[1], B[1])
        
        return min_x <= C[0] <= max_x and min_y <= C[1] <= max_y
    
    @staticmethod
    def is_in_line_bound(pt, A, B):
        pt_x, pt_y = pt
        A_x, A_y = A
        B_x, B_y = B
        min_x = min(A_x, B_x)
        max_x = max(A_x, B_x)
        min_y = min(A_y, B_y)
        max_y = max(A_y, B_y)
        
        return min_x <= pt_x <= max_x and min_y <= pt_y <= max_y
    
    @staticmethod
    def projected_dist_must_inside(C, A, B, dist_func):
        new_point = Spatial.point_projection_on_line(C, A, B)
        
        if not Spatial.is_in_line_bound(C, A, B):
            # If this projection node is not in the line,
            # then compute the minimum of distances start node 
            # and end node. 
            dist_to_start = dist_func(C, A)
            dist_to_end   = dist_func(C, B)
            
            if dist_to_start < dist_to_end:
                return dist_to_start
            else:
                return dist_to_end
    
    @staticmethod
    def projected_dist(C, A, B, dist_func):
        new_point = Spatial.point_projection_on_line(C, A, B)
        return dist_func(C, new_point)
    
    @staticmethod
    def point_projection_on_line(C, A, B):
        Cx, Cy = C[:2]
        Ax, Ay = A[:2]
        Bx, By = B[:2]
        
        L_2 = (Bx-Ax)**2 + (By-Ay)**2
    
        if L_2 == 0:
            return [Ax, Ay]
    
        r = ((Ay-Cy)*(Ay-By) - (Ax-Cx)*(Bx-Ax))/ L_2

        newX = Ax + r*(Bx-Ax)
        newY = Ay + r*(By-Ay)
        newPoint = [newX, newY]
        
        return newPoint