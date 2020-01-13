import pygame
from texture import PLAYER, ENEMY_WARRIOR, ENEMY_GUNNER, GUN, BULLET_PLAYER, PUNCH, BULLET_ENEMY
from settings import BLOCK_SIZE, PLAYER_SPEED, ENEMY_SPEED, BULLET_SPEED
from events import RELOAD_EVENT
from random import randint


class Body(pygame.sprite.Sprite):
    def __init__(self, texture, x=None, y=None, offset=(0, 0), groups=None):
        if groups is None:
            groups = []
        super().__init__(groups)
        self.type = None
        self.speed = (0, 0)
        self.normal_speed = None
        self.images = texture
        self.image = self.images[0]
        self.image_left = pygame.transform.flip(self.images[0], True, False)
        self.image_right = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x * BLOCK_SIZE + offset[0]
        self.rect.y += y * BLOCK_SIZE + offset[1]
        # mask (hit box) of player sprite
        self.mask = pygame.mask.from_surface(self.image)

        if texture == PLAYER or texture == ENEMY_WARRIOR:
            self.health = 100
        elif texture == ENEMY_GUNNER:
            self.health = 60

    def check_collision(self, walls):
        left_collision = pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 4,
                                     self.rect.width // 3, self.rect.height // 2)
        right_collision = pygame.Rect(self.rect.x + self.rect.width // 3 * 2, self.rect.y + self.rect.height // 3,
                                      self.rect.width // 3, self.rect.height // 2)
        top_collision = pygame.Rect(self.rect.x + self.rect.width // 4, self.rect.y,
                                    self.rect.width // 2, self.rect.height // 3)
        down_collision = pygame.Rect(self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 3 * 2,
                                     self.rect.width // 2, self.rect.height // 3)

        collided_walls = pygame.sprite.spritecollide(self, walls, False)

        for wall in collided_walls:
            if wall.rect.colliderect(left_collision) and self.speed[0] < 0:
                self.speed = 0, self.speed[1]
                self.rect.x += 5
            if wall.rect.colliderect(right_collision) and self.speed[0] > 0:
                self.speed = 0, self.speed[1]
                self.rect.x -= 5
            if wall.rect.colliderect(top_collision) and self.speed[1] < 0:
                self.speed = self.speed[0], 0
                self.rect.y += 5
            if wall.rect.colliderect(down_collision) and self.speed[1] > 0:
                self.speed = self.speed[0], 0
                self.rect.y -= 5


class Player(Body):
    def __init__(self, x, y, offset=(0, 0)):
        super().__init__(PLAYER, x=x, y=y, offset=offset)
        self.gun = Gun(x, y, BLOCK_SIZE, offset=offset, player=self)
        self.bullet_sprites = pygame.sprite.Group()
        self.normal_speed = PLAYER_SPEED * BLOCK_SIZE / 10
        self.score = 0
        self.action = None

    def control_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_d]:
            speed_x = 0
        elif keys[pygame.K_a]:
            speed_x = self.normal_speed * (-1)
            self.image = self.image_left
        elif keys[pygame.K_d]:
            speed_x = self.normal_speed
            self.image = self.image_right
        else:
            speed_x = 0
        if keys[pygame.K_w] and keys[pygame.K_s]:
            speed_y = 0
        elif keys[pygame.K_w]:
            speed_y = self.normal_speed * (-1)
        elif keys[pygame.K_s]:
            speed_y = self.normal_speed
        else:
            speed_y = 0
        if keys[pygame.K_r]:
            if not self.action and self.gun.ammo != self.gun.standart_ammo:
                pygame.time.set_timer(RELOAD_EVENT, self.gun.reload_time)
                self.action = RELOAD_EVENT
                # TODO Reload sound
        self.speed = speed_x, speed_y

    def update(self, events, walls=None):
        types = list(map(lambda x: x.type, events))
        if pygame.KEYDOWN in types or pygame.KEYUP in types:
            self.control_player()
        if RELOAD_EVENT in types:
            pygame.time.set_timer(RELOAD_EVENT, 0)
            self.action = None
            self.gun.reload()
        if pygame.MOUSEBUTTONDOWN in types:
            if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                if not self.action:
                    self.gun.fire(events[types.index(pygame.MOUSEBUTTONDOWN)].pos)
        if walls:
            self.check_collision(walls)
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.gun.render(surface)


class EnemyMelee(Body):
    def __init__(self, x, y, offset=(0, 0), room_number=0, groups=None):
        if groups is None:
            groups = []
        self.images = ENEMY_WARRIOR
        # self.speed = True
        super().__init__(self.images, x=x, y=y, offset=offset, groups=groups)
        self.type = 'melee'
        self.image_left = pygame.transform.flip(self.images[0], True, False)
        self.image_right = self.images[0]
        self.standart_image = self.images[0]
        self.hitted_image = self.images[1]
        self.room_number = room_number
        self.player = None

        # mask (hitbox) of player sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.normal_speed = ENEMY_SPEED * BLOCK_SIZE / 10
        self.speed_x = 0
        self.speed_y = 0
        self.speed = self.speed_x, self.speed_y

        self.c = 0
        self.play_hit = False
        self.timer = 0
        self.play_attack = False
        self.time_attack = 0
        self.hit = False

    def attack(self):
        x, y = self.player.rect[:2]
        kx = x - self.rect.x
        ky = y - self.rect.y
        self.punch = pygame.sprite.Sprite()
        self.punch.image = PUNCH[0]
        self.punch.rect = self.punch.image.get_rect()
        self.punch.mask = pygame.mask.from_surface(self.punch.image)
        if self.c != 0:
            if kx != 0:
                self.punch.rect.x = self.rect.x + round(kx / self.c * BLOCK_SIZE) \
                                    + randint(-BLOCK_SIZE / 5, BLOCK_SIZE / 5)
            if ky != 0:
                self.punch.rect.y = self.rect.y + round(ky / self.c * BLOCK_SIZE) \
                                    + randint(-BLOCK_SIZE / 5, BLOCK_SIZE / 5)
        self.hit = True

    def move(self):
        if not self.play_attack:
            vector = self.player.rect[:2]
            kx = vector[0] - self.rect.x
            ky = vector[1] - self.rect.y
            self.c = (kx ** 2 + ky ** 2) ** 0.5
            if self.c > 0:
                self.speed_x = round(kx / self.c * self.normal_speed)
                self.speed_y = round(ky / self.c * self.normal_speed)
            if self.speed_x > 0:
                self.image = self.image_right
            elif self.speed_x < 0:
                self.image = self.image_left
            else:
                if kx < 0:
                    self.image = self.image_left
                elif kx > 0:
                    self.image = self.image_right
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def update(self, *args, walls=None):
        bullets = None
        room = None
        if args:
            bullets, room = args
        if room == self.room_number:
            if self.play_hit:
                self.timer += 1
                if self.timer >= 30:
                    self.play_hit = False
                    self.timer = 0
                    self.image = self.standart_image
            if self.play_attack:
                self.time_attack += 1
                if self.time_attack == 25:
                    self.play_attack = False
                    self.time_attack = 0
                    self.attack()
            group = self.groups()[0].copy()
            for sprite in group:
                if type(sprite) is not EnemyMelee:
                    group.remove(sprite)
            group.remove(self)
            if walls:
                s = self.speed
                self.speed = self.speed_x, self.speed_y
                self.check_collision(walls)
                self.speed = s
            if not pygame.sprite.spritecollideany(self, group):
                if not pygame.sprite.collide_rect(self, self.player):
                    self.move()
                self.speed = True
            elif pygame.sprite.spritecollideany(self, group):
                list_collided = pygame.sprite.spritecollide(self, group, False)
                if self.speed:
                    for s in list_collided:
                        s.speed = False
                    if not pygame.sprite.collide_rect(self, self.player):
                        self.move()
                self.speed = True
            if bullets:
                if pygame.sprite.spritecollide(self, bullets, True):
                    self.image = self.hitted_image
                    self.play_hit = True
                    self.timer = 0
                    self.health -= 20
                    # TODO Sound of hit
            if (abs(self.player.rect.x - self.rect.x)) <= (BLOCK_SIZE * 1.5) and \
                    (abs(self.player.rect.y - self.rect.y)) <= (BLOCK_SIZE * 1.5):
                self.play_attack = True
            if self.hit and pygame.sprite.collide_mask(self.punch, self.player):
                self.punch.kill()
                self.player.health -= 10
            if self.health <= 0:
                self.player.score += 10
                self.kill()

    def render(self, surface):
        if self.hit:
            surface.blit(self.punch.image, (self.punch.rect.x, self.punch.rect.y))
            self.timer += 1
            if self.timer == 1:
                self.hit = False
                self.timer = 0


class EnemyGunner(Body):
    def __init__(self, x, y, offset=(0, 0), room_number=0, groups=None):
        if groups is None:
            groups = []
        self.images = ENEMY_GUNNER
        super().__init__(self.images, x=x, y=y, offset=offset, groups=groups)
        self.type = 'gunner'
        self.image_left = pygame.transform.flip(self.images[0], True, False)
        self.image_right = self.images[0]
        self.standart_image = self.images[0]
        self.hitted_image = self.images[1]
        self.room_number = room_number
        self.player = None
        self.images = ENEMY_GUNNER
        self.gun = Gun(x, y, BLOCK_SIZE, player=self)
        # mask (hitbox) of player sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.normal_speed = ENEMY_SPEED * BLOCK_SIZE / 10
        self.speed_x = 0
        self.speed_y = 0
        self.speed = self.speed_x, self.speed_y
        self.c = 0
        self.play_hit = False
        self.timer = 0
        self.play_attack = False
        self.time_attack = 0
        self.hit = False
        self.action = None

    def attack(self):
        if self.player:
            self.gun.fire(self.player.rect[:2])
        self.hit = True

    def move(self):
        vector = self.player.rect[:2]
        kx = vector[0] - self.rect.x
        ky = vector[1] - self.rect.y
        self.c = (kx ** 2 + ky ** 2) ** 0.5
        if self.c > 0:
            if self.c // BLOCK_SIZE < 5:
                self.speed_x = -round(kx / self.c * self.normal_speed)
                self.speed_y = -round(ky / self.c * self.normal_speed)
            # enemy can move to player while distance with him > 8
            elif self.c // BLOCK_SIZE > 8:
                self.speed_x = round(kx / self.c * self.normal_speed)
                self.speed_y = round(ky / self.c * self.normal_speed)
            else:
                self.speed_x = 0
                self.speed_y = 0
        if self.speed_x > 0:
            self.image = self.image_right
        elif self.speed_x < 0:
            self.image = self.image_left
        else:
            if kx < 0:
                self.image = self.image_left
            elif kx > 0:
                self.image = self.image_right
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def update(self, *args, walls=None):
        if self.play_hit:
            self.timer += 1
            if self.timer >= 20:
                self.play_hit = False
                self.timer = 0
                self.image = self.standart_image
        bullets = None
        room = None
        if args:
            bullets, room = args
        if room == self.room_number:
            group = self.groups()[0].copy()
            for sprite in group:
                if type(sprite) is not EnemyGunner:
                    group.remove(sprite)
            group.remove(self)
            if walls:
                s = self.speed
                self.speed = self.speed_x, self.speed_y
                self.check_collision(walls)
                self.speed = s
            if not pygame.sprite.spritecollideany(self, group):
                if not pygame.sprite.collide_rect(self, self.player):
                    self.move()
                self.speed = True
            elif pygame.sprite.spritecollideany(self, group):
                list_collided = pygame.sprite.spritecollide(self, group, False)
                if self.speed:
                    for s in list_collided:
                        s.speed = False
                    if not pygame.sprite.collide_rect(self, self.player):
                        self.move()
                self.speed = True
            if bullets:
                if pygame.sprite.spritecollide(self, bullets, True):
                    self.image = self.hitted_image
                    self.play_hit = True
                    self.timer = 0
                    self.health -= 20
                    # TODO Sound of hit
            self.time_attack += 1
            if (abs(self.player.rect.x - self.rect.x)) <= (BLOCK_SIZE * 10) and \
                    (abs(self.player.rect.y - self.rect.y)) <= (BLOCK_SIZE * 10) and\
                    not self.action and self.time_attack >= 25:
                self.attack()
                self.time_attack = 0
        if self.health <= 0:
            self.player.score += 10
            self.kill()
        self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    def render(self, surface):
        self.gun.render(surface)


class Gun:
    def __init__(self, x, y, width, height=0, offset=(0, 0), player=None):
        if height == 0:
            height = width
        self.player = player
        self.images = GUN
        self.image = self.images[0]
        self.image_left = pygame.transform.flip(self.images[0], True, False)
        self.image_right = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x * width + offset[0]
        self.rect.y += y * height + offset[1]
        self.w_h = width, height
        self.bullet_sprites = pygame.sprite.Group()
        self.max_range = 750
        self.damage = 30
        self.standart_ammo = 15
        self.ammo = self.standart_ammo
        self.reload_time = 2000

    def reload(self):
        if self.player.images == ENEMY_GUNNER:
            pass
        self.ammo = self.standart_ammo

    def fire(self, mouse_position):
        x, y = self.rect[:2]
        if self.ammo > 0:
            self.ammo -= 1
            Bullet(x, y, BLOCK_SIZE,
                   mouse_pos=mouse_position,
                   group=self.bullet_sprites, player=self.player,
                   max_range=self.max_range, damage=self.damage)
        elif self.player.images == ENEMY_GUNNER:
            self.reload()

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
        self.bullet_sprites.draw(surface)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height=0,
                 mouse_pos=(0, 0),
                 group=None, player=None,
                 max_range=None, damage=0):
        super().__init__(group)
        if height == 0:
            height = width
        self.all_groups = group
        self.player = player
        self.damage = damage

        if self.player.type == 'gunner':
            self.speed = BULLET_SPEED * width / 35
        else:
            self.speed = BULLET_SPEED * width / 10
        if self.player.images == PLAYER:
            self.images = BULLET_PLAYER
        else:
            self.images = BULLET_ENEMY
        # self.images = BULLET_ENEMY
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # mask (hitbox) of bullet sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += x
        self.rect.y += y
        self.vector = mouse_pos
        self.kx = self.vector[0] - self.rect.x + randint(-20, 20)
        self.ky = self.vector[1] - self.rect.y + randint(-20, 20)
        self.c = (self.kx ** 2 + self.ky ** 2) ** 0.5
        self.change_texture = 0
        self.max_range = max_range

    def update(self):
        self.rect.x += int(self.kx / self.c * self.speed)
        self.rect.y += int(self.ky / self.c * self.speed)
        self.change_texture += 1
        if self.change_texture == 10:
            self.image = self.images[self.images.index(self.image) - 1]
            self.change_texture = 0
        distance = (self.rect.x + self.rect.width // 2
                    - self.player.rect.x + self.player.rect.width // 2
                    - BLOCK_SIZE) ** 2 + \
                   (self.rect.y + self.rect.height // 2
                    - self.player.rect.y + self.player.rect.height // 2
                    - BLOCK_SIZE) ** 2
        if distance >= self.max_range ** 2:
            self.kill()
