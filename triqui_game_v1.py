import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pantalla de juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Triqui')  # Línea corregida

# Fuente para los nombres de los jugadores
font = pygame.font.Font(None, 36)

# Variables del juego
players = []
current_player = 0
board = [['' for _ in range(3)] for _ in range(3)]
game_over = False

# Cargar archivos de sonido
pygame.mixer.music.load('game_proj/sounds/furelise.mp3')  # Ruta relativa a la melodía de fondo
gong_sound = pygame.mixer.Sound('game_proj/sounds/gong.mp3')  # Ruta relativa al sonido de gong

def draw_board():
    screen.fill(WHITE)
    # Dibujar líneas horizontales
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE * 2), (WIDTH, CELL_SIZE * 2), LINE_WIDTH)
    # Dibujar líneas verticales
    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, HEIGHT), LINE_WIDTH)

def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 10), 
                                 (col * CELL_SIZE + CELL_SIZE - 10, row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
                pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE - 10, row * CELL_SIZE + 10), 
                                 (col * CELL_SIZE + 10, row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 
                                   CELL_SIZE // 2 - 10, LINE_WIDTH)

def check_winner():
    # Verificar filas, columnas y diagonales
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def main():
    global current_player, game_over
    
    # Solicitar nombres de los jugadores
    players.append(input("Nombre del jugador 1 (X): "))
    players.append(input("Nombre del jugador 2 (O): "))
    current_player = random.choice([0, 1])
    
    # Iniciar melodía de fondo en bucle
    pygame.mixer.music.play(-1)  # -1 significa que la música se reproducirá en bucle
    
    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // CELL_SIZE
                clicked_col = mouseX // CELL_SIZE
                if board[clicked_row][clicked_col] == '':
                    if current_player == 0:
                        board[clicked_row][clicked_col] = 'X'
                    else:
                        board[clicked_row][clicked_col] = 'O'
                    winner = check_winner()
                    if winner:
                        game_over = True
                        pygame.mixer.music.stop()  # Detener melodía de fondo
                        gong_sound.play()  # Reproducir sonido de gong
                        print(f"¡{players[current_player]} ha ganado!")
                    else:
                        current_player = 1 - current_player
        
        draw_board()
        draw_marks()
        pygame.display.flip()

if __name__ == "__main__":
    main()
