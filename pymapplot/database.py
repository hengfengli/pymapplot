import sqlite3
import sys
from graph import *
from spatial import *

class DB:
    
    @staticmethod
    def load_edges(cur, nodes):
        sys.stdout.write("\nLoading edges... ")
        sys.stdout.flush()
        
        cur.execute("select count(*) from edges")
        
        num_edges = cur.fetchone()[0]
        
        edges = {}
        
        cur.execute("select id, in_node, out_node from edges")
        
        query_result = cur.fetchall()
        
        for id, in_node, out_node in query_result:
            weight = Spatial.dist_nodes(nodes[in_node], nodes[out_node])
            angle = Spatial.calc_angle(nodes[in_node], nodes[out_node])
            edges[id] = Edge(id, nodes[in_node], nodes[out_node], weight, angle)
        
        return edges
    
    @staticmethod
    def load_nodes(cur):
        sys.stdout.write("\nLoading nodes... ")
        sys.stdout.flush()

        cur.execute("select count(*) from nodes")
        
        num_nodes = cur.fetchone()[0]
        
        # initalize the list
        # nodes = [None for i in range(num_nodes)]
        nodes = {}
        
        cur.execute("select id, latitude, longitude from nodes")
        
        query_result = cur.fetchall()
        
        for id, lat, lon in query_result:
            
            nodes[id] = Node(lon, lat, id)
        
        return nodes
    
    @staticmethod
    def load_map(db_filename):
        conn = sqlite3.connect(db_filename)
        
        cur = conn.cursor()
        
        nodes = DB.load_nodes(cur)
        
        edges = DB.load_edges(cur, nodes)
        
        conn.close()
        
        print "\nwe have %d nodes and %d edges in %s." \
                % (len(nodes), len(edges), db_filename)
        
        return Graph(nodes, edges)
    
    @staticmethod
    def output_graph_to_db(nodes, edges, filename):
        
        sys.stdout.write("\nOutputting graph to database... ")
        sys.stdout.flush()
        
        # connect to database
        conn = sqlite3.connect(filename)
        
        cur = conn.cursor()
        
        # one transaction
        cur.execute("DROP TABLE IF EXISTS nodes")
        cur.execute("DROP TABLE IF EXISTS edges")
        cur.execute("CREATE TABLE nodes (id INTEGER, latitude FLOAT, longitude FLOAT)")
        cur.execute("CREATE TABLE edges (id INTEGER, in_node INTEGER, out_node INTEGER)")
        cur.execute("DELETE FROM nodes")
        cur.execute("DELETE FROM edges")
        conn.commit()
        
        LON = 0
        LAT = 1
        for graph_node_id in range(len(nodes)):
            graph_node = nodes[graph_node_id]
            # insert graph node into nodes table
            cur.execute("INSERT INTO nodes VALUES (" + str(graph_node_id) + "," + str(graph_node[LAT]) + "," + str(graph_node[LON]) + ")")
        
        START = 0
        END = 1
        for graph_edge_id in range(len(edges)):
            graph_edge = edges[graph_edge_id]
            # insert edge into edges table
            cur.execute("INSERT INTO edges VALUES (" + str(graph_edge_id) + "," + str(graph_edge[START]) + "," + str(graph_edge[END]) + ")")
        
        # commit inserts
        conn.commit()
        
        # close database connection
        conn.close()
        
        print "write into a db file. done."