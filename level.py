import pygame
from objects import Object
from player import Player


class Level:
    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.level_map = self.load_level(filename)
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.update_sprite()

    def update_sprite(self):
        for row in range(self.height):
            for col in range(self.width):
                obj = None
                if self.level_map[row][col] == 'W':
                    obj = Object('wall', col, row, 25)
                elif self.level_map[row][col] == '.':
                    obj = Object('empty', col, row, 25)
                elif self.level_map[row][col] == 'P':
                    obj = Object('empty', col, row, 25)
                    self.player = Player(col, row, 25, colorkey=(0, 255, 0))
                if obj is not None:
                    self.all_sprites.add(obj)

    def load_level(self, filename):
        filename = 'Maps/' + filename
        with open(filename, mode='r') as file:
            level_map = [line.strip() for line in file]
        self.width = len(level_map[0])
        self.height = len(level_map)
        return [list(row) for row in level_map]

    def render(self, surface):
        self.all_sprites.draw(surface)
        self.player.render(surface)

    def check_collision(self):
        for sprite in self.all_sprites:
            if sprite.class_name == 'wall' and sprite.rect.colliderect(self.player.rect):
                if sprite.rect.collidepoint(self.player.rect.midtop) and self.player.speed[1] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midbottom) and self.player.speed[1] > 0:
                    self.player.speed = self.player.speed[0], 0
                if sprite.rect.collidepoint(self.player.rect.midleft) and self.player.speed[0] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midright) and self.player.speed[0] > 0:
                    self.player.speed = 0, self.player.speed[1]

    def update(self):
        self.player.normalize_speed()
        self.check_collision()
        self.player.update()
