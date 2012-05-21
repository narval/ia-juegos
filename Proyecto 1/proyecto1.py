#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Constantes import *
from Personaje import *
from Jugador import *
from Enemigo import *
from Funciones import *
from Comportamiento import *


def main():

    # variables
    tipo_control = 0
    mute = False 

    # Inicialización del programa
    num_enemigos = int(raw_input("Por favor di un numero: "))


    # Creando la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pro-proyecto1")


    # Carga la imagen del fondo
    background_image = pygame.transform.smoothscale(load_image("imagenes/fondo.jpg"), (WIDTH, HEIGHT))

    
    # Crea el jugador   
    jugador = Jugador([WIDTH /2 ,HEIGHT /2], [60,60], "imagenes/jugador3.png", [grupo_todos, grupo_personajes, grupo_dibujables, grupo_colisionables], "Jugador")
    
    objetivo = jugador


    # Crea el target (mouse)
    target_mouse = Personaje(pygame.mouse.get_pos(), [50,50], "imagenes/target.png", [grupo_todos, grupo_dibujables], "Mouse")
    pygame.mouse.set_visible(False)


    # Crea los enemigos
    for num in range(0, num_enemigos):
        Enemigo(jugador, [100*num,100], [30,30], "imagenes/aliado.png", [grupo_todos, grupo_personajes, grupo_enemigos, grupo_dibujables, grupo_colisionables],"E" + str(num)).add(grupo_enemigos)


    obstaculo1 = Personaje( [500,400], [80,80], "imagenes/obstaculo2.png", [grupo_todos, grupo_dibujables, grupo_personajes, grupo_colisionables, grupo_obstaculos], "Obstaculo1")
    pygame.mouse.set_visible(False)

    # Crea la clase de comportamientos
    comportamiento = Comportamiento()


    # Crea el reloj del juego
    clock = pygame.time.Clock()


    # Arreglo que contiene las teclas apretadas antes de comenzar
    keysanteriores = pygame.key.get_pressed()

    # inicia la fastidiosa y repetitiva musica
    sonar_musica("sonido/483578_Can-Of-Infinite-Min.mp3", -1) 

    #sonar_sonido("sonido/Bottle Rocket-SoundBible.com-332895117.mp3")

    # loop principal del juego
    while True:       
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()


        # Maneja los eventos en general
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        # Maneja el cambio en el comportamiento de los enemigos
        if not keysanteriores[K_LSHIFT] and keys[K_LSHIFT]:
            comportamiento.siguiente()

        # Maneja el tipo de control del jugador
        if not keysanteriores[K_t] and keys[K_t]:
            tipo_control = (tipo_control + 1) % 3

        #print mute, keysanteriores[K_m], keys[K_m]
        if not keysanteriores[K_m] and keys[K_m]:
            if not mute:
                pygame.mixer.music.pause()
                mute = True
            else:
                pygame.mixer.music.unpause()
                mute = False

        if not keysanteriores[K_0] and keys[K_0]:
            Enemigo(jugador, [100*num_enemigos,100], [30,30], "imagenes/aliado.png", [grupo_todos, grupo_personajes, grupo_enemigos, grupo_dibujables,       grupo_colisionables],"E" + str(num_enemigos)).add(grupo_enemigos)
            num_enemigos += 1
            
        if not keysanteriores[K_9] and keys[K_9]:
            Enemigo(jugador, [100*num_enemigos,100], [50,100], "imagenes/jefe.png", [grupo_todos, grupo_personajes, grupo_enemigos, grupo_dibujables,       grupo_colisionables],"T" + str(num_enemigos)).add(grupo_enemigos)
            num_enemigos += 1
            
        if not keysanteriores[K_p] and keys[K_p]:
            Enemigo(jugador, [100*num_enemigos,100], [70,70], "imagenes/char.png", [grupo_todos, grupo_personajes, grupo_enemigos, grupo_dibujables,       grupo_colisionables],"T" + str(num_enemigos)).add(grupo_enemigos)
            num_enemigos += 1 
            
            
        keysanteriores = keys
# ------- Manejo de los personajes y objetos

        # Texto que muestra el comportamiento actual en pantalla
        advertencia, advertencia_rect = texto("comportamiento: " + comportamiento.comportamiento_actual(), [WIDTH/2, 50], (244, 244, 244))
        control, control_rect = texto("control: " + str(tipo_control + 1), [WIDTH/8, 50], (244, 244, 244))
        objetivo_tx, objetivo_rect = texto("objetivo: " + objetivo.nombre, [(WIDTH * 4) / 5, 80], (244, 244, 244))

        # Maneja el jugador
        if tipo_control == 0:
            jugador.moverse_general(keys)
        elif tipo_control == 1:
            jugador.moverse_relativo(keys)
        elif tipo_control == 2:
            jugador.moverse_personal(keys)

        
        # Maneja el target (mouse)
        target_mouse.posi = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0]
        target_mouse.angulo = jugador.angulo
        target_mouse.rect.center = [target_mouse.posi[0], target_mouse.posi[1]]
        target_mouse.actualizar(time)

        # Maneja los enemigos
        for e in grupo_enemigos:
            e.acel, e.acel_angular = comportamiento.movimiento_total(e)
            if mouse[2]:
                e.target = target_mouse
                objetivo = target_mouse
                grupo_personajes.add(target_mouse)
            else:
                e.target = jugador
                objetivo = jugador
                grupo_personajes.remove(target_mouse)
            
        # Actualiza el estado de los personajes
        for p in grupo_personajes:
            p.actualizar(time)
            


# -------  Se dibujan los elementos en la pantalla
        # Dibuja el fondo
        screen.blit(background_image, (0, 0))

        # Dibuja los objetos dibujables
        for d in grupo_dibujables:       
            screen.blit(d.image, d.rect)
        screen.blit(jugador.image, jugador.rect)
        screen.blit(advertencia, advertencia_rect)
        screen.blit(control, control_rect)
        screen.blit(objetivo_tx, objetivo_rect)
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
