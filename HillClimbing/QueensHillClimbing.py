# 8 Queens Hill Climbing

import copy
from timeit import default_timer as timer

class Queen:
    def __init__(self, id, row, column):
        self.id = id
        self.row = row
        self.column = column

class Board(object):
    def __init__(self,queens,queensConflicts):
        self.queens = queens
        self.queensConflicts = queensConflicts
        
    def find_queen(self, queenId):
        for queen in self.queens:
            if queen.id == queenId:
                return queen

    def isSolution(self):
        if True not in self.queensConflicts.values():
            print("Victoria")
            return True
        return False
    
    def quantityOfConflicts(self):
        quantityOfConflicts = 0
        for key, value in self.queensConflicts.items():
            if value == True:
                quantityOfConflicts += 1
        return quantityOfConflicts

def watch_conflicts(row, column, board):
    conflict = 0
    for queen in board.queens:
        if abs(queen.row - row) == abs(queen.column - column):
            if(queen.column != column):
                conflict += 1
        if queen.row == row and queen.column != column:
            conflict += 1
    return conflict

def refresh_conflicts(board):
    for queen in board.queens:
        if watch_conflicts(queen.row, queen.column, board) != 0:
            board.queensConflicts[queen.id] = True
        else:
            board.queensConflicts[queen.id] = False
        
# Funcion de heuristica
def calculate_better_position(queenId, board):
    heuristics = [-1,-1,-1,-1,-1,-1,-1,-1]
    #row           0  1  2  3  4  5  6  7
    #Debemos calcular la cantidad de conflictos por fila y elegir el menor
    actualQueen = board.find_queen(queenId)
    for row in range(len(heuristics)):
        quantityOfConflicts = 0
        quantityOfConflicts = watch_conflicts(row, actualQueen.column, board)
        heuristics[row] = quantityOfConflicts
    
    board.queens[actualQueen.id].row = heuristics.index(min(heuristics))
    refresh_conflicts(board)
    return board
        
    
#Hill climbing
    # Evaluar el estado inicial
    # Si es un estado objetivo entonces devolverlo y parar
    # si no ACTUAL = Inicial
    # Mientras haya operadores aplicables a ACTUAL y no se haya encontrado solución
        # Seleccionar un operador no aplicado todavía a ACTUAL
        # aplicar operador y generar NUEVOESTADO
        # evaluar NUEVOESTADO
        # si es un estado objetivo entonces devolverlo y parar
        # si no 
            # si NUEVOESTADO es mejor que ACTUAL
                #entonces ACTUAl = NUEVOESTADO
            #fin si
        #fin si
    # fin mientras
    #fin si

def hill_climbing(board):
    isSolution = board.isSolution()
    actual = board
    while isSolution != True:
        #Condicion de victoria

        if actual.isSolution() == True:
            isSolution = True
        
        for queenId, isOnConflict in actual.queensConflicts.items():
            if isOnConflict == True:
                actual = calculate_better_position(queenId,actual)
                nuevoestado = actual
                if nuevoestado.isSolution() == True:
                    isSolution = True
                if nuevoestado.quantityOfConflicts() < actual.quantityOfConflicts():
                    actual = nuevoestado             
            
                

def main():
    queens = []
    queens.append(Queen(0,1,0))
    queens.append(Queen(1,4,1))
    queens.append(Queen(2,6,2))
    queens.append(Queen(3,3,3))
    queens.append(Queen(4,0,4))
    queens.append(Queen(5,2,5))
    queens.append(Queen(6,5,6))
    queens.append(Queen(7,7,7))

    queenConflicts = {0:False, 1: False, 2:False, 3:True, 4:False,5:False,6:False,7:True}
    board = Board(queens,queenConflicts)

    start = timer()
    hill_climbing(board)
    end = timer()
    print(end - start)
main()