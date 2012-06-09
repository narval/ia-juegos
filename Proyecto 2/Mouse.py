#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *
from Objeto import *

class Mouse(Objeto):
    
    def __init__(self, inicio, nombre = "sin nombre"):
        pygame.sprite.Sprite.__init__(self)
        grupo_dibujables.add(self)
        Objeto.__init__(self)        
        
        # Atributos principales
        self.tam = [50, 50]
        self.nombre = nombre
        self.image = load_image("imagenes/target.png", True)
        self.image = pygame.transform.smoothscale(self.image, (self.tam[0], self.tam[1]))
        self.original = self.image
        self.mask = pygame.mask.from_surface(self.image)
        
        # Atributos físicos y de posicion
        self.rect = self.image.get_rect()
        
    def actualizar(self, time):
        self.image = self.original
        self.rect = self.image.get_rect()      

        self.image = pygame.transform.rotozoom(self.image, (-self.angulo - 90), (1.0+ self.posi[2]*0.0007))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = [self.posi[0], self.posi[1]]
