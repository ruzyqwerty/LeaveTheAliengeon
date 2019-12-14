import pygame
from level import Level


pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level(10, screen)
FPS = 60
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    level.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
