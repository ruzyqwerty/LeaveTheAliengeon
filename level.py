import pygame
from objects import Object
from player import Player
from random import randint


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
        if count < 3:
            count = 3
        offset_x, offset_y = (0, 0)
        count -= 2
        passage = 0, randint(1, 4)
        width, height = self.load_room('room_spawn.txt', (offset_x, offset_y), passage=passage)
        self.rooms.append('spawn_room')
        exit = passage[1]
        self.load_coridor(exit, width, height)

        while len(self.rooms) - 2 != count:
            enter = 0
            if exit == 1:
                enter = 3
            elif exit == 2:
                enter = 4
            elif exit == 3:
                enter = 1
            elif exit == 4:
                enter = 2
            exit = randint(1, 4)
            while exit == enter:
                exit = randint(1, 4)
            width, height = self.load_room('room_fight.txt', self.offset, passage=(enter, exit))
            if width is not None:
                self.rooms.append('fight_room')
                if enter == 2:
                    offset_x -= width * 25
                elif enter == 1:
                    offset_y -= height * 25
                self.load_coridor(exit, width, height)

    def load_coridor(self, exit, width, height):
        offset_x, offset_y = self.offset
        if exit == 2 or exit == 4:
            x = 0
            if exit == 2:
                x += width * 25
            else:
                x -= width // 2 * 25
            y = (height // 2 - 2) * 25
            width, height = self.load_room('corridor_horizontal.txt', (offset_x + x, offset_y + y))
            offset_x += x
            if exit == 2:
                offset_x += width * 25  # TODO bug crashing when game start
        elif exit == 1 or exit == 3:
            y = 0
            if exit == 1:
                y -= height // 2 * 25
            else:
                y += height * 25
            x = (width // 2 - 2) * 25
            width, height = self.load_room('corridor_vertical.txt', (offset_x + x, offset_y + y))
            offset_y += y
            if exit == 3:
                offset_y += height * 25  # TODO bug crashing when game start
        self.offset = offset_x, offset_y

    def load_room(self, name, offset, passage=None):
        new_sprites = pygame.sprite.Group()
        name = 'Rooms/' + name
        with open(name, mode='r') as file:
            room_map = [line.strip() for line in file]
        width = len(room_map[0])
        height = len(room_map)
        room_map = [list(row) for row in room_map]
        row, col = 0, 0
        if passage is not None:
            enter, exit = passage
            if enter == 1 or enter == 3:
                if enter == 1:
                    row = 0
                    col = width // 2
                elif enter == 3:
                    row = height - 1
                    col = width // 2
                    offset = offset[0], offset[1] - height * 25
                room_map[row][col] = '.'
                room_map[row][col - 1] = '.'
                room_map[row][col + 1] = '.'
            elif enter == 2 or enter == 4:
                if enter == 2:
                    row = height // 2
                    col = width - 1
                    offset = offset[0] - width * 25, offset[1]
                elif enter == 4:
                    row = height // 2
                    col = 0
                room_map[row][col] = '.'
                room_map[row - 1][col] = '.'
                room_map[row + 1][col] = '.'
            if exit == 1 or exit == 3:
                if exit == 1:
                    row = 0
                    col = width // 2
                elif exit == 3:
                    row = height - 1
                    col = width // 2
                room_map[row][col] = '.'
                room_map[row][col - 1] = '.'
                room_map[row][col + 1] = '.'
            elif exit == 2 or exit == 4:
                if exit == 2:
                    row = height // 2
                    col = width - 1
                elif exit == 4:
                    row = height // 2
                    col = 0
                room_map[row][col] = '.'
                room_map[row - 1][col] = '.'
                room_map[row + 1][col] = '.'
        for row in range(height):
            for col in range(width):
                obj = None
                if room_map[row][col] == 'W':
                    obj = Object('wall', col, row, 25, offset=offset)
                elif room_map[row][col] == '.':
                    obj = Object('empty', col, row, 25, offset=offset)
                elif room_map[row][col] == 'P':
                    obj = Object('empty', col, row, 25, offset=offset)
                    self.player = Player(col, row, 25, offset=offset, colorkey=(0, 255, 0))
                if obj is not None:
                    # self.all_sprites.add(obj)
                    new_sprites.add(obj)
        collided = pygame.sprite.groupcollide(new_sprites, self.all_sprites, False, False)
        if len(collided) <= 5:
            self.all_sprites.add(new_sprites)
            self.offset = offset
            return width, height
        return None, None

    def render(self):
        self.all_sprites.draw(self.surface)
        # for sprite in self.all_sprites:
        #     self.surface.blit(sprite.image, (sprite.rect.x + self.offset[0], sprite.rect.y - self.offset[1]))
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
        x = - (self.player.rect.x + self.player.rect.w // 2 - 300)
        y = - (self.player.rect.y + self.player.rect.h // 2 - 200)
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
