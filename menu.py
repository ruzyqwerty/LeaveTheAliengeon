import pygame
from settings import FULLSCREEN

LABEL_WIDTH, LABEL_HEIGHT = 1200, 250
LABEL_BACKGROUND = (255, 255, 255)
LABEL_FONT_SIZE = 210
LABEL_FONT_COLOR = (255, 200, 0)
LABEL_FRAME_COLOR = (255, 150, 150)
LABEL_FRAME_WIDTH = 30
CLICK_SOUND = pygame.mixer.Sound('click.wav')


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.events = []

        self.buttons_sprites = pygame.sprite.Group()
        self.setting_sprites = pygame.sprite.Group()

        self.btn_play = Button(self.buttons_sprites, name='Play')
        self.btn_settings = Button(self.buttons_sprites, name='Settings')
        self.btn_exit = Button(self.buttons_sprites, name='Exit')
        self.btn_continue = Button(name='Continue')

        self.settings = Settings()
        self.setting_sprites.add(self.settings.buttons_sprites)

        self.settings_on = False
        self.game_on_pause = False

    def render(self):
        if not self.settings_on:
            self.buttons_sprites.draw(self.surface)
        else:
            self.setting_sprites.draw(self.surface)

    def update(self, events):
        if not self.settings_on:
            types = list(map(lambda x: x.type, events))
            if pygame.MOUSEBUTTONDOWN in types:
                CLICK_SOUND.play()
                if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                    x, y = events[types.index(pygame.MOUSEBUTTONDOWN)].pos
                    if not self.game_on_pause and self.btn_play.rect.collidepoint(x, y):
                        self.events.append('play')
                        self.btn_play.change_name('New game')
                        self.game_on_pause = True
                        self.buttons_sprites.add(self.btn_continue)
                    elif self.game_on_pause:
                        if self.btn_continue.rect.collidepoint(x, y):
                            self.events.append('play')
                        elif self.btn_play.rect.collidepoint(x, y):
                            self.events.append('new game')
                    if self.btn_settings.rect.collidepoint(x, y):
                        self.settings_on = True
                    elif self.btn_exit.rect.collidepoint(x, y):
                        self.events.append('exit')
        else:
            if self.settings.update(events):
                self.settings_on = False


class Settings:
    def __init__(self):
        self.events = []

        self.buttons_sprites = pygame.sprite.Group()

        self.btn_settings_fullscreen = Button(self.buttons_sprites, name='Fullscreen - On')
        self.btn_back = Button(self.buttons_sprites, name='Back')
        self.fullscreen = FULLSCREEN

        if self.fullscreen:
            self.btn_settings_fullscreen.change_name('Fullscreen - On')
        else:
            self.btn_settings_fullscreen.change_name('Fullscreen - Off')

    def update(self, events):
        types = list(map(lambda x: x.type, events))
        if pygame.MOUSEBUTTONDOWN in types:
            CLICK_SOUND.play()
            if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                x, y = events[types.index(pygame.MOUSEBUTTONDOWN)].pos
                if self.btn_settings_fullscreen.rect.collidepoint(x, y):
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.btn_settings_fullscreen.change_name('Fullscreen - On')
                    else:
                        self.btn_settings_fullscreen.change_name('Fullscreen - Off')
                elif self.btn_back.rect.collidepoint(x, y):
                    return True
        return False


class Button(pygame.sprite.Sprite):
    def __init__(self, *groups, name=None):
        super().__init__(groups)
        self.text = None

        self.change_name(name)

    def create(self):
        screen = pygame.Surface((LABEL_WIDTH, LABEL_HEIGHT))
        screen.fill(LABEL_BACKGROUND)
        font = pygame.font.Font(None, LABEL_FONT_SIZE)
        text = font.render(self.text, 1, LABEL_FONT_COLOR)
        text_x = LABEL_WIDTH // 2 - text.get_width() // 2
        text_y = LABEL_HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, LABEL_FRAME_COLOR, (
        text_x - LABEL_FRAME_WIDTH, text_y - LABEL_FRAME_WIDTH, text_w + LABEL_FRAME_WIDTH * 2,
        text_h + LABEL_FRAME_WIDTH * 2), LABEL_FRAME_WIDTH)
        return screen

    def correct_buttons(self):
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.rect.x += (screen_width // 2 - self.rect.width // 2)
        if self.text.lower() == 'continue':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) - self.rect.height * 1.5
        elif self.text.lower() == 'play' or self.text.lower() == 'new game' or self.text.lower().startswith(
                'fullscreen'):
            self.rect.y += (screen_height // 2 - self.rect.height // 2) - self.rect.height * 0.5
        elif self.text.lower() == 'settings':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) + self.rect.height - self.rect.height * 0.5
        elif self.text.lower() == 'exit' or self.text.lower() == 'back':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) + self.rect.height * 2 - self.rect.height * 0.5

    def change_name(self, name):
        if name != self.text:
            self.text = name
            self.image = self.create()
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.75), int(screen_height * 0.25)))
        self.rect = self.image.get_rect()

        self.correct_buttons()
