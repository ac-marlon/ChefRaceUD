import threading
import numpy as np
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Proceso:
    def __init__(self,idProceso,quantum,nombre,recurso,t,tr):
        self.idProceso=idProceso
        self.nombre=nombre
        self.recurso=recurso
        self.t=t
        self.tr=tr
        self.quantum=quantum
        self.sus=0
        self.blo=0
        self.lis=0
        self.zc=0
        
    def __str__(self):
        return self.nombre+" "+str(self.idProceso)
        
    def procesar(self):
        self.quantum-=1
        self.t-=1
        self.zc+=1
        print("Preparando",self.nombre,self.idProceso,"quantum",self.quantum,"t",self.t,"recurso",self.recurso)
            
    def asignarQ(self,ttotal): 
        if self.t>=ttotal*0.7:
            return self.t
        elif self.t>=ttotal*0.4:
            return round(self.t*0.6)
        else:
            return round(self.t*0.4)

class PolloConPapas(Proceso):
    def __init__(self,idProceso,recurso,quantum=0,nombre="Pollo con papas",t=25,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)
        
class PolloConPapasIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/pollo.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] + 80 , cont_size[1] - 600)

class Malteada(Proceso):
    def __init__(self,idProceso,recurso,quantum=0,nombre="Malteada",t=10,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)

class MalteadaIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/malteada.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] + 80 , cont_size[1] - 600)

class Ensalada(Proceso):
    def __init__(self,idProceso,recurso,quantum=0,nombre="Ensalada",t=15,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)
        
class EnsaladaIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/ensalada.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] + 80 , cont_size[1] - 600)


