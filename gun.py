import pygame
from texture import GUN


class Gun:
    def __init__(self, x, y, width, height=0, offset=(0, 0), colorkey=None):
        if height == 0:
            height = width
        self.images = GUN
        self.image = self.images[0]
        self.image_left = pygame.transform.flip(self.images[0], True, False)
        self.image_right = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x * width + offset[0]
        self.rect.y += y * height + offset[1]
        self.w_h = width, height

    def on_hand(self):
        x, y = self.rect[:2]
        return x, y

    def update(self, player_x, player_y, right=True):
        self.rect.x = player_x
        self.rect.y = player_y
        self.rect.y += 2 * self.w_h[1] / 10
        if right:
            self.image = self.image_right
            self.rect.x += 3 * self.w_h[0] / 10
        else:
            self.image = self.image_left
            self.rect.x -= 3 * self.w_h[0] / 10

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
