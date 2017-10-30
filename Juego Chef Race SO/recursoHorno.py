import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Horno(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/horno.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 130, cont_size[1] - 430)
