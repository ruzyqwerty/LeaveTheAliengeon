import pygame
from objects import Object
from player import Player
from random import randint
from settings import BLOCK_SIZE


class Level:
    def __init__(self, count, surface):
        self.width = 0
        self.height = 0
        self.player = None
        self.all_sprites = pygame.sprite.Group()
        self.camera_offset = (0, 0)
        self.offset = (0, 0)
        self.surface = surface
        self.rooms = []

        self.load_level(count)

    def load_level(self, count):
        width, height = self.load_room('room_spawn.txt')
        self.load_corridor('corridor_horizontal.txt', width, height)
        for _ in range(count - 2):
            width, height = self.load_room('room_fight.txt')
            self.load_corridor('corridor_horizontal.txt', width, height)

    def load_room(self, name):
        room = Room(name, self.offset)
        self.all_sprites.add(room.room_sprites)
        if room.player is not None:
            self.player = room.player
        width, height = room.width, room.height
        self.rooms.append(room)
        return width, height

    def load_corridor(self, name, width, height):
        offset_x, offset_y = self.offset
        offset_x += width * BLOCK_SIZE
        self.offset = offset_x, offset_y
        corridor = Room(name, (offset_x, offset_y + (height // 2 - 2) * BLOCK_SIZE))
        width, height = corridor.width, corridor.height
        self.all_sprites.add(corridor.room_sprites)
        offset_x += width * BLOCK_SIZE
        self.offset = offset_x, offset_y

    def render(self):
        self.all_sprites.draw(self.surface)
        self.player.render(self.surface)

    def check_collision(self):
        for sprite in self.all_sprites:
            if sprite.class_name == 'wall' and sprite.rect.colliderect(self.player.rect):
                if sprite.rect.collidepoint(self.player.rect.midtop) and self.player.speed[1] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midbottom) and self.player.speed[1] > 0:
                    self.player.speed = self.player.speed[0], 0
                if sprite.rect.collidepoint(self.player.rect.midleft) and self.player.speed[0] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midright) and self.player.speed[0] > 0:
                    self.player.speed = 0, self.player.speed[1]

    def center_camera(self):
        # x = - (self.player.rect.x + self.player.rect.w // 2 - 300)
        # y = - (self.player.rect.y + self.player.rect.h // 2 - 200)
        x = - (self.player.rect.x + self.player.rect.w // 2 - pygame.display.Info().current_w // 2)
        y = - (self.player.rect.y + self.player.rect.h // 2 - pygame.display.Info().current_h // 2)
        for sprite in self.all_sprites:
            sprite.rect.x += x
            sprite.rect.y += y
        self.player.rect.x += x
        self.player.rect.y += y

    def update(self):
        self.center_camera()
        self.player.normalize_speed()
        self.check_collision()
        self.player.update()
        self.render()


class Room:
    def __init__(self, name, offset, passage=None):
        self.class_name = name
        if name.startswith('corridor'):
            self.class_name = 'corridor'
        elif name.startswith('room'):
            self.class_name = 'room'
        self.offset = offset
        self.room_sprites = pygame.sprite.Group()
        self.player = None
        self.width, self.height = self.load_room(name, passage)

    def load_room(self, name, passage=None):
        name = 'Rooms/' + name
        with open(name, mode='r') as file:
            room_map = [line.strip() for line in file]
        width = len(room_map[0])
        height = len(room_map)
        room_map = [list(row) for row in room_map]
        if passage is not None:
            pass
        for row in range(height):
            for col in range(width):
                obj = None
                if room_map[row][col] == 'W':
                    obj = Object('wall', col, row, BLOCK_SIZE, offset=self.offset)
                elif room_map[row][col] == '.':
                    obj = Object('empty', col, row, BLOCK_SIZE, offset=self.offset)
                elif room_map[row][col] == 'P':
                    obj = Object('empty', col, row, BLOCK_SIZE, offset=self.offset)
                    self.player = Player(col, row, BLOCK_SIZE, offset=self.offset, colorkey=-1)
                if obj is not None:
                    self.room_sprites.add(obj)
        return width, height