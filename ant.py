import pygame
import random as rand

class Ant:
    """Represents an ant that will move along the nodal pathways.
    """
    def __init__(self, rect, colony_node):
        """Initialization method for an ant object.

        Args:
            colony_node: The node from which all ants start at and will return to.
        """
        self.rect = rect
        self.radius = self.rect.width // 2
        self.colony_node = colony_node
        self.path = []
        self.path.append(self.colony_node)
        self.path_length = 0
        self.curr_node = self.colony_node
        self.prev_node = None
        self.color = (0, 0, 0)
        self.at_node = True
        self.found_food = False
        self.px_amount = 5
        self.initial_exploration = True
    
    def draw(self, surface):
        """Draws this ant on the specified surface.

        Args:
            surface: The pygame surface to draw this ant on.
        """
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
        if self.found_food:
            pygame.draw.circle(surface, (0, 255, 0), self.rect.center, self.radius // 2)
    
    def clear_path(self):
        """Removes all nodes along this ant's path.
        """
        self.path_length = 0
        self.path.clear()
        self.prev_node = None
        self.path.append(self.colony_node)
        self.initial_exploration = False
    
    def choose(self):
        """The ants will make a choice as to which node they will attempt to travel to.
        """
        if self.curr_node is self.colony_node and self.found_food:
            self.found_food = False
            self.clear_path()
        elif self.found_food:
            self.prev_node = self.curr_node
            self.curr_node = self.path.pop()
            self.update_pheromone(self.prev_node, self.curr_node)
            self.at_node = False
        else:
            if self.curr_node.has_food:
                self.found_food = True
                return
            alpha = 1
            # beta = 2
            # Calculating sum of all possible neighboring path pheromone levels and distances.
            total = 0.0
            neighbors = self.curr_node.neighbors
            pathways = self.curr_node.path_to_neighbor
            for i, neighbor in enumerate(neighbors):
                if neighbor is not self.prev_node or len(neighbors) == 1:
                    if not self.initial_exploration:
                        total += pathways[i].pheromone**alpha #* (1 / pathways[i].get_dist(80))**beta
                    else:
                        total += 1
            
            # Above seems to be working fine.
            if total != 0:
                prob = 0.0
                choice = rand.random()
                for i, neighbor in enumerate(neighbors):
                    if neighbor is not self.prev_node or len(neighbors) == 1:
                        if not self.initial_exploration:
                            prob += (pathways[i].pheromone**alpha) / total #* (1/pathways[i].get_dist(80))**beta) / total
                        else:
                            prob += 1 / total
                        
                        if choice <= prob:
                            self.prev_node = self.curr_node
                            self.curr_node = neighbor
                            self.path.append(self.curr_node)
                            self.path_length += pathways[i].get_dist(80)
                            self.at_node = False
                            break

    def move(self):
        """Ants move from their previous node to the node they have selected (self.curr_node).
        """
        ant = pygame.math.Vector2(self.rect.center)
        node = pygame.math.Vector2(self.curr_node.rect.center)
        dist = ant.distance_to(node)

        if dist <= 5:
            self.at_node = True
        else:
            pathing = node - ant
            pathing /= dist
            pathing *= self.px_amount
            self.rect.center += pathing

    def update_pheromone(self, from_node, to_node):
        """Updates the pheromone trail on the path from one node to another.

        Args:
            from_node: The node we are traveling from.
            to_node: The node we are traveling to.
        """
        q = 1
        path = None
        for i, node in enumerate(from_node.neighbors):
            if node is to_node:
                path = from_node.path_to_neighbor[i]
                break
        
        if path is not None:
            path.pheromone += (q / self.path_length)