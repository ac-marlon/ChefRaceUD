class Recurso:
    def __init__(self,nombre):
        self.nombre=nombre
        self.libre=True
    def __str__(self):
        return(nombre)
    def utilizar(self):
        if self.libre:
            print("usando el ",self.nombre)
            self.libre=False
        else:
            print("el ",self.nombre," esta ocupado")
    def liberar(self):
        if not self.libre:
            print("el ",self.nombre," fue liberado")
            self.libre=True
        else:
            print("el ",self.nombre," no estaba siendo usado")

class Horno(Recurso):
    def __init__(self,nombre="Horno"):
        Recurso.__init__(self,nombre)

class Cuchillos(Recurso):
    def __init__(self,nombre="Cuchillos"):
        Recurso.__init__(self,nombre)

class Licuadora(Recurso):
    def __init__(self,nombre="Licuadora"):
        Recurso.__init__(self,nombre)


