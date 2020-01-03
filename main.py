import pygame
from settings import WINDOW_SIZE, FULLSCREEN, FPS

pygame.init()

if FULLSCREEN:
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode(WINDOW_SIZE)

from level import Level
from menu import Menu

from texture import AIM

all_sprites = pygame.sprite.Group()
cursor = pygame.sprite.Sprite()
cursor.image = AIM[0]
cursor.rect = cursor.image.get_rect()
all_sprites.add(cursor)

screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level(5, screen)

on_pause = False
start_menu = True
menu = Menu(screen)

running = True
while running:
    screen.fill((255, 255, 255))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not start_menu:
            on_pause = not on_pause
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(0)
            cursor.rect.x = pygame.mouse.get_pos()[0]
            cursor.rect.y = pygame.mouse.get_pos()[1]

    if on_pause or start_menu:
        menu.update(events)
        if 'exit' in menu.events:
            menu.events.remove('exit')
            running = False
        if 'play' in menu.events:
            menu.events.remove('play')
            start_menu = False
            on_pause = False
        if 'new game' in menu.events:
            level = Level(5, screen)
            on_pause = False
    else:
        level.update(events)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
