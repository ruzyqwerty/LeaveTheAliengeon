import pygame
from level import Level

size = width, height = (600, 400)


pygame.init()
# screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
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
        # TODO На Esc можно сделать смену режима окна (полный/неполный экран), я не придумал как чтобы все работало
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #     pygame.display.set_mode(size, flags=pygame.RESIZABLE)

    level.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
