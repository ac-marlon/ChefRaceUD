import threading
import time
import numpy as np
class Proceso:
    def __init__(self,idProceso,quantum,nombre,recurso,t,tr):
        self.idProceso=idProceso
        self.nombre=nombre
        self.recurso=recurso
        self.t=t
        self.tr=tr
        self.quantum=quantum
        self.terminado=False
    def __str__(self):
        return self.nombre+" "+str(self.idProceso)
    def procesar(self):
        while self.quantum and self.t:
            
            print("Preparando ",self.nombre," ",self.idProceso," quantum ",self.quantum,"t",self.t)
            self.quantum-=1
            self.t-=1
            time.sleep(1)
    def asignarQ(self):
        return np.random.randint(5,15) 

class PolloConPapas(Proceso):
    def __init__(self,idProceso,quantum=0,nombre="Pollo con papas",recurso="Horno",t=25,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)

class Malteada(Proceso):
    def __init__(self,idProceso,quantum=0,nombre="Malteada",recurso="Licuadora",t=5,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)

class Ensalada(Proceso):
    def __init__(self,idProceso,quantum=0,nombre="Ensalada",recurso="Cuchillo",t=12,tr=0):
        Proceso.__init__(self,idProceso,quantum,nombre,recurso,t,tr)

