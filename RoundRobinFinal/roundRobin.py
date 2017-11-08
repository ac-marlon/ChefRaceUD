import cola
import time
import procesos as ps
import recursos as rs
import queue
import threading
import numpy as np
import pygame
from pygame.sprite import Sprite
from pygame.locals import *
import util
import sys, pygame, util
from receta import Receta
from recursos import CuchillosIma
from recursos import LicuadoraIma
from recursos import HornoIma
from pizarra import Pizarra
from procesos import PolloConPapasIma
from procesos import MalteadaIma
from procesos import EnsaladaIma
import time

size = width, height = 900, 712
screen = pygame.display.set_mode(size)

class Procesador(threading.Thread):
    def __init__(self,idProcesador,*args):
        threading.Thread.__init__(self)
        self.idProcesador=idProcesador 
        self.proceso=None
        self.lis=cola.Cola()
        self.ter=cola.Cola()
        self.blo=cola.Cola()
        self.sus=cola.Cola()
        self._args=args
        self.uso=True
        self.ttotal=0
        
    def __str__(self):
        return str(self.idProcesador)
        
    def run(self):
        while self.uso:
            self.usarProcesador(*self._args)
            
    def usarProcesador(self,q):
        while not self.proceso==None or not q.empty() or not self.lis.es_vacia() or not self.sus.es_vacia() or not self.blo.es_vacia():
            time.sleep(1)
            
            if not q.empty():
                nuevo=q.get()
                self.asignar(nuevo)
                self.ttotal+=nuevo.t
            if not self.lis.es_vacia() and self.proceso==None:
                posible=self.lis.desencolar()
                if posible.recurso.libre:
                    self.ocupado=True
                    self.proceso=posible
                    self.proceso.recurso.libre=False
                    print("\ncomenzando proceso",self.proceso,"en el procesador",self)
                else:
                    print("\nel proceso",posible,"requiere de un recurso ocupado, encolando en bloqueado")
                    self.blo.encolar(posible)
            
            self.contarColaBlo()
            self.contarColaLis()            
            self.revisarColaSus()
            self.revisarColaBlo()
            
            if not self.proceso==None:
                self.proceso.procesar()
                self.ttotal-=1
                if self.proceso.t>0 and self.proceso.quantum==0:
                    self.proceso.tr=5
                    self.proceso.recurso.libre=True
                    self.sus.encolar(self.proceso)
                    print("\nse reencolo el proceso",self.proceso,"a suspendidos")
                    self.proceso=None
                elif self.proceso.t==0:
                    self.proceso.recurso.libre=True                    
                    print("\nterminando proceso",self.proceso,"en el procesador",self,",sus",self.proceso.sus,",lis",self.proceso.lis,",blo",self.proceso.blo,",zona critica",self.proceso.zc)
                    self.ter.encolar(self.proceso)
                    self.proceso=None
                    q.task_done()
        print("termino el procesador",self,"lista de tareas completadas en este procesador:")
        for i in range(self.ter.tam):
            print(self.ter.desencolar())
        self.uso=False
        
    def revisarColaSus(self):
        tam = self.sus.tam
        for i in range(tam):
            n=self.sus.desencolar()
            n.tr-=1
            n.sus+=1
            if n.tr==0:
                self.asignar(n)
                print("\nse saco el proceso",n,"de la cola de suspendidos y entro a la cola de listo")
            else:
                self.sus.encolar(n)
                
    def revisarColaBlo(self):
        for i in range(self.blo.tam):
            posible=self.blo.desencolar()
            print(posible,posible.recurso,posible.recurso.libre)
            if posible.recurso.libre:
                self.asignar(posible)
                print("\nse saco el proceso",posible," de la cola de bloqueados y entro en la cola de listos")
            else:
                self.blo.encolar(posible)

    def contarColaLis(self):
        tam = self.lis.tam

        for i in range(tam):
            n=self.lis.desencolar()
            n.lis+=1
            self.lis.encolar(n)
            

    def contarColaBlo(self):
        tam = self.blo.tam
        for i in range(self.blo.tam):
            n=self.blo.desencolar()
            n.blo+=1
            self.blo.encolar(n)
    
    def asignar(self,proceso):
        proceso.quantum=proceso.asignarQ(self.ttotal)
        self.lis.encolar(proceso)

