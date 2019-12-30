import pygame
from texture import PLAYER, ENEMY, GUN, BULLET_PLAYER, BULLET_ENEMY
from settings import BLOCK_SIZE, PLAYER_SPEED, ENEMY_SPEED, BULLET_SPEED


class Body:
    def __init__(self, texture, x=None, y=None, offset=(0, 0)):
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

    # def update(self):
    #     self.rect.x += self.speed[0]
    #     self.rect.y += self.speed[1]
    #     pass

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Player(Body):
    def __init__(self, x, y, offset=(0, 0)):
        super().__init__(PLAYER, x=x, y=y, offset=offset)
        self.gun = Gun(x, y, BLOCK_SIZE, offset=offset, player=self)
        self.bullet_sprites = pygame.sprite.Group()
        self.normal_speed = PLAYER_SPEED * BLOCK_SIZE / 10

    def normalize_speed(self):
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
        self.speed = speed_x, speed_y

    def update(self, events):
        # super().update()
        types = list(map(lambda x: x.type, events))
        if pygame.KEYDOWN in types or pygame.KEYUP in types:
            self.normalize_speed()
        if pygame.MOUSEBUTTONDOWN in types:
            if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                self.fire(events[types.index(pygame.MOUSEBUTTONDOWN)].pos)
        # super().update(events)
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    def render(self, surface):
        super().render(surface)
        # surface.blit(self.image, (self.rect.x, self.rect.y))
        self.gun.render(surface)

    def fire(self, mouse_positon):
        self.gun.fire(mouse_positon)


class Enemy(Body):
    def __init__(self, x, y, offset=(0, 0)):
        self.images = ENEMY
        super().__init__(ENEMY, x=x, y=y, offset=offset)
        # self.image = self.images[0]
        # self.image_left = pygame.transform.flip(self.images[0], True, False)
        # self.image_right = self.images[0]
        # self.rect = self.image.get_rect()
        # self.rect.x += x * BLOCK_SIZE + offset[0]
        # self.rect.y += y * BLOCK_SIZE + offset[1]
        # self.gun = Gun(x, y, BLOCK_SIZE, offset=offset, player=self)
        self.bullet_sprites = pygame.sprite.Group()
        # mask (hitbox) of player sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.normal_speed = ENEMY_SPEED * BLOCK_SIZE / 10
        # self.normal_speed = PLAYER_SPEED

    def update(self):
        # super().update()
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        # self.gun.update(self.rect.x, self.rect.y, self.image == self.image_right)

    def render(self, surface):
        super().render(surface)
        # surface.blit(self.image, (self.rect.x, self.rect.y))
        # self.gun.render(surface)
        pass

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

    def fire(self, mouse_position):
        x, y = self.rect[:2]
        Bullet(x, y, BLOCK_SIZE, colorkey=-1, mouse_pos=mouse_position, group=self.bullet_sprites, player=self.player, max_range=750)

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
    def __init__(self, x, y, width, height=0, offset=(0, 0), mouse_pos=(0, 0), colorkey=None, group=None, player=None, max_range=None):
        super().__init__(group)
        if height == 0:
            height = width
        self.all_groups = [group]
        self.player = player
        self.speed = BULLET_SPEED * width / 10
        # self.speed = BULLET_SPEED
        self.images = BULLET_PLAYER
        # self.images = BULLET_ENEMY
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # mask (hitbox) of bullet sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += x  # * width - offset[0]
        self.rect.y += y  # * height - offset[1]
        self.vector = mouse_pos
        self.kx = self.vector[0] - self.rect.x
        self.ky = self.vector[1] - self.rect.y
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
        distance = (self.rect.x + self.rect.width // 2 - self.player.rect.x + self.player.rect.width // 2) ** 2 + (self.rect.y + self.rect.height // 2 - self.player.rect.y + self.player.rect.height // 2) ** 2
        if distance >= self.max_range ** 2:
            self.kill()

