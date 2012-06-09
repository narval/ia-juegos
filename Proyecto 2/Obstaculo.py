#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *
from Personaje import *

class Obstaculo(Objeto):
    
    def __init__(self, inicio, nombre = "sin nombre"):
        pygame.sprite.Sprite.__init__(self)
        grupo_obstaculos.add(self)
        grupo_dibujables.add(self)
        grupo_colisionables.add(self)
        Objeto.__init__(self)
        
        # Atributos principales
        self.tam = [80, 80]
        self.nombre = nombre
        self.image = load_image("imagenes/obstaculo2.png", True)
        self.image = pygame.transform.smoothscale(self.image, (self.tam[0], self.tam[1]))
        self.original = self.image
        self.mask = pygame.mask.from_surface(self.image)
        
        # Atributos físicos y de posicion
        self.rect = self.image.get_rect()
        self.rect.center = inicio
        self.posi = [self.rect.centerx, self.rect.centery, 0]
        self.angulo = 0
        
        # Atributos de comportamientos
        self.target = self
        
        # Atributos para colisiones
        self.colisiona = True
        self.colisionable = False
        if self in grupo_colisionables:
            self.colisionable = True
    
    
