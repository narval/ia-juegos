#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from pygame.locals import *

# Función para cargar las imágenes
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
        image.convert_alpha()
        
        #image = pygame.transform.laplacian(image)
    return image

def sonar_musica(filename, loop):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loop)

def sonar_sonido(filename):
    sonido = pygame.mixer.Sound(filename)
    reloj = pygame.time.Clock()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.event.set_allowed(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    print "sonar sonido"
    #pygame.event.wait()
    

# Función para crear una superficie (imagen) a partir de un texto
def texto(texto, posi, color=(244, 244, 244)):
    fuente = pygame.font.Font(None, 35)
    salida = fuente.render(texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.center = posi
    return salida, salida_rect

# Función para sumar dos vectores
def suma_v(a, b):
    salida = []
    for i in range(0, min(len(a), len(b))):
        salida = salida + [a[i] + b[i]]
    return salida

# Función para restar dos vectores
def resta_v(a, b):
    salida = []
    for i in range(0, min(len(a), len(b))):
        salida = salida + [a[i] - b[i]]
    return salida

# Función para escalar un vector (multiplicarlo por un escalar)
def escalar_v(a, b):
    salida = []
    for i in range(0, len(a)):
        salida = salida + [a[i] * b]
    return salida

