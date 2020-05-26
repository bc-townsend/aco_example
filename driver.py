import sys
import random as rand
from math import sqrt
import pygame

class Button:
    """Class represents a GUI button and has a pressed down state and a normal state.
    """
    def __init__(self, rect, text, normal_color, pressed_color, size):
        """Initialize method for a Button.

        Args:
            rect: The pygame rectangle that this button should correspond to.
            text: The text that should be present in the button.
            normal_color: The color of the button when it is in it's normal state.
            pressed_color: The color of the button when it is in it's pressed state.
            size: Font size for the text.
        """
        self.rect = rect
        self.text = text

        self.normal_text_color = (255, 255, 255)
        self.pressed_text_color = (0, 0, 0)

        self.font = pygame.font.SysFont('Arial', size)
        self.words = self.font.render(self.text, True, self.normal_text_color)

        self.normal_color = normal_color
        self.pressed_color = pressed_color

        self.is_hovered = False
        self.is_pressed = False
    
    def draw(self, surface):
        """Draws the button to the specified surface in either it's pressed or normal state.

        Args:
            surface: The surface on which we should draw the button.
        """
        if self.is_hovered or self.is_pressed:
            color = self.pressed_color
            self.words = self.font.render(self.text, True, self.pressed_text_color)
        else:
            color = self.normal_color
            self.words = self.font.render(self.text, True, self.normal_text_color)
        pygame.draw.rect(surface, color, self.rect)
        # Make sure to blit the text on AFTER we draw the rectangle.
        surface.blit(self.words, self.rect.topleft)
    
    def hovered(self):
        """Determines whether or not the rectangle for this button is being hovered over currently.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.is_hovered:
                self.is_hovered = True
        else:
            self.is_hovered = False
    
    def pressed(self, evnt):
        """Determines whether or not the button has been pressed.

        Args:
            evnt: The current event being triggered by the user.
        """
        if self.is_hovered:
            if evnt.type == pygame.MOUSEBUTTONDOWN and evnt.button == 1:
                self.is_pressed = not self.is_pressed
    
    def update(self, x, y):
        """Updates the rectangle's x and y coordinates so that it can move if needed.

        Args:
            x: The new x-coordinate location.
            y: The new y-coordinate location.
        """
        self.rect.x = x
        self.rect.y = y

class Node:
    """Represents a nodal object in the game. These are the stop points for the ants (where they will choose which neighboring node to travel to on a path).
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
            self.info_text = ''
        text = self.info_font.render(self.info_text, True, (255, 255, 255))
        loc = (self.rect.centerx - (self.radius / 3), self.rect.centery - (self.radius / 2))
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
        return sqrt(x_diff**2 + y_diff**2) / node_size

    def draw(self, surface):
        """Draws this path on the specified surface.

        Args:
            surface: The pygame surface to draw this path on.
        """
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
        center_point = ((self.end_pos[0] + self.start_pos[0])/2, (self.end_pos[1] + self.start_pos[1])/2)
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

