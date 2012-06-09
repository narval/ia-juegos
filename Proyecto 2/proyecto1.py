#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Constantes import *
from Mouse import *
from Jugador import *
from Pulpo import *
from Triangulo import *
from Funciones import *
from Comportamiento import *
from Obstaculo import *


def main():

    # variables de juego
    tipo_control = 0
    mute = False
    irect = (0, 0)
    frect = (0, 0)
    seleccion = False
    grupo_seleccionados = grupo_enemigos


    # Inicialización del programa
    #num_enemigos = int(raw_input("Por favor di un numero: "))
    num_enemigos = 4
    num_aliados = 0


    # Creando la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    # para fullscreen  
    #pygame.display.toggle_fullscreen
    pygame.display.set_caption("Pro-proyecto1")
	
    

    # Carga la imagen del fondo
    background_image = pygame.transform.smoothscale(load_image("imagenes/fondo.jpg"), (WIDTH, HEIGHT))

    
    # Crea el jugador   
    jugador = Jugador([WIDTH /2 ,HEIGHT /2], "Jugador")
    
    objetivo = jugador


    # Crea el target (mouse)
    target_mouse = Mouse(pygame.mouse.get_pos(), "Mouse")
    pygame.mouse.set_visible(False)


    # Crea los enemigos
    for num in range(0, num_enemigos):
        Pulpo([100*num,100],"E" + str(num)).add(grupo_enemigos)


    #obstaculo1 = Obstaculo( [500,400], "Obstaculo1")
    pygame.mouse.set_visible(False)



    # Crea el reloj del juego
    clock = pygame.time.Clock()


    # Arreglo que contiene las teclas apretadas antes de comenzar
    keysanteriores = pygame.key.get_pressed()
    mouse_anterior = pygame.mouse.get_pressed()
    target = jugador

    # inicia la fastidiosa y repetitiva musica
    #sonar_musica("sonido/483578_Can-Of-Infinite-Min.mp3", -1) 

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
        

        # Maneja el tipo de control del jugador
        if not keysanteriores[K_t] and keys[K_t]:
            tipo_control = (tipo_control + 1) % 3


        if not keysanteriores[K_m] and keys[K_m]:
            if not mute:
                pygame.mixer.music.pause()
                mute = True
            else:
                pygame.mixer.music.unpause()
                mute = False
         
            
        if not keysanteriores[K_p] and keys[K_p]:
            Pulpo([100*num_enemigos,100], "P" + str(num_enemigos))
            num_enemigos += 1 
            
        if not keysanteriores[K_o] and keys[K_o]:
            Triangulo([100*num_aliados,100], "T" + str(num_aliados))
            num_aliados += 1
            
        if not keysanteriores[K_RETURN] and keys[K_RETURN]:
            pygame.display.toggle_fullscreen()
            
            
        
# ------- Manejo de los personajes y objetos

        # Texto que muestra el comportamiento actual en pantalla
        #advertencia, advertencia_rect = texto("comportamiento: " + comportamiento.comportamiento_actual(), [WIDTH/2, 50], (244, 244, 244))
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
        
        """
        selector = None
        if mouse[0]:
            if seleccion:
                frect = target_mouse.rect.topleft
                rectselect = pygame.Rect(min(irect[0], frect[0]), min(irect[1],frect[1]),\
                 math.fabs(frect[0]-irect[0]), math.fabs(frect[1]-irect[1]))
                 
                selector = Personaje([rectselect.centerx, rectselect.centery], \
                [rectselect.width + 1, rectselect.height+ 1], "imagenes/selector.png", [grupo_todos, grupo_dibujables], "selector")
                grupo_seleccionados = pygame.sprite.spritecollide(selector, grupo_enemigos, False)
                if grupo_seleccionados == []:
                    grupo_seleccionados = grupo_enemigos
                #print grupo_seleccionados
                
            else:
                seleccion = True
                irect = target_mouse.rect.topleft
        else:
            seleccion = False
        """
        
                

        if mouse[2]:
            grupo_colisionables.add(target_mouse)
            colisiones = target_mouse.colisionar()
            if len(colisiones) == 1:
                target = colisiones[0]
                objetivo = colisiones[0]
                grupo_personajes.remove(target_mouse)
            elif len(colisiones) == 0:
                target = target_mouse
                objetivo = target_mouse
            grupo_colisionables.remove(target_mouse)
            
            
        
        
        # Maneja los enemigos
        
        for e in grupo_seleccionados:
            # Maneja el cambio en el comportamiento de los enemigos
            #if not keysanteriores[K_LSHIFT] and keys[K_LSHIFT]:
            #    e.siguiente_comportamiento()
            #print grupo_seleccionados
            e.target = target
            e.moverse()
            
        for a in grupo_aliados:
            a.target = target
            a.moverse()
            
                    
                    
                    

       
            
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
        #screen.blit(advertencia, advertencia_rect)
        screen.blit(control, control_rect)
        screen.blit(objetivo_tx, objetivo_rect)
        pygame.display.flip()
        
        """
        if selector != None:
            selector.kill()
            del selector
        """
            
        keysanteriores = keys
        mouse_anterior = mouse
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
