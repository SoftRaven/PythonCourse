import pygame


class Queen(pygame.sprite.Sprite):
    def __init__(self, cell, color):
        pygame.sprite.Sprite.__init__(self)

        # attributes
        self.x = cell.x
        self.y = cell.y
        self.size = cell.size
        self.clicked = False

        # initialize image property
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # draw queen figure
        pygame.draw.polygon(self.image, color,
                            [[self.size / 2, 0], [self.size, self.size],
                             [self.size / 2, self.size - 10], [0, self.size]])

        # initialize rect property
        self.rect = self.image.get_rect()

        # set position to rect
        self.rect.top = self.x
        self.rect.left = self.y

    def set_clicked(self):
        self.clicked = True

    def set_unclicked(self):
        self.clicked = False
