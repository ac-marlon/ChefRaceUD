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

class Horno(Recurso, Sprite):
    def __init__(self, cont_size, nombre="Horno"):
        Recurso.__init__(self,nombre)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/horno.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 430, cont_size[1] - 430)       

class Cuchillos(Recurso, Sprite):
    def __init__(self, cont_size, nombre="Cuchillos"):
        Recurso.__init__(self,nombre)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cuchillos.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 420, cont_size[1] - 685)         

class Licuadora(Recurso, Sprite):
    def __init__(self, cont_size, nombre="Licuadora"):
        Recurso.__init__(self,nombre)
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/licuadora.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 390, cont_size[1] - 575)        
