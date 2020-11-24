import pygame
from colors import *


class Button:
    def __init__(self, screen, message, color, hover_color, position_x, position_y, width, height, action=None):
        # initialize attributes
        self.message = message
        self.screen = screen
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color

        # get mouse position
        mouse = pygame.mouse.get_pos()
        # get click event
        click = pygame.mouse.get_pressed()

        # initialize image property
        self.image = pygame.Surface((width, width), pygame.SRCALPHA)

        # initialize rect property
        self.rect = self.image.get_rect()

        # if mouse hover button
        if position_x + width > mouse[0] > position_x and position_y + height > mouse[1] > position_y:
            # draw rect with hover color
            pygame.draw.rect(screen, hover_color, (position_x, position_y, width, height))
            self.set_up_text(self.message)
            # if clicked do action
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (position_x, position_y, width, height))
            self.set_up_text(self.message)



    # render text sprite
    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    # set new text to button
    def set_up_text(self, message):
        pygame.draw.rect(self.screen, self.color, (self.position_x, self.position_y, self.width, self.height))
        start_button_text = pygame.font.Font('fonts/Montserrat-Regular.ttf', 16)
        button_text_surf, button_text_rect = self.text_objects(message, start_button_text)
        button_text_rect.center = (self.position_x + (self.width / 2), (self.position_y + (self.height / 2)))
        self.screen.blit(button_text_surf, button_text_rect)

