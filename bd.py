#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: bd.py $Date$
version: $Id$
    LICENCIA PÚBLICA PARA QUE HAGA LO QUE LE DÉ LA GANA
                    Versión 2, diciembre de 2004
 
 Derechos de autor (C) 2004 Sam Hocevar
  14 rue de Plaisance, 75014 París, Francia
 Se permite la copia y distribución de forma literal o modificada
 copias de este documento de licencia, y su modificación están permitidas siempre
 que el se cambie el nombre.
 
            LICENCIA PÚBLICA PARA QUE HAGA LO QUE LE DÉ LA GANA
   TÉRMINOS Y CONDICIONES PARA LA COPIA, DISTRIBUCIÓN & MODIFICACIÓN
 
  0. Eso sí, HAGA LO QUE LE DÉ LA GANA.
"""
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *

# Creamos un reloj
Reloj= pygame.time.Clock()

# Iniciamos Pygame
pygame.init()

# Creamos una surface (la ventana de juego), asignándole un alto y un ancho
Ventana = pygame.display.set_mode((600, 400))

# Le ponemos un título a la ventana
pygame.display.set_caption("bd Clone")

# Cargamos las imágenes
Fondo = pygame.image.load("res/fondo.jpg")
Imagen = pygame.image.load("res/sprite.png")

coordX = 300
coordY = 200
Coordenadas = (coordX, coordY)

incrementoX = 0
incrementoY = 0

# Bucle infinito para mantener el programa en ejecución
while True:

    Ventana.blit(Fondo, (0, 0))
    Ventana.blit(Imagen, Coordenadas)    
    pygame.display.flip()

   # Manejador de eventos
    for evento in pygame.event.get():
        # Pulsación de la tecla escape
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                sys.exit()
            elif evento.key == pygame.K_RIGHT:
                incrementoX = 5
            elif evento.key == pygame.K_DOWN:
                incrementoY = 5
            elif evento.key == pygame.K_LEFT:
                incrementoX = -5
            elif evento.key == pygame.K_UP:
                incrementoY = -5
        if evento.type == pygame.KEYUP:
            incrementoX = 0
            incrementoY = 0
        if evento.type == pygame.QUIT:
            sys.exit()
    coordX = coordX + incrementoX
    coordY = coordY + incrementoY

    Coordenadas = (coordX, coordY)

    # Asignamos un "tic" de 30 milisegundos
    Reloj.tick(60)
