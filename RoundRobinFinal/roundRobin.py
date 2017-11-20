import cola
import time
from procesos import *
import recursos as rs
import queue
import threading
import numpy as np
import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mouse import *
import util
import sys, pygame, util
from receta import Receta
from recursos import *
from pizarra import Pizarra

size = width, height = 900, 712
screen = pygame.display.set_mode(size)
mutex = threading.Lock()

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
		self.minIter=50

	def __str__(self):
		return str(self.idProcesador)

	def run(self):
		while self.uso:
			self.usarProcesador(*self._args)

	def usarProcesador(self,q):
		while not self.proceso==None or not q.empty() or not self.lis.es_vacia() or not self.sus.es_vacia() or not self.blo.es_vacia() or self.minIter>0:
			time.sleep(2.5) #tiempo para cada accion en el procesador
			self.minIter-=1
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
					self.proceso.estado=3
#					print("\ncomenzando proceso",self.proceso,"en el procesador",self)
				else:
#					print("\nel proceso",posible,"requiere de un recurso ocupado, encolando en bloqueado")
					self.blo.encolar(posible)
					posible.estado=1

			self.contarColaBlo()
			self.contarColaLis()
			self.revisarColaSus()
			self.revisarColaBlo()

			if not self.proceso==None:
				self.proceso.procesar()
				print("procesador",self,"con",self.proceso)
				self.ttotal-=1
				if self.proceso.t>0 and self.proceso.quantum==0:
					self.proceso.tr=5
					self.proceso.recurso.libre=True
					self.sus.encolar(self.proceso)
					self.proceso.estado=2
#					print("\nse reencolo el proceso",self.proceso,"a suspendidos")
					self.proceso=None
				elif self.proceso.t==0:
					self.proceso.recurso.libre=True
#					print("\nterminando proceso",self.proceso,"en el procesador",self,",sus",self.proceso.sus,",lis",self.proceso.lis,",blo",self.proceso.blo,",zona critica",self.proceso.zc)
					self.ter.encolar(self.proceso)
					self.proceso.estado=4
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
#				print("\nse saco el proceso",n,"de la cola de suspendidos y entro a la cola de listo")
			else:
				self.sus.encolar(n)

	def revisarColaBlo(self):
		for i in range(self.blo.tam):
			posible=self.blo.desencolar()
			if posible.recurso.libre:
				self.asignar(posible)
#				print("\nse saco el proceso",posible," de la cola de bloqueados y entro en la cola de listos")
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
		proceso.estado=0
		self.lis.encolar(proceso)

