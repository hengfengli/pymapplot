from spatial import *
from graph import *
import sys


NODE_ID = 0
NODE_LON = 2
NODE_LAT = 3
EDGE_ID = 0
EDGE_IN_NODE = 1
EDGE_OUT_NODE = 2

class Fileio:
    @staticmethod
    def readConfig(filename):
        import yaml
        # from pprint import pprint

        with open(filename) as dataFile:
            data = yaml.load(dataFile)
        
        # pprint(data)
        return data
    
    @staticmethod
    def load_map(dir):
        
        sys.stdout.write("\nLoading nodes... ")
        sys.stdout.flush()
        nodes = {}
        with open(dir + "vertex.txt") as reader:
            num_nodes = int(reader.readline())
            
            for line in reader.readlines():
                cols = line.strip().split(' ')
                
                id = int(cols[NODE_ID])
                lon = float(cols[NODE_LON])
                lat = float(cols[NODE_LAT])
                
                nodes[id] = Node(lon, lat, id)
        
        sys.stdout.write("\nLoading edges... ")
        sys.stdout.flush()
        edges = {}
        with open(dir + "edges.txt") as reader:
            num_nodes = int(reader.readline())
            num_edges = int(reader.readline())
            
            for line in reader.readlines():
                cols = line.strip().split(' ')
                
                id = int(cols[EDGE_ID])
                in_node = nodes[int(cols[EDGE_IN_NODE])]
                out_node = nodes[int(cols[EDGE_OUT_NODE])]
                weight = Spatial.dist_nodes(in_node, out_node)
                angle = Spatial.calc_angle(in_node, out_node)
                edges[id] = Edge(id, in_node, out_node, weight, angle)
        
        print "\nwe have %d nodes and %d edges in %s." \
                % (len(nodes), len(edges), dir)
        
        return Graph(nodes, edges)