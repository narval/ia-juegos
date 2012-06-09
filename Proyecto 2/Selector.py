#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

class Selector():
    def __init__(self):
        self.primera = [0, 0]
        self.ultima = [1, 1]
        self.seleccionando = False
        
    def inicio(self):
        self.seleccionando = True
        self.primera = target_mouse.rect.topleft
        
    del final(self):
        self.seleccion = False
        self.ultima = target_mouse.rect.topleft
        
        rectselect = pygame.Rect(min(irect[0], frect[0]), min(irect[1],frect[1]),\
                 math.fabs(frect[0]-irect[0]), math.fabs(frect[1]-irect[1]))
        
    
