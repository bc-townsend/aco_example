import pygame
from math import sqrt


class Path:
    """Represents a path object. These are connections between nodes.
    """

    def __init__(self, color, node1, node2):
        """Initialization method for a path object.

        Args:
            color: The color of this path.
            node1: One of the nodes to be connected as neighbors.
            node2: The other node to be connected as neighbors.
        """
        self.color = color
        self.node1 = node1
        self.node2 = node2
        self.start_pos = node1.rect.center
        self.end_pos = node2.rect.center
        self.width = 30

        # Pheromone value determines how likely an ant is to travel along this path.
        self.pheromone = 1
        self.phero_evap = 0.1
        self.font = pygame.font.SysFont('Arial', 28)

    def get_dist(self, node_size):
        """Returns the length/distance of this path.

        Args:
            node_size: Used to calculate the distance so that the numbers are not incredibly large due to pixel measurements.
        """
        x_diff = self.node2.rect.centerx - self.node1.rect.centerx
        y_diff = self.node2.rect.centery - self.node1.rect.centery
        return sqrt(x_diff ** 2 + y_diff ** 2) / node_size

    def draw(self, surface):
        """Draws this path on the specified surface.

        Args:
            surface: The pygame surface to draw this path on.
        """
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
        center_point = ((self.end_pos[0] + self.start_pos[0]) / 2, (self.end_pos[1] + self.start_pos[1]) / 2)
        text = self.font.render(f'{round(self.get_dist(80), 1)}', True, (255, 255, 255))
        surface.blit(text, center_point)

    def phero_evaporation(self):
        """Controls how much pheromone this path loses.
        """
        self.pheromone -= (self.pheromone * self.phero_evap)

    def __eq__(self, obj):
        return isinstance(obj, Path) and self.node1 is obj.node1 and self.node2 is obj.node2

    def __str__(self):
        return f'Path {self.node1.node_id}->{self.node2.node_id}. Phero: {self.pheromone}'
