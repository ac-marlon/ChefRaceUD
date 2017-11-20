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
import util
import sys, pygame, util
from receta import Receta
from recursos import CuchillosIma
from recursos import LicuadoraIma
from recursos import HornoIma
from pizarra import Pizarra

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
		self.minIter=50

	def __str__(self):
		return str(self.idProcesador)

	def run(self):
		while self.uso:
			self.usarProcesador(*self._args)

	def usarProcesador(self,q):
		while not self.proceso==None or not q.empty() or not self.lis.es_vacia() or not self.sus.es_vacia() or not self.blo.es_vacia() or self.minIter>0:
			time.sleep(2)
			self.minIter-=1
			if not q.empty(): self.asignar(q.get())
			self.lis.ordenar()
			if not self.lis.es_vacia() and self.proceso==None:
				posible=self.lis.desencolar()
				if posible.recurso.libre:
					self.ocupado=True
					self.proceso=posible
					self.proceso.recurso.utilizar()
					self.proceso.estado=3
				else:
					posible.bloquear()
					self.blo.encolar(posible)
			elif not self.lis.es_vacia() and not self.proceso==None:
				posible=self.lis.desencolar()
				if self.proceso.t>posible.t and posible.recurso.libre:
					self.proceso.suspender()
					self.sus.encolar(self.proceso)
					self.proceso=posible
					self.proceso.recurso.utilizar()
				else:
					self.lis.encolar(posible)

			self.contarColaBlo()
			self.contarColaLis()
			self.revisarColaSus()
			self.revisarColaBlo()

			if not self.proceso==None:
				self.proceso.procesar()
				if self.proceso.t==0:
					self.proceso.recurso.liberar()
					print("\nterminando proceso",self.proceso,"en el procesador",self,",sus",self.proceso.sus,",lis",self.proceso.lis,",blo",self.proceso.blo,",zona critica",self.proceso.zc)
					self.proceso.estado=4
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
		proceso.estado=0
		self.lis.encolar(proceso)

