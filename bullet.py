import copy
from texture import BULLET
from settings import BULLET_SPEED


class Bullet:
    def __init__(self, surface, x, y, width, height=0, offset=(0, 0), mouse_pos=(0, 0), colorkey=None):
        if height == 0:
            height = width
        self.speed = BULLET_SPEED * width / 30
        self.surface = surface
        self.images = BULLET
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x + offset[0]
        self.rect.y += y + offset[1]
        print(self.rect)
        self.vector = mouse_pos
        self.c = ((self.vector[0] - self.rect.x) ** 2 + (self.vector[1] - self.rect.y) ** 2) ** 0.5
        self.kx = self.vector[0] - self.rect.x
        self.ky = self.vector[1] - self.rect.y

    def render(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += int(self.kx / self.c * self.speed)
        self.rect.y += int(self.ky / self.c * self.speed)
        self.render()
        pass
