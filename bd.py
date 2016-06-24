#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: bd.py $Id$
date: $Date$
"""

# Importar print como funcion
from __future__ import print_function

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pygame
from pygame.locals import *

import sys

WIDTH = 600
HEIGHT = 400
WINDOW = (WIDTH, HEIGHT)

def main():

    pygame.init()

    Reloj= pygame.time.Clock()

    Ventana = pygame.display.set_mode(WINDOW)
    pygame.display.set_caption("bd Clone")

    Fondo = pygame.image.load("res/fondo.jpg")

    imgHeroe = pygame.image.load("res/sprite.png")
    imgArena = pygame.image.load("res/desert.png")
    
    #trans = imgHeroe.get_at((0, 0))
    #Imagen.set_colorkey(trans)
    
    hX = 300
    hY = 300
    hC = (hX, hY)
    incX = 0
    incY = 0
    pos = 0
    
    Heroe = miSprite(hC, imgHeroe, 6)
    arrayArena = []
    for i in range(5):
        arrayArena.append(miSprite((i*128 + 32, 200), imgArena, 1, 32, 32))

    while True:

        Ventana.blit(Fondo, (0, 0))
        Ventana.blit(Heroe.image, Heroe.rect)
        for i in range(5):
            Ventana.blit(arrayArena[i].image, arrayArena[i].rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                #key = pygame.key.get_pressed()
                if evento.key == pygame.K_ESCAPE:
                    sys.exit()
                elif evento.key == pygame.K_RIGHT:
                    incX = 5
                    pos = 4
                elif evento.key == pygame.K_DOWN:
                    incY = 5
                    pos = 1
                elif evento.key == pygame.K_LEFT:
                    incX = -5
                    pos = 3
                elif evento.key == pygame.K_UP:
                    incY = -5
                    pos = 2
            if evento.type == pygame.KEYUP:
                incX = 0
                incY = 0
                pos = 0
            if evento.type == pygame.QUIT:
                sys.exit()
        
        hY += incY
        hX += incX
        hC = (hX, hY)
        
        Heroe.update(hC, pos)
        Reloj.tick(30)


class miSprite(pygame.sprite.Sprite):

    def __init__(self, coord, imagen, animaciones=6, width=32, height=64):
        #pygame.sprite.Sprite.__init__(self)

        self.tile = imagen
        self._width = width
        self._height = height
        self.arrayAnim = []
        # _maxAnim es el numero de animaciones que tengo en la imagen
        self._maxAnim = animaciones
        # dir es la direccion: abajo,arriba,der,izq
        for dir in range(4):
            # anim es el numero de animaciones
            for anim in range(self._maxAnim):
                self.arrayAnim.append(self.tile.subsurface(\
                    (anim*self._width, dir*self._height, \
                    self._width, self._height)))
        self.anim = 0

        self.actualizado = pygame.time.get_ticks()
        self.image = self.arrayAnim[self.anim]
        self.rect = self.image.get_rect()
        self.rect.center = coord


    def update(self, coord, dir):
        self.rect.center = coord
        if dir:
            self.anim += 1
            if self.anim > self._maxAnim:
                self.anim = 1
            pos = (dir - 1) * self._maxAnim
            self.image = self.arrayAnim[(self.anim - 1) + pos]
        self.actualizado = pygame.time.get_ticks()




if __name__ == "__main__":
    main()
    
