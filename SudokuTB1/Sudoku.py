from termcolor import colored
from timeit import default_timer as timer
import random
#n = 9
#sudoku = [[0 for x in range(n)] for y in range(n)]

# for i in range(n):
# 	sudoku[i] = [int(x) for x in input().split()]

# Los 0 significan casillas vacias
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
        self.queue = []
        self.isSolution = False
        self.fixedCells = {}

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

                # Se añaden al diccionario de celdas fijas como True
                self.fixedCells[row, column] = True

                # Se seleccionan los numeros que faltan añadir a la fila
                set_fijos.add(self.sudoku[row][column])
            else:

                # Se añaden al diccionario de celdas fijas como False
                self.fixedCells[row, column] = False
        return set_nums.difference(set_fijos)

    def insert_row_values(self):
        #Lista de numeros a insertar
        num_list = []

        #Iniciamos la inserción de números
        for row in range(9):
            num_list = self.filter_row_values(row)

            for column in range(9):
                if self.sudoku[row][column] == 0:
                    self.sudoku[row][column] = num_list.pop()

    # Nuestra heurisitca dependerá de la cantidad de veces que se repite el número según las reglas del sudoku (conflictos)
    def __heuristics__(self, row, column):
        #self.cellHeuristic.clear()
        # Validar la cantidad de conflictos con su mismo numero
        if self.fixedCells[row][column] == False:
            self.cellHeuristic[row, column] = 1 / \
                self.__calculate_options__(row, column)

    def __calculate_options__(self, row, column):

        options = 0

        # Validar si existe el mismo numero en la columna
        for it in range(9):
            if self.sudoku[it][column] == 0:
                options += 1

        rowGroup = row//3
        columnGroup = column//3

        # Validar si existe el mismo numero en el cuadrado
        for i in range(rowGroup * 3, rowGroup * 3 + 3):
            for j in range(columnGroup * 3, columnGroup * 3 + 3):
                if self.sudoku[i][j] == 0:
                    options += 1
        return options

    def hill_climbing(self):

        rand = random.randint(1, 10)
        self.sudoku[rand][rand]

        #Aqui empieza hill climbing
        if self.cellHeuristic[initialNode] == sol:
            ##print("First node sol, gl!")
            return initialNode
        else:
            actualNode = initialNode

            while self.cellHeuristic[actualNode] != sol:
                for i in range(1,heuristicVals.__len__()):
                    neighborNode = heuristicVals[i]
                    if self.cellHeuristic[neighborNode] == sol:
                        ##print("Solution found")
                        return neighborNode
                    else:
                        if self.cellHeuristic[neighborNode] > self.cellHeuristic[actualNode]: 
                            actualNode = neighborNode    

    def is_solution(self):
        a=0


    def validation(self, row, column, value):
            # Validar si existe el mismo numero en la fila o la columna
            if(self.sudoku[row][column] == 0):
                for it in range(9):
                    if self.sudoku[row][it] == value:
                        return False
                    if self.sudoku[it][column] == value:
                        return False

                rowGroup = row//3
                columnGroup = column//3

                # Validar si existe el mismo numero en el cuadrado
                for i in range(rowGroup * 3, rowGroup * 3 + 3):
                    for j in range(columnGroup * 3, columnGroup * 3 + 3):
                        if self.sudoku[i][j] == value:
                            return False
                return True
            else:
                print("No puedes ingresar un numero en esta posicion")


# start = timer()
game = Sudoku(example)
print("\nSudoku inicial\n\n")
game.show()
game.insert_row_values()
# while game.isSolution != True:
#    game.fill_number()
#end = timer()
#print(end - start)
print("\nEstado inicial\n\n")
game.show()
print(" ")
