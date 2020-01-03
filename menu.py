import pygame
from texture import BUTTONS


class Menu:
    def __init__(self):
        self.buttons_sprite = pygame.sprite.Group()
        self.btn_play = Button('play', groups=(self.buttons_sprite))
        self.btn_settings = Button('settings', groups=(self.buttons_sprite))
        self.btn_exit = Button('exit', groups=(self.buttons_sprite))

    def draw(self, surface):
        self.buttons_sprite.draw(surface)


class Button(pygame.sprite.Sprite):
    def __init__(self, name, groups=None):
        super().__init__(groups)
        self.image = BUTTONS[name]
        self.rect = self.image.get_rect()
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.rect.x += (screen_width // 2 - self.rect.width // 2)
        if name == 'play':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) - self.rect.height
        elif name == 'settings':
            self.rect.y += (screen_height // 2 - self.rect.height // 2)
        elif name == 'exit':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) + self.rect.height