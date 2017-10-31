import cola
import procesos as ps
import recursos as rs
import queue
import threading
class Procesador(threading.Thread):
    def __init__(self,idProcesador,*args):
        threading.Thread.__init__(self)
        self.idProcesador=idProcesador
        self.ocupado=False
        self.proceso=None
        self.lis=cola.Cola()
        self.blo=cola.Cola()
        self.sus=cola.Cola()
        self._args=args
    def __str__(self):
        return str(self.idProcesador)
    def run(self):
        while True:
            self.procesar(*self._args)
    def procesar(self,q):
        while not q.empty():
            self.asignar(q.get())
            if self.lis.es_vacia(): break
            self.proceso=self.lis.desencolar()
            print("comenzando proceso ",self.proceso," en el procesador ",self)
            self.proceso.procesar()
            self.revisarColaSus()
            self.revisarColaBlo()
            if self.proceso.t>0:
                self.proceso.tr=5
                self.sus.encolar(self.proceso)
                print("se reencolo el proceso a suspendidos")
            else:
                print("terminando proceso",self.proceso," en el procesador",self)
                q.task_done()
    def revisarColaSus(self):
        for i in range(len(self.sus.items)):
            self.sus.items[i].tr-=1
        if not self.sus.es_vacia():
            print(self.sus.items[0],"tr",self.sus.items[0].tr)
            print(" ")
            if self.sus.items[0].tr==0:
                self.lis.encolar(self.sus.desencolar())
                print("se saco un proceso y entro a la cola de listo")
    def revisarColaBlo(self):
        pass

    def asignar(self,proceso):
        proceso.quantum=proceso.asignarQ()
        self.lis.encolar(proceso)
        print("asignacion",self.lis.items)

class cliente:
    def __init__(self):
        self.cola1=queue.Queue()
        self.cola1.put(ps.Malteada(0))
        self.cola2=queue.Queue()
        self.cola2.put(ps.PolloConPapas(0))
        self.cola3=queue.Queue()
        self.cola3.put(ps.Ensalada(0))
        self.procesador1=Procesador(1,self.cola1)        
        self.procesador2=Procesador(2,self.cola2)      
        self.procesador3=Procesador(3,self.cola3)
    def iniciar(self):
        self.procesador1.start()
        self.procesador2.start()
        self.procesador3.start()
        self.cola1.put(ps.Malteada(1))
        self.cola2.put(ps.PolloConPapas(1))
        self.cola3.put(ps.PolloConPapas(2))
        self.cola1.put(ps.Malteada(2))
        self.cola2.put(ps.Ensalada(1))
        self.cola3.put(ps.PolloConPapas(3))
        self.cola2.put(ps.Malteada(3))
        self.cola1.put(ps.Ensalada(2))
        self.cola2.put(ps.Ensalada(3))
        self.cola1.put(ps.Malteada(4))
        self.cola3.put(ps.PolloConPapas(4))
        self.cola1.put(ps.Ensalada(4))
        self.cola1.put(ps.Malteada(5))

        self.cola1.join()
        self.cola2.join()
        self.cola3.join()

         

cliente = cliente()
cliente.iniciar()
