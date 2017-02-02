from spatial import Spatial, METERS_PER_DEGREE_LONLAT

class TrajNode:
    def __init__(self, lon, lat, time, traj_id):
        self.lat = lat
        self.lon = lon
        self.time = time
        self.traj_id = traj_id
        self.angle = None
        
        self.node_id = None
        # self.prev_node_id = None
        # self.next_node_id = None
    
    def __str__(self):
       return "%.7f %.7f %d" % (self.lat, self.lon, int(self.time))
    
    def __repr__(self):
       return self.__str__()
    
    def set_angle(self, angle):
        self.angle = angle

class Trajectory:
    @staticmethod
    def load_all_trips(data_dir, start_index=0, end_index=888):
        num_trips = end_index+1
        
        times = []
        all_time_diff = []
        
        gps_trips = []
        max_speed_record = []
        for trip_no in range(start_index, num_trips):
            trip, time_diff, max_speed = Trajectory.load_trip( "%strip_%d.txt" \
                        % (data_dir, trip_no), trip_no)
            
            max_speed_record.append(max_speed)
            # Time difference should be less than 5 mins, otherwise, split it. 
            split_flags = map(lambda x: x < 300, time_diff)
            flag_indices = [i+1 for i, flag in enumerate(split_flags) if not flag]
            
            # print flag_indices
            
            # print "%d/%d" % (len(trip.nodes), len(time_diff))
            # print "%3d %5f %s" % (trip_no, max_speed, time_diff)
            # skip outlier
            # if max_speed > 30: continue
            
            all_time_diff.extend(time_diff)
            times.append(trip.nodes[-1].time - trip.nodes[0].time)
            
            if len(flag_indices) == 0:
                gps_trips.append(trip)
                continue
            
            # split trips based on indices of flags
            if flag_indices[0] != 0:
                flag_indices = [0] + flag_indices
            if flag_indices[-1] != len(trip.nodes)-1:
                flag_indices = flag_indices + [len(trip.nodes)-1]
            
            # print "len:", len(trip.nodes)
            # print "updated:", flag_indices
            
            for i in range(len(flag_indices)-1):
                # exclude the right side, [i, i+1)
                new_trip = Trajectory(trip.nodes[flag_indices[i]:flag_indices[i+1]])
                
                # less than 3 points, don't add it. 
                if len(new_trip.nodes) <= 3: continue
                gps_trips.append(new_trip)
        
        # calculate the total travel distance
        total_dist = 0.
        for trip in gps_trips:
            for prev, next in zip(trip.nodes[:-1], trip.nodes[1:]):
                total_dist += Spatial.calc_real_dist(
                    [prev.lon, prev.lat], [next.lon, next.lat]
                )
        
        print "*" * 50
        print "Total distance (m):", total_dist
        print "Total hours:", sum(times)/3600
        print "Avg. time interval:", sum(all_time_diff) * 1.0/ len(all_time_diff)
        print "Min time interval:", min(all_time_diff)
        print "Max time interval:", max(all_time_diff)
        print "Number of trips:", num_trips
        print "Number of normal traces:", len(gps_trips)
        print "Max speed:", max(max_speed_record)
        # assert(len(gps_trips) == num_trips)
        print "*" * 50
        
        return gps_trips
    
    @staticmethod
    def load_trip(filename, traj_id, separator=",", ID=0, LAT=1, LON=2, TIME=3):
        with open(filename) as reader:
            
            points = []
            
            for line in reader.readlines():
                cols = line.strip().split(separator)
                
                lat  = float(cols[LAT])
                lon  = float(cols[LON])
                time = float(cols[TIME])
                
                traj_node = TrajNode(lon, lat, time, traj_id)
                
                traj_node.node_id = int(cols[ID])
                # if cols[4] != "None":
                #     traj_node.prev_node_id = int(cols[4])
                # if cols[5] != "None":
                #     traj_node.next_node_id = int(cols[5])
                
                points.append(traj_node)
        
        
        time_diff = []
        max_speed = -1.0
        # add directions at each GPS point
        for i in range(len(points)-1):
            angle = Spatial.calc_angle(points[i], points[i+1])
            points[i].set_angle(angle)
            
            dist = Spatial.dist_nodes(points[i], points[i+1])
            travel_time = points[i+1].time - points[i].time
            
            travel_speed = dist/METERS_PER_DEGREE_LONLAT * 1.0/travel_time
            if travel_speed > max_speed:
                max_speed = travel_speed
            
            time_diff.append(travel_time)
        
        # avg_diff = sum_diff * 1.0/ (len(points)-1)
        # print "traj_id:", traj_id, "avg diff:", avg_diff
        
        return Trajectory(points), time_diff, max_speed
    
    def __init__(self, nodes):
        self.nodes = nodes
    
    @property
    def size(self):
        return len(self.nodes)
    
    def __str__(self):
       return "%s" % (self.nodes)
    
    def __repr__(self):
       return self.__str__()