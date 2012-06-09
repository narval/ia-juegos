#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120


# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class Nodo():

    def __init__(self, (x, y), id=0):
        self.x = x
        self.y = y
        self.id = id
        
    def get_coordenadas():
        return (self.x, self.y)
        
    def get_id():
        return self.id
        
        
        
    def to_string(self):
        return "Nodo(" + str(self.id) + ", (" + str(self.x) + ", " + str(self.y) + "))"
        
    
