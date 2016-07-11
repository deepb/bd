#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: game.py $Id$
date: $Date$
"""

import pygame as gm
from pygame.locals import *

import sys
import random

from locals import *
from sprite import miSprite, miSpriteRandom

from db import miDB

class Juego():
    
    def __init__(self, *args):
        self.init()
        if FULLSCREEN:
            self.Ventana = gm.display.set_mode(VENTANA, gm.FULLSCREEN)
        else:
            self.Ventana = gm.display.set_mode(VENTANA)
        self.DB = miDB()
        # DEBUG
        #self.DB.truncateDB()
        
    def init(self, *args):
        # Reloj
        self.Reloj= gm.time.Clock()
        # Fuente Puntos
        self.puntosFont = gm.font.Font(None, 30)
        # Fondo y Titulo
        self.Fondo = gm.image.load(RES_BG + "/fondo.jpg")
        self.BD = gm.image.load(RES_BG + "/bd.png")
        # Sprites
        imgHeroe = gm.image.load(RES_TILES + "/sprite.png")
        imgFire = gm.image.load(RES_TILES + "/fire.png")
        imgExit = gm.image.load(RES_TILES + "/exit.png")
        # Heroe Sprite
        self.Heroe = miSprite((ANCHO//2, ALTO//2), imgHeroe, 6)
        # Exit Sprite
        self.Exit = miSpriteRandom(\
            (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
            imgExit)
        self.Exit.randomVel()
        # Fuego Sprite
        self.aFire = []
        for i in range(MAX_FIRE):
            self.aFire.append(miSpriteRandom(\
                (random.randrange(0, ANCHO), random.randrange(0, ALTO)),\
                imgFire))
            self.aFire[i].randomVel()
        # Marcadores
        self.puntos = POINTS
        self.game = True
        
    def newGame(self, game=True):
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
                    elif evento.key == gm.K_f:
                        gm.display.toggle_fullscreen()
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
        self.game = False
        return False
    
    def ouch(self):
        self.play("ouch.wav")
        self.puntos -= POINTS//20
        return True
    
    def play(self, tune):
        sound = gm.mixer.Sound(RES_SOUND + "/" + tune)
        sound.set_volume(0.5)
        if not gm.mixer.get_busy():
            sound.play()

    def gameover(self):
        self.statusFont("Game Over!", (200, 200, 200), (ALTO//2, ANCHO//2+40))
        self.game = False
        return True
    
    def blur(self, fondo, cont=50.0):
        if cont < 1.0:
            cont = 1.0
        escala = 1.0/float(cont)
        tam_fondo = fondo.get_size()
        tam_escala = (int(tam_fondo[0] * escala), 
                    int(tam_fondo[1] * escala))
        blur = gm.transform.smoothscale(fondo, tam_escala)
        blur = gm.transform.smoothscale(blur, tam_fondo)
        return blur

    def statusFont(self, text="", color=(0, 255, 255), pos=(ALTO//2, ANCHO//2)):
        font = gm.font.Font(None, 40)
        f = font.render(text, 1, color)
        self.Ventana.blit(f, pos)
        gm.display.flip()

    def printName(self, name):
        self.Ventana.blit(self.Fondo, (0, 0))
        self.statusFont("Felicidades", (0, 255, 255), (ALTO//2, ANCHO//2-100))
        self.statusFont("Has salido!", (0, 255, 255), (ANCHO//2, ALTO//2))
        self.statusFont("Nombre?", (0, 255, 255), (ALTO//2-50, ANCHO//2-50))
        self.statusFont(name, (0, 255, 255), (ALTO//2+100, ANCHO//2-50))

    def getName(self):
        name = ''
        self.printName(name)
        while len(name) < 5:
            evento = gm.event.wait()
            if evento.type == gm.KEYDOWN:
                if evento.key == gm.K_ESCAPE:
                    name = "AAAAA"
                elif evento.key == gm.K_a:
                    name += 'A'
                elif evento.key == gm.K_b:
                    name += 'B'
                elif evento.key == gm.K_c:
                    name += 'C'
                elif evento.key == gm.K_d:
                    name += 'D'
                elif evento.key == gm.K_e:
                    name += 'E'
                elif evento.key == gm.K_f:
                    name += 'F'
                elif evento.key == gm.K_g:
                    name += 'G'
                elif evento.key == gm.K_h:
                    name += 'H'
                elif evento.key == gm.K_i:
                    name += 'I'
                elif evento.key == gm.K_j:
                    name += 'J'
                elif evento.key == gm.K_k:
                    name += 'K'
                elif evento.key == gm.K_l:
                    name += 'L'
                elif evento.key == gm.K_m:
                    name += 'M'
                elif evento.key == gm.K_n:
                    name += 'N'
                elif evento.key == gm.K_o:
                    name += 'O'
                elif evento.key == gm.K_p:
                    name += 'P'
                elif evento.key == gm.K_q:
                    name += 'Q'
                elif evento.key == gm.K_r:
                    name += 'R'
                elif evento.key == gm.K_s:
                    name += 'S'
                elif evento.key == gm.K_t:
                    name += 'T'
                elif evento.key == gm.K_u:
                    name += 'U'
                elif evento.key == gm.K_v:
                    name += 'V'
                elif evento.key == gm.K_w:
                    name += 'W'
                elif evento.key == gm.K_x:
                    name += 'X'
                elif evento.key == gm.K_y:
                    name += 'Y'
                elif evento.key == gm.K_z:
                    name += 'Z'
                elif evento.key == gm.K_BACKSPACE:
                    name = name[:-1]
                elif evento.key == gm.K_RETURN:
                    name += ' '*5 
            self.printName(name)
        return name
    
    def getTop(self):
        top = self.DB.getTop()
        
        self.statusFont("Nombre      Puntos", (0, 255, 255), \
                (ALTO//2-50, ANCHO//2-130))
        if len(top):
            m = -100
            for t in top:
                self.statusFont("%s" % t[0],\
                (0, 255, 255), (ALTO//2-50, ANCHO//2+m))
                self.statusFont("%d" % t[1],\
                (0, 255, 255), (ALTO//2+150, ANCHO//2+m))
                m += 25
    
    def menu(self):
        self.Ventana.blit(self.blur(self.Fondo, 10.0), (0, 0))
        self.Ventana.blit(self.BD, (130, 20))
        while True:
            self.statusFont("Pulsa cualquier tecla para jugar", \
                (0, 255, 255), (ALTO//2-130, ANCHO//2+100))
            gm.display.flip()
            self.tick()
            evento = gm.event.wait()
            if evento.type == gm.KEYDOWN:
                if evento.key == gm.K_ESCAPE:
                    sys.exit()
                elif evento.key == gm.K_f:
                    gm.display.toggle_fullscreen()
                else:
                    self.init()
                    ret = self.newGame()
                    if not ret:
                        name = self.getName()
                        self.Ventana.blit(self.blur(self.Fondo, 10.0), (0, 0))
                        self.Ventana.blit(self.BD, (130, 20))
                        self.DB.addTop(name, self.puntos)
                self.getTop()
            if evento.type == gm.QUIT:
                sys.exit()      

class Ventana():
    
    def __init__(self):
        gm.init()
        #gm.display.set_mode(VENTANA)
        gm.display.set_caption("bd Clone")
        
    def flip(self):
        gm.display.flip()


