import pygame

LEVEL_OBJECTS = {
    'wall': 'wall_1.png',
    'empty': 'floor_1.png'
}


class Object(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height=0, colorkey=None):
        super().__init__()
        if height == 0:
            height = width
        self.class_name = name
        self.image = None
        name = LEVEL_OBJECTS[name]
        name = 'Resources/' + name
        self.load_image(name, width, height, colorkey)
        self.rect = self.image.get_rect()
        self.rect.x += x * width
        self.rect.y += y * height

    def load_image(self, name, width, height, colorkey):
        image = pygame.image.load(name).convert()

        if colorkey is not None:
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        self.image = image

    def update(self):
        pass
