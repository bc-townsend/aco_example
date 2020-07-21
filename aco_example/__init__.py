import sys
import pygame

from .ant import Ant
from .button import Button
from .node import Node
from .path import Path

def run():
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
    NUM_ANTS = 50

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
