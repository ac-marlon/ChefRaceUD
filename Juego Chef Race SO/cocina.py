import sys, pygame
from chef import Chef
from receta import Receta
from recursoCuchillos import Cuchillos
from recursoLicuadora import Licuadora
from recursoHorno import Horno

size = width, height = 900, 712
speed = [0, 2]
screen = pygame.display.set_mode(size)

def main():
    pygame.init() 
    fondo = pygame.image.load("imagenes/cocina.png")
    fondorect = fondo.get_rect()
    pygame.display.set_caption( "Chef Race (Universidad Distrital)" )
    chef1 = Chef((width*(1/2), height))
    chef2 = Chef((width*(3.2/2), height))
    chef3 = Chef((width*(5.4/2), height))
    listaChefs = [chef1, chef2, chef3]
    receta = Receta(size)
    cuchillos = Cuchillos(size)
    licuadora = Licuadora(size)
    horno = Horno(size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
                
        screen.blit(fondo, fondorect)
        
        for elemento in listaChefs:
            screen.blit(elemento.image, elemento.rect)
            
        screen.blit(receta.image, receta.rect)
        screen.blit(cuchillos.image, cuchillos.rect)
        screen.blit(licuadora.image, licuadora.rect)
        screen.blit(horno.image, horno.rect)
        pygame.display.update()

if __name__ == '__main__': 
    main()
