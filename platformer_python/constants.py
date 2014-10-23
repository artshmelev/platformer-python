# -*- coding: utf-8 -*-

import os

FPS = 60

WIDTH = 1366
HEIGHT = 768
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
VIEW_HEIGHT = HALF_HEIGHT - 5

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

PLAYER_WIDTH = 22
PLAYER_HEIGHT = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BRIGHTBLUE = (0, 170, 255)

BG_COLOR = BRIGHTBLUE
WAITING_BG_COLOR = BLACK
FONT_COLOR = WHITE

SPRITE_COLOR = (136, 136, 136)

MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35

ANIMATION_DELAY = 0.1

ROOT_FOLDER = os.path.dirname(__file__)
GRAPHICS_PATH = os.path.join(ROOT_FOLDER, 'graphics')
PRINCESS_PATH = os.path.join(GRAPHICS_PATH, 'princess_l.png')
SOUNDS_PATH = os.path.join(ROOT_FOLDER, 'sounds')
GAME_MUSIC_PATH = os.path.join(SOUNDS_PATH, 'SuperMarioBrosFull.mp3')
VICTORY_MUSIC_PATH = os.path.join(SOUNDS_PATH, 'StageClear.mp3')

IMGS_PATH = [
    os.path.join(GRAPHICS_PATH, '0.png'),
    os.path.join(GRAPHICS_PATH, 'j.png'),
    os.path.join(GRAPHICS_PATH, 'jl.png'),
    os.path.join(GRAPHICS_PATH, 'jr.png'),
    os.path.join(GRAPHICS_PATH, 'r1.png'),
    os.path.join(GRAPHICS_PATH, 'r2.png'),
    os.path.join(GRAPHICS_PATH, 'r3.png'),
    os.path.join(GRAPHICS_PATH, 'r4.png'),
    os.path.join(GRAPHICS_PATH, 'r5.png'),
    os.path.join(GRAPHICS_PATH, 'l1.png'),
    os.path.join(GRAPHICS_PATH, 'l2.png'),
    os.path.join(GRAPHICS_PATH, 'l3.png'),
    os.path.join(GRAPHICS_PATH, 'l4.png'),
    os.path.join(GRAPHICS_PATH, 'l5.png'),
]
