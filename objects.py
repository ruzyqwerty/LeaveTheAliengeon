import pygame
from random import choice

WALLS = ['wall_1.png', 'wall_2.png', 'wall_3.png']
FLOORS = ['floor_1.png', 'floor_2.png', 'floor_3.png', 'floor_4.png']
LEVEL_OBJECTS = {
    'wall': choice(WALLS),
    'empty': choice(FLOORS)
}


class Object(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height=0, offset=(0, 0), colorkey=None):
        super().__init__()
        if height == 0:
            height = width
        self.class_name = name
        self.image = None
        name = LEVEL_OBJECTS[name]
        name = 'Resources/' + name
        self.load_image(name, width, height, colorkey)
        self.rect = self.image.get_rect()
        self.rect.x += x * width + offset[0]
        self.rect.y += y * height + offset[1]

    def load_image(self, name, width, height, colorkey):
        image = pygame.image.load(name).convert()

        if colorkey is not None:
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        self.image = image

    def update(self):
        pass
