#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120


# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class Arco():

    def __init__(self, (origen, destino), id=0):
        self.origen = origen
        self.destino = destino
        self.costo = math.sqrt((destino[0] - origen[0])**2 + (destino[1] - origen[1])**2)
        self.id = id
        
    def get_costo():
        return self.costo

    def origen():
        return self.origen
        
    def destino():
        return self.destino
        
    def id():
        return self.id    
        
    def inverso(self):
        return Arco((self.destino, self.origen), self.id)
        
    def to_string(self):
        return "Arco(" + self.id + ", (" + self.origen + ", " + self.destino + "))"
