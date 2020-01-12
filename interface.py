import pygame

LABEL_WIDTH, LABEL_HEIGHT = 400, 70
LABEL_BACKGROUND = (230, 230, 230)
LABEL_FONT_SIZE = 72
LABEL_FONT_COLOR = (0, 0, 0)
LABEL_FRAME_COLOR = (180, 180, 180)
LABEL_FRAME_WIDTH = 10


class Interface:
    def __init__(self, surface):
        self.surface = surface
        self.all_sprites = pygame.sprite.Group()
        self.lblHP = Label('HP: {}'.format('100'), self.all_sprites)
        self.lblScore = Label('Score: {}'.format('0'), self.all_sprites)
        self.lblRoomDone = Label('Room done: {}'.format('0'), self.all_sprites)
        self.lblAmmo = Label('Ammo: {}/{}'.format(0, 0), self.all_sprites)
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.lblScoreX = screen_width // 2 - self.lblScore.rect.width // 2
        self.lblRoomDoneX = screen_width - self.lblRoomDone.rect.width
        self.lblAmmoY = screen_height - self.lblAmmo.rect.height

    def render(self):
        self.all_sprites.draw(self.surface)

    def update(self):
        self.all_sprites.update()
        self.lblScore.rect.x = self.lblScoreX
        self.lblRoomDone.rect.x = self.lblRoomDoneX
        self.lblAmmo.rect.y = self.lblAmmoY


class Label(pygame.sprite.Sprite):
    def __init__(self, text, *groups):
        super().__init__(groups)
        self.text = text
        self.image = self.create()
        self.rect = self.image.get_rect()

    def create(self):
        screen = pygame.Surface((LABEL_WIDTH, LABEL_HEIGHT))
        screen.fill(LABEL_BACKGROUND)
        font = pygame.font.Font(None, LABEL_FONT_SIZE)
        text = font.render(self.text, 1, LABEL_FONT_COLOR)
        text_x = LABEL_WIDTH // 2 - text.get_width() // 2
        text_y = LABEL_HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, LABEL_FRAME_COLOR, (0, 0, LABEL_WIDTH, LABEL_HEIGHT), LABEL_FRAME_WIDTH)
        return screen

    def change_text(self, text):
        if self.text != text:
            self.text = text
            self.image = self.create()
            self.rect = self.image.get_rect()

