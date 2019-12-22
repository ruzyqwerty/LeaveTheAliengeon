from texture import GUN


class Gun:
    def __init__(self, x, y, width, height=0, offset=(0, 0), colorkey=None):
        if height == 0:
            height = width
        self.bullet_speed = 1
        self.images = GUN
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x += x * width + offset[0]
        self.rect.y += y * height + offset[1]

    # def on_hand(self):
    #     pass

    def is_fire(self, mouse_click):
        pass

    def update(self, player_x, player_y):
        self.rect.x = player_x
        self.rect.y = player_y

    def render(self, surface):
        surface.blit(self.image, (self.rect.x + 12, self.rect.y + 8))
