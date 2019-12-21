import pygame
from texture import LEVEL_OBJECTS
from settings import BLOCK_SIZE


class Object(pygame.sprite.Sprite):
    def __init__(self, name, x, y, offset=(0, 0)):
        super().__init__()
        self.class_name = name
        self.image = LEVEL_OBJECTS[name]
        self.rect = self.image.get_rect()
        self.rect.x += x * BLOCK_SIZE + offset[0]
        self.rect.y += y * BLOCK_SIZE + offset[1]

    def update(self):
        pass
