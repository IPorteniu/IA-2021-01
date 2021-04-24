import pygame
from Sudoku import Sudoku
from timeit import default_timer as timer
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

example_2 = [
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

# Variables de utilidad para el Sudoku gráfico
WIDTH = 720
BACKGROUND_COLOR = (251, 247, 245)
NUMBERS_COLOR = (52, 31, 151)

# Dibujamos las lineas del Sudoku gráfico
def draw_lines(window):
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(window, (0, 0, 0), (50 + 50*i, 50),
                             (50 + 50 * i, 500), 4)
            pygame.draw.line(window, (0, 0, 0), (50, 50+50*i),
                             (500, 50 + 50*i), 4)
        pygame.draw.line(window, (0, 0, 0), (50 + 50*i, 50),
                         (50 + 50 * i, 500), 2)
        pygame.draw.line(window, (0, 0, 0), (50, 50+50*i), (500, 50 + 50*i), 2)
    pygame.display.update()

# Dibujamos/insertamos los valores al Sudoku gráfico
def draw_values(sudoku, window):
    my_font = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(sudoku[0])):
        for j in range(0, len(sudoku[0])):
            # Aca colocamos el sudoku
            if 0 < sudoku[i][j]<10:
                value = my_font.render(str(sudoku[i][j]), True, NUMBERS_COLOR)
                window.blit(value, ((j+1)*50 + 15, (i+1)*50))
    pygame.display.update()

# Dibujamos el menú del Sudoku gráfico
def draw_menu(window):
    my_font = pygame.font.SysFont('Comic Sans MS', 15)
    # Primer texto render
    first = my_font.render('1.- Hill Climbing ',True,NUMBERS_COLOR)
    first_rect = first.get_rect()
    first_rect.center = (120,600)
    window.blit(first,first_rect)
    # Segundo texto render
    second = my_font.render('2.- Demostración Simulated Annealing',True,NUMBERS_COLOR)
    second_rect = second.get_rect()
    second_rect.center = (140,620)
    window.blit(second,second_rect)
    pygame.display.update()

# Eventos que se activan según la tecla presionada
def key_stroke(sudoku, window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                return
            if event.type == pygame.KEYDOWN:
                sudoku.insert_row_values()
                if event.key == 49:
                    window.fill(BACKGROUND_COLOR)
                    draw_lines(window)
                    start = timer()
                    draw_values(sudoku.hill_climbing(),window)
                    end = timer()
                    print(end-start)
                    
                if event.key == 50:
                    window.fill(BACKGROUND_COLOR)
                    draw_lines(window)
                    start = timer()
                    draw_values(sudoku.simulated_annealing(),window)
                    end = timer()
                    print(end-start)

# Función de inicio
def start():
    # Se cargan todas las variables e inicia todo el programa
    example = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]]
    pygame.init()
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    window.fill(BACKGROUND_COLOR)
    draw_lines(window)
    draw_values(example,window)
    draw_menu(window)
    sudoku = Sudoku(example)
    draw_values(sudoku.sudoku,window)
    key_stroke(sudoku, window)

# Main
start()