class cliente:
    def __init__(self):
        self.numPo=0
        self.numMa=0
        self.numEn=0
        
        self.recursos=[rs.Horno(),rs.Cuchillos(),rs.Licuadora()]
        
        self.cola1=queue.Queue()
        self.cola1.put(ps.Malteada(0,self.recursos[2]))
        self.numMa+=1

        self.cola2=queue.Queue()
        self.cola2.put(ps.PolloConPapas(0,self.recursos[0]))
        self.numPo+=1

        self.cola3=queue.Queue()
        self.cola3.put(ps.Ensalada(0,self.recursos[1])) 
        self.numEn+=1

        self.colaProcesadores=queue.Queue()
        
        self.procesador1=Procesador(1,self.cola1)        
        self.procesador2=Procesador(2,self.cola2)      
        self.procesador3=Procesador(3,self.cola3)

    def iniciar(self):        
        self.procesador1.start()
        self.procesador2.start()
        self.procesador3.start()
        
        for i in range(15):
            s=np.random.randint(3)
            if s == 0:
                self.cola1.put(self.crear_pedido_aleatorio())
            elif s == 1:
                self.cola2.put(self.crear_pedido_aleatorio())
            else: 
                self.cola3.put(self.crear_pedido_aleatorio())
        
        self.cola1.join()
        self.cola2.join()
        self.cola3.join()

    def crear_pedido_aleatorio(self):
        aleatorio=np.random.randint(3)
        print("Aleatorio es:", aleatorio)
        aux=aleatorio+1
        print("Recursos: " + "1 = Licuadora" + "2 = Cuchillos" + "3 = Horno")
        if aleatorio==0:
            print("El recurso a elegir es: Licuadora")
            main.chef1.estado="trabajandoLicuadora1"
            a=ps.PolloConPapas(self.numPo,self.recursos[0])
            self.numPo+=1
        elif aleatorio==1:
            print("El recurso a elegir es: Cuchillos")
            main.chef2.estado="trabajandoCuchillo1"
            a=ps.Ensalada(self.numEn,self.recursos[1])
            self.numEn+=1
        else:
            print("El recurso a elegir es: Horno")
            main.chef3.estado="trabajandoHorno1"
            a= ps.Malteada(self.numMa,self.recursos[2])
            self.numMa+=1
        return a

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
    
    main.chef1 = Chef((width-900,height))
    main.chef2 = Chef((width-700,height))
    main.chef3 = Chef((width-500,height))
    pizarra1 = Pizarra((width-900,height))
    pizarra2 = Pizarra((width-700,height))
    pizarra3 = Pizarra((width-500,height))
    receta1 = Receta((width,height))
    receta2 = Receta((width+200,height))
    receta3 = Receta((width+400,height))
    
    listaChefs = [main.chef1, main.chef2, main.chef3]
    listaPizarras = [pizarra1, pizarra2, pizarra3]
    listaRecetas = [receta1, receta2, receta3]
    cuchillos = CuchillosIma(size)
    licuadora = LicuadoraIma(size)
    horno = HornoIma(size)
    
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
                            main.chef1.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-700, +70)
                            eventop1.set()
                        elif event.button == 2 and event.pos == (x, y):
                            main.chef2.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-505, +70)  
                            eventop1.set()                          
                        elif event.button == 3 and event.pos == (x, y):
                            main.chef3.estado = "trabajandoLicuadora1"
                            sLicuadora.play()
                            licuadora.rect.move_ip(-305, +70)
                            eventop1.set()
                            
                for x in range(770, 890):
                    for y in range(282, 402):
                        if event.button == 1 and event.pos == (x, y):
                            main.chef1.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-690, +45)
                            eventop2.set()
                        elif event.button == 2 and event.pos == (x, y):
                            main.chef2.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-490, +45)
                            eventop2.set()
                        elif event.button == 3 and event.pos == (x, y):
                            main.chef3.estado = "trabajandoHorno1"
                            sHorno.play()
                            horno.rect.move_ip(-290, +45)
                            eventop2.set()

                for x in range(780, 900):
                    for y in range(27, 125):
                        if event.button == 1 and event.pos == (x, y):
                            main.chef1.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-700, +95)
                            eventop3.set()
                        elif event.button == 2 and event.pos == (x, y):
                            main.chef2.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-500, +95)
                            eventop3.set()
                        elif event.button == 3 and event.pos == (x, y):
                            main.chef3.estado = "trabajandoCuchillo1"
                            sCuchillo.play()
                            cuchillos.rect.move_ip(-300, +95)
                            eventop3 .set()
             
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
        
eventop1 = threading.Event() 
eventop2 = threading.Event()
eventop3 = threading.Event()
hiloAnimacion = threading.Thread(name='Animacion', target = main)
cliente = cliente()

if __name__ == '__main__':
    hiloAnimacion.start()
time.sleep(6)  
cliente.iniciar()
