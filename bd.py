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

def main():

    pygame.init()

    Reloj= pygame.time.Clock()

    Ventana = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("bd Clone")

    Fondo = pygame.image.load("res/fondo.jpg")

    Imagen = pygame.image.load("res/sprite.png")
    transparente = Imagen.get_at((0, 0))
    Imagen.set_colorkey(transparente)
    
    hX = 100
    hY = 100
    hC = (hX, hY)
    incX = 0
    incY = 0
    pos = 0
    
    Heroe = miSprite(hC, Imagen)

    while True:

        Ventana.blit(Fondo, (0, 0))
        Ventana.blit(Heroe.image, Heroe.rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                #key = pygame.key.get_pressed()
                if evento.key == pygame.K_ESCAPE:
                    sys.exit()
                if evento.key == pygame.K_RIGHT:
                    incX = 5
                    pos = 4
                if evento.key == pygame.K_DOWN:
                    incY = 5
                    pos = 1
                if evento.key == pygame.K_LEFT:
                    incX = -5
                    pos = 3
                if evento.key == pygame.K_UP:
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

    def __init__(self, coord, imagen):
        #pygame.sprite.Sprite.__init__(self)

        self.tile = imagen
        self.arrayAnim = []
        # _maxAnim es el numero de animaciones que tengo en la imagen
        self._maxAnim = 6
        # dir es la direccion: abajo,arriba,der,izq
        for dir in range(4):
            # anim es el numero de animaciones
            for anim in range(self._maxAnim):
                self.arrayAnim.append(self.tile.subsurface((anim*32,dir*64,32,64)))
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
    
