#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame
import math
from Funciones import *
from Constantes import *

class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        grupo_todos.add(self)
