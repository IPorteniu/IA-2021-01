from termcolor import colored
import math
from timeit import default_timer as timer
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

solution = [
    [4, 3, 5, 2, 6, 9, 7, 8, 1],
    [6, 8, 2, 5, 7, 1, 4, 9, 3],
    [1, 9, 7, 8, 3, 4, 5, 6, 2],
    [8, 2, 6, 1, 9, 5, 3, 4, 7],
    [3, 7, 4, 6, 8, 2, 9, 1, 5],
    [9, 5, 1, 7, 4, 3, 6, 2, 8],
    [5, 1, 9, 3, 2, 6, 8, 7, 4],
    [2, 4, 8, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 8, 2, 5, 9]
]
example = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]
example2 = [
    [6, 0, 7, 9, 0, 0, 2, 0, 3],
    [9, 0, 3, 4, 2, 0, 8, 6, 0],
    [0, 0, 0, 0, 8, 3, 0, 0, 1],
    [5, 3, 0, 0, 6, 0, 9, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 3, 7],
    [4, 0, 0, 1, 3, 2, 5, 0, 0],
    [0, 4, 0, 0, 7, 0, 6, 0, 9],
    [7, 2, 0, 0, 0, 0, 0, 0, 0],
    [8, 9, 1, 2, 5, 0, 0, 7, 0]
]

