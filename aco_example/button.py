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
