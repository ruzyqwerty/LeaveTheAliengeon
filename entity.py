import pygame
from texture import PLAYER, ENEMY, GUN, BULLET_PLAYER, BULLET_ENEMY
from settings import BLOCK_SIZE, PLAYER_SPEED, ENEMY_SPEED, BULLET_SPEED


class Body(pygame.sprite.Sprite):
    def __init__(self, texture, x=None, y=None, offset=(0, 0), groups=None):
        if groups is None:
            groups = []
        super().__init__(groups)
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

        self.health = 100


class Player(Body):
    def __init__(self, x, y, offset=(0, 0)):
        super().__init__(PLAYER, x=x, y=y, offset=offset)
        self.gun = Gun(x, y, BLOCK_SIZE, offset=offset, player=self)
        self.bullet_sprites = pygame.sprite.Group()
        self.normal_speed = PLAYER_SPEED * BLOCK_SIZE / 10
        self.score = 0

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
            self.gun.reload()
        self.speed = speed_x, speed_y

    def update(self, events):
        types = list(map(lambda x: x.type, events))
        if pygame.KEYDOWN in types or pygame.KEYUP in types:
            self.control_player()
        if pygame.MOUSEBUTTONDOWN in types:
            if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                self.gun.fire(events[types.index(pygame.MOUSEBUTTONDOWN)].pos)
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.gun.render(surface)



class Enemy(Body):
    def __init__(self, x, y, offset=(0, 0), room_number=0, groups=None, shooting_enemy=False):
        if groups is None:
            groups = []
        self.images = ENEMY
        super().__init__(ENEMY, x=x, y=y, offset=offset, groups=groups)
        self.room_number = room_number
        self.player = None
        self.shooting_enemy = shooting_enemy
        if self.shooting_enemy:
            self.gun = Gun(x, y, BLOCK_SIZE, offset=offset, player=self)
        self.bullet_sprites = pygame.sprite.Group()
        # mask (hitbox) of player sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.normal_speed = ENEMY_SPEED * BLOCK_SIZE / 10

    def move(self):
        vector = self.player.rect[:22]
        kx = vector[0] - self.rect.x
        ky = vector[1] - self.rect.y
        c = (kx ** 2 + ky ** 2) ** 0.5
        if c > 0:
            self.rect.x += round(kx / c * self.normal_speed)
            self.rect.y += round(ky / c * self.normal_speed)

    def update(self, *args):
        bullets = None
        room = None
        if args:
            bullets, room = args
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if room == self.room_number:
            self.move()
            if bullets:
                if pygame.sprite.spritecollideany(self, bullets):
                    self.health -= 20
        if self.health <= 0:
            self.player.score += 10
            self.kill()
        if self.shooting_enemy:
            self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    # def fire(self, mouse_positon):
    #     self.gun.fire(mouse_positon)


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

    def reload(self):
        self.ammo = self.standart_ammo

    def fire(self, mouse_position):
        x, y = self.rect[:2]
        if self.ammo > 0:
            self.ammo -= 1
            Bullet(x, y, BLOCK_SIZE,
                   colorkey=-1, mouse_pos=mouse_position,
                   group=self.bullet_sprites, player=self.player,
                   max_range=777, damage=self.damage)

    def on_hand(self):
        x, y = self.rect[:2]
        return x, y

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
                 mouse_pos=(0, 0), colorkey=None,
                 group=None, player=None,
                 max_range=None, damage=0):
        super().__init__(group)
        if height == 0:
            height = width
        self.all_groups = [group]
        self.player = player
        self.damage = damage
        self.speed = BULLET_SPEED * width / 10
        # self.speed = BULLET_SPEED
        self.images = BULLET_PLAYER
        # self.images = BULLET_ENEMY
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # mask (hitbox) of bullet sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += x
        self.rect.y += y
        self.vector = mouse_pos
        self.kx = self.vector[0] - self.rect.x
        self.ky = self.vector[1] - self.rect.y
        self.c = (self.kx ** 2 + self.ky ** 2) ** 0.5
        self.change_texture = 0
        self.max_range = max_range

    def check_hit(self, object_rect):
        if self.rect.colliderect(object_rect):
            return True
        return False

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
