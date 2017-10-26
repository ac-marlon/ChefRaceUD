import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Cuchillos(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image = pygame.image.load("imagenes/cuchillos.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(cont_size[0] - 120, cont_size[1] - 685)

    def update():
        #animacion sprite
        0
