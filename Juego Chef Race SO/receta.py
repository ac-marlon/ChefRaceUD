import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Receta(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/receta.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0]-800, cont_size[1] - 695)
