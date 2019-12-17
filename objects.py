import pygame
from texture import LEVEL_OBJECTS


class Object(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height=0, offset=(0, 0), colorkey=None):
        super().__init__()
        if height == 0:
            height = width
        self.class_name = name
        self.image = LEVEL_OBJECTS[name]
        self.rect = self.image.get_rect()
        self.rect.x += x * width + offset[0]
        self.rect.y += y * height + offset[1]

    def update(self):
        pass