class Sudoku(object):
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.cellHeuristic = {}
        self.unfixedCells = {0: [], 1: [], 2: [],
                             3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

    def show(self):
        for i in range(9):
            mamadisimo = str(self.sudoku[i]).replace(
                "[", "").replace("]", "").replace(",", "")
            mamadisimo = mamadisimo[:5] + " | " + \
                mamadisimo[6:11] + " | " + mamadisimo[12:]
            print(mamadisimo)
            if (i+1) % 3 == 0 and i != 8:
                print(colored("─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─", 'red'))

    def __filter_row_values__(self, row):
        # Numeros potenciales en un Sudoku
        set_nums = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

        # Numeros iniciales del sudoku por fila
        set_fijos = set([])

        for column in range(9):

            # Condicional para hallar numeros iniciales
            if self.sudoku[row][column] != 0:

                # Se seleccionan los numeros que faltan añadir a la fila
                set_fijos.add(self.sudoku[row][column])
            else:

                # Se añaden al diccionario de celdas no fijas como True
                self.unfixedCells[row].append(column)
        return set_nums.difference(set_fijos)

    def insert_row_values(self):
        # Lista de numeros a insertar
        num_list = []

        # Iniciamos la inserción de números
        for row in range(9):
            num_list = self.__filter_row_values__(row)

            for column in range(9):
                if self.sudoku[row][column] == 0:
                    self.sudoku[row][column] = num_list.pop()

    def __heuristics__(self, row, column):
        # Nuestra heurisitca dependerá de la cantidad de veces que se
        # repite el número según las reglas del sudoku (conflictos)
        # Validar la cantidad de conflictos con su mismo numero
        return self.__calculate_options__(row, column, self.sudoku)

    def __calculate_options__(self, row, column, sudoku):
        options = 0
        columnNumbers = []
        squareNumbers = []
        # Validar si existe el mismo numero en la columna
        for it in range(9):
            columnNumbers.append(sudoku[it][column])
        options += 9 - len(np.unique(columnNumbers))
        rowGroup = row//3
        columnGroup = column//3

        # Validar si existe el mismo numero en el cuadrado
        for i in range(rowGroup * 3, rowGroup * 3 + 3):
            for j in range(columnGroup * 3, columnGroup * 3 + 3):
                squareNumbers.append(sudoku[i][j])
        options += 9 - len(np.unique(squareNumbers))
        return options

    def hill_climbing(self):

        plt.axis([0, 100, 0, 80])
        plt.ylabel("Heuristica")
        plt.xlabel("Iteracion")
        plt.title("Hill Climbing")

        if self.isSolution(self.sudoku) == True:
            print("Sudoku vino resuelto")
            return self.sudoku
        else:
            estadoActual = self.sudoku
            score = 0
            minHeuristica = 100
            inc = 0

            while self.isSolution(estadoActual) != True:

                plt.scatter(inc, self.evaluation(estadoActual))
                plt.pause(0.01)
                
                nuevoEstado = self.__swap_cell_values__(copy.deepcopy(estadoActual))
                nuevaHeuristica = self.evaluation(nuevoEstado)
                actualHeuristica =self.evaluation(estadoActual)
                if nuevaHeuristica < minHeuristica:
                    minHeuristica = nuevaHeuristica 

                print("\nHeuristica Actual: " + str(actualHeuristica))
                print("Nueva Heuristica: " + str(nuevaHeuristica))
                print("Minima Heuristica: " + str(minHeuristica))
                inc +=1
                

                if self.isSolution(nuevoEstado) == True:
                    print("Se encontró la solución")
                    self.sudoku = nuevoEstado
                    return nuevoEstado
                    
                elif nuevaHeuristica < actualHeuristica:
                    estadoActual = nuevoEstado

                else:
                    score += 25

                if score == 1000:
                    estadoActual = nuevoEstado
                    score = 0

    def simulated_annealing(self):

        temperatura = 100
        speed = 0.001
        stuckCount = 0
        plt.ylabel("Heuristica")
        plt.xlabel("Temperatura")
        plt.title("Simulated Annealing")

        if self.isSolution(self.sudoku) == True:
            print("Sudoku vino resuelto")
            return self.sudoku
        else:
            estadoActual = self.sudoku
            retries = 0
            minHeuristica = 100

            while temperatura > 1:
        
                nuevoEstado = self.__swap_cell_values__(copy.deepcopy(estadoActual))

                plt.scatter(temperatura, self.evaluation(estadoActual))
                plt.pause(0.0001)


                if self.isSolution(estadoActual) == True:
                    print("Se encontró la solución")
                    self.sudoku = estadoActual
                    return estadoActual

                actualHeuristica = self.evaluation(estadoActual)
                nuevaHeuristica = self.evaluation(nuevoEstado)
                if nuevaHeuristica < minHeuristica:
                    minHeuristica = nuevaHeuristica 

                deltaE = nuevaHeuristica - actualHeuristica

                print("\nN° of retry: " + str(retries))    
                print("\nTemperatura: " + str(temperatura))  
                print("Heuristica Actual: " + str(actualHeuristica))
                print("Nueva Heuristica: " + str(nuevaHeuristica))
                print("delta: " + str(deltaE))
                print("Exponencial(e^(-delta/t)): " + str(math.exp(-(deltaE / temperatura))))
                print("\nMinima Heuristica: " + str(minHeuristica))

                if self.__funcion_aceptacion__(deltaE,temperatura):
                    estadoActual = nuevoEstado
    
                temperatura *= (1-speed)

                # if actualHeuristica < nuevaHeuristica:
                #       stuckCount += 1
                # else:
                #     stuckCount = 0

                # if (stuckCount > 20):
                #     temperatura += .5

                retries += 1
               
            print("N° of retries: " + str(retries))
            self.sudoku = estadoActual

    def __funcion_aceptacion__(self, deltaE, temperatura):
        boltzmann = math.exp(-(deltaE*10 / temperatura))
        rand = random.random()
        if deltaE < 0:
            return True
        elif  rand <= boltzmann:
            return True
        return False


    def __swap_cell_values__(self, sudoku):
        # Obtenemos un row al azar
        row = random.randint(0, 8)
        # Obtenemos todas las columnas, a traves del row, que sean intercambiables
        columns = copy.deepcopy(self.unfixedCells[row])
        worstHeuristic = 0
        worstHeuristicColumn = 0

        # Encontramos la mayor heuristica y en que columna se encuentra
        for column in columns:
            aux = self.__heuristics__(row, column)
            if aux > worstHeuristic:
                worstHeuristic = aux
                worstHeuristicColumn = column

        # Eliminamos la mejor columna de nuestra lista auxiliar
        # para que no la tome nuevamente
        columns.remove(worstHeuristicColumn)
        
        # Elegimos una nueva columna al azar, la cual sera semetica al SWAP
        newCellColumn = random.choice(columns)
        
        sudoku[row][worstHeuristicColumn], sudoku[row][newCellColumn] = sudoku[row][newCellColumn], sudoku[row][worstHeuristicColumn]

        return sudoku

    def isSolution(self, sudoku):

         validation = []
         sumaCol = 0
         sumaRow = 0
         for row in range(9):
             for column in range(9):
                 sumaCol += sudoku[column][row]
                 sumaRow += sudoku[row][column]
             if sumaRow == 45 and sumaCol == 45:
                 validation.append(True)
             else:
                 validation.append(False)
             sumaCol = 0
             sumaRow = 0

         if False not in validation:
             return True
         return False

    def evaluation(self, sudoku):
        options = 0
        for i in range(9):
            options += self.__calculate_options__(i,i,sudoku)
        return options
