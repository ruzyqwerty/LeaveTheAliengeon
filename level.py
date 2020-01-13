import pygame
from objects import Object, Coin, Heart
from entity import Player, EnemyMelee, EnemyGunner
from random import randint, choice
from settings import BLOCK_SIZE


class Level:
    def __init__(self, count, surface, difficult_level, player=None):
        self.width = 0
        self.height = 0
        self.player = player
        self.difficult_level = difficult_level
        self.all_sprites = pygame.sprite.Group()
        self.all_state_sprites = pygame.sprite.Group()
        self.drawing_sprites_layer_1 = pygame.sprite.Group()
        self.drawing_sprites_layer_2 = pygame.sprite.Group()
        self.all_dynamic_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_bullet_sprites = pygame.sprite.Group()
        self.punch_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.bonus_sprites = pygame.sprite.Group()
        self.is_fight = False
        self.teleport = None
        self.non_active_sprites = pygame.sprite.Group()
        self.camera_offset = (0, 0)
        self.offset = (0, 0)
        self.surface = surface
        self.rooms = []
        self.last_room = 0
        self.room_done = 0
        self.score = 0

        self.isLevelEnd = False
        self.needRestart = False

        self.load_level(count)

    def load_level(self, count):
        width, height = self.load_room('room_spawn.txt')
        self.load_horizontal_corridor(width, height)
        for i in range(count - 2):
            passage = None
            rando = randint(1, 10)
            if rando % 2 == 0:
                passage = self.load_bonus_room(width, height)
            width, height = self.load_room('room_fight.txt', passage=passage, number=i + 1)
            self.load_horizontal_corridor(width, height)
        self.load_room('room_portal.txt', number=count)

    def load_bonus_room(self, width, height):
        offset_x, offset_y = self.offset
        where_is_exit = randint(1, 10)
        bonuses = ['coin', 'heart']
        bonus = choice(bonuses)
        if where_is_exit % 2 == 0:
            offset = self.load_vertical_corridor(width, height, 1)
            offset_y -= offset
            offset_y -= height * BLOCK_SIZE
            room = Room('room_bonus.txt', (offset_x, offset_y), passage=2)
            width, height = room.width, room.height
            self.load_bonus(bonus, width // 2, height // 2, (offset_x, offset_y))
            self.all_state_sprites.add(room.room_sprites)
            self.wall_sprites.add(room.wall_sprites)
            self.all_sprites.add(room.room_sprites)
            return 1
        else:
            offset = self.load_vertical_corridor(width, height, 2)
            offset_y += offset
            offset_y += height * BLOCK_SIZE
            room = Room('room_bonus.txt', (offset_x, offset_y), passage=1)
            width, height = room.width, room.height
            self.load_bonus(bonus, width // 2, height // 2, (offset_x, offset_y))
            self.all_state_sprites.add(room.room_sprites)
            self.wall_sprites.add(room.wall_sprites)
            self.all_sprites.add(room.room_sprites)
            return 2

    def load_bonus(self, name, x, y, offset):
        if name == 'coin':
            bonus = Coin(self.bonus_sprites, self.all_state_sprites, self.all_sprites, x=x,
                 y=y, offset=offset)
        elif name == 'heart':
            bonus = Heart(self.bonus_sprites, self.all_state_sprites, self.all_sprites, x=x,
                 y=y, offset=offset)

    def load_room(self, name, passage=None, number=0):
        room = Room(name, self.offset, self.difficult_level, passage=passage, number=number)
        self.all_sprites.add(room.room_sprites, room.block_walls)
        self.wall_sprites.add(room.wall_sprites)
        self.all_state_sprites.add(room.room_sprites)
        self.non_active_sprites.add(room.block_walls)
        if room.player is not None:
            if self.player is None:
                self.player = room.player
            else:
                self.player.rect.x = room.player.rect.x
                self.player.rect.y = room.player.rect.y
        elif room.teleport is not None:
            self.teleport = room.teleport
            self.all_dynamic_sprites.add(self.teleport)
            self.all_sprites.add(self.teleport)
        elif len(room.enemies_sprites) > 0:
            self.enemies_sprites.add(room.enemies_sprites)
            self.all_sprites.add(room.enemies_sprites)
            for enemy in room.enemies_sprites:
                if enemy.player is None:
                    enemy.player = self.player
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

    def center_camera(self):
        x = - (self.player.rect.x + self.player.rect.w // 2 - pygame.display.Info().current_w // 2)
        y = - (self.player.rect.y + self.player.rect.h // 2 - pygame.display.Info().current_h // 2)
        for sprite in self.all_sprites:
            sprite.rect.x += x
            sprite.rect.y += y
        self.player.rect.x += x
        self.player.rect.y += y
        self.optimize()

    def optimize(self):
        self.drawing_sprites_layer_1 = pygame.sprite.Group()
        self.drawing_sprites_layer_2 = pygame.sprite.Group()
        for sprite in self.all_state_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites_layer_1.add(sprite)
        for sprite in self.all_dynamic_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites_layer_1.add(sprite)
        for sprite in self.enemies_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites_layer_2.add(sprite)
        for sprite in self.bonus_sprites:
            if sprite.rect.colliderect((0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)):
                self.drawing_sprites_layer_2.add(sprite)

    def update_rooms(self):
        if self.last_room + 1 < len(self.rooms):
            if pygame.sprite.spritecollideany(self.player, self.rooms[self.last_room + 1].scripts):
                self.last_room += 1
                if not self.all_state_sprites.has(self.non_active_sprites):
                    self.all_state_sprites.add(self.non_active_sprites)
                if not self.wall_sprites.has(self.non_active_sprites):
                    self.wall_sprites.add(self.non_active_sprites)
                self.is_fight = True
                self.player.rect.x += BLOCK_SIZE
            if self.last_room != 0 and len(self.rooms[self.last_room].enemies_sprites) <= 0:
                self.all_state_sprites.remove(self.non_active_sprites)
                self.wall_sprites.remove(self.non_active_sprites)
                self.is_fight = False
                if self.room_done != self.last_room:
                    self.room_done += 1

    def render(self):
        self.drawing_sprites_layer_1.draw(self.surface)
        self.drawing_sprites_layer_2.draw(self.surface)
        self.player.render(self.surface)
        for enemy in self.enemies_sprites:
            enemy.render(self.surface)

    def check_new_bullets(self):
        if not self.all_sprites.has(self.player.gun.bullet_sprites):
            self.all_sprites.remove(self.player.gun.bullet_sprites)
            self.all_sprites.add(self.player.gun.bullet_sprites)
            self.bullet_sprites.remove(self.player.gun.bullet_sprites)
            self.bullet_sprites.add(self.player.gun.bullet_sprites)
        pygame.sprite.groupcollide(self.wall_sprites, self.bullet_sprites, False, True)
        for enemy in self.enemies_sprites:
            if enemy.type == 'gunner':
                if not self.all_sprites.has(enemy.gun.bullet_sprites):
                    self.all_sprites.remove(enemy.gun.bullet_sprites)
                    self.all_sprites.add(enemy.gun.bullet_sprites)
                    self.enemy_bullet_sprites.remove(enemy.gun.bullet_sprites)
                    self.enemy_bullet_sprites.add(enemy.gun.bullet_sprites)
        pygame.sprite.groupcollide(self.wall_sprites, self.enemy_bullet_sprites, False, True)

    def check_score(self):
        if self.score != self.player.score:
            self.score = self.player.score

    def check_portal(self):
        if pygame.sprite.collide_rect(self.player, self.teleport):
            self.isLevelEnd = True

    def check_bonus(self):
        if pygame.sprite.spritecollideany(self.player, self.bonus_sprites, False):
            bonus = pygame.sprite.spritecollideany(self.player, self.bonus_sprites, False)
            item, value = bonus.pick_up()
            if item == 'score':
                self.player.score += value
            elif item == 'hp':
                self.player.health += value
            bonus.kill()

    def check_player(self):
        if self.player.health <= 0:
            self.needRestart = True

    def update(self, events):
        self.center_camera()
        self.update_rooms()
        self.check_portal()
        self.check_bonus()
        self.check_player()
        # TODO NEED FIX!!!
        for enemy in self.enemies_sprites:
            enemy.update(self.bullet_sprites, self.last_room, walls=self.wall_sprites)
        for enemy_bullet in self.enemy_bullet_sprites:
            if pygame.sprite.spritecollideany(self.player, self.enemy_bullet_sprites):
                self.player.health -= enemy_bullet.damage
                enemy_bullet.kill()
        self.punch_sprites.update()
        self.player.update(events, walls=self.wall_sprites)
        self.check_new_bullets()
        self.check_score()
        self.all_sprites.update()
        self.enemy_bullet_sprites.update()


class Room:
    def __init__(self, name, offset, difficult_level=0, passage=None, number=0):
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
        self.enemies_sprites = pygame.sprite.Group()
        self.scripts = pygame.sprite.Group()
        self.player = None
        self.teleport = None
        self.width, self.height = self.load_room(name, passage)
        if 'fight' in name:
            self.generate_enemies(difficult_level)

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

    def generate_enemies(self, difficult_level):
        busy = set()
        min_count = difficult_level
        max_count = difficult_level * 5 // 2
        count = randint(min_count, max_count)
        for _ in range(count):
            col, row = randint(1 + 2, self.width - 2 - 2), randint(1 + 2, self.height - 2 - 2)
            if (col, row) not in busy:
                busy.add((col, row))
                shooting = bool(randint(0, 1))
                if shooting:
                    enemy = EnemyGunner(col, row, offset=self.offset, room_number=self.number,
                                        groups=self.enemies_sprites)
                else:
                    enemy = EnemyMelee(col, row, offset=self.offset, room_number=self.number,
                                       groups=self.enemies_sprites)
                if enemy:
                    enemy.damage *= (1 + 0.1 * (difficult_level - 1))
