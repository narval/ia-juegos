#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Hecho Por Isaac López Procopio
# 07-41120

from Nodo import *
from Arco import *
from Grafo import *

# Clase para los enemigos u aliados según sea el caso
# Son los personajes con inteligencia
class main_grafo():

    def main():
        mapa = Grafo()
        mapa.agregar_nodo(Nodo((0,1), "nodo1"))
        mapa.agregar_nodo(Nodo((0,0), "nodo2"))
        mapa.agregar_arco(Nodo((0,1), "nodo1"))
        print mapa.to_string()
        
        return 0
        
    main()
