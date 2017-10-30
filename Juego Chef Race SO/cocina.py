import sys, pygame, util
from chef import Chef
from receta import Receta
from recursoCuchillos import Cuchillos
from recursoLicuadora import Licuadora
from recursoHorno import Horno
from pizarra import Pizarra
import time

size = width, height = 900, 712
screen = pygame.display.set_mode(size)

def main():
    pygame.init()
    pygame.mixer.init()
    
    fondo = pygame.image.load("imagenes/cocina.png")
    intro = pygame.image.load("imagenes/intro.png")
    fondorect = fondo.get_rect()
    introrect = intro.get_rect()
    
    pygame.display.set_caption( "Chef Race (Universidad Distrital)" )
    pizarra = pygame.image.load("imagenes/pizarra.png")
    sInicio = util.cargar_sonido('sonidos/inicio.wav')
    sHorno = util.cargar_sonido('sonidos/horno.wav')
    sCuchillo = util.cargar_sonido('sonidos/cuchillo.wav')
    sLicuadora = util.cargar_sonido('sonidos/licuadora.wav')
    sPrincipal = util.cargar_sonido('sonidos/principal.wav')
    
    chef1 = Chef((width-900,height))
    chef2 = Chef((width-700,height))
    chef3 = Chef((width-500,height))
    pizarra1 = Pizarra((width-900,height))
    pizarra2 = Pizarra((width-700,height))
    pizarra3 = Pizarra((width-500,height))
    receta1 = Receta((width,height))
    receta2 = Receta((width+200,height))
    receta3 = Receta((width+400,height))
    
    listaChefs = [chef1, chef2, chef3]
    listaPizarras = [pizarra1, pizarra2, pizarra3]
    listaRecetas = [receta1, receta2, receta3]
    cuchillos = Cuchillos(size)
    licuadora = Licuadora(size)
    horno = Horno(size)
    
    reloj = pygame.time.Clock()
    fuente1 = pygame.font.Font(None,70)
    fuente2 = pygame.font.Font(None,25)
    textoBienvenida = fuente1.render("Bienvenido a Chef Race UD", 1, (255,255,255))
    textoAutor1 = fuente2.render("Marlon Arias", 1, (0,0,0))
    textoAutor2 = fuente2.render("David Amado", 1, (0,0,0))
    textoAutor3 = fuente2.render("Realizado por:", 1, (0,0,0))

    sInicio.play()
    aux = 3
    
    while aux > 0:  
        screen.blit(intro, introrect)
        screen.blit(textoAutor1,(width-170,height-680))
        screen.blit(textoAutor2,(width-170,height-660))
        screen.blit(textoAutor3,(width-170,height-700))
        screen.blit(textoBienvenida,((width-880, (height/2)+30)))
        pygame.display.update()
        time.sleep(1)
        aux=aux-1
        
    sPrincipal.play(1)

    while 1:    
        reloj.tick(30)
        
        for event in pygame.event.get():   
            if event.type == pygame.QUIT: 
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(810, 881):
                    for y in range(137, 257):
                        if event.button == 1 and event.pos == (x, y):
                            chef1.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-700, +70)
                        elif event.button == 2 and event.pos == (x, y):
                            chef2.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-505, +70)
                        elif event.button == 3 and event.pos == (x, y):
                            chef3.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-305, +70)
                            
                for x in range(770, 890):
                    for y in range(282, 402):
                        if event.button == 1 and event.pos == (x, y):
                            chef1.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-690, +45)
                        elif event.button == 2 and event.pos == (x, y):
                            chef2.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-490, +45)
                        elif event.button == 3 and event.pos == (x, y):
                            chef3.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-290, +45)

                for x in range(780, 900):
                    for y in range(27, 125):
                        if event.button == 1 and event.pos == (x, y):
                            chef1.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-700, +95)
                        elif event.button == 2 and event.pos == (x, y):
                            chef2.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-500, +95)
                        elif event.button == 3 and event.pos == (x, y):
                            chef3.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-300, +95)
             
        for elemento in listaChefs:
            elemento.update()
            
        time.sleep(0.5)
        screen.blit(fondo, fondorect)
        
        for elemento in listaChefs:
            screen.blit(elemento.image, elemento.rect)

        for elemento in listaPizarras:
            screen.blit(elemento.image, elemento.rect)

        for elemento in listaRecetas:
            screen.blit(elemento.image, elemento.rect)

        screen.blit(cuchillos.image, cuchillos.rect)
        screen.blit(licuadora.image, licuadora.rect)
        screen.blit(horno.image, horno.rect)
        
        pygame.display.update()

if __name__ == '__main__': 
    main()
