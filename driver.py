import sys
from math import sqrt
import pygame

class Button:
    def __init__(self, rect, text, normal_color, pressed_color, size):
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
        if self.is_hovered or self.is_pressed:
            color = self.pressed_color
            self.words = self.font.render(self.text, True, self.pressed_text_color)
        else:
            color = self.normal_color
            self.words = self.font.render(self.text, True, self.normal_text_color)
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(self.words, self.rect.topleft)
    
    def hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.is_hovered:
                self.is_hovered = True
        else:
            self.is_hovered = False
    
    def pressed(self, evnt):
        if self.is_hovered:
            if evnt.type == pygame.MOUSEBUTTONDOWN and evnt.button == 1:
                self.is_pressed = not self.is_pressed
    
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Node:
    def __init__(self, node_id, color, rect):
        self.node_id = node_id
        self.color = color
        self.rect = rect
        self.radius = self.rect.width // 2
        self.font = pygame.font.SysFont('Arial', 20)
        self.info_font = pygame.font.SysFont('Arial', 38)
        self.info_text = ''

        self.is_colony = False
        self.has_food = False

        self.neighbors = {}
    
    def add_neighbor(self, neighbor, connection):
        self.neighbors[neighbor] = connection
    
    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
        text = self.font.render(f'{self.node_id}', True, (255, 255, 255))
        surface.blit(text, self.rect.topleft)

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
        self.rect.x = x
        self.rect.y = y

class Path:
    def __init__(self, color, node1, node2):
        self.color = color
        self.node1 = node1
        self.node2 = node2
        self.start_pos = node1.rect.center
        self.end_pos = node2.rect.center
        self.width = 20

        self.pheromone = 1

        self.font = pygame.font.SysFont('Arial', 28)
    
    def get_dist(self, node_size):
        x_diff = self.node2.rect.centerx - self.node1.rect.centerx
        y_diff = self.node2.rect.centery - self.node1.rect.centery
        return int(sqrt(x_diff**2 + y_diff**2) // node_size)

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
        center_point = ((self.end_pos[0] + self.start_pos[0])/2, (self.end_pos[1] + self.start_pos[1])/2)
        text = self.font.render(f'{self.get_dist(80)}', True, (255, 255, 255))
        surface.blit(text, center_point)

class Ant:
    def __init__(self, colony_node):
        self.colony_node = colony_node
        self.path = []
        self.curr_node = self.colony_node
        self.prev_node = None
        self.speed = 5
    
    def clear_path(self):
        self.path.clear()
    
    def move(self):
        print('moving')

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
    SCREEN_HEIGHT = 600
    SCREEN_COLOR = (30, 30, 30)
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
    BUTTON_Y = 200
    BUTTON_WIDTH = (SCREEN_WIDTH // 5) - 20
    BUTTON_HEIGHT = 40
    PATH_COLOR = (0, 60, 180)
    add_path_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'ADD PATH', PATH_COLOR, (0, 100, 200), 36)

    # Setup for 'Add Food' button.
    BUTTON_Y += BUTTON_HEIGHT + 20
    BUTTON_WIDTH = (SCREEN_WIDTH // 5) - 20
    BUTTON_HEIGHT = 40
    add_food_button = Button(pygame.Rect(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 'ADD FOOD', (0, 80, 0), (0, 160, 0), 34)

    # Setup the trash can for items.
    TRASH_WIDTH = (SCREEN_WIDTH // 5) - 20
    TRASH_HEIGHT = 60
    trash = pygame.Rect(10, SCREEN_HEIGHT - TRASH_HEIGHT - 10, TRASH_WIDTH, TRASH_HEIGHT)
    TRASH_COLOR = (40, 40, 40)
    TRASH_FONT = pygame.font.SysFont('Arial', 53)
    TRASH_TEXT = TRASH_FONT.render('TRASH', True, WHITE)

    # Start running the game application.
    RUNNING = True

    # Selected game object.
    SELECTED = None
    FROM_NODE = None

    # Paths between nodes.
    paths = []

    while RUNNING:
        # Handling to game events.
        for event in pygame.event.get():
            # Check to see if button is pressed.
            if not add_food_button.is_pressed:
                add_path_button.pressed(event)
            if not add_path_button.is_pressed:
                add_food_button.pressed(event)

            # User exiting the game.
            if event.type == pygame.QUIT:
                RUNNING = False
            # User presses a key down.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False

            # User pressing mouse button (1) down.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
        add_path_button.hovered()
        add_path_button.draw(menu)
        add_food_button.hovered()
        add_food_button.draw(menu)

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

        # Drawing all paths between the nodes.
        for path in paths:
            path.draw(screen)

        # Drawing all of the nodes.
        for node in nodes:
            node.draw(screen)

        # Update the display to show all the drawn objects on screen.
        pygame.display.flip()

    # Exiting the application.
    pygame.quit()
    sys.exit()
