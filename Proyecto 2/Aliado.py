#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
from Jugador import *
from Personaje import *
import math
import copy

# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class Aliado(Personaje):

    def __init__(self):
        Personaje.__init__(self)
        grupo_aliados.add(self)       
        
        
    def actualizar(self, time):
        print self.seleccionado
        if self.tipo_estado:
            if self.seleccionado:
                self.original = self.ataque_selec
                print "blaaaaaa"
            else:
                self.original = self.ataque
        else:
            if self.seleccionado:
                self.original = self.defensa_selec
            else:
                self.original = self.defensa
                
        Personaje.actualizar(self, time)
         
            
    def moverse(self):
        self.acel, self.acel_angular = self.comportamiento.movimiento_total(self.target)
