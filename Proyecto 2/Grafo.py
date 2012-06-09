#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

from Nodo import *
from Arco import *

# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class Grafo():

    def __init__(self):
        self.lista_n = []
        self.lista_a = []
        self.num_nodos = 0
        self.num_arcos = 0
        
    def agregar_nodo(self, nodo):
        self.lista_nn += [nodo]
        self.num_nodos += 1
        
    def agregar_arco(self, arco):
        self.lista_s = self.lista_s + [arco]
        self.lista_a[nodo.get_fuente] += [arco]
        self.num_arcos += 1
        
    def to_string(self):
        salida = "O-------Grafo-------O\n\n"
        salida += "---Arcos---\n"
        salida += "# Arcos: " + str(self.num_arcos) + "\n"
        for a in self.lista_a:
            salida += a.to_string() + "\n"
        salida += "\n---Nodos---\n"
        salida += "# Nodos: " + str(self.num_nodos) + "\n"
        for n in self.lista_n:
            salida += n.to_string() + "\n"
        return salida
        