if __name__ == "__main__":
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    EVENT_X = 0
    EVENT_Y = 1

    # Initialize the game.
    pygame.init()
    pygame.display.set_caption('Ant Colony Optimization Example')

    # Setup background screen.
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    SCREEN_COLOR = (60, 60, 60)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(SCREEN_COLOR)
    
    # Setup menu surface.
    MENU_WIDTH = SCREEN_WIDTH // 5
    MENU_HEIGHT = SCREEN_HEIGHT
    MENU_COLOR = (80, 80, 80)
    menu = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu.fill(MENU_COLOR)

    # Setup for node information.
    NODE_LOCATION = 20
    NODE_RADIUS = 40
    NODE_COLOR = (0, 80, 200)
    nodes = []
    ID = 0
    nodes.append(Node(ID, NODE_COLOR, pygame.Rect(NODE_LOCATION, NODE_LOCATION, NODE_RADIUS*2, NODE_RADIUS*2)))
    nodes[0].is_colony = True
    ID += 1

    NODE_SPAWN = pygame.Rect(NODE_LOCATION, NODE_LOCATION, NODE_RADIUS*2, NODE_RADIUS*2)

    # Setup for 'Add Path' button.
    BUTTON_Y = 140
    BUTTON_WIDTH = (SCREEN_WIDTH // 5) - 20
    BUTTON_HEIGHT = 40
    PATH_COLOR = (0, 60, 180)
    add_path_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'ADD PATH', PATH_COLOR, (0, 100, 200), 36)

    # Setup for 'Add Food' button.
    BUTTON_Y += BUTTON_HEIGHT + 140
    add_food_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'ADD FOOD', (0, 80, 0), (0, 160, 0), 34)

    # Setup for 'Run' button.
    BUTTON_Y += BUTTON_HEIGHT + 140
    run_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'RUN', (100, 100, 100), (200, 200, 200), 36)

    # Setup for 'Clear' button.
    BUTTON_Y += BUTTON_HEIGHT + 140
    clear_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'CLEAR', (40, 40, 40), (210, 210, 210), 36)

    # Setup the trash can for items.
    TRASH_WIDTH = (SCREEN_WIDTH // 5) - 20
    TRASH_HEIGHT = 60
    trash = pygame.Rect(10, SCREEN_HEIGHT - TRASH_HEIGHT - 10, TRASH_WIDTH, TRASH_HEIGHT)
    TRASH_COLOR = (40, 40, 40)
    TRASH_FONT = pygame.font.SysFont('Arial', 53)
    TRASH_TEXT = TRASH_FONT.render('TRASH', True, WHITE)

    # Information text.
    INFO_FONT = pygame.font.SysFont('Arial', 16)

    path_text = ['Toggle the \'Add Path\'',
                 'button in order to add',
                 'paths between nodes.',
                 'When toggled on, click the',
                 'two nodes you would like',
                 'to add a path between.']
    path_info = []
    for line in path_text:
        path_info.append(INFO_FONT.render(line, False, WHITE))
    
    food_text = ['Toggle the \'Add Food\'',
                 'button in order to add',
                 'food to nodes. When',
                 'toggled on, click a node',
                 'to add/remove food',
                 'from it.']
    food_info = []
    for line in food_text:
        food_info.append(INFO_FONT.render(line, False, WHITE))
    
    run_text = ['Toggle the \'Run\' button',
                'in order to have the ants',
                'find the shortest path to',
                'the food!']
    run_info = []
    for line in run_text:
        run_info.append(INFO_FONT.render(line, False, WHITE))

    # Start running the game application.
    RUNNING = True

    # Selected game object.
    SELECTED = None
    FROM_NODE = None

    # Paths between nodes.
    paths = []

    # Setup for ant colony.
    colony = []
    NUM_ANTS = 80

    clock = pygame.time.Clock()
    phero_clock = 0
    while RUNNING:
        phero_clock += clock.tick(60)

        # Handling to game events.
        for event in pygame.event.get():
            # Check to see if button is pressed.
            add_path_button.pressed(event)
            add_food_button.pressed(event)
            run_button.pressed(event)
            clear_button.pressed(event)

            # User exiting the game.
            if event.type == pygame.QUIT:
                RUNNING = False
            # User presses a key down.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False

            # User pressing mouse button (1) down.
            if not run_button.is_pressed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if clear_button.is_pressed:
                            nodes.clear()
                            paths.clear()
                            clear_button.is_pressed = False
                        for i, node in enumerate(nodes):
                            dx = node.rect.centerx - event.pos[EVENT_X]
                            dy = node.rect.centery - event.pos[EVENT_Y]
                            dist_sq = dx**2 + dy**2

                            if dist_sq <= NODE_RADIUS**2:
                                # Below is selection for adding paths between nodes.
                                if add_path_button.is_pressed and node.rect.x >= MENU_WIDTH:
                                    if FROM_NODE is None:
                                        FROM_NODE = i
                                    else:
                                        if FROM_NODE != i:
                                            path = Path(PATH_COLOR, nodes[int(FROM_NODE)], nodes[i])
                                            paths.append(path)
                                            nodes[int(FROM_NODE)].add_neighbor(nodes[i], path)
                                            nodes[i].add_neighbor(nodes[int(FROM_NODE)], path)
                                        FROM_NODE = None
                                
                                elif add_food_button.is_pressed and node.rect.x >= MENU_WIDTH:
                                    if not node.is_colony:
                                        node.has_food = not node.has_food

                                # Otherwise, just select it for repositioning.
                                else:
                                    SELECTED = i
                                selected_offset_x = node.rect.x - event.pos[EVENT_X]
                                selected_offset_y = node.rect.y - event.pos[EVENT_Y]

                # User releasing mouse button (1).
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        SELECTED = None
                
                # User moving the mouse on screen.
                elif event.type == pygame.MOUSEMOTION:
                    if SELECTED is not None:
                        selected_node = nodes[int(SELECTED)]
                        new_x = event.pos[EVENT_X] + selected_offset_x
                        new_y = event.pos[EVENT_Y] + selected_offset_y
                        selected_node.update(new_x, new_y)

                        # Updating paths.
                        for path in paths:
                            if path.node1 is selected_node:
                                path.start_pos = selected_node.rect.center
                            if path.node2 is selected_node:
                                path.end_pos = selected_node.rect.center

        # Blitting objects onto surfaces.
        screen.fill(SCREEN_COLOR)
        screen.blit(menu, (0, 0))
        pygame.draw.rect(menu, MENU_COLOR, NODE_SPAWN)

        # Drawing any objects onto the screen. Should draw them from furthest back to closest.
        pygame.draw.rect(menu, TRASH_COLOR, trash)
        menu.blit(TRASH_TEXT, trash.topleft)
        if not run_button.is_pressed:
            add_path_button.hovered()
            add_path_button.draw(menu)
            add_food_button.hovered()
            add_food_button.draw(menu)
            clear_button.hovered()
            clear_button.draw(menu)
        run_button.hovered()
        run_button.draw(menu)

        # Blitting button information text.
        y_pos = add_path_button.rect.bottom + 5
        for i, line in enumerate(path_info):
            menu.blit(line, (add_path_button.rect.left, y_pos + (i*16) + (5*i)))
        
        y_pos = add_food_button.rect.bottom + 5
        for i, line in enumerate(food_info):
            menu.blit(line, (add_food_button.rect.left, y_pos + (i*16) + (5*i)))
        
        y_pos = run_button.rect.bottom + 5
        for i, line in enumerate(run_info):
            menu.blit(line, (run_button.rect.left, y_pos + (i*16) + (5*i)))

        # Remove any nodes that collide with the trash can.
        REMOVE_INDEX = trash.collidelist(nodes)
        if REMOVE_INDEX != -1:
            SELECTED = None
            to_remove = nodes[REMOVE_INDEX]
            nodes.remove(nodes[REMOVE_INDEX])

            if len(nodes) > 0 and to_remove.is_colony:
                nodes[0].is_colony = True

            path_removal = []
            for i, path in enumerate(paths):
                if path.node1 is to_remove:
                    path.node2.remove_neighbor(path.node1)
                    path_removal.append(path)
                
                if path.node2 is to_remove:
                    path.node1.remove_neighbor(path.node2)
                    path_removal.append(path)
            
            for path in path_removal:
                paths.remove(path)

        # Making sure we never run out of nodes.
        if len(nodes) <= 0:
            nodes.append(Node(ID, NODE_COLOR, pygame.Rect(NODE_LOCATION, NODE_LOCATION, NODE_RADIUS*2, NODE_RADIUS*2)))
            nodes[0].is_colony = True
            ID += 1
        
        if NODE_SPAWN.collidelist(nodes) == -1:
            nodes.append(Node(ID, NODE_COLOR, pygame.Rect(NODE_LOCATION, NODE_LOCATION, NODE_RADIUS*2, NODE_RADIUS*2)))
            ID += 1

        # Drawing all paths between the nodes and performing pheromone evaporation.
        should_evap = (phero_clock / 1000) > 1 and run_button.is_pressed
        for path in paths:
            path.draw(screen)
            if should_evap:
                path.phero_evaporation()
            #print(path)
        
        if should_evap:
            should_evap = False
            phero_clock = 0

        # Drawing all of the nodes.
        for node in nodes:
            node.draw(screen)

        # Running the actual ant colony optimization simulation.
        if run_button.is_pressed and len(colony) <= 0:
            COLONY_NODE = nodes[0]
            NUM_ANTS *= len(COLONY_NODE.neighbors)
            ant_size = COLONY_NODE.radius / 2
            left_top = (COLONY_NODE.rect.centerx - ant_size / 2, COLONY_NODE.rect.centery - ant_size /2)
            for i in range(NUM_ANTS):
                colony.append(Ant(pygame.Rect(left_top, (ant_size, ant_size)), COLONY_NODE))
        elif not run_button.is_pressed and len(colony) > 0:
            colony.clear()
            for path in paths:
                path.pheromone = 1
        
        for ant in colony:
            if ant.at_node:
                ant.choose()
            else:
                ant.move()
            ant.draw(screen)

        # Update the display to show all the drawn objects on screen.
        pygame.display.flip()

    # Exiting the application.
    pygame.quit()
    sys.exit()
