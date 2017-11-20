import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Pizarra(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/pizarra.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] + 80 , cont_size[1] - 600)
        self.arregloRecetas=[]
