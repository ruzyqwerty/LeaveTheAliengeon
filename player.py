import pygame
from texture import PLAYER
from settings import BLOCK_SIZE, PLAYER_SPEED


class Player:
    def __init__(self, x, y, offset=(0, 0)):
        self.images = PLAYER
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x * BLOCK_SIZE + offset[0]
        self.rect.y += y * BLOCK_SIZE + offset[1]
        self.speed = (0, 0)
        self.normal_speed = PLAYER_SPEED * BLOCK_SIZE / 10
        # self.normal_speed = PLAYER_SPEED

    def normalize_speed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            speed_x = self.normal_speed * (-1)
        elif keys[pygame.K_RIGHT]:
            speed_x = self.normal_speed
        else:
            speed_x = 0
        if keys[pygame.K_UP]:
            speed_y = self.normal_speed * (-1)
        elif keys[pygame.K_DOWN]:
            speed_y = self.normal_speed
        else:
            speed_y = 0
        self.speed = speed_x, speed_y

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
