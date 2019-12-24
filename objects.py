import pygame
from texture import LEVEL_OBJECTS
from settings import BLOCK_SIZE


class Object(pygame.sprite.Sprite):
    def __init__(self, groups, name, x, y, width, height=0, offset=(0, 0), colorkey=None):
        super().__init__(groups)
        if height == 0:
            height = width
        self.class_name = name
        self.image = LEVEL_OBJECTS[name]
        self.rect = self.image.get_rect()
        self.rect.x += x * BLOCK_SIZE + offset[0]
        self.rect.y += y * BLOCK_SIZE + offset[1]

    def update(self):
        pass
