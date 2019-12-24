import pygame
from settings import WINDOW_SIZE, FULLSCREEN, FPS

pygame.init()
if FULLSCREEN:
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode(WINDOW_SIZE)

from level import Level

from texture import AIM

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = AIM[0]
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)

screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level(2, screen)
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(0)
            sprite.rect.x = pygame.mouse.get_pos()[0]
            sprite.rect.y = pygame.mouse.get_pos()[1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                level.fire(event.pos, level.gun.rect[:2])
        # TODO На Esc можно сделать смену режима окна (полный/неполный экран), я не придумал как чтобы все работало
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #     pygame.display.set_mode(size, flags=pygame.RESIZABLE)

    level.update()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
