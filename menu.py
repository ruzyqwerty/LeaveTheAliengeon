import pygame


class Menu:
    def __init__(self, surface):
        self.buttons_sprite = pygame.sprite.Group()
        self.btn_play = Button('play', groups=(self.buttons_sprite))
        self.btn_settings = Button('settings', groups=(self.buttons_sprite))
        self.btn_exit = Button('exit', groups=(self.buttons_sprite))
        self.surface = surface

        self.events = []

    def draw(self):
        self.buttons_sprite.draw(self.surface)

    def update(self, events):
        types = list(map(lambda x: x.type, events))
        if pygame.MOUSEBUTTONDOWN in types:
            if events[types.index(pygame.MOUSEBUTTONDOWN)].button == pygame.BUTTON_LEFT:
                x, y = events[types.index(pygame.MOUSEBUTTONDOWN)].pos
                if self.btn_play.rect.collidepoint(x, y):
                    self.events.append('play')
                elif self.btn_settings.rect.collidepoint(x, y):
                    self.events.append('settings')
                elif self.btn_exit.rect.collidepoint(x, y):
                    self.events.append('exit')
        self.draw()


class Button(pygame.sprite.Sprite):
    def __init__(self, name, groups=None):
        super().__init__(groups)
        # self.image = BUTTONS[name]
        self.image = self.create(name)
        self.image = pygame.transform.scale(self.image, (500, 150))
        self.rect = self.image.get_rect()
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.rect.x += (screen_width // 2 - self.rect.width // 2)
        if name == 'play':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) - self.rect.height
        elif name == 'settings':
            self.rect.y += (screen_height // 2 - self.rect.height // 2)
        elif name == 'exit':
            self.rect.y += (screen_height // 2 - self.rect.height // 2) + self.rect.height

    def create(self, text):
        screen = pygame.Surface((1200, 400))
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 400)
        text = font.render(text, 1, (255, 150, 0))
        text_x = 1200 // 2 - text.get_width() // 2
        text_y = 400 // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 10)
        return screen