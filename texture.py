import pygame
from random import choice
from settings import BLOCK_SIZE


def load_image(name, colorkey=None):
    name = 'Resources/' + name
    image = pygame.image.load(name).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
    return image


WALLS = [load_image('wall_1.png'), load_image('wall_2.png'), load_image('wall_3.png')]
FLOORS = [load_image('floor_1.png'), load_image('floor_2.png'), load_image('floor_3.png'), load_image('floor_4.png')]

LEVEL_OBJECTS = {
    'wall': choice(WALLS),
    'empty': choice(FLOORS)
}

PLAYER = [load_image('player_idle_1.png', -1), load_image('player_idle_2.png', -1)]

GUN = [load_image('gun_rifle.png', -1)]

AIM = [load_image('aim_1.png', (0, 255, 0))]

BULLET = [load_image('bullet_1.png', (0, 255, 0))]
