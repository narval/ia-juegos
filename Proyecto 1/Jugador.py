#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *
from Personaje import *

class Jugador(Personaje):

    def moverse_general(self, keys):
        self.mover(keys)
        self.ajuste_orientacion()

    def moverse_relativo(self, keys):
        if keys[K_w]:
            self.acel = suma_v([math.cos(math.radians(self.angulo))*0.01, math.sin(math.radians(self.angulo))*0.01, 0], self.acel)
        if keys[K_s]:
            self.acel = resta_v(self.acel, [math.cos(math.radians(self.angulo))*0.01, math.sin(math.radians(self.angulo))*0.01, 0])
        if keys[K_d]:
            self.acel_angular += 0.008
        if keys[K_a]:
            self.acel_angular -= 0.008
        if keys[K_ESCAPE]:
            texto("Saliendo", [WIDTH / 2, HEIGHT / 2]) 
            sys.exit(0)
        if keys[K_SPACE] and self.posi[2] <= 0:
            self.acel[2] = 10
            #sonar_sonido("sonido/Bottle Rocket-SoundBible.com-332895117.mp3")

    def moverse_personal(self, keys):
        if keys[K_w]:
            mouse = pygame.mouse.get_pos()
            print math.fabs(mouse[0] - self.posi[0]) , math.fabs(mouse[1] - self.posi[1])
            if math.fabs(mouse[0] - self.posi[0]) + math.fabs(mouse[1] - self.posi[1]) > 5:
                self.acel = suma_v([math.cos(math.radians(self.angulo))*0.01, math.sin(math.radians(self.angulo))*0.01, 0], self.acel)
        if keys[K_s]:
            self.acel = resta_v(self.acel, [math.cos(math.radians(self.angulo))*0.01, math.sin(math.radians(self.angulo))*0.01, 0])
        if keys[K_d]:
            self.acel = suma_v([-math.sin(math.radians(self.angulo))*0.01, math.cos(math.radians(self.angulo))*0.01, 0], self.acel)
        if keys[K_a]:
            self.acel = suma_v([math.sin(math.radians(self.angulo))*0.01, -math.cos(math.radians(self.angulo))*0.01, 0], self.acel)
        if keys[K_ESCAPE]:
            texto("Saliendo", [WIDTH / 2, HEIGHT / 2]) 
            sys.exit(0)
        if keys[K_SPACE] and self.posi[2] <= 0:
            self.acel[2] = 10
        self.ajuste_orientacion()
            #sonar_sonido("sonido/Bottle Rocket-SoundBible.com-332895117.mp3")

    def mover(self, keys):
        if keys[K_w]:
            self.acel[1] -= 0.01
        if keys[K_s]:
            self.acel[1] += 0.01
        if keys[K_d]:
            self.acel[0] += 0.01
        if keys[K_a]:
            self.acel[0] -= 0.01
        if keys[K_ESCAPE]:
            texto("Saliendo", [WIDTH / 2, HEIGHT / 2]) 
            sys.exit(0)
        if keys[K_SPACE] and self.posi[2] <= 0:
            self.acel[2] = 10
            #sonar_sonido("sonido/Bottle Rocket-SoundBible.com-332895117.mp3")

        self.keysanteriores = keys

    def ajuste_orientacion(self):
        mouse = pygame.mouse.get_pos()
        dirx = mouse[0] - self.posi[0]
        diry = mouse[1] - self.posi[1]
        anguloanterior = self.angulo
        self.acel_angular = self.ajustar_angulo(math.degrees(math.atan2(diry, dirx)) + 360  % 360, 0.001)
