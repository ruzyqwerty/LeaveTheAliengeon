import pygame

NAMES = ['player_idle_1.png', 'player_idle_2.png']


class Player:
    def __init__(self, x, y, width, height=0, colorkey=None):
        if height == 0:
            height = width
        self.images = []
        self.image = None
        self.load_image(width, height, colorkey)
        self.rect = self.image.get_rect()
        self.rect.x += x * width
        self.rect.y += y * height

    def load_image(self, width, height, colorkey):
        for name in NAMES:
            name = 'Resources/' + name
            image = pygame.image.load(name).convert()

            if colorkey is not None:
                image.set_colorkey(colorkey)
            else:
                image = image.convert_alpha()
            image = pygame.transform.scale(image, (width, height))
            self.images.append(image)
        self.image = self.images[0]

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
