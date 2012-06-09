#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
from Jugador import *
from Personaje import *
from Enemigo import *
import math
import random

# Clase que maneja los comportamientos de los enemigos
class Maquina():

    @staticmethod
    def estados_pulpo():
        return [
            [Comportamiento.merodear_like_a_pro()]
            [Comportamiento.pulpo()]
            ]
