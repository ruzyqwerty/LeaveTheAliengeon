import pygame
from settings import WINDOW_SIZE, FULLSCREEN, FPS

pygame.init()
if FULLSCREEN:
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode(WINDOW_SIZE)

from level import Level

screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level(5, screen)
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # TODO На Esc можно сделать смену режима окна (полный/неполный экран), я не придумал как чтобы все работало
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #     pygame.display.set_mode(size, flags=pygame.RESIZABLE)

    level.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
