from termcolor import colored
import math
from timeit import default_timer as timer
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

class Sudoku(object):
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.cell_heuristic = {}
        self.unfixed_cells = {0: [], 1: [], 2: [],
                             3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

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
                self.unfixed_cells[row].append(column)
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
        column_numbers = []
        square_numbers = []
        # Validar si existe el mismo numero en la columna
        for it in range(9):
            column_numbers.append(sudoku[it][column])
        options += 9 - len(np.unique(column_numbers))
        row_group = row//3
        column_group = column//3

        # Validar si existe el mismo numero en el cuadrado
        for i in range(row_group * 3, row_group * 3 + 3):
            for j in range(column_group * 3, column_group * 3 + 3):
                square_numbers.append(sudoku[i][j])
        options += 9 - len(np.unique(square_numbers))
        return options

    def hill_climbing(self):

        # Utilidades de la gráfica
        plt.ylabel("Heuristica")
        plt.xlabel("Iteracion")
        plt.title("Hill Climbing")

         # Condición por si el primer estado es la solución
        if self.is_solution(self.sudoku) == True:
            print("Sudoku vino resuelto")
            return self.sudoku
        else:

            #Se asigna el estado actual a una variable
            estado_actual = self.sudoku
            # Utilidades de info
            score = 0
            min_heuristica = 100
            inc = 0

            while self.is_solution(estado_actual) != True:

                #Utilidades de la gráfica
                if inc % 1250 == 0:
                    
                    plt.scatter(inc/1250, self.evaluation(estado_actual))
                    plt.pause(0.00000000000001)
                
                # Se selecciona al vecino a comparar
                nuevo_estado = self.__swap_cell_values__(copy.deepcopy(estado_actual))
                # Se calculan las heurísticas
                nueva_heuristica = self.evaluation(nuevo_estado)
                actual_heuristica =self.evaluation(estado_actual)
                # Se comparan las heurísticas
                if nueva_heuristica < min_heuristica:
                    min_heuristica = nueva_heuristica 
                
                #Utilidades de info
                print("\nHeuristica Actual: " + str(actual_heuristica))
                print("Nueva Heuristica: " + str(nueva_heuristica))
                print("Minima Heuristica: " + str(min_heuristica))
                inc +=1
                
                # Condición de victoría por si el nuevo estado(o vecino) es la solución
                if self.is_solution(nuevo_estado) == True:
                    print("Se encontró la solución")
                    print(inc)
                    self.sudoku = nuevo_estado
                    return nuevo_estado

                # Si la heurísitca del vecino es mejor que la actual se intercambian    
                elif nueva_heuristica < actual_heuristica:
                    estado_actual = nuevo_estado

                # Técnica de random restart para no atascarse en un mínimo local
                else:
                    score += 25

                if score == 1000:
                    estado_actual = nuevo_estado
                    score = 0

    # Definición de Simulated Annealing(SA)
    def simulated_annealing(self):

        # Variables necesarias para SA
        temperatura = 100
        speed = 0.003
        # Variable usada en técnica utilizada más abajo
        # stuckCount = 0 
        min_heuristica = 100
        # Utilidades de la gráfica
        plt.ylabel("Heuristica")
        plt.xlabel("Temperatura")
        plt.title("Simulated Annealing")

        # Condición por si el primer estado es la solución
        if self.is_solution(self.sudoku) == True:
            print("Sudoku vino resuelto")
            return self.sudoku
        else:
            # Se asigna el estado actual a una variable
            estado_actual = self.sudoku
            # Contador de veces iterado
            retries = 0
            # Condición de fin si es que no encuentra una solución
            while temperatura > 0.001:
                # Se selecciona al vecino a comparar
                nuevo_estado = self.__swap_cell_values__(copy.deepcopy(estado_actual))
                # Utilidades de la gráfica 
                plt.scatter(temperatura, self.evaluation(estado_actual))
                plt.pause(0.1)

                # Condición de fin si es que el estado actual es la solución
                if self.is_solution(estado_actual) == True:
                    print("Se encontró la solución")
                    self.sudoku = estado_actual
                    return estado_actual

                # Se halla la energía de ambos estados 
                actual_heuristica = self.evaluation(estado_actual)
                nueva_heuristica = self.evaluation(nuevo_estado)
                # Utilidad para reconocer la mayor heuristica lograda
                if nueva_heuristica < min_heuristica:
                    min_heuristica = nueva_heuristica 
                # Se halla el delta de energía
                delta_e = nueva_heuristica - actual_heuristica

                # Utilidades para información 
                print("\nN° of retry: " + str(retries))    
                print("\nTemperatura: " + str(temperatura))  
                print("Heuristica Actual: " + str(actual_heuristica))
                print("Nueva Heuristica: " + str(nueva_heuristica))
                print("Minima Heuristica: " + str(min_heuristica))
                print("delta: " + str(delta_e))
                print("\nExponencial(e^(-delta/t)): " + str(math.exp(-(delta_e / temperatura))))
             
                # Función de aceptación
                if self.__funcion_aceptacion__(delta_e,temperatura):
                    estado_actual = nuevo_estado
                
                # Cambio de temperatura segun su factor de enfriamiento
                temperatura *= (1-speed)
                retries += 1

                # Técnica de aumento de temperatura para evitar minimos locales
                # if nueva_heuristica >= actual_heuristica:
                #     stuckCount += 1
                # else:
                #     stuckCount = 0

                # if (stuckCount > 50):
                #     temperatura += 2

            # Se devuelve el último estado en caso se termina de enfriar la temperatura   
            print("N° of retries: " + str(retries))
            self.sudoku = estado_actual
        return estado_actual

    # Función donde se valida el cambio de estados para el SA
    def __funcion_aceptacion__(self, delta_e, temperatura):
        boltzmann = math.exp(-(delta_e *10 / temperatura))
        rand = random.random()
        if delta_e < 0:
            return True
        elif  rand <= boltzmann:
            return True
        return False

    # Función para cambiar la celda con peor heurística por otra de manera aleatoria
    def __swap_cell_values__(self, sudoku):
        # Obtenemos un row al azar
        row = random.randint(0, 8)
        # Obtenemos todas las columnas, a traves del row, que sean intercambiables
        columns = copy.deepcopy(self.unfixed_cells[row])
        worst_heuristic = 0
        worst_heuristic_column = 0

        # Encontramos la mayor heuristica y en que columna se encuentra
        for column in columns:
            aux = self.__heuristics__(row, column)
            if aux > worst_heuristic:
                worst_heuristic = aux
                worst_heuristic_column = column

        # Eliminamos la mejor columna de nuestra lista auxiliar
        # para que no la tome nuevamente
        columns.remove(worst_heuristic_column)
        
        # Elegimos una nueva columna al azar, la cual sera semetica al SWAP
        new_cell_column = random.choice(columns)
        
        # Se efectúa el cambio de celdas
        sudoku[row][worst_heuristic_column], sudoku[row][new_cell_column] = sudoku[row][new_cell_column], sudoku[row][worst_heuristic_column]

        return sudoku

    # Funcion para determinar si se halló la solución
    def is_solution(self, sudoku):
        
        # La suma de filas y la de columnas del sudoku deberán retornar 45(1+2+3+4+5+6+7+8+9)
        validation = []
        suma_col = 0
        suma_row = 0
        for row in range(9):
            for column in range(9):
                suma_col += sudoku[column][row]
                suma_row += sudoku[row][column]
            if suma_row == 45 and suma_col == 45:
                validation.append(True)
            else:
                validation.append(False)
            suma_col = 0
            suma_row = 0
        if False not in validation:
            return True
        return False

    # Función para hallar la heurística de un estado
    def evaluation(self, sudoku):
        options = 0
        for i in range(9):
            options += self.__calculate_options__(i,i,sudoku)
        return options
