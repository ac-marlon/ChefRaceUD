import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class ComensalAlto(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cliente1.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 135, cont_size[1] - 690)

class ComensalMedio(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cliente2.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 135, cont_size[1] - 460)
        
class ComensalBajo(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cliente3.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 135, cont_size[1] - 220)
