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

    def ia_insert(self):
        self.heuristics()
        if len(self.queue) != 0:
            cell = self.queue.pop()
            for it in range(1, 10):
                if self.validation(cell[0], cell[1], it) == True:
                    self.sudoku[cell[0]][cell[1]] = it
                    # print(it,cell[0],cell[1])
                    # print("I've found a solution")
                    break
        else:
            self.isSolution = True
            return


    def insert(self, row, column, value):
        if self.validation(row, column, value) == True:
            self.sudoku[row][column] = value
            self.heuristics()
        else:
            print("Estas incumpliendo las reglas")

    def show(self):
        for i in range(9):
            mamadisimo = str(self.sudoku[i]).replace(
                "[", "").replace("]", "").replace(",", "")
            mamadisimo = mamadisimo[:5] + " | " + \
                mamadisimo[6:11] + " | " + mamadisimo[12:]
            print(mamadisimo)
            if (i+1) % 3 == 0 and i != 8:
                print(colored("─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─", 'red'))

    def heuristics(self):
        self.cellHeuristic.clear()
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    self.cellHeuristic[i, j] = 1 / \
                        self.__calculate_options__(i, j)
        if list(self.cellHeuristic.values()) != []:
            self.queue.append(self.__get_random_max_cell_heuristic__())

    def __get_random_max_cell_heuristic__(self):
        maxval = max(self.cellHeuristic.values())
        res = [k for k, v in self.cellHeuristic.items() if v == maxval]
        # if len(res) >= 2:
        #     print(len(res))
        #     pos = random.randint(0, len(res))
        #     return res[pos-1]
        # print(len(res))
        return res[0]
        

    def __calculate_options__(self, row, column):

        options = 0
        for it in range(9):
            if self.sudoku[row][it] == 0:
                options += 1
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


start = timer()
game = Sudoku(example)
print("\nSudoku inicial\n\n")
game.show()
while game.isSolution != True:
    game.ia_insert()
end = timer()
print(end - start)
print("\nSolucion\n\n")
game.show()
print(" ")
