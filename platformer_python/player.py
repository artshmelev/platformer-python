# -*- coding: utf-8 -*-

import pygame

from platformer_python.blocks import DangerousBlock
from platformer_python.blocks import Princess
from platformer_python.constants import *
from platformer_python.pyganim import PygAnimation

IMGS = [pygame.image.load(path) for path in IMGS_PATH]

ANIMATION_RIGHT = [IMGS_PATH[i] for i in range(4, 9)]
ANIMATION_LEFT = [IMGS_PATH[i] for i in range(9, 14)]
ANIMATION_JUMP_LEFT = [(IMGS_PATH[2], 0.1)]
ANIMATION_JUMP_RIGHT = [(IMGS_PATH[3], 0.1)]
ANIMATION_JUMP = [(IMGS_PATH[1], 0.1)]
ANIMATION_STAY = [(IMGS_PATH[0], 0.1)]


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Player, self).__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.start_x = x
        self.start_y = y
        self.on_ground = False
        self.winner = False
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(SPRITE_COLOR)
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image.set_colorkey(SPRITE_COLOR)

        bolt_anim = []
        for anim in ANIMATION_RIGHT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.anim_right = PygAnimation(bolt_anim)
        self.anim_right.play()

        bolt_anim = []
        for anim in ANIMATION_LEFT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.anim_left = PygAnimation(bolt_anim)
        self.anim_left.play()

        self.anim_stay = PygAnimation(ANIMATION_STAY)
        self.anim_stay.play()
        self.anim_stay.blit(self.image, (0, 0))

        self.anim_jump_l = PygAnimation(ANIMATION_JUMP_LEFT)
        self.anim_jump_l.play()
        self.anim_jump_r = PygAnimation(ANIMATION_JUMP_RIGHT)
        self.anim_jump_r.play()
        self.anim_jump = PygAnimation(ANIMATION_JUMP)
        self.anim_jump.play()

        self.cur_frame = 0

    def update(self, left, right, up, platforms):
        if up:
            if self.on_ground:
                self.y_vel = -JUMP_POWER
            self.image.fill(SPRITE_COLOR)
            self.anim_jump.blit(self.image, (0, 0))
            self.cur_frame = 1
        if left:
            self.x_vel = -MOVE_SPEED
            self.image.fill(SPRITE_COLOR)
            if up:
                self.anim_jump_l.blit(self.image, (0, 0))
                self.cur_frame = 2
            else:
                self.anim_left.blit(self.image, (0, 0))
                self.cur_frame = 9 + self.anim_left._propGetCurrentFrameNum()
        if right:
            self.x_vel = MOVE_SPEED
            self.image.fill(SPRITE_COLOR)
            if up:
                self.anim_jump_r.blit(self.image, (0, 0))
                self.cur_frame = 3
            else:
                self.anim_right.blit(self.image, (0, 0))
                self.cur_frame = 4 + self.anim_right._propGetCurrentFrameNum()
        if not (left or right):
            self.x_vel = 0
            if not up:
                self.image.fill(SPRITE_COLOR)
                self.anim_stay.blit(self.image, (0, 0))
                self.cur_frame = 0

        if not self.on_ground:
            self.y_vel += GRAVITY
        self.on_ground = False

        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)
        self.rect.x += self.x_vel
        self.collide(self.x_vel, 0, platforms)

    def collide(self, x_vel, y_vel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_vel > 0:
                    self.rect.right = p.rect.left
                if x_vel < 0:
                    self.rect.left = p.rect.right
                if y_vel > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.y_vel = 0
                if y_vel < 0:
                    self.rect.top = p.rect.bottom
                    self.y_vel = 0
                if isinstance(p, Princess):
                    self.winner = True
                if isinstance(p, DangerousBlock):
                    self.die()

    def die(self):
        self.teleport(self.start_x, self.start_y)

    def teleport(self, x, y):
        self.__init__(x, y)
