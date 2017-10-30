import pygame
from pygame.sprite import Sprite
from pygame.locals import *
import util

class Chef(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.estados = ["espera", "trabajandoCuchillo1", "trabajandoCuchillo2",
                        "trabajandoHorno1", "trabajandoHorno2",
                        "trabajandoLicuadora1", "trabajandoLicuadora2"]
        self.estado = self.estados[0]
        self.imagenes = [util.cargar_imagen('imagenes/chef.png'),
                                        util.cargar_imagen('imagenes/chefCuchi.png'),
                                        util.cargar_imagen('imagenes/chefCuchi2.png'),
                                        util.cargar_imagen('imagenes/chefHorno.png'),
                                        util.cargar_imagen('imagenes/chefHorno2.png'),
                                        util.cargar_imagen('imagenes/chefLicu.png'),
                                        util.cargar_imagen('imagenes/chefLicu2.png')]
        self.image = self.imagenes[0]
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0], cont_size[1]-250)

    def update(self):
        #animacion sprite
        if self.estado == self.estados[0]:
            self.image = self.imagenes[0]
            
        elif self.estado == self.estados[1]:
            self.image = self.imagenes[1]
            self.estado = self.estados[2]
            
        elif self.estado == self.estados[2]:
            self.image = self.imagenes[2]
            self.estado = self.estados[1]
            
        elif self.estado == self.estados[3]:
            self.image = self.imagenes[3]
            self.estado = self.estados[4]
            
        elif self.estado == self.estados[4]:
            self.image = self.imagenes[4]
            self.estado = self.estados[3]
            
        elif self.estado == self.estados[5]:
            self.image = self.imagenes[5]
            self.estado = self.estados[6]
            
        elif self.estado == self.estados[6]:
            self.image = self.imagenes[6]
            self.estado = self.estados[5]
