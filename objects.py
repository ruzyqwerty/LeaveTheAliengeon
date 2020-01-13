import pygame
from texture import LEVEL_OBJECTS, BONUSES
from settings import BLOCK_SIZE
from audio import COIN_UP_SOUND, HEART_UP_SOUND


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


class Bonus(pygame.sprite.Sprite):
    def __init__(self, *groups, name, x, y, offset=(0, 0)):
        super().__init__(groups)
        self.image = BONUSES[name]
        self.rect = self.image.get_rect()
        self.rect.x += x * BLOCK_SIZE + offset[0]
        self.rect.y += y * BLOCK_SIZE + offset[1]


class Coin(Bonus):
    def __init__(self, *groups, x, y, offset):
        super().__init__(groups, name='coin', x=x, y=y, offset=offset)

    def pick_up(self):
        COIN_UP_SOUND.play()
        return 'score', 70


class Heart(Bonus):
    def __init__(self, *groups, x, y, offset):
        super().__init__(groups, name='heart', x=x, y=y, offset=offset)

    def pick_up(self):
        HEART_UP_SOUND.play()
        return 'hp', 50
