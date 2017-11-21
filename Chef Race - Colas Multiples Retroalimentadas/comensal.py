import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Comensal(Sprite):
    def __init__(self, cont_size):
        Sprite.__init__(self)
        self.cont_size = cont_size
        self.image1 = pygame.image.load("imagenes/cliente1.png")
        self.image2 = pygame.image.load("imagenes/cliente2.png")
        self.image3 = pygame.image.load("imagenes/cliente3.png")
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect3 = self.image3.get_rect()
        self.rect1.move_ip(cont_size[0] - 85, cont_size[1] - 590)
        self.rect2.move_ip(cont_size[0] - 85, cont_size[1] - 360)
        self.rect3.move_ip(cont_size[0] - 85, cont_size[1] - 120)
        self.arregloPrioridad=[]
