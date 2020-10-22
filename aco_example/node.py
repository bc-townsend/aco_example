import pygame


class Node:
    """Represents a nodal object in the game. These are the stop points for the ants (where they will choose which
    neighboring node to travel to on a path).
    """

    def __init__(self, node_id, color, rect):
        """Initialization method for a Node.

        Args:
            node_id: The identification number we assign to this node.
            color: The color of this node.
            rect: The pygame rectangle object that this node should correspond to.
        """
        self.node_id = node_id
        self.color = color
        self.rect = rect
        self.radius = self.rect.width // 2
        self.font = pygame.font.SysFont('Arial', 20)
        self.info_font = pygame.font.SysFont('Arial', 38)
        self.info_text = ''

        # Determines whether or not this node is a colony or food-bearing node.
        self.is_colony = False
        self.has_food = False

        self.neighbors = []
        self.path_to_neighbor = []

    def add_neighbor(self, neighbor, connection):
        """Adds a neighbor to this node's list of neighbors.

        Args:
            neighbor: The neighboring node.
            connection: The path from this node to its neighbor.
        """
        self.neighbors.append(neighbor)
        self.path_to_neighbor.append(connection)

    def remove_neighbor(self, neighbor):
        """Removes a neighbor from this node's list of neighbors.

        Args:
            neighbor: The node to remove from the list of neighbors.
        """
        if neighbor in self.neighbors:
            index = self.neighbors.index(neighbor)
            self.neighbors.remove(neighbor)
            self.path_to_neighbor.pop(index)

    def draw(self, surface):
        """Draws this node on the specified surface.

        Args:
            surface: The pygame surface to draw this node on.
        """
        # Nodes are in the shape of circles.
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
        text = self.font.render(f'{self.node_id}', True, (255, 255, 255))
        surface.blit(text, self.rect.topleft)

        # Determine the text to be displayed on the node.
        if self.has_food:
            self.info_text = 'F'
        elif self.is_colony:
            self.info_text = 'C'
        else:
            self.info_text = None

        text = self.info_font.render(self.info_text, True, (255, 255, 255))
        loc = (self.rect.centerx - (self.radius / 3), self.rect.centery - (self.radius / 2))
        if self.info_text is not None:
            surface.blit(text, loc)

    def update(self, x, y):
        """Updates the node's location if it is moved.

        Args:
            x: The new x-coordinate location of this node.
            y: The new y-coordinate location of this node.
        """
        self.rect.x = x
        self.rect.y = y

    def __eq__(self, obj):
        return isinstance(obj, Node) and obj.node_id == self.node_id

    def __str__(self):
        return f'Node({self.node_id})'