class Cliente:
	def __init__(self):
		self.numPo=0
		self.numMa=0
		self.numEn=0

		self.recursos=[rs.Horno(size),rs.Cuchillos(size),rs.Licuadora(size)]
		self.cola1=queue.Queue()
		self.cola2=queue.Queue()
		self.cola3=queue.Queue()

		self.colaProcesadores=queue.Queue()
		self.procesador1=Chef((width-900,height),1,self.cola1)
		self.procesador2=Chef((width-700,height),2,self.cola2)
		self.procesador3=Chef((width-500,height),3,self.cola3)

		pygame.init()
		pygame.mixer.init()
		
		self.tiempoCron = 0
		self.contEnsaladas = 0
		self.contMalteadas = 0
		self.contPollos = 0

		self.fondo = pygame.image.load("imagenes/cocina.png")
		self.intro = pygame.image.load("imagenes/intro.png")
		self.instrucciones = pygame.image.load("imagenes/instrucciones.png")
		self.fondorect = self.fondo.get_rect()
		self.introrect = self.intro.get_rect()
		self.insrect = self.instrucciones.get_rect()

		pygame.display.set_caption( "Chef Race (Universidad Distrital)" )
		self.pizarra = pygame.image.load("imagenes/pizarra.png")
		self.sInicio = util.cargar_sonido('sonidos/inicio.wav')
		self.sHorno = util.cargar_sonido('sonidos/horno.wav')
		self.sCuchillo = util.cargar_sonido('sonidos/cuchillo.wav')
		self.sLicuadora = util.cargar_sonido('sonidos/licuadora.wav')
		self.sPrincipal = util.cargar_sonido('sonidos/principal.wav')

		self.pizarra1 = Pizarra((width-900,height))
		self.pizarra2 = Pizarra((width-700,height))
		self.pizarra3 = Pizarra((width-500,height))
		self.receta1 = Receta((width,height))
		self.receta2 = Receta((width+200,height))
		self.receta3 = Receta((width+400,height))

		self.comida1 = PolloConPapas(000,self.recursos[0],size)
		self.comida2 = Ensalada(111,self.recursos[1],size)
		self.comida3 = Malteada(222,self.recursos[2],size)

		self.listaChefs = [self.procesador1, self.procesador2, self.procesador3]
		self.listaPizarras = [self.pizarra1, self.pizarra2, self.pizarra3]
		self.listaRecetas = [self.receta1, self.receta2, self.receta3]
		self.listaComida = [self.comida1, self.comida2, self.comida3]
		self.cuchillos = Cuchillos(size)
		self.licuadora = Licuadora(size)
		self.horno = Horno(size)

		self.reloj = pygame.time.Clock()
		self.fuente1 = pygame.font.Font(None,70)
		self.fuente2 = pygame.font.Font(None,25)
		self.textoBienvenida = self.fuente1.render("Bienvenido a Chef Race UD", 1, (255,255,255))
		self.textoAutor1 = self.fuente2.render("Marlon Arias", 1, (0,0,0))
		self.textoAutor2 = self.fuente2.render("David Amado", 1, (0,0,0))
		self.textoAutor3 = self.fuente2.render("Realizado por:", 1, (0,0,0))

	def iniciar(self):

		self.sInicio.play()
		aux = 3

		while aux > 0:
			screen.blit(self.intro, self.introrect)
			screen.blit(self.textoAutor1,(width-170,height-680))
			screen.blit(self.textoAutor2,(width-170,height-660))
			screen.blit(self.textoAutor3,(width-170,height-700))
			screen.blit(self.textoBienvenida,((width-880, (height/2)+30)))
			pygame.display.update()
			time.sleep(1)
			aux=aux-1

		self.sPrincipal.play(1)
		
		self.hiloAnimacion = threading.Thread(name='Animacion', target = self.pintar)
		self.hiloAnimacion.setDaemon(True)
		self.hiloEventos = threading.Thread(name='EventosMouse', target = self.capturarEventos)
		self.hiloEventos.setDaemon(True)
		hilos = [self.procesador1, self.procesador2, self.procesador3, self.hiloEventos, self.hiloAnimacion]
		for h in hilos:
			h.start()
		
		#self.crearProceso(5) #Creacion de procesos aleatorios para testear el algoritmo

		self.cola1.join()
		self.cola2.join()
		self.cola3.join()
		self.hiloAnimacion.join()
		self.hiloEventos.join()

	def capturarEventos(self):
		while True:
			for event in pygame.event.get():				
				if event.type == pygame.QUIT:
					sys.exit()
				
				if event.type == pygame.KEYDOWN:
					#Chef 1:
					if event.key == pygame.K_q:
						proceso=Ensalada(self.numEn,self.recursos[1],size)
						self.numEn+=1
						estado="trabajandoCuchillo1"
						self.cola1.put(proceso)
						self.procesador1.estado=estado
						self.pizarra1.arregloRecetas.append(proceso)
						print("--PICO q")
					if event.key == pygame.K_a:
						proceso = Malteada(self.numMa,self.recursos[2],size)
						self.numMa+=1
						estado="trabajandoLicuadora1"
						self.cola1.put(proceso)
						self.procesador1.estado=estado
						self.pizarra1.arregloRecetas.append(proceso)
						print("--PICO a")
					if event.key == pygame.K_z:
						proceso=PolloConPapas(self.numPo,self.recursos[0],size)
						self.numPo+=1
						estado="trabajandoHorno1"
						self.cola1.put(proceso)
						self.procesador1.estado=estado
						self.pizarra1.arregloRecetas.append(proceso)
						print("--PICO z")
					
					#Chef 2:
					if event.key == pygame.K_w:
						proceso=Ensalada(self.numEn,self.recursos[1],size)
						self.numEn+=1
						estado="trabajandoCuchillo1"
						self.cola2.put(proceso)
						self.procesador2.estado=estado
						self.pizarra2.arregloRecetas.append(proceso)
						print("--PICO w")
					if event.key == pygame.K_s:
						proceso = Malteada(self.numMa,self.recursos[2],size)
						self.numMa+=1
						estado="trabajandoLicuadora1"
						self.cola2.put(proceso)
						self.procesador2.estado=estado
						self.pizarra2.arregloRecetas.append(proceso)
						print("--PICO s")
					if event.key == pygame.K_x:
						proceso=PolloConPapas(self.numPo,self.recursos[0],size)
						self.numPo+=1
						estado="trabajandoHorno1"
						self.cola2.put(proceso)
						self.procesador2.estado=estado
						self.pizarra2.arregloRecetas.append(proceso)
						print("--PICO x")
						
					#Chef 3:
					if event.key == pygame.K_e:
						proceso=Ensalada(self.numEn,self.recursos[1],size)
						self.numEn+=1
						estado="trabajandoCuchillo1"
						self.cola3.put(proceso)
						self.procesador3.estado=estado
						self.pizarra3.arregloRecetas.append(proceso)
						print("--PICO e")
					if event.key == pygame.K_d:
						proceso = Malteada(self.numMa,self.recursos[2],size)
						self.numMa+=1
						estado="trabajandoLicuadora1"
						self.cola3.put(proceso)
						self.procesador3.estado=estado
						self.pizarra3.arregloRecetas.append(proceso)
						print("--PICO d")
					if event.key == pygame.K_c:
						proceso=PolloConPapas(self.numPo,self.recursos[0],size)
						self.numPo+=1
						estado="trabajandoHorno1"
						self.cola3.put(proceso)
						self.procesador3.estado=estado
						self.pizarra3.arregloRecetas.append(proceso)
						print("--PICO c")						
							
	def pintar(self):
		while self.procesador1.uso or self.procesador2.uso or self.procesador3.uso:
			self.reloj.tick(30)

			for elemento in self.listaChefs:
				elemento.update()

			time.sleep(0.5)
			screen.blit(self.fondo, self.fondorect)			
			screen.blit(self.instrucciones, (707,462))
			
			self.textoInstrucciones = self.fuente2.render("Instrucciones:", 1, (0,0,0))
			screen.blit(self.textoInstrucciones,(707,442))
			
			self.contEnsaladas = self.numEn
			self.contMalteadas = self.numMa
			self.contPollos = self.numPo
			
			self.contEnsaladas = self.fuente2.render(str(self.contEnsaladas), 1, (0,0,0))
			screen.blit(self.contEnsaladas,(685,60))
			self.contMalteadas = self.fuente2.render(str(self.contMalteadas), 1, (0,0,0))
			screen.blit(self.contMalteadas,(685,170))
			self.contPollos = self.fuente2.render(str(self.contPollos), 1, (0,0,0))
			screen.blit(self.contPollos,(685,300))
			
			self.textoCronometro = self.fuente2.render("Tiempo:" + str(self.tiempoCron), 1, (0,0,0))
			screen.blit(self.textoCronometro,(5,5))
			self.tiempoCron += 1

			for elemento in self.listaChefs:
				screen.blit(elemento.image, elemento.rect)

			for elemento in self.listaPizarras:
				screen.blit(elemento.image, elemento.rect)
				#print("Longitud arregloRecetas: " + str(len(elemento.arregloRecetas)))
				try:
					for i in range(len(elemento.arregloRecetas)):
						if elemento.arregloRecetas[i].estado==0:
							screen.blit(elemento.arregloRecetas[i].iml, (elemento.rect[0]+30,elemento.rect[1]+i*60+10))
						elif elemento.arregloRecetas[i].estado==1:
							screen.blit(elemento.arregloRecetas[i].imb, (elemento.rect[0]+30,elemento.rect[1]+i*60+10))
						elif elemento.arregloRecetas[i].estado==2:
							screen.blit(elemento.arregloRecetas[i].ims, (elemento.rect[0]+30,elemento.rect[1]+i*60+10))
						elif elemento.arregloRecetas[i].estado==3:
							screen.blit(elemento.arregloRecetas[i].ime, (elemento.rect[0]+30,elemento.rect[1]+i*60+10))
						elif elemento.arregloRecetas[i].estado==4:
							elemento.arregloRecetas.remove(elemento.arregloRecetas[i])
						else:
							pass
				except IndexError:
					print("Oops! El arregloRecetas se ha desbordado")
					print("No te preocupes, puede continuar...\n")

			for elemento in self.listaRecetas:
				screen.blit(elemento.image, elemento.rect)

			for elemento in self.listaComida:
				screen.blit(elemento.iml, elemento.rect)

			screen.blit(self.cuchillos.image, self.cuchillos.rect)
			screen.blit(self.licuadora.image, self.licuadora.rect)
			screen.blit(self.horno.image, self.horno.rect)

			pygame.display.update()

	def crearProceso(self,nProcesos):
		for i in range(nProcesos):
			self.asignarPedidoAleatorio()

	def asignarPedidoAleatorio(self):
		aleatorio1=np.random.randint(3)
		aleatorio2=np.random.randint(3)
		if aleatorio1==0:
			proceso=PolloConPapas(self.numPo,self.recursos[0],size)
			self.numPo+=1
			estado="trabajandoHorno1"

		elif aleatorio1==1:
			proceso=Ensalada(self.numEn,self.recursos[1],size)
			self.numEn+=1
			estado="trabajandoCuchillo1"
		else:
			proceso= Malteada(self.numMa,self.recursos[2],size)
			self.numMa+=1
			estado="trabajandoLicuadora1"

		if aleatorio2==0:
			self.cola1.put(proceso)
			self.procesador1.estado=estado
			self.pizarra1.arregloRecetas.append(proceso)
		elif aleatorio2==1:
			self.cola2.put(proceso)
			self.procesador2.estado=estado
			self.pizarra2.arregloRecetas.append(proceso)
		elif aleatorio2==2:
			self.cola3.put(proceso)
			self.procesador3.estado=estado
			self.pizarra3.arregloRecetas.append(proceso)
		else:
			pass

class Chef(Sprite, Procesador):
	def __init__(self, cont_size,idProcesador,*args):
		Sprite.__init__(self)
		Procesador.__init__(self,idProcesador,*args)
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
		if self.proceso==None:
			self.image = self.imagenes[0]
			print("el procesador",self,"no tiene proceso")
		else:
			if self.proceso.recurso.nombre=="Cuchillos":
				if self.estado == self.estados[1]:
					self.image = self.imagenes[1]
					self.estado = self.estados[2]
				else:
					self.image = self.imagenes[2]
					self.estado = self.estados[1]
			elif self.proceso.recurso.nombre=="Horno":
				if self.estado == self.estados[3]:
					self.image = self.imagenes[3]
					self.estado = self.estados[4]
				else:
					self.image = self.imagenes[4]
					self.estado = self.estados[3]
			else:
				if self.estado == self.estados[5]:
					self.image = self.imagenes[5]
					self.estado = self.estados[6]
				else:
					self.image = self.imagenes[6]
					self.estado = self.estados[5]

cliente = Cliente()
cliente.iniciar()
