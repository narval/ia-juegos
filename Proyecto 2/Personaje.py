#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *
from Objeto import *
import random

# Clase principal de los ejementos moviles en el juego
class Personaje(Objeto):

    def __init__(self):
        grupo_dibujables.add(self)
        grupo_colisionables.add(self)
        grupo_actualizables.add(self)
        grupo_personajes.add(self)
        Objeto.__init__(self)
        self.tipo_estado = 0
            
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
            if len(self.colisionar()) > 0:
                self.angulo = angulo_anterior
                self.image = imagen_anterior
                self.rect = rectangulo_anterior
                self.rect.center = [self.posi[0], self.posi[1]]
                self.mask = pygame.mask.from_surface(self.image)

        # Segunda revisada para saber si estan incrustados dos objetos
        if self.colisionable:
            if len(self.colisionar()) > 0:
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
            salida = []
            for objetivo in p:
                if objetivo != self:
                    
                    #print self.nombre, " casi colisiona con ", objetivo.nombre
                    if pygame.sprite.collide_mask(self, objetivo):
                        #print self.nombre, " colisiona con ", objetivo.nombre
                        salida = salida + [objetivo]
            return salida
        return []               

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
        
#------------------------ ALgoritmos ----------------------------#

    # algoritmo de busqueda simple    
    def seek(self, target):
        target = target.posi
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
    def seek_llegada(self, target):
        target = target.posi
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
    def flee(self, target):
        target = target.posi
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
    def flee_llegada(self, target):
        target = target.posi
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
    def face(self, target):
        target = target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        angulon = math.degrees(math.atan2(diry, dirx))
        return [0, 0, 0], self.ajustar_angulo(angulon)

    # Algoritmo con conducta opuesta face
    # es decir que orienta al enemigo en dirección
    # opuesta de donde se encuentra el objetivo     
    def anti_face(self, target):
        target = target.posi
        dirx = target[0] - self.posi[0]
        diry = target[1] - self.posi[1]
        angulon = math.degrees(math.atan2(diry, dirx))
        return [0, 0, 0], -self.ajustar_angulo(angulon)

    # Algoritmo que orienta la dirección del enemigo
    # en el sentido de su velocidad actual (solo para los
    # ejes x, y    
    def face_frente(self, target):
        angulo = math.degrees(math.atan2(self.vel[1], self.vel[0]))
        return [0, 0, 0], self.ajustar_angulo(angulo)

    # Algoritmo de "deambulamiento" simple
    # funciona con dos numeros al azar que sirven para
    # setear una dirección y un tiempo
    # durante ese tiempo el enemigo se moverá hacia esa
    # dirección, para luego elegir una nueva    
    def wandering(self, target):
        self.tiempo -= 1
        if self.tiempo < 0:
            self.tiempo = int(random.uniform(1, 50))
            valor = random.uniform(-1, 1)
            return [0, 0, 0], (valor * 0.1)
        else:            
            return self.ir_derecho(target)

    # Algoritmo de "deambulamiento" cinemático en el que
    # se proyecta una circunferencia en frente del enemigo
    # y luego se elije un punto al azar del borde. Dicho punto
    # será el objetivo hacia el cual se moverá el enemigo    
    def kinematic_wander(self, target):
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
    def ir_derecho(self, target):
        return [math.cos(math.radians(self.angulo))*0.003, math.sin(math.radians(self.angulo))*0.003, 0], 0

    
    def ir_nadando(self, target):
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
    
    

    # Algoritmo que cambia la dirección actual por la dirección 
    # del objetivo    
    def alinearse(self, target):
        salida = [0, 0, 0], self.ajustar_angulo(target.angulo)
        return salida

    # Algoritmo cuya funcion es la de acelerár en el sentido
    # en que se mueve el objetivo hasta que alcanza su velocidad    
    def velocitymatch(self, target):
        target = target.vel
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
    def separacion(self, target):
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
    def evitarcolision(self, target):
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
    def evitarcolision2(self, target):
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
    def evitarcolision3(self, target):
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
    def girar(self, target):           
        modulo = math.sqrt((target.posi[0] - self.posi[0])**2 + (target.posi[1] - self.posi[1])**2)
        orientacion = [(self.posi[0] - target.posi[0]) / modulo, (self.posi[1] - target.posi[1]) / modulo]
        if orientacion[0] != 0:
            x = orientacion[0] / (modulo * 5)
        if orientacion[1] != 0:
            y = orientacion[1] / (modulo * 5)
        return [y, -x, 0], 0

