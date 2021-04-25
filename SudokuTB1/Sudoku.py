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
        set_fixed = set([])

        for column in range(9):

            # Condicional para hallar numeros iniciales
            if self.sudoku[row][column] != 0:

                # Se seleccionan los numeros que faltan añadir a la fila
                set_fixed.add(self.sudoku[row][column])
            else:

                # Se añaden al diccionario de celdas no fijas como True
                self.unfixed_cells[row].append(column)
        return set_nums.difference(set_fixed)

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
            current_state = self.sudoku
            # Utilidades de info
            score = 0
            min_heuristic = 100
            inc = 0

            while self.is_solution(current_state) != True:

                #Utilidades de la gráfica
                if inc % 1250 == 0:
                    
                    plt.scatter(inc/1250, self.evaluation(current_state))
                    plt.pause(0.00000000000001)
                
                # Se selecciona al vecino a comparar
                new_state = self.__swap_cell_values__(copy.deepcopy(current_state))
                # Se calculan las heurísticas
                new_heuristic = self.evaluation(new_state)
                current_heuristic =self.evaluation(current_state)
                # Se comparan las heurísticas
                if new_heuristic < min_heuristic:
                    min_heuristic = new_heuristic 
                
                #Utilidades de info
                print("\nHeuristica Actual: " + str(current_heuristic))
                print("Nueva Heuristica: " + str(new_heuristic))
                print("Minima Heuristica: " + str(min_heuristic))
                inc +=1
                
                # Condición de victoría por si el nuevo estado(o vecino) es la solución
                if self.is_solution(new_state) == True:
                    print("Se encontró la solución")
                    print(inc)
                    self.sudoku = new_state
                    return new_state

                # Si la heurísitca del vecino es mejor que la actual se intercambian    
                elif new_heuristic < current_heuristic:
                    current_state = new_state

                # Técnica de random restart para no atascarse en un mínimo local
                else:
                    score += 25

                if score == 1000:
                    current_state = new_state
                    score = 0

    # Definición de Simulated Annealing(SA)
    def simulated_annealing(self):

        # Variables necesarias para SA
        temperature = 100
        speed = 0.003
        # Variable usada en técnica utilizada más abajo
        # stuckCount = 0 
        min_heuristic = 100
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
            current_state = self.sudoku
            # Contador de veces iterado
            retries = 0
            # Condición de fin si es que no encuentra una solución
            while temperature > 0.001:
                # Se selecciona al vecino a comparar
                new_state = self.__swap_cell_values__(copy.deepcopy(current_state))
                # Utilidades de la gráfica 
                plt.scatter(temperature, self.evaluation(current_state))
                plt.pause(0.1)

                # Condición de fin si es que el estado actual es la solución
                if self.is_solution(current_state) == True:
                    print("Se encontró la solución")
                    self.sudoku = current_state
                    return current_state

                # Se halla la energía de ambos estados 
                current_heuristic = self.evaluation(current_state)
                new_heuristic = self.evaluation(new_state)
                # Utilidad para reconocer la mayor heuristica lograda
                if new_heuristic < min_heuristic:
                    min_heuristic = new_heuristic 
                # Se halla el delta de energía
                delta_e = new_heuristic - current_heuristic

                # Utilidades para información 
                print("\nN° of retry: " + str(retries))    
                print("\ntemperature: " + str(temperature))  
                print("Heuristica Actual: " + str(current_heuristic))
                print("Nueva Heuristica: " + str(new_heuristic))
                print("Minima Heuristica: " + str(min_heuristic))
                print("delta: " + str(delta_e))
                print("\nExponencial(e^(-delta/t)): " + str(math.exp(-(delta_e / temperature))))
             
                # Función de aceptación
                if self.__acceptance_function__(delta_e,temperature):
                    current_state = new_state
                
                # Cambio de temperature segun su factor de enfriamiento
                temperature *= (1-speed)
                retries += 1

                # Técnica de aumento de temperature para evitar minimos locales
                # if new_heuristic >= current_heuristic:
                #     stuckCount += 1
                # else:
                #     stuckCount = 0

                # if (stuckCount > 50):
                #     temperature += 2

            # Se devuelve el último estado en caso se termina de enfriar la temperature   
            print("N° of retries: " + str(retries))
            self.sudoku = current_state
        return current_state

    # Función donde se valida el cambio de estados para el SA
    def __acceptance_function__(self, delta_e, temperature):
        boltzmann = math.exp(-(delta_e *10 / temperature))
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
        column_sum = 0
        row_sum = 0
        for row in range(9):
            for column in range(9):
                column_sum += sudoku[column][row]
                row_sum += sudoku[row][column]
            if row_sum == 45 and column_sum == 45:
                validation.append(True)
            else:
                validation.append(False)
            column_sum = 0
            row_sum = 0
        if False not in validation:
            return True
        return False

    # Función para hallar la heurística de un estado
    def evaluation(self, sudoku):
        options = 0
        for i in range(9):
            options += self.__calculate_options__(i,i,sudoku)
        return options
