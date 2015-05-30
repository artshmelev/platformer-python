#!/usr/bin/python -O
# -*- coding: utf-8 -*-

import sys
import time
import pygame
from pygame.locals import *

from platformer_python.blocks import Platform
from platformer_python.blocks import DangerousBlock
from platformer_python.blocks import Princess
from platformer_python.camera import camera_configure
from platformer_python.camera import Camera
from platformer_python.constants import *
from platformer_python.helperspygame import RendererPygame
from platformer_python.helperspygame import ResourceLoaderPygame
from platformer_python.helperspygame import get_layers_from_map
from platformer_python.net.connection import ConnectionListener
from platformer_python.net.connection import connection
from platformer_python.player import Player
from platformer_python.player import IMGS
from platformer_python.tmxreader import TileMapParser


entities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platforms = []


class NetworkListener(ConnectionListener):

    def Network_connected(self, data):
        print 'connected to the server'

    def Network_error(self, data):
        print 'error:', data['error']

    def Network_disconnected(self, data):
        print 'disconnected from the server'

    def Network_startgame(self, data):
        print 'start game'
        global running
        running = True

    def Network_endgame(self, data):
        print 'end game'
        global running
        running = False

    def Network_gethero(self, data):
        global hero1
        if hero1:
            hero1.rect.x = data['left']
            hero1.rect.y = data['top']
            hero1.cur_frame = data['cur_frame']

    def Network_getwinner(self, data):
        global hero1
        hero1.winner = True


def main():
    global SCREEN, FPSCLOCK, BASICFONT, running, listener, hero1
    hero1 = None

    listener = NetworkListener()
    addr = raw_input('Enter host:port (or just type ENTER): ')
    if addr == '':
        listener.connect(('localhost', 8000))
    else:
        addr = addr.split(':')
        if len(addr) != 2:
            terminate()
        listener.connect((addr[0], int(addr[1])))

    pygame.init()
    # pygame.time.wait(2000)
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Platformer Game')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    running = False

    while True:
        while not running:
            connection.pump()
            listener.pump()
            waiting_screen()
        run_game()


def run_game():
    global hero1
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.load(GAME_MUSIC_PATH)
    pygame.mixer.music.play(-1)

    renderer0 = RendererPygame()
    renderer1 = RendererPygame()

    screen0 = pygame.Surface((WIDTH, VIEW_HEIGHT))
    screen1 = pygame.Surface((WIDTH, VIEW_HEIGHT))
    move_left = move_right = False
    move_up = False

    player_x, player_y, total_level_w, total_level_h, sprite_layers = \
                                                        load_level('map01.tmx')
    hero0 = Player(player_x, player_y)
    hero1 = Player(player_x, player_y)

    camera0 = Camera(camera_configure, total_level_w, total_level_h)
    camera1 = Camera(camera_configure, total_level_w, total_level_h)

    while True:
        connection.pump()
        listener.pump()
        if not running:
            pygame.mixer.music.stop()
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_left = True
                elif event.key == K_RIGHT:
                    move_right = True
                elif event.key == K_UP:
                    move_up = True
                elif event.key == K_ESCAPE:
                    terminate()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    move_left = False
                elif event.key == K_RIGHT:
                    move_right = False
                elif event.key == K_UP:
                    move_up = False

        if hero0.winner or hero1.winner:
            if hero0.winner:
                listener.send({'action': 'sendwinner'})
                connection.pump()
            pygame.mixer.music.stop()
            pygame.mixer.music.load(VICTORY_MUSIC_PATH)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                FPSCLOCK.tick(FPS)
            return

        SCREEN.fill(RED)
        screen0.fill(BG_COLOR)
        screen1.fill(BG_COLOR)

        hero0.update(move_left, move_right, move_up, platforms)
        listener.send({
            'action': 'sendhero',
            'left': hero0.rect.x,
            'top': hero0.rect.y,
            'cur_frame': hero0.cur_frame
        })

        camera0.update(hero0)
        camera1.update(hero1)

        center_offset0 = camera0.reverse((HALF_WIDTH, VIEW_HEIGHT/2))
        center_offset1 = camera1.reverse((HALF_WIDTH, VIEW_HEIGHT/2))

        renderer0.set_camera_position_and_size(
            center_offset0[0], center_offset0[1],
            WIDTH, VIEW_HEIGHT, 'center'
        )
        renderer1.set_camera_position_and_size(
            center_offset1[0], center_offset1[1],
            WIDTH, VIEW_HEIGHT, 'center'
        )

        for layer in sprite_layers:
            if not layer.is_object_group:
                renderer0.render_layer(screen0, layer)
                renderer1.render_layer(screen1, layer)

        for e in entities:
            screen0.blit(e.image, camera0.apply(e))
            screen1.blit(e.image, camera1.apply(e))

        screen0.blit(IMGS[hero0.cur_frame], camera0.apply(hero0))
        screen1.blit(IMGS[hero1.cur_frame], camera1.apply(hero1))

        SCREEN.blit(screen0, (0, 0))
        SCREEN.blit(screen1, (0, VIEW_HEIGHT + 10))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def load_level(filename):
    path = os.path.join(GRAPHICS_PATH, filename)
    world_map = TileMapParser().parse_decode(path)
    resources = ResourceLoaderPygame()
    resources.load(world_map)

    sprite_layers = get_layers_from_map(resources)
    platforms_layer = sprite_layers[1]
    dang_blocks_layer = sprite_layers[2]
    monsters_layer = sprite_layers[3]

    for row in xrange(platforms_layer.num_tiles_x):
        for col in xrange(platforms_layer.num_tiles_y):
            if platforms_layer.content2D[col][row] is not None:
                pf = Platform(row*PLATFORM_WIDTH, col*PLATFORM_HEIGHT)
                platforms.append(pf)

    for row in xrange(dang_blocks_layer.num_tiles_x):
        for col in xrange(dang_blocks_layer.num_tiles_y):
            if dang_blocks_layer.content2D[col][row] is not None:
                db = DangerousBlock(row*PLATFORM_WIDTH, col*PLATFORM_HEIGHT)
                platforms.append(db)

    player_x = player_y = None
    for monster in monsters_layer.objects:
        x = monster.x
        y = monster.y
        if monster.name == 'Player':
            player_x = x
            player_y = y - PLATFORM_HEIGHT
        if monster.name == 'Princess':
            pr = Princess(x, y-PLATFORM_HEIGHT)
            platforms.append(pr)
            entities.add(pr)

    total_level_w = platforms_layer.num_tiles_x * PLATFORM_WIDTH
    total_level_h = platforms_layer.num_tiles_y * PLATFORM_HEIGHT
    return (player_x, player_y, total_level_w, total_level_h, sprite_layers)


def waiting_screen():
    t = (round(time.time(), 1) * 10) % 10
    if t in (0, 1, 2):
        text = 'Waiting other player .    '
    elif t in (3, 4, 5):
        text = 'Waiting other player . .  '
    else:
        text = 'Waiting other player . . .'

    text_surf = BASICFONT.render(text, 1, FONT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = (HALF_WIDTH, HALF_HEIGHT)

    SCREEN.fill(WAITING_BG_COLOR)
    SCREEN.blit(text_surf, text_rect)

    for event in pygame.event.get():
        if event.type == QUIT or \
           event.type == KEYDOWN and event.key == K_ESCAPE:
            terminate()

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
