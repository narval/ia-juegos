#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
from Jugador import *
from Personaje import *
from Enemigo import *
import math
import random

# Clase que maneja los comportamientos de los enemigos
class Comportamiento():
    def __init__(self):
        self.comportamiento = self.defecto()
        self.actual = 0

    # Función que devuelve un String con el nombre del comportamiento
    # que se está ejecutando actualmente
    def comportamiento_actual(self):
        return self.comportamientos()[self.actual][0]

    # Función que cambia el comportamiento actual por el siguiente
    # en la lista
    def siguiente(self):
        self.actual = (self.actual + 1) % (len(self.comportamientos()))
        self.comportamiento = self.comportamientos()[self.actual][1]()

    # Función que devuelve la lista indexada (diccionario) con los
    # nombres de los comportamientos y una instancia de sus métodos
    @staticmethod
    def comportamientos():
        return [
            ["defecto"    ,                 Comportamiento.defecto],
            ["delfin"    ,                  Comportamiento.delfin],
            ["pulpo"    ,                   Comportamiento.pulpo],
            ["caza" ,                       Comportamiento.caza],
            ["rodear" ,                     Comportamiento.rodear],
            ["huir" ,                       Comportamiento.huir],
            ["merodear_tontamemte" ,        Comportamiento.merodear_tontamemte],
            ["merodear_like_a_boss" ,       Comportamiento.merodear_like_a_boss],
            ["merodear_like_a_pro" ,        Comportamiento.merodear_like_a_pro],
            ["bailar" ,                     Comportamiento.bailar],
            ["defender" ,                   Comportamiento.defender],
            ["defender_alinearse" ,         Comportamiento.defender_alinearse],
            ["rodear_amenazantemente" ,     Comportamiento.rodear_amenazantemente],
            ["defensa_giratoria" ,          Comportamiento.defensa_giratoria]
            ]

    # Función que devuelve la lista indexada de los nombres de los
    # algoritmos de movientos de los enemigos y su método
    @staticmethod
    def movimientos():
        return { 
            "seek"    :             Enemigo.seek,
            "seek_llegada" :        Enemigo.seek_llegada,
            "flee" :                Enemigo.flee,
            "flee_llegada" :        Enemigo.flee_llegada,
            "face" :                Enemigo.face,
            "anti_face" :           Enemigo.anti_face,
            "face_frente" :         Enemigo.face_frente,
            "ir_nadando" :          Enemigo.ir_nadando,
            "ir_pulpo" :            Enemigo.ir_pulpo,
            "wandering" :           Enemigo.wandering,
            "kinematic_wander" :    Enemigo.kinematic_wander,
            "ir_derecho" :          Enemigo.ir_derecho,
            "alinearse" :           Enemigo.alinearse,
            "velocity_match" :      Enemigo.velocitymatch,
            "separacion" :          Enemigo.separacion,
            "evitarcolision" :      Enemigo.evitarcolision,
            "evitarcolision2" :     Enemigo.evitarcolision2,
            "evitarcolision3" :     Enemigo.evitarcolision3,
            "girar" :               Enemigo.girar
            }

#------ Sección de comportamientos
#-----En esta sección se listan y ponderan los algoritmos
#-----que componen cada comportamiento
    @staticmethod
    def defecto():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          1],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def delfin():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         1],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_nadando" ,          1],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          1],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def caza():
        return [
            ["seek"    ,             2],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                1],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          4],
            ["evitarcolision2" ,     1],
            ["evitarcolision3" ,    10]
            ]

    @staticmethod
    def rodear():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        4],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                1],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          5],
            ["evitarcolision" ,      0]
            ]
            
    @staticmethod
    def pulpo():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                1],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_pulpo" ,            1],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          1],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def rodear_amenazantemente():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        4],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                1],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          6],
            ["girar" ,               1]
            ]

    @staticmethod
    def huir():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                1],
            ["flee_llegada" ,        1],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         1],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          4],
            ["evitarcolision" ,      0]
            ]


    @staticmethod
    def merodear_tontamemte():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         1],
            ["wandering" ,           1],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          0],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def merodear_like_a_boss():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         1],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          1],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          1],
            ["evitarcolision" ,      1]
            ]

    @staticmethod
    def merodear_like_a_pro():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         1],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          1],
            ["alinearse" ,           0],
            ["velocity_match" ,      0],
            ["separacion" ,          1],
            ["evitarcolision2" ,     1]
            ]

    @staticmethod
    def bailar():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           1],
            ["velocity_match" ,      1],
            ["separacion" ,          1],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def defender():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        5],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           1],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      1],
            ["separacion" ,          7],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def defender_alinearse():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        5],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           1],
            ["face_frente" ,         0],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           2],
            ["velocity_match" ,      1],
            ["separacion" ,          7],
            ["evitarcolision" ,      0]
            ]

    @staticmethod
    def defensa_giratoria():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        5],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         3],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      1],
            ["separacion" ,         10],
            ["girar" ,               4]
            ]

    @staticmethod
    def You_shall_not_pass():
        return [
            ["seek"    ,             0],
            ["seek_llegada" ,        0],
            ["flee" ,                0],
            ["flee_llegada" ,        0],
            ["face" ,                0],
            ["anti_face" ,           0],
            ["face_frente" ,         3],
            ["wandering" ,           0],
            ["kinematic_wander" ,    0],
            ["ir_derecho" ,          0],
            ["alinearse" ,           0],
            ["velocity_match" ,      1],
            ["separacion" ,         10],
            ["girar" ,               4]
            ]

# ------- Fin area de comportamientos

    # Función que calcula el vextor aceleración y la aceleración angular
    # resultante de aplicar los comportamientos sobre un enemigo
    def movimiento_total(self, enemigo):
        aceleracion = [0, 0, 0]
        acel_angular = 0
        for algoritmo in range(0, len(self.comportamiento)):
            if self.comportamiento[algoritmo][1] != 0:
                com = self.movimientos()[self.comportamiento[algoritmo][0]]
                aceleracion = suma_v(aceleracion, escalar_v(com(enemigo)[0], self.comportamiento[algoritmo][1]))
                acel_angular += com(enemigo)[1] * self.comportamiento[algoritmo][1]    
        return aceleracion, acel_angular
