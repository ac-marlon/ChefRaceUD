import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Recurso:
    def __init__(self,nombre):
        self.nombre=nombre
        self.libre=True
        
    def __str__(self):
        return(self.nombre)
        
    def utilizar(self):
        if self.libre:
            print("usando el",self.nombre)
            self.libre=False
        else:
            print("el",self.nombre,"esta ocupado")
            
    def liberar(self):
        if not self.libre:
            print("el",self.nombre,"fue liberado")
            self.libre=True
        else:
            print("el",self.nombre,"no estaba siendo usado")

class Horno(Recurso):
    def __init__(self,nombre="Horno"):
        Recurso.__init__(self,nombre)
        
class HornoIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/horno.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 130, cont_size[1] - 430)        

class Cuchillos(Recurso):
    def __init__(self,nombre="Cuchillos"):
        Recurso.__init__(self,nombre)

class CuchillosIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cuchillos.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 120, cont_size[1] - 685)        

class Licuadora(Recurso):
    def __init__(self,nombre="Licuadora"):
        Recurso.__init__(self,nombre)
        
class LicuadoraIma(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        speed = [0, 2]
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/licuadora.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 90, cont_size[1] - 575)        
