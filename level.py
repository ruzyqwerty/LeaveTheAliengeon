from typing import Any, Union

import pygame
from objects import Object
from entity import Player, Enemy
from random import randint
from settings import BLOCK_SIZE


class Level:
    def __init__(self, count, surface):
        self.width = 0
        self.height = 0
        self.player = None
        self.all_sprites = pygame.sprite.Group()
        self.all_state_sprites = pygame.sprite.Group()
        self.drawing_sprites = pygame.sprite.Group()
        self.all_dynamic_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.teleport = None
        self.non_active_sprites = pygame.sprite.Group()
        self.camera_offset = (0, 0)
        self.offset = (0, 0)
        self.surface = surface
        self.rooms = []
        self.enemies = []
        self.last_room = 0

        self.load_level(count)

    def load_level(self, count):
        width, height = self.load_room('room_spawn.txt')
        self.load_horizontal_corridor(width, height)
        for i in range(count - 2):
            passage = None
            rando = randint(1, 10)
            if rando % 2 == 0:
                passage = self.load_bonus_room(width, height)
            width, height = self.load_room('room_fight.txt', passage, number=i + 1)
            self.load_horizontal_corridor(width, height)
        self.load_room('room_portal.txt', number=count)

    def load_bonus_room(self, width, height):
        offset_x, offset_y = self.offset
        where_is_exit = randint(1, 10)
        if where_is_exit % 2 == 0:
            offset = self.load_vertical_corridor(width, height, 1)
            offset_y -= offset
            offset_y -= height * BLOCK_SIZE
            room = Room('room_bonus.txt', (offset_x, offset_y), 2)
            self.all_state_sprites.add(room.room_sprites)
            self.all_sprites.add(room.room_sprites)
            return 1
        else:
            offset = self.load_vertical_corridor(width, height, 2)
            offset_y += offset
            offset_y += height * BLOCK_SIZE
            room = Room('room_bonus.txt', (offset_x, offset_y), 1)
            self.all_state_sprites.add(room.room_sprites)
            self.all_sprites.add(room.room_sprites)
            return 2

    def load_room(self, name, passage=None, number=0):
        room = Room(name, self.offset, passage, number=number)
        self.all_sprites.add(room.room_sprites, room.block_walls)
        self.wall_sprites.add(room.wall_sprites)
        self.all_state_sprites.add(room.room_sprites)
        self.non_active_sprites.add(room.block_walls)
        if room.player is not None:
            self.player = room.player
        if room.teleport is not None:
            self.teleport = room.teleport
            self.all_dynamic_sprites.add(self.teleport)
            self.all_sprites.add(self.teleport)
        if room.enemies is not None:
            self.enemies.extend(room.enemies)
        width, height = room.width, room.height
        self.rooms.append(room)
        return width, height

    def load_vertical_corridor(self, width, height, passage):
        offset_x, offset_y = self.offset
        corridor = Room('corridor_vertical.txt', (offset_x + (width // 2 - 2) * BLOCK_SIZE, offset_y))
        if passage == 1:
            for sprite in corridor.room_sprites:
                sprite.rect.y -= corridor.height * BLOCK_SIZE
        if passage == 2:
            for sprite in corridor.room_sprites:
                sprite.rect.y += height * BLOCK_SIZE
        self.all_state_sprites.add(corridor.room_sprites)
        self.all_sprites.add(corridor.room_sprites)
        self.wall_sprites.add(corridor.wall_sprites)
        return corridor.height * BLOCK_SIZE

    def load_horizontal_corridor(self, width, height):
        offset_x, offset_y = self.offset
        offset_x += width * BLOCK_SIZE
        corridor = Room('corridor_horizontal.txt', (offset_x, offset_y + (height // 2 - 2) * BLOCK_SIZE))
        width, height = corridor.width, corridor.height
        self.all_state_sprites.add(corridor.room_sprites)
        self.all_sprites.add(corridor.room_sprites)
        self.wall_sprites.add(corridor.wall_sprites)
        offset_x += width * BLOCK_SIZE
        self.offset = offset_x, offset_y

    def check_collision(self):
        for sprite in self.wall_sprites:
            if sprite.class_name == 'wall' and sprite.rect.colliderect(self.player.rect):
                if sprite.rect.collidepoint(self.player.rect.midtop) and self.player.speed[1] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midbottom) and self.player.speed[1] > 0:
                    self.player.speed = self.player.speed[0], 0
                if sprite.rect.collidepoint(self.player.rect.midleft) and self.player.speed[0] < 0 \
                        or sprite.rect.collidepoint(self.player.rect.midright) and self.player.speed[0] > 0:
                    self.player.speed = 0, self.player.speed[1]

    def center_camera(self):
        x = - (self.player.rect.x + self.player.rect.w // 2 - pygame.display.Info().current_w // 2)
        y = - (self.player.rect.y + self.player.rect.h // 2 - pygame.display.Info().current_h // 2)
        for sprite in self.all_sprites:
            sprite.rect.x += x
            sprite.rect.y += y
        for enemy in self.enemies:
            enemy.rect.x += x
            enemy.rect.y += y
        self.player.rect.x += x
        self.player.rect.y += y
        self.optimize()

    def optimize(self):
        self.drawing_sprites.clear(self.surface, self.surface)
        for sprite in self.all_state_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites.add(sprite)
        for sprite in self.all_dynamic_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites.add(sprite)

    def update_rooms(self):
        if self.last_room + 1 < len(self.rooms):
            if pygame.sprite.spritecollideany(self.player, self.rooms[self.last_room + 1].scripts):
                self.last_room += 1
                self.all_state_sprites.add(self.non_active_sprites)
                self.wall_sprites.add(self.non_active_sprites)

    def render(self):
        self.drawing_sprites.draw(self.surface)
        self.all_dynamic_sprites.draw(self.surface)
        for enemy in self.enemies:
            if enemy.room_number == self.last_room or enemy.room_number == self.last_room + 1:
                enemy.render(self.surface)
        self.player.render(self.surface)

    def update(self, events):
        self.center_camera()
        self.check_collision()
        self.update_rooms()
        self.player.update(events)
        if not self.all_sprites.has(self.player.gun.bullet_sprites):
            self.all_sprites.remove(self.player.gun.bullet_sprites)
            self.all_sprites.add(self.player.gun.bullet_sprites)
        self.all_sprites.update()
        self.render()


class Room:
    def __init__(self, name, offset, passage=None, number=0):
        self.class_name = name
        self.number = number
        if name.startswith('corridor'):
            self.class_name = 'corridor'
        elif name.startswith('room'):
            self.class_name = 'room'
        self.offset = offset
        self.room_sprites = pygame.sprite.Group()
        self.block_walls = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.scripts = pygame.sprite.Group()
        self.enemies = None
        self.player = None
        self.teleport = None
        self.width, self.height = self.load_room(name, passage)
        if 'fight' in name:
            self.generate_enemies()

    def load_room(self, name, passage=None):
        name = 'Rooms/' + name
        with open(name, mode='r') as file:
            room_map = [line.strip() for line in file]
        width = len(room_map[0])
        height = len(room_map)
        room_map = [list(row) for row in room_map]
        if passage is not None:
            row = None
            if passage == 1:
                row = 0
            elif passage == 2:
                row = height - 1
            if row is not None:
                room_map[row][width // 2 - 1] = '|'
                room_map[row][width // 2] = '|'
                room_map[row][width // 2 + 1] = '|'
        for row in range(height):
            for col in range(width):
                obj = None
                if room_map[row][col] == 'W':
                    obj = Object((self.room_sprites, self.wall_sprites),
                                 'wall', col, row, BLOCK_SIZE, offset=self.offset)
                elif room_map[row][col] == '.':
                    obj = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                elif room_map[row][col] == '|':
                    obj = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                    block_wall = Object((self.block_walls,), 'wall', col, row, BLOCK_SIZE, offset=self.offset)
                    self.block_walls.add(block_wall)
                elif room_map[row][col] == 'S':
                    obj = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                    script = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                    self.scripts.add(script)
                    self.room_sprites.add(script)
                elif room_map[row][col] == 'P':
                    obj = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                    self.player = Player(col, row, offset=self.offset)
                elif room_map[row][col] == 'T':
                    obj = Object((self.room_sprites,), 'empty', col, row, BLOCK_SIZE, offset=self.offset)
                    self.teleport = Object((self.room_sprites,),
                                           'teleport', col - 2, row - 4, BLOCK_SIZE, offset=self.offset)
                if obj is not None:
                    self.room_sprites.add(obj)
        return width, height

    def generate_enemies(self):
        busy = set()
        count = randint(2, 5)
        for _ in range(count):
            if self.enemies is None:
                self.enemies = []
            col, row = randint(1, self.width - 2), randint(1, self.height - 2)
            if (col, row) not in busy:
                busy.add((col, row))
                enemy = Enemy(col, row, offset=self.offset, room_number=self.number)
                self.enemies.append(enemy)
