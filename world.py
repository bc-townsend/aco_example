"""
    NOTE: the functionality of this class is transitioning to the driver.py for now.
    Ant Colony Optimization path finding algorithm visualization.
    Author: Brandon Townsend
    Date: April 2, 2020
"""
import colony as c

class World:
    def __init__(self):
        self.nodes = {}
    
    def build_from_file(self, nodefile, pathfile):
        with open(nodefile, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                info = line.split()
                self.add_node(int(info[0]), int(info[1]))
        
        with open(pathfile, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                info = line.split()
                self.add_path(int(info[0]), int(info[1]), int(info[2]))
    
    def add_node(self, node_id, food=0):
        self.nodes[node_id] = Node(node_id, food)
    
    def add_path(self, node1_id, node2_id, distance):
        if node1_id in self.nodes and node2_id in self.nodes:
            node1   = self.nodes[node1_id]
            node2   = self.nodes[node2_id]
            path    = Path(distance)
            node1.add_neighbor(node2, path)
            node2.add_neighbor(node1, path)

class Node:
    def __init__(self, node_id, food=0):
        self.node_id = node_id
        self.food = food
        self.neighbors = {}

    def add_food(self, food):
        self.food += food
    
    def remove_food(self, food):
        self.food -= food
    
    def clear_food(self):
        self.food = 0
    
    def add_neighbor(self, neighbor, path):
        if isinstance(neighbor, Node) and isinstance(path, Path):
            self.neighbors[neighbor] = path
        else:
            print('Neighbor is not a Node or path is not a Path.')
    
    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]
    
    def __eq__(self, obj):
        return isinstance(obj, Node) and obj.node_id == self.node_id

class Path:
    def __init__(self, distance):
        self.distance = distance
        self.pheromone = 1
    
    def set_distance(self, distance):
        self.distance = distance

    def set_pheromone(self, pheromone):
        self.pheromone = pheromone