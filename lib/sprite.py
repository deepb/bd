#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: sprite.py $Id$
date: $Date$
"""

import pygame as gm

import random

from locals import *

class miSprite(gm.sprite.Sprite):

    def __init__(self, coord, imagen, animaciones=6, ancho=32, alto=64):

        self.tile = imagen
        self._ancho = ancho
        self._alto = alto
        self.arrayAnim = []
        # _maxAnim es el numero de animaciones que tengo en la imagen
        self._maxAnim = animaciones
        # dir es la direccion: abajo,arriba,der,izq
        for dir in range(4):
            # anim es el numero de animaciones
            for anim in range(self._maxAnim):
                self.arrayAnim.append(self.tile.subsurface(\
                    (anim*self._ancho, dir*self._alto, \
                    self._ancho, self._alto)))
        self.anim = 0
        self.vx = 0
        self.vy = 0
        
        self.image = self.arrayAnim[self.anim]
        self.rect = self.image.get_rect()
        self.rect.center = coord
        
    def checkCoord(self, coord):
        if coord[0] < self._ancho/2:
            coord[0] = self._ancho/2
            self.anim = 0
        elif coord[0] > ANCHO - self._ancho/2:
            coord[0] = ANCHO - self._ancho/2
            self.anim = 0            
        
        if coord[1] < self._alto/2:
            coord[1] = self._alto/2
            self.anim = 0
        elif coord[1] > ALTO - self._alto/2:
            coord[1] = ALTO - self._alto/2
            self.anim = 0
        
        return coord
        
    def update(self, coord, dir=0):
        self.rect.center = coord
        if dir:
            self.anim += 1
            if self.anim > self._maxAnim:
                self.anim = 1
            pos = (dir - 1) * self._maxAnim
            self.image = self.arrayAnim[(self.anim - 1) + pos]

class miSpriteRandom(miSprite):

    def __init__(self, coord, imagen, ancho=32, alto=32):
        self._ancho = ancho
        self._alto = alto
        self.vx = 0
        self.vy = 0
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.center = coord
         
    def checkRandom(self, coord):
        if coord[0] < self._ancho/2:
            coord[0] = self._ancho/2
            self.vx = - self.vx 
        elif coord[0] > ANCHO - self._ancho/2:
            coord[0] = ANCHO - self._ancho/2
            self.vx = - self.vx 
        
        if coord[1] < self._alto/2:
            coord[1] = self._alto/2
            self.vy = - self.vy 
        elif coord[1] > ALTO - self._alto/2:
            coord[1] = ALTO - self._alto/2
            self.vy = - self.vy 
        
        return coord

    def randomVel(self):
        self.vx = random.randrange(-RANDOM_SPEED, RANDOM_SPEED)
        self.vy = random.randrange(-RANDOM_SPEED, RANDOM_SPEED)
