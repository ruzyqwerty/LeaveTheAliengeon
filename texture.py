from random import choice

WALLS = ['wall_1.png', 'wall_2.png', 'wall_3.png']
FLOORS = ['floor_1.png', 'floor_2.png', 'floor_3.png', 'floor_4.png']

LEVEL_OBJECTS = {
    'wall': choice(WALLS),
    'empty': choice(FLOORS)
}

NAMES = ['player_idle_1.png', 'player_idle_2.png']