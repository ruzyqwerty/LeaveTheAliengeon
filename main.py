import pygame
from level import Level
from player import Player
from objects import Object


pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level("m1.txt")
FPS = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    level.render(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()