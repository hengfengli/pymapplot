from collections import deque, defaultdict
from spatial import Spatial, METERS_PER_DEGREE_LONLAT

class Boundary:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        
        self.center_x = (min_x+max_x)/2.
        self.center_y = (min_y+max_y)/2.
        
        self.width  = max_x-min_x
        self.height = max_y-min_y
        self.ratio = self.width/self.height
        
    def __str__(self):
        return "%.7f,%.7f,%.7f,%.7f - %.7f" \
            % (self.min_x, self.max_x, self.min_y, self.max_y, self.ratio)

    def __repr__(self):
        return self.__str__()
        
    def gen_axes(self):
        p1 = [self.min_x, self.min_y]
        p2 = [self.max_x, self.min_y]
        p3 = [self.max_x, self.max_y]
        p4 = [self.min_x, self.max_y]
        
        return [[p1,p2], [p3,p4]], [[p2,p3],[p4,p1]]
    
    def split(self, line, axis):
        start = line[0]
        end = line[1]
        
        p1 = [self.min_x, self.min_y]
        p2 = [self.max_x, self.min_y]
        p3 = [self.max_x, self.max_y]
        p4 = [self.min_x, self.max_y]
        
        if axis == 0:
            # split in x axis
            low = Boundary(self.min_x, start[axis], self.min_y, self.max_y)
            high = Boundary(start[axis], self.max_x, self.min_y, self.max_y)
        else:
            low = Boundary(self.min_x, self.max_x, self.min_y, start[axis])
            high = Boundary(self.min_x, self.max_x, start[axis], self.max_y)
        
        return low, high

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        
        # create adjacent list
        # node1 -> edge1, edge2, edge3, ...
        # node2 -> edge4, edge5, edge6, ...
        self.adj_list = defaultdict(set)
        
        for edge in edges.values():
            self.adj_list[edge.in_node.id].add(edge.id)
    
    def adj(self, v):
        return self.adj_list[v]
    
    def gen_sub_graph(self, node_id, great_circle_dist):
        
        subgraph = GenSubGraph(self, node_id, great_circle_dist)
        
        return subgraph.gen()
    
    def add_graph(self, graph):        
        for edge_id, edge in graph.edges.items():
            self.add_edge(edge)
    
    def add_edge(self, edge):
        if edge.in_node.id not in self.nodes:
            self.nodes[edge.in_node.id] = edge.in_node
        if edge.out_node.id not in self.nodes:
            self.nodes[edge.out_node.id] = edge.out_node
        if edge.id not in self.edges:
            self.edges[edge.id] = edge

class Edge:
    def __init__(self, id, in_node, out_node, weight, angle=0):
        self.id = id
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.angle = angle
    
    def __str__(self):
        return "%s %s %f" % (self.in_node, self.out_node, self.weight)
    
    def __repr__(self):
        return self.__str__()

class Node:
    def __init__(self, lon, lat, id=-1):
        self.id = id
        self.lat = lat
        self.lon = lon
    
    def __str__(self):
       return "%d %.7f %.7f" % (self.id, self.lon, self.lat)
    
    def __repr__(self):
       return self.__str__()


class GenSubGraph:
    def __init__(self, G, s, max_dist):
        
        self.marked = defaultdict(bool)
        for node in G.nodes.values():
            self.marked[node.id] = False
        
        self.s = s
        self.G = G
        self.max_dist = max_dist
        self.edge_set = self.bfs(G, s)
    
    def gen(self):
        
        sub_edges = {}
        sub_nodes = {}
        
        for e_id in self.edge_set:
            e = self.G.edges[e_id]
            sub_edges[e_id] = e
            sub_nodes[e.in_node.id] = e.in_node
            sub_nodes[e.out_node.id] = e.out_node
        
        return Graph(sub_nodes, sub_edges)
    
    def bfs(self, G, s):
        
        edge_set = set()
        
        queue = deque()
        self.marked[s] = True
        queue.append(s)
        
        while len(queue) != 0:
            v = queue.popleft()
            for e_id in G.adj(v):
                e = G.edges[e_id]
                w = e.out_node.id
                if not self.marked[w] and Spatial.dist_nodes(G.nodes[s], \
                                                        G.nodes[w]) < self.max_dist:
                    self.marked[w] = True
                    edge_set.add(e_id)
                    queue.append(w)
        
        return edge_set

