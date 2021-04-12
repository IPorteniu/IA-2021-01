import random 
import numpy

# pip install tabulate
from tabulate import tabulate

numeros = numpy.random.choice(range(0,31),6)

#Clase individuos
class Individuo(object):
    def __init__(self, id,x):
        self.id = id
        self.x = x
        self.binary = ''
        self.f_value = pow(x, 2)

    def calcular(self):
        self.regularizar_binario()
        self.x = int(self.binary,2)
        self.f_value = pow(self.x,2)
    
    def regularizar_binario(self):
        binary_string =  str(bin(self.x))
        self.binary = binary_string[2:]

#Función para seleccionar individuos dentro de los 32 posibles
def Inicializar(numeros):
    Individuos = []
    for i in range(6):
        Individuos.append(Individuo(i, numeros[i]))
        Individuos[i].calcular()
    Mostrar(Individuos)
    return Individuos

#Función para determinar las parejas de los seleccionados
def Parejas():
    Aleatorio = random.sample(range(3,6), 3)
    Pareja = {}
    for i in range(3):
        Pareja[i] = Aleatorio[i]
        Pareja[Aleatorio[i]] = i
    return Pareja

#Función para seleccionar a la mejor pareja de las establecidas según mayor f(x)
def Seleccion(Individuos):
    print('---Seleccion---')
    Pareja = Parejas()
    print('Parejas',Pareja)
    for key, value in Pareja.items():
        if Individuos[key].f_value >= Individuos[value].f_value:
            Individuos[value] = Individuos[key]
    Mostrar(Individuos)

#Función para cruzar a los individuos
def Cruce(Individuos):
    print('----Cruce----') 
    Pareja = Parejas()
    print('Parejas',Pareja)
    item = 0
    for key, value in Pareja.items():
        if item % 2 == 0:
            Punto = random.randint(1, 3)
            print('punto', Punto)
            Hijo1 = []
            Hijo2 = []
            Padre = Individuos[key]
            Madre = Individuos[value]
            Hijo1.extend(Padre.binary[0:Punto])
            Hijo1.extend(Padre.binary[Punto:])
            Hijo2.extend(Madre.binary[0:Punto])
            Hijo2.extend(Madre.binary[Punto:])

            Individuos[key].binary = Hijo1
            Individuos[value].binary = Hijo2

            # Recalcular los binarios a decimal y actualizar datos del objeto
            Individuos[key].calcular()
            Individuos[value].calcular()
        item = item + 1
    Mostrar(Individuos)

#Función para mutar a los hijos luego del cruce basada en probabilidad de mutación
def Mutacion(Individuos):
    print('-----Mutacion-----')
    for i in range(3):
        ElegirI = random.randint(0,5)
        print(ElegirI)
        ElegirGen = random.randint(0, 5)
        Individuos[ElegirI].id = ElegirGen
        print("****")
    Mostrar(Individuos)

#Función para demostrar el incremento de valores
def promedios(Individuos):
    promedio = 0
    for Individuo in Individuos:
        promedio += Individuo.f_value
    print("El promedio es", promedio/6)

#Función para imprimir los resultados de cada paso en tablas            
def Mostrar(Individuos):
    data = []
    for i in range(6):
        aux = [Individuos[i].id, Individuos[i].binary, Individuos[i].x, Individuos[i].f_value]
        data.append(aux)
    print(tabulate(data,headers=["ID", "Binario","Valor de X", "Valor de f(x)"]))


Individuos = Inicializar(numeros)
Seleccion(Individuos)
Cruce(Individuos)
Mutacion(Individuos)
promedios(Individuos)