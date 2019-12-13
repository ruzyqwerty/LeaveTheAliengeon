import pygame

NAMES = ['player_idle_1.png', 'player_idle_2.png']


class Player:
    def __init__(self, x, y, width, height=0, colorkey=None):
        if height == 0:
            height = width
        self.images = []
        self.image = None
        self.load_image(width, height, colorkey)
        self.rect = self.image.get_rect()
        self.rect.x += x * width
        self.rect.y += y * height

        self.speed = 3

    def load_image(self, width, height, colorkey):
        for name in NAMES:
            name = 'Resources/' + name
            image = pygame.image.load(name).convert()

            if colorkey is not None:
                image.set_colorkey(colorkey)
            else:
                image = image.convert_alpha()
            image = pygame.transform.scale(image, (width, height))
            self.images.append(image)
        self.image = self.images[0]

    def player_control(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
