"""
    Ant Colony Optimization path finding algorithm visualization.
    Author: Brandon Townsend
    Date: 4 April 2020
"""

class Ant:
    def __init__(self, colony_node):
        self.path = []
        self.curr_node = colony_node
        self.prev_node = None
    
    def clear_path(self):
        self.path.clear()
    
    def move(self):
        return self.curr_node