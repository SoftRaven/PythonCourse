import pygame
from colors import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, i, j, color, size):
        pygame.sprite.Sprite.__init__(self)

        # attributes
        self.x = x
        self.y = y
        self.j = j
        self.i = i
        self.size = size
        self.filled = False
        self.color = color

        # initialize image property
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)

        # initialize rect property and sprite position
        self.rect = self.image.get_rect()
        self.rect.top = x
        self.rect.left = y

    def set_filled(self):
        self.filled = True

    def set_unfilled(self):
        self.filled = False

    # if queen placed incorrectly
    def set_red(self):
        self.image.fill(RED)

    # if queen placed correctly
    def set_default_color(self):
        self.image.fill(self.color)
