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

import pygame as gm
from pygame.locals import *
try:
    import pygame.freetype as Font
except ImportError as err:
    print("Aviso: No funciona freetype")

import sys
import time
import random

ANCHO = 640
ALTO = 480
VENTANA = [ANCHO, ALTO]

RES = "res"
RES_TILES = RES + "/tiles"
RES_SOUND = RES + "/sounds"
RES_BG = RES + "/bg"

MAX_FIRE = 10

RELOJ_TICKS = 30
RANDOM_SPEED = 10

class miSprite(gm.sprite.Sprite):

    def __init__(self, coord, imagen, animaciones=6, ancho=32, alto=64):
        #gm.sprite.Sprite.__init__(self)

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
        #self.actualizado = gm.time.get_ticks()

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

def main():
    
    def init():
        global Reloj, Ventana, Fondo, Heroe, Exit, aFire, Status

        gm.init()
        Reloj= gm.time.Clock()
        
        Ventana = gm.display.set_mode(VENTANA)
        gm.display.set_caption("bd Clone")
        
        Status = gm.font.Font(None, 30)
        
        Fondo = gm.image.load(RES_BG + "/fondo.jpg")
        
        imgHeroe = gm.image.load(RES_TILES + "/sprite.png")
        imgFire = gm.image.load(RES_TILES + "/fire.png")
        imgExit = gm.image.load(RES_TILES + "/exit.png")
        Heroe = miSprite((ANCHO//2, ALTO//2), imgHeroe, 6)
        Exit = miSpriteRandom(\
            (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
            imgExit)
        Exit.randomVel()
        aFire = []

        for i in range(MAX_FIRE):
            aFire.append(miSpriteRandom(\
                (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
                imgFire))
            aFire[i].randomVel()
        
        
    def newGame():
        global Reloj, Ventana, Fondo, Heroe, Exit, aFire, Status, puntos

        hX = 300
        hY = 300
        hC = [hX, hY]
        incX = 0
        incY = 0
        pos = 0        
        
        puntos = 200
        
        while True:
        
            Ventana.blit(Fondo, (0, 0))
            Ventana.blit(Heroe.image, Heroe.rect)
            for i in range(MAX_FIRE):
                Ventana.blit(aFire[i].image, aFire[i].rect)
            Ventana.blit(Exit.image, Exit.rect)

            st = Status.render("Puntos: "+ str(puntos), 0, (0, 255, 255))
            Ventana.blit(st, (0, 0))
            
            gm.display.flip()
        
            for evento in gm.event.get():
                if evento.type == gm.KEYDOWN:
                    #key = pygame.key.get_pressed()
                    if evento.key == gm.K_ESCAPE:
                        sys.exit()
                    elif evento.key == gm.K_RIGHT or\
                        evento.key == gm.K_d:
                        incX = 5
                        incY = 0
                        pos = 4
                    elif evento.key == gm.K_DOWN or\
                        evento.key == gm.K_s:
                        incX = 0
                        incY = 5
                        pos = 1
                    elif evento.key == gm.K_LEFT or\
                        evento.key == gm.K_a:
                        incX = -5
                        incY = 0
                        pos = 3
                    elif evento.key == gm.K_UP or\
                        evento.key == gm.K_w:
                        incX = 0
                        incY = -5
                        pos = 2
                if evento.type == gm.KEYUP:
                    incX = 0
                    incY = 0
                    pos = 0
                if evento.type == gm.QUIT:
                    sys.exit()
            
            hY += incY
            hX += incX
            hC = Heroe.checkCoord([hX, hY])
            [hX, hY] = hC
            Heroe.update(hC, pos)
            for i in range(MAX_FIRE):
                aC = aFire[i].rect.center
                aX = aC[0] + aFire[i].vx
                aY = aC[1] + aFire[i].vy
                aC = aFire[i].checkRandom([aX, aY])
                aFire[i].update(aC)
                if gm.sprite.collide_mask(aFire[i], Heroe):
                    ouch()
            aC = Exit.rect.center
            aX = aC[0] + Exit.vx
            aY = aC[1] + Exit.vy
            aC = Exit.checkRandom([aX, aY])
            Exit.update(aC)
            if gm.sprite.collide_mask(Exit, Heroe):
                return game()

            puntos -= 1
            if puntos < 0:
                return gameover()
            Reloj.tick(30)

    def game():
        global Ventana
        colisionSound = gm.mixer.Sound(RES_SOUND + "/guitarra.wav")
        colisionSound.set_volume(0.5)
        if not gm.mixer.get_busy():
            colisionSound.play()
            
        font = gm.font.Font(None, 40)
        go = font.render("Has salido!", 1, (0, 255, 255))
        Ventana.blit(go, (ALTO//2, ANCHO//2))
        gm.display.flip()
        return False
    
    def ouch():
        global puntos
        colisionSound = gm.mixer.Sound(RES_SOUND + "/ouch.wav")
        colisionSound.set_volume(0.5)
        if not gm.mixer.get_busy():
            colisionSound.play()
        puntos -= 10
        return True
    
    def gameover():
        global Ventana

        font = gm.font.Font(None, 40)
        go = font.render("Game Over!", 1, (128, 0, 0))
        Ventana.blit(go, (ALTO//2, ANCHO//2))
        gm.display.flip()
        return True
    
    def getName():
        return "AAA"
    
    def getTop():
        print("TOP")
    

    while True:
        init()
        evento = gm.event.wait()
        if evento.type == gm.KEYDOWN:
            ret = newGame()
            if ret:
                name = getName()
                getTop()
        if evento.type == gm.QUIT:
            sys.exit()      
        
if __name__ == "__main__":
    main()
    
    
