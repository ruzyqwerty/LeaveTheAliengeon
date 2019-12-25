import pygame
from texture import BULLET_PLAYER, BULLET_ENEMY
from settings import BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height=0, offset=(0, 0), mouse_pos=(0, 0), colorkey=None, group=None):
        super().__init__(group)
        if height == 0:
            height = width
        self.speed = BULLET_SPEED * width / 10
        # self.speed = BULLET_SPEED
        self.images = BULLET_PLAYER
        # self.images = BULLET_ENEMY
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # mask (hitbox) of bullet sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += x  # * width - offset[0]
        self.rect.y += y  # * height - offset[1]
        self.vector = mouse_pos
        self.kx = self.vector[0] - self.rect.x
        self.ky = self.vector[1] - self.rect.y
        self.c = (self.kx ** 2 + self.ky ** 2) ** 0.5
        self.change_texture = 0

    def update(self):
        self.rect.x += int(self.kx / self.c * self.speed)
        self.rect.y += int(self.ky / self.c * self.speed)
        self.change_texture += 1
        if self.change_texture == 10:
            self.image = self.images[self.images.index(self.image) - 1]
            self.change_texture = 0
        pass
