# -*- coding: utf-8 -*-

import pygame

from platformer_python.constants import PLATFORM_WIDTH
from platformer_python.constants import PLATFORM_HEIGHT
from platformer_python.constants import PRINCESS_PATH


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Platform, self).__init__()
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class DangerousBlock(Platform):

    def __init__(self, x, y):
        super(DangerousBlock, self).__init__(x, y)


class Princess(Platform):

    def __init__(self, x, y):
        super(Princess, self).__init__(x, y)
        self.image = pygame.image.load(PRINCESS_PATH)