class cliente:
	def __init__(self):
		self.numPo=0
		self.numMa=0
		self.numEn=0

		self.recursos=[rs.Horno(),rs.Cuchillos(),rs.Licuadora()]
		self.cola1=queue.Queue()
		self.cola2=queue.Queue()
		self.cola3=queue.Queue()

		self.colaProcesadores=queue.Queue()
		self.procesador1=Chef((width-900,height),1,self.cola1)
		self.procesador2=Chef((width-700,height),2,self.cola2)
		self.procesador3=Chef((width-500,height),3,self.cola3)

		pygame.init()
		pygame.mixer.init()

		self.fondo = pygame.image.load("imagenes/cocina.png")
		self.intro = pygame.image.load("imagenes/intro.png")
		self.fondorect = self.fondo.get_rect()
		self.introrect = self.intro.get_rect()

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
		self.cuchillos = CuchillosIma(size)
		self.licuadora = LicuadoraIma(size)
		self.horno = HornoIma(size)

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

		self.procesador1.start()
		self.procesador2.start()
		self.procesador3.start()
		self.hiloAnimacion = threading.Thread(name='Animacion', target = self.pintar)
		self.hiloEventos = threading.Thread(name='Animacion', target = self.capturarEventos)
		#self.hiloEventos.daemon=True
		self.hiloEventos.start()
		self.hiloAnimacion.daemon=True
		self.hiloAnimacion.start()
		
		self.cola1.join()
		self.cola2.join()
		self.cola3.join()
		self.hiloAnimacion.join()
		self.hiloEventos.join()

	def capturarEventos(self):
		while self.procesador1.uso or self.procesador2.uso or self.procesador3.uso:
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					print("Evento ratonBtn capturado")
					for x in range(700, 760):
						for y in range(282, 342):
							proceso = Malteada(self.numMa,self.recursos[2],size)
							self.numMa+=1
							estado="trabajandoLicuadora1"
							if event.button == 1 and event.pos == (x, y):
								self.cola1.put(proceso)
								self.procesador1.estado=estado
								self.pizarra1.arregloRecetas.append(proceso)
								print("pico el click izq")
							elif event.button == 2 and event.pos == (x, y):
								self.cola2.put(proceso)
								self.procesador2.estado=estado
								self.pizarra2.arregloRecetas.append(proceso)
								print("pico el click cent")
							elif event.button == 3 and event.pos == (x, y):
								self.cola3.put(proceso)
								self.procesador3.estado=estado
								self.pizarra3.arregloRecetas.append(proceso)
								print("pico el click der")

					for x in range(700, 760):
						for y in range(27, 87):
							proceso=PolloConPapas(self.numPo,self.recursos[0],size)
							self.numPo+=1
							estado="trabajandoHorno1"
							if event.button == 1 and event.pos == (x, y):
								self.cola1.put(proceso)
								self.procesador1.estado=estado
								self.pizarra1.arregloRecetas.append(proceso)
								print("pico el click izq")
							elif event.button == 2 and event.pos == (x, y):
								self.cola2.put(proceso)
								self.procesador2.estado=estado
								self.pizarra2.arregloRecetas.append(proceso)
								print("pico el click cent")
							elif event.button == 3 and event.pos == (x, y):
								self.cola3.put(proceso)
								self.procesador3.estado=estado
								self.pizarra3.arregloRecetas.append(proceso)
								print("pico el click der")

					for x in range(700, 750):
						for y in range(137, 197):
							proceso=Ensalada(self.numEn,self.recursos[1],size)
							self.numEn+=1
							estado="trabajandoCuchillo1"
							if event.button == 1 and event.pos == (x, y):
								self.cola1.put(proceso)
								self.procesador1.estado=estado
								self.pizarra1.arregloRecetas.append(proceso)
								print("pico el click izq")
							elif event.button == 2 and event.pos == (x, y):
								self.cola2.put(proceso)
								self.procesador2.estado=estado
								self.pizarra2.arregloRecetas.append(proceso)
								print("pico el click cent")
							elif event.button == 3 and event.pos == (x, y):
								self.cola3.put(proceso)
								self.procesador3.estado=estado
								self.pizarra3.arregloRecetas.append(proceso)
								print("pico el click der")

	def pintar(self):
		while self.procesador1.uso or self.procesador2.uso or self.procesador3.uso:
			self.reloj.tick(3)

			for elemento in self.listaChefs:
				elemento.update()

			time.sleep(0.5)
			screen.blit(self.fondo, self.fondorect)

			for elemento in self.listaChefs:
				screen.blit(elemento.image, elemento.rect)

			for elemento in self.listaPizarras:
				screen.blit(elemento.image, elemento.rect)
				for i in elemento.arregloRecetas:
					if elemento.arregloRecetas[elemento.arregloRecetas.index(i)].estado==0:
						screen.blit(i.iml, (elemento.rect[0]+30,elemento.rect[1]+elemento.arregloRecetas.index(i)*60+10))
					elif elemento.arregloRecetas[elemento.arregloRecetas.index(i)].estado==1:
						screen.blit(i.imb, (elemento.rect[0]+30,elemento.rect[1]+elemento.arregloRecetas.index(i)*60+10))
					elif elemento.arregloRecetas[elemento.arregloRecetas.index(i)].estado==2:
						screen.blit(i.ims, (elemento.rect[0]+30,elemento.rect[1]+elemento.arregloRecetas.index(i)*60+10))
					elif elemento.arregloRecetas[elemento.arregloRecetas.index(i)].estado==3:
						screen.blit(i.ime, (elemento.rect[0]+30,elemento.rect[1]+elemento.arregloRecetas.index(i)*60+10))
					elif elemento.arregloRecetas[elemento.arregloRecetas.index(i)].estado==4:
						elemento.arregloRecetas.remove(i)

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
			self.asignar_pedido_aleatorio()

	def asignar_pedido_aleatorio(self):
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
		elif aleatorio2==1:
			self.cola2.put(proceso)
			self.procesador2.estado=estado
		else:
			self.cola3.put(proceso)
			self.procesador3.estado=estado

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

cliente = cliente()
cliente.iniciar()
