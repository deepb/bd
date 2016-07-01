#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: bd.py $Id$
date: $Date$
"""

# Importar print como funcion
from __future__ import print_function

import pygame as gm
from pygame.locals import *

import sys
import random

ANCHO = 640
ALTO = 480
VENTANA = [ANCHO, ALTO]
FULLSCREEN = False

RES = "res"
RES_TILES = RES + "/tiles"
RES_SOUND = RES + "/sounds"
RES_BG = RES + "/bg"

MAX_FIRE = 4

RELOJ_TICKS = 30
RANDOM_SPEED = 10

POINTS = 200

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

class Juego():
    
    def __init__(self):
        self.init()
        if FULLSCREEN:
            self.Ventana = gm.display.set_mode(VENTANA, gm.FULLSCREEN)
        else:
            self.Ventana = gm.display.set_mode(VENTANA)
        self.top = []
        
    def init(self):
        self.Reloj= gm.time.Clock()
        
        self.puntosFont = gm.font.Font(None, 30)
        
        self.Fondo = gm.image.load(RES_BG + "/fondo.jpg")
        
        imgHeroe = gm.image.load(RES_TILES + "/sprite.png")
        imgFire = gm.image.load(RES_TILES + "/fire.png")
        imgExit = gm.image.load(RES_TILES + "/exit.png")
        self.Heroe = miSprite((ANCHO//2, ALTO//2), imgHeroe, 6)
        self.Exit = miSpriteRandom(\
            (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
            imgExit)
        self.Exit.randomVel()
        self.aFire = []

        for i in range(MAX_FIRE):
            self.aFire.append(miSpriteRandom(\
                (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
                imgFire))
            self.aFire[i].randomVel()
        self.puntos = POINTS
        self.game = True
        
    def newGame(self, game=True):
        global FULLSCREEN
        
        hX = VENTANA[0]//2
        hY = VENTANA[1]//2
        hC = [hX, hY]
        incX = 0
        incY = 0
        pos = 0        
        
        self.puntos = POINTS
        self.game = game
        
        while self.game:
            self.Ventana.blit(self.Fondo, (0, 0))
            self.Ventana.blit(self.Heroe.image, self.Heroe.rect)
            for i in range(MAX_FIRE):
                self.Ventana.blit(self.aFire[i].image, self.aFire[i].rect)
            self.Ventana.blit(self.Exit.image, self.Exit.rect)

            pf = self.puntosFont.render("Puntos: "+ str(self.puntos), 1, (0, 255, 255))
            self.Ventana.blit(pf, (VENTANA[0]-150, 0))
            
            gm.display.flip()
        
            for evento in gm.event.get():
                if evento.type == gm.KEYDOWN:
                    if evento.key == gm.K_ESCAPE:
                        self.game = False
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
#                    elif evento.key == gm.K_f:
#                        FULLSCREEN = not FULLSCREEN
#                        gm.display.toggle_fullscreen()
                if evento.type == gm.KEYUP:
                    incX = 0
                    incY = 0
                    pos = 0
                if evento.type == gm.QUIT:
                    self.game = False
                    sys.exit()
            
            hY += incY
            hX += incX
            hC = self.Heroe.checkCoord([hX, hY])
            [hX, hY] = hC
            self.Heroe.update(hC, pos)
            for i in range(MAX_FIRE):
                aC = self.aFire[i].rect.center
                aX = aC[0] + self.aFire[i].vx
                aY = aC[1] + self.aFire[i].vy
                aC = self.aFire[i].checkRandom([aX, aY])
                self.aFire[i].update(aC)
                if gm.sprite.collide_mask(self.aFire[i], self.Heroe):
                    self.ouch()
            aC = self.Exit.rect.center
            aX = aC[0] + self.Exit.vx
            aY = aC[1] + self.Exit.vy
            aC = self.Exit.checkRandom([aX, aY])
            self.Exit.update(aC)
            if gm.sprite.collide_mask(self.Exit, self.Heroe):
                return self.onExit()

            self.puntos -= 1
            if self.puntos < 0:
                return self.gameover()
            self.tick()
            
    def tick(self):
        self.Reloj.tick(30)
        
    def onExit(self):
        self.play("guitarra.wav")
        self.statusFont("Has salido!", (0, 255, 255), (ANCHO//2-50, ALTO//2))
        self.game = False
        return False
    
    def ouch(self):
        self.play("ouch.wav")
        self.puntos -= POINTS//20
        return True
    
    def play(self, tune):
        colisionSound = gm.mixer.Sound(RES_SOUND + "/" + tune)
        colisionSound.set_volume(0.5)
        if not gm.mixer.get_busy():
            colisionSound.play()

    def gameover(self):
        self.statusFont("Game Over!", (128, 0, 0), (ANCHO//2-50, ALTO//2))
        self.game = False
        return True
    
    def statusFont(self, text="", color=(0, 255, 255), pos=(ALTO//2, ANCHO//2)):
        font = gm.font.Font(None, 40)
        f = font.render(text, 1, color)
        self.Ventana.blit(f, pos)
        gm.display.flip()

    def getName(self):
        name = raw_input("Nombre: ")
        return name
    
    def getTop(self):
        print("="*20)
        print("Jugador\tPuntos")
        print("="*20)
        for top in self.top:
            if len(top):
                print(top)

    def menu(self):
        self.Ventana.blit(self.Fondo, (0, 0))
        while True:
            self.statusFont("Pulsa cualquier tecla", \
                (0, 255, 255), (ALTO//2-50, ANCHO//2))
            gm.display.flip()
            self.tick()
            evento = gm.event.wait()
            if evento.type == gm.KEYDOWN:
                self.init()
                ret = self.newGame()
                if not ret:
                    name = self.getName()
                    self.top.append(str(name) + "\t" + str(self.puntos))
                self.getTop()
            if evento.type == gm.QUIT:
                sys.exit()      

class Ventana():
    
    def __init__(self):

        gm.init()
        gm.display.set_mode(VENTANA)
        gm.display.set_caption("bd Clone")
        
    def flip(self):
        gm.display.flip()


def main():
    Ventana()
    juego = Juego()
    juego.menu()
    
if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
    
