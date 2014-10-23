# -*- coding: utf-8 -*-

import pygame


from platformer_python.constants import WIDTH
from platformer_python.constants import HALF_WIDTH
from platformer_python.constants import VIEW_HEIGHT


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + HALF_WIDTH, -t + VIEW_HEIGHT/2

    l = min(0, l)
    l = max(-camera.width + WIDTH, l)
    t = max(-camera.height + VIEW_HEIGHT, t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)


class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):
        return pos[0] - self.state.left, pos[1] - self.state.top
