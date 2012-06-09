#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

from Enemigo import *
from Comportamiento import *

class Pulpo(Enemigo):

    def __init__(self, inicio, nombre = "sin nombre"):
        pygame.sprite.Sprite.__init__(self)
        Enemigo.__init__(self)
        
        
        # Atributos principales
        self.tam = [30, 30]
        self.nombre = nombre
        self.image = load_image("imagenes/char.png", True)
        self.image = pygame.transform.smoothscale(self.image, (self.tam[0], self.tam[1]))
        self.original = self.image
        self.mask = pygame.mask.from_surface(self.image)
        
        # Atributos físicos y de posicion
        self.rect = self.image.get_rect()
        self.rect.center = inicio
        self.posi = [self.rect.centerx, self.rect.centery, 0]
        self.vel = [0.0, 0.0, 0.0]
        self.acel = [0, 0, 0]
        self.tiempo = 50
        self.angulo = 0
        self.vel_angular = 0
        self.acel_angular = 0
        
        # Atributos de comportamientos
        self.target = self
        self.comportamiento = Comportamiento(self)
        
        # Atributos para colisiones
        self.colisiona = True
        self.colisionable = False
        if self in grupo_colisionables:
            self.colisionable = True
            
            
    def ir_pulpo(self, target):
        self.recorrido += 2
        self.recorrido %= 360
        #target = self.target.posi
        x = target[0] - self.posi[0]
        y = target[1] - self.posi[1]
        module = math.sqrt(x**2 + y**2)
        if module != 0:
            casi =  [(x*0.003)/module, (y*0.003)/module, 0] 
            tangencial = [casi[0]*math.sin(math.radians(self.recorrido)), casi[1]*math.sin(math.radians(self.recorrido)), 0]
        else:
            casi, tangencial = [0, 0, 0], [0, 0, 0]
        return suma_v(casi, tangencial), 0
