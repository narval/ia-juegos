#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *

# Clase principal de los ejementos moviles en el juego
class Personaje(pygame.sprite.Sprite):
    def __init__(self, inicio, tam, imagefile = None, grupos = None, nombre = "sin nombre"):
        pygame.sprite.Sprite.__init__(self)
        self.nombre = nombre
        self.image = load_image(imagefile, True)
        self.image = pygame.transform.smoothscale(self.image, (tam[0], tam[1]))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = inicio
        self.posi = [self.rect.centerx, self.rect.centery, 0]
        self.vel = [0.0, 0.0, 0.0]
        self.acel = [0, 0, 0]
        self.tiempo = 50
        self.angulo = 0
        self.vel_angular = 0
        self.acel_angular = 0
        self.target = self
        self.keysanteriores = None

        self.mask = pygame.mask.from_surface(self.image)
        self.groups = grupos
        for g in grupos:
            g.add(self)
        self.colisiona = True
        self.colisionable = False
        if self in grupo_colisionables:
            self.colisionable = True
            
    # Método de actualización:
    # actualiza los atributos, transforma la imagen, revisa colisiones
    # revisa restricciónes etc.
    def actualizar(self, time):  
        self.vel[0] /= 10
        self.vel[1] /= 10
        self.vel[2] /= 10
        
        self.vel_angular /= 2

        if abs(self.vel[0]) <= 0.00001:
            self.vel[0] = 0
        if abs(self.vel[1]) <= 0.00001:
            self.vel[1] = 0
        if abs(self.vel[2]) <= 0.00001:
            self.vel[2] = 0

# --------- Gravedad

        self.acel[2] -= 0.3

# -------- Ajusta la velocidad y la posicion respecto al tiempo

        self.vel = suma_v(self.vel, [(self.acel[0] * time), (self.acel[1] * time), (self.acel[2] * time)])

        posi_anterior = self.posi
        rectangulo_anterior = self.rect

        self.posi = suma_v(self.posi, [(self.vel[0] * time), (self.vel[1] * time), (self.vel[2] * time)])

        # Restricciones de posicion
        self.posi[0] %= WIDTH
        self.posi[1] %= HEIGHT
        if self.posi[2] < 0:
            self.posi[2] = 0
        
        self.rect.center = [self.posi[0], self.posi[1]]

        # Si el movimiento causó una colisión se revierten los cambios
        if self.colisionable:
            if self.colisionar():
                self.posi[0:2] = posi_anterior[0:2]
                self.rect = rectangulo_anterior

# -------- Ajusta la velocidad angular y el angulo respecto al tiempo

        self.vel_angular += (self.acel_angular * time)

        angulo_anterior = self.angulo
        rectangulo_anterior = self.rect
        imagen_anterior = self.image
        posi_anterior = self.posi

        self.angulo += (self.vel_angular * time)

        self.image = self.original
        self.rect = self.image.get_rect()      

        self.image = pygame.transform.rotozoom(self.image, (-self.angulo - 90), (1.0+ self.posi[2]*0.0007))        

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = [self.posi[0], self.posi[1]]

        # Para saber si el giro produjo una colisión
        if self.colisionable:
            if self.colisionar():
                self.angulo = angulo_anterior
                self.image = imagen_anterior
                self.rect = rectangulo_anterior
                self.rect.center = [self.posi[0], self.posi[1]]
                self.mask = pygame.mask.from_surface(self.image)

        # Segunda revisada para saber si estan incrustados dos objetos
        if self.colisionable:
            if self.colisionar():
                self.acel = suma_v(self.acel, self.separacion_incrustacion()[0])
                self.acel[2] = 0
                self.vel[2] = 0
                self.vel = suma_v(self.vel, [(self.acel[0] * time), (self.acel[1] * time), (self.acel[2] * time)])
                self.posi = suma_v(self.posi, [(self.vel[0] * time), (self.vel[1] * time), (self.vel[2] * time)])

# -------- Ajusta el rectangulo a la posicion

        self.rect.centerx = self.posi[0]
        self.rect.centery = self.posi[1]

# -------- Hace que la aceleracion sea instantanea (La anula en cada iteracion)

        self.acel[0] = 0
        self.acel[1] = 0
        self.acel[2] = 0

        self.acel_angular = 0
  

# --------- Para los saltos
        if self.colisionable:
            if self.posi[2] > 0:
                self.remove(grupo_colisionables)
                self.colisiona = False
            else:
                self.add(grupo_colisionables)
                self.colisiona = True

    # Función que hace cambia el angulo del personaje para
    # que se acerque al ángulo requerido
    def ajustar_angulo(self, angulo, velocidad = 0.0):
        error = min((angulo + 360 - self.angulo)%360, (self.angulo + 360 - angulo)%360)
        a = 0
        if error > 2:
            if((self.angulo - angulo + 360)%360 < 180):
                if velocidad == 0:               
                    return -0.008
                else:
                    return -velocidad*error
            else:
                if velocidad == 0:               
                    return 0.008
                else:
                    return velocidad*error
        else:
            return 0

    # Revisa si el personaje colisionacon otro elemento colisionable
    def colisionar(self):

        # Esta parte se usa para que chocar con un borde de la pantalla 
        # sean considerado como una colisión
        """
        if self.rect.left <= 0:
            self.rect.left = 1
            self.posi[0] = self.rect.centerx
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH -1
            self.posi[0] = self.rect.centerx
        if self.rect.top <= 0:
            self.rect.top = 1
            self.posi[1] = self.rect.centery
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT -1
            self.posi[1] = self.rect.centery
        """
        
        p = pygame.sprite.spritecollide(self, grupo_colisionables, False, pygame.sprite.collide_rect)

        if len(p) > 1:
            for objetivo in p:
                if objetivo != self:
                    #print self.nombre, " colisiono con ", objetivo.nombre
                    if pygame.sprite.collide_mask(self, objetivo):
                        return 1
        return 0               

    # Algoritmo que genera una aceleración "repulsiva" entre el personaje
    # y los objetos colisionables y con altura semejante 
    def separacion_incrustacion(self):
        grupo = grupo_personajes
        x, y = 0, 0
        for aliado in grupo:
            if aliado != self and aliado.colisiona and abs(self.posi[2] - aliado.posi[2]) < 5:
                modulo = math.sqrt((aliado.posi[0] - self.posi[0])**2 + (aliado.posi[1] - self.posi[1])**2)
                if (modulo < 150):
                    orientacion = [(self.posi[0] - aliado.posi[0]) / modulo, (self.posi[1] - aliado.posi[1]) / modulo]
                    if orientacion[0] != 0:
                        x += orientacion[0] / modulo**2
                    if orientacion[1] != 0:
                        y += orientacion[1] / modulo**2
        return [x, y, 0], 0


