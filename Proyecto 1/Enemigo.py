#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
from Jugador import *
from Personaje import *
from Comportamiento import *
import math
import random
import copy

# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class Enemigo(Personaje):
    def __init__(self, jugador, inicio, tam, imagefile = None, grupos = None, nombre = "sin nombre"):
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
        self.colisiona = True
        self.recorrido = 0
        self.comportamiento = Comportamiento(self)

        self.mask = pygame.mask.from_surface(self.image)
        self.groups = grupos
        for g in grupos:
            g.add(self)
        self.target = jugador
        self.colisionable = False
        if self in grupo_colisionables:
            self.colisionable = True
         
            
    def moverse(self):
        self.acel, self.acel_angular = self.comportamiento.movimiento_total()
        
    def siguiente_comportamiento(self):
        self.comportamiento.siguiente()

    # algoritmo de busqueda simple
    def seek(self):
        target = self.target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        module = math.sqrt(dirx**2 + diry**2)
        x , y = 0, 0
        if dirx != 0:
            x = (dirx * 0.003) / module
        if diry != 0:
            y = (diry * 0.003) / module
        return [x, y, 0], 0

    # algoritmo de busqueda con disminución gradual de la 
    # velocidad al acercarse al objetivo
    def seek_llegada(self):
        target = self.target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        module = math.sqrt(dirx**2 + diry**2)
        if module > 100:
            x = (dirx * 0.003) / module
            y = (diry * 0.003) / module
        else:
            x = 0.003 * ((dirx) / 200)
            y = 0.003 * ((diry) / 200)
        return [x, y, 0], 0

    # algoritmo de huida simple
    def flee(self):
        target = self.target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        module = math.sqrt(dirx**2 + diry**2)
        if module != 0:
            x = -(dirx * 0.003) / module
            y = -(diry * 0.003) / module
        else:
            x, y = 0, 0
        return [x, y, 0], 0

    # algoritmo de busqueda con aumento gradual de la 
    # velocidad por cercania al objetivo
    def flee_llegada(self):
        target = self.target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        module = math.sqrt(dirx**2 + diry**2)
        if module > 100:
            x = -(dirx * 0.003) / module
            y = -(diry * 0.003) / module
        else:
            x = -0.003 * (30 / (dirx))
            y = -0.003 * (30 / (diry))
        return [x, y, 0], 0

    # Algoritmo de orientación simple que
    # rota al enemigo para que apunte al objetivo (target)
    def face(self):
        target = self.target.posi
        self.image = self.original
        self.rect = self.original.get_rect()
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        angulon = math.degrees(math.atan2(diry, dirx))
        return [0, 0, 0], self.ajustar_angulo(angulon)

    # Algoritmo con conducta opuesta face
    # es decir que orienta al enemigo en dirección
    # opuesta de donde se encuentra el objetivo 
    def anti_face(self):
        target = self.target.posi
        self.image = self.original
        self.rect = self.original.get_rect()
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        angulon = math.degrees(math.atan2(diry, dirx))
        return [0, 0, 0], -self.ajustar_angulo(angulon)

    # Algoritmo que orienta la dirección del enemigo
    # en el sentido de su velocidad actual (solo para los
    # ejes x, y
    def face_frente(self):
        angulo = math.degrees(math.atan2(self.vel[1], self.vel[0]))
        return [0, 0, 0], self.ajustar_angulo(angulo)

    # Algoritmo de "deambulamiento" simple
    # funciona con dos numeros al azar que sirven para
    # setear una dirección y un tiempo
    # durante ese tiempo el enemigo se moverá hacia esa
    # dirección, para luego elegir una nueva
    def wandering(self):
        self.tiempo -= 1
        if self.tiempo < 0:
            self.tiempo = int(random.uniform(1, 50))
            valor = random.uniform(-1, 1)
            return [0, 0, 0], (valor * 0.1)
        else:            
            return self.ir_nadando()

    # Algoritmo de "deambulamiento" cinemático en el que
    # se proyecta una circunferencia en frente del enemigo
    # y luego se elije un punto al azar del borde. Dicho punto
    # será el objetivo hacia el cual se moverá el enemigo
    def kinematic_wander(self):
        offset = 300
        radio = 200
        targetposi = [self.posi[0] + math.cos(math.radians(self.angulo))*offset,\
        self.posi[1] + math.sin(math.radians(self.angulo))*offset, self.posi[2]]
        valor = random.uniform(-1, 1)
        target = ([math.cos(math.radians(valor * 180))*radio + targetposi[0],\
        math.sin(math.radians(valor * 180))*radio + targetposi[1], 0 + targetposi[2]])

        copia = copy.copy(self)
        copia.posi = target
        target_viejo = self.target
        self.target = copia
        salida = self.seek()
        self.target = target_viejo
        del copia
        return salida

    # Algoritmo simple que incrementa la aceleración hacia 
    # la dirección del enemigo
    def ir_derecho(self):
        return [math.cos(math.radians(self.angulo))*0.003, math.sin(math.radians(self.angulo))*0.003, 0], 0

    def ir_nadando(self):
        self.recorrido += 2
        self.recorrido %= 360
        target = self.target.posi
        x = target[0] - self.posi[0]
        y = target[1] - self.posi[1]
        module = math.sqrt(x**2 + y**2)
        casi = [0, 0, 0], 0
        tangencial = [0, 0, 0], 0
        if module != 0:
            casi =  [(x*0.003)/module, (y*0.003)/module, 0] 
            tangencial = [casi[1]*math.sin(math.radians(self.recorrido)), -casi[0]*math.sin(math.radians(self.recorrido)), 0]
            return suma_v(casi, tangencial), 0
        else:
            return [0, 0, 0], 0
        
    def ir_pulpo(self):
        self.recorrido += 2
        self.recorrido %= 360
        target = self.target.posi
        x = target[0] - self.posi[0]
        y = target[1] - self.posi[1]
        module = math.sqrt(x**2 + y**2)
        if module != 0:
            casi =  [(x*0.003)/module, (y*0.003)/module, 0] 
            tangencial = [casi[0]*math.sin(math.radians(self.recorrido)), casi[1]*math.sin(math.radians(self.recorrido)), 0]
        else:
            casi, tangencial = [0, 0, 0], [0, 0, 0]
        return suma_v(casi, tangencial), 0

    # Algoritmo que cambia la dirección actual por la dirección 
    # del objetivo
    def alinearse(self):
        salida = [0, 0, 0], self.ajustar_angulo(self.target.angulo)
        return salida

    # Algoritmo cuya funcion es la de acelerár en el sentido
    # en que se mueve el objetivo hasta que alcanza su velocidad
    def velocitymatch(self):
        target = self.target.vel
        module = math.sqrt(target[0]**2 + target[1]**2)
        modulo = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        if module != 0:
            velocidad = [target[0]/module, target[1]/module]
            if math.fabs(module - modulo) > 0:
                return [velocidad[0]*0.01, velocidad[1]*0.01, 0], 0
        return [0, 0, 0], 0
    
    # Algoritmo que produce repulsión hacia el sentido
    # opuesto a los objetos colisionables cercanos
    # esto se usa para mantener una separación sobre los 
    # enemigos o demás personajes
    def separacion(self):
        grupo = grupo_personajes
        x, y = 0, 0
        for aliado in grupo:
            if aliado != self and (self.posi[2] - aliado.posi[2]) < 5:
                modulo = math.sqrt((aliado.posi[0] - self.posi[0])**2 + (aliado.posi[1] - self.posi[1])**2)
                if (modulo < 150):
                    orientacion = [(self.posi[0] - aliado.posi[0]) / modulo, (self.posi[1] - aliado.posi[1]) / modulo]
                    if orientacion[0] != 0:
                        x += orientacion[0]*2 / modulo**2
                    if orientacion[1] != 0:
                        y += orientacion[1]*2 / modulo**2
        return [x, y, 0], 0
        
    # Algoritmo que evita colisionamiento entre el enemigo
    # y otros objetos "colisionables"
    # Funciona de la siguiente forma: Genera una linea de rectángulos en frente
    # con los que prueba si hay colisiones. De ser así cambia la orientación
    # hacia un lado para cambiar la ruta a una en la que no haya colisión
    def evitarcolision(self):
        distancia = 40
        a = 0     
        for i in range(1,7):
            orient =  [math.cos(math.radians(self.angulo))*distancia, math.sin(math.radians(self.angulo))*distancia]
            posicion = [self.posi[0] + orient[0], self.posi[1] + orient[1]]
            prueba = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            prueba.center = posicion
            rectangulo = pygame.sprite.Sprite()
            rectangulo.rect = prueba
            rectangulo.image = self.image
            rectangulo.add(grupo_dibujables)
            p = pygame.sprite.spritecollide(rectangulo, grupo_colisionables, False)
            if len(p) > 0:
                for objetivo in p:             
                    if objetivo != self:
                        a += 0.05/ (i**2)
            distancia += 25
            rectangulo.kill()
            del rectangulo
        return [0, 0, 0], a
   
    # Algoritmo que evita colisionamiento entre el enemigo
    # y otros objetos "colisionables"
    # Funciona de la siguiente forma: Genera una linea de rectángulos en frente
    # con los que prueba si hay colisiones. De ser así genera una aceleración
    # en sentido contrario a la dirección que los une
    def evitarcolision2(self):
        distancia = 40
        a = [0, 0, 0]     
        x = 0
        y = 0
        for i in range(1,7):
            orient =  [math.cos(math.radians(self.angulo))*distancia, math.sin(math.radians(self.angulo))*distancia]
            posicion = [self.posi[0] + orient[0], self.posi[1] + orient[1]]
            prueba = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            prueba.center = posicion
            rectangulo = pygame.sprite.Sprite()
            rectangulo.rect = prueba
            rectangulo.image = self.image
            rectangulo.add(grupo_dibujables)
            p = pygame.sprite.spritecollide(rectangulo, grupo_colisionables, False)
            if len(p) > 0:
                for objetivo in p:             
                    if objetivo != self:
                        modulo = math.sqrt((objetivo.posi[0] - self.posi[0])**2 + (objetivo.posi[1] - self.posi[1])**2)
                        if (modulo < 150):
                            orientacion = [(self.posi[0] - objetivo.posi[0]) / modulo, (self.posi[1] - objetivo.posi[1]) / modulo]
                            if orientacion[0] != 0:
                                x += orientacion[0]*2 / modulo**2
                            if orientacion[1] != 0:
                                y += orientacion[1]*2 / modulo**2
                            a = suma_v(a, [x, y, 0])
            distancia += 25
            rectangulo.kill()
            del rectangulo
        return a, 0

    # Algoritmo que evita colisionamiento entre el enemigo
    # y otros objetos "colisionables"
    # Funciona de la siguiente forma: Genera una linea de rectángulos en frente
    # con los que prueba si hay colisiones. De ser así genera una aceleración
    # en sentido perpendicular a la dirección que los une
    def evitarcolision3(self):
        distancia = 40
        x = 0
        y = 0
        for i in range(1,7):
            orient =  [math.cos(math.radians(self.angulo))*distancia, math.sin(math.radians(self.angulo))*distancia]
            posicion = [self.posi[0] + orient[0], self.posi[1] + orient[1]]
            prueba = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            prueba.center = posicion
            rectangulo = pygame.sprite.Sprite()
            rectangulo.rect = prueba
            rectangulo.image = self.image
            rectangulo.add(grupo_dibujables)
            p = pygame.sprite.spritecollide(rectangulo, grupo_obstaculos, False)
            if len(p) > 0:
                for objetivo in p:             
                    modulo = math.sqrt((objetivo.posi[0] - self.posi[0])**2 + (objetivo.posi[1] - self.posi[1])**2)
                    orientacion = [(self.posi[0] - objetivo.posi[0]) / modulo, (self.posi[1] - objetivo.posi[1]) / modulo]
                    if orientacion[0] != 0:
                        x += orientacion[0]*2 / modulo**2
                    if orientacion[1] != 0:
                        y += orientacion[1]*2 / modulo**2
            distancia += 25
            rectangulo.kill()
            del rectangulo
        return [y, -x, 0], 0

    # Algoritmo simple que genera aceleración tangencial respecto
    # al objetivo. Si se usa mientras hay aceleración radial
    # el movimiento generado describe una elipse (gira)
    def girar(self):           
        modulo = math.sqrt((self.target.posi[0] - self.posi[0])**2 + (self.target.posi[1] - self.posi[1])**2)
        orientacion = [(self.posi[0] - self.target.posi[0]) / modulo, (self.posi[1] - self.target.posi[1]) / modulo]
        if orientacion[0] != 0:
            x = orientacion[0] / (modulo * 5)
        if orientacion[1] != 0:
            y = orientacion[1] / (modulo * 5)
        return [y, -x, 0], 0

