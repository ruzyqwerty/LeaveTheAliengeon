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

        self.speed = (0, 0)
        self.normal_speed = 3

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
