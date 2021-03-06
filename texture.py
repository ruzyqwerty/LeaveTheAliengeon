import pygame
from random import choice
from settings import BLOCK_SIZE


def load_image(name, colorkey=None, width=BLOCK_SIZE, height=BLOCK_SIZE):
    name = 'Data/Resources/' + name
    image = pygame.image.load(name).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    return image


WALLS = [load_image('wall_1.png'), load_image('wall_2.png'), load_image('wall_3.png')]
FLOORS = [load_image('floor_1.png'), load_image('floor_2.png'), load_image('floor_3.png'), load_image('floor_4.png')]
TELEPORTS = [
             load_image('teleport_1.png', width=BLOCK_SIZE * 3, height=BLOCK_SIZE * 5, colorkey=(0, 0, 0)),
             load_image('teleport_2.png', width=BLOCK_SIZE * 3, height=BLOCK_SIZE * 5, colorkey=(0, 0, 0)),
             load_image('teleport_3.png', width=BLOCK_SIZE * 3, height=BLOCK_SIZE * 5, colorkey=(0, 0, 0)),
             load_image('teleport_4.png', width=BLOCK_SIZE * 3, height=BLOCK_SIZE * 5, colorkey=(0, 0, 0)),
             ]

LEVEL_OBJECTS = {
    'wall': choice(WALLS),
    'empty': choice(FLOORS),
    'teleport': choice(TELEPORTS)
}

PLAYER = [load_image('player_idle_1.png', -1), load_image('player_idle_2.png', -1)]

ENEMY_WARRIOR = [load_image('enemy_warrior_1.png', -1), load_image('enemy_warrior_1_hitted.png', -1)]
ENEMY_GUNNER = [load_image('enemy_gunner_1.png', -1), load_image('enemy_gunner_1_hitted.png', -1)]
PUNCH = [load_image('punch_1.png', -1)]

GUN = [load_image('gun_rifle.png', -1)]

AIM = [load_image('aim_1.png', (0, 255, 0))]

BULLET_PLAYER = [load_image('bullet_p_1.png', (0, 255, 0)), load_image('bullet_p_2.png', (0, 255, 0))]
BULLET_ENEMY = [load_image('bullet_e_1.png', (0, 255, 0)), load_image('bullet_e_2.png', (0, 255, 0))]

BONUSES = {
    'heart': load_image('bonus_heart_1.png', -1),
    'coin': load_image('bonus_coin_1.png', -1)
}
