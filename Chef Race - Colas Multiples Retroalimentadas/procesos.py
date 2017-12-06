import threading
import numpy as np
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Proceso:
    def __init__(self,idProceso,prioridad,quantum,nombre,recurso,t,tr):
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
        self.te=0
        self.prioridad=prioridad #0:max ; 1:med ; 2:min
        self.estado=0 #0:listo ; 1:blo ; 2:sus ; 3:ejecucion ; 4:terminado
    def __repr__(self):
        return repr((self.nombre, self.recurso, self.t))
    def __str__(self):
        return self.nombre+" "+str(self.idProceso)
    def bloquear(self):
        self.estado=1

    def suspender(self):
        print("asdasdasdasd mk suspendio")
        self.tr=5
        self.estado=2
        self.recurso.liberar()

    def procesar(self):
        self.estado=3
        if self.prioridad==0: self.quantum-=1
        self.t-=1
        self.zc+=1
#       print("Preparando",self.nombre,self.idProceso,"quantum",self.quantum,"t",self.t,"recurso",self.recurso)

    def asignarTiempoEnvejecimiento(self,ttotal):
        cons=20
        if self.t>=ttotal*0.7:
            self.te=cons
        elif self.t>=ttotal*0.4:
            self.te=cons*1.5
        else:
            self.te=cons*2.5


    def asignarQ(self,ttotal):
        if self.t>=ttotal*0.7:
            print(self,"ttotal",ttotal,"quantum",self.t)
            return self.t
        elif self.t>=ttotal*0.4:
            print(self,"ttotal",ttotal,"quantum",self.t)
            return round(self.t*0.8)
        else:
            print(self,"ttotal",ttotal,"quantum",self.t)
            return round(self.t*0.6)

class PolloConPapas(Sprite, Proceso):
    def __init__(self,idProceso,prioridad,recurso,cont_size,quantum=0,nombre="Pollo con papas",t=25,tr=0):
        Proceso.__init__(self,idProceso,prioridad,quantum,nombre,recurso,t,tr)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.iml = pygame.image.load("imagenes/pollolisto.png")
        self.imb = pygame.image.load("imagenes/polloblo.png")
        self.ims = pygame.image.load("imagenes/pollosus.png")
        self.ime = pygame.image.load("imagenes/polloejec.png")
        self.mini = pygame.image.load("imagenes/pollomini.png")
        self.rect = self.iml.get_rect()
        self.rect.move_ip(cont_size[0] - 200, cont_size[1] - 430)

class Malteada(Sprite, Proceso):
    def __init__(self,idProceso,prioridad,recurso,cont_size,quantum=0,nombre="Malteada",t=10,tr=0):
        Proceso.__init__(self,idProceso,prioridad,quantum,nombre,recurso,t,tr)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.iml = pygame.image.load("imagenes/malteadalisto.png")
        self.imb = pygame.image.load("imagenes/malteadablo.png")
        self.ims = pygame.image.load("imagenes/malteadasus.png")
        self.ime = pygame.image.load("imagenes/malteadaejec.png")
        self.mini = pygame.image.load("imagenes/malteadamini.png")
        self.rect = self.iml.get_rect()
        self.rect.move_ip(cont_size[0] - 200, cont_size[1] - 575)

class Ensalada(Sprite, Proceso):
    def __init__(self,idProceso,prioridad,recurso,cont_size,quantum=0,nombre="Ensalada",t=15,tr=0):
        Proceso.__init__(self,idProceso,prioridad,quantum,nombre,recurso,t,tr)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.iml = pygame.image.load("imagenes/ensaladalisto.png")
        self.imb = pygame.image.load("imagenes/ensaladablo.png")
        self.ims = pygame.image.load("imagenes/ensaladasus.png")
        self.ime = pygame.image.load("imagenes/ensaladaejec.png")
        self.mini = pygame.image.load("imagenes/ensaladamini.png")
        self.rect = self.iml.get_rect()
        self.rect.move_ip(cont_size[0] - 200, cont_size[1] - 685)
