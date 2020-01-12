import pygame
from settings import WINDOW_SIZE, FULLSCREEN, FPS, ROOMS_COUNT


def update_data():
    interface.lblHP.text = 'HP: {}'.format(level.player.health)
    interface.lblScore.text = 'Score: {}'.format(level.player.score)
    interface.lblRoomDone.text = 'Room done: {}'.format(level.room_done)
    interface.lblAmmo.text = 'Ammo: {}/{}'.format(level.player.gun.ammo, level.player.gun.standart_ammo)


pygame.init()

if FULLSCREEN:
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode(WINDOW_SIZE)

from level import Level
from menu import Menu
from interface import Interface

from texture import AIM

all_sprites = pygame.sprite.Group()
cursor = pygame.sprite.Sprite()
cursor.image = AIM[0]
cursor.rect = cursor.image.get_rect()
all_sprites.add(cursor)

rooms_count = ROOMS_COUNT
last_fullscreen = FULLSCREEN
MAX_WIN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h

screen.fill((255, 255, 255))
clock = pygame.time.Clock()
level = Level(rooms_count, screen)

on_pause = False
start_menu = True
menu = Menu(screen)
interface = Interface(screen)

running = True
while running:
    screen.fill((255, 255, 255))
    # TODO Back music
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
        if menu.settings.fullscreen != last_fullscreen:
            last_fullscreen = menu.settings.fullscreen
            if menu.settings.fullscreen:
                screen = pygame.display.set_mode(MAX_WIN_SIZE)
                screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.RESIZABLE)
            else:
                screen = pygame.display.set_mode(WINDOW_SIZE)
            for sprite in menu.buttons_sprites:
                sprite.change_name(sprite.text)
            for sprite in menu.setting_sprites:
                sprite.change_name(sprite.text)
            menu.surface = screen
            interface.surface = screen
            level.surface = screen
        if 'exit' in menu.events:
            menu.events.remove('exit')
            running = False
        if 'play' in menu.events:
            menu.events.remove('play')
            start_menu = False
            on_pause = False
        if 'new game' in menu.events:
            menu.events.remove('new game')
            level = Level(rooms_count, screen)
            on_pause = False
        menu.render()
    else:
        if level.isLevelEnd:
            player = level.player
            room_done = level.room_done
            rooms_count += 1
            level = Level(rooms_count, screen, player)
            level.room_done = room_done
        level.update(events)
        update_data()
        interface.update()
        level.render()
        interface.render()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
