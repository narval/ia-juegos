#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Hecho Por Isaac López Procopio
# 07-41120

import sys, pygame

# Constantes
WIDTH = 1024
HEIGHT = 650

# Grupos globales por defecto
grupo_todos = pygame.sprite.LayeredUpdates()
grupo_colisionables = pygame.sprite.RenderUpdates()
grupo_personajes = pygame.sprite.RenderUpdates()
grupo_enemigos = pygame.sprite.RenderUpdates()
grupo_dibujables = pygame.sprite.RenderUpdates()
grupo_obstaculos = pygame.sprite.RenderUpdates()
