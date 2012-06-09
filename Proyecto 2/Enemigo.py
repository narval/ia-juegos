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
class Enemigo(Personaje):

    def __init__(self):
        Personaje.__init__(self)
        grupo_enemigos.add(self)       
         
            
    def moverse(self):
        self.acel, self.acel_angular = self.comportamiento.movimiento_total(self.target)


