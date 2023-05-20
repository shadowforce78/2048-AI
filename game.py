import pygame
import random
import tensorflow as tf
import numpy as np

# Définition des constantes
WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048")


# Fonction pour initialiser la grille
def init_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    return grid


# Fonction pour ajouter une nouvelle tuile à la grille
def add_new_tile(grid):
    empty_cells = [
        (i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0
    ]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = random.choice([2, 4])


# Fonction pour afficher la grille
def draw_grid(grid):
    window.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = grid[row][col]
            cell_color = CELL_COLORS.get(cell_value, (255, 255, 255))
            pygame.draw.rect(
                window,
                cell_color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            if cell_value != 0:
                font = pygame.font.Font(None, 50)
                text = font.render(str(cell_value), True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2,
                    )
                )
                window.blit(text, text_rect)
    pygame.display.update()


# Fonction pour déplacer les tuiles vers la gauche
def move_left(grid):
    for row in range(GRID_SIZE):
        merged_row = False  # Indicateur pour la fusion dans la ligne
        for col in range(1, GRID_SIZE):
            if grid[row][col] != 0:
                value = grid[row][col]
                i = col - 1
                while i >= 0 and grid[row][i] == 0:
                    grid[row][i] = value
                    grid[row][i + 1] = 0
                    i -= 1
                if i >= 0 and grid[row][i] == value and not merged_row:
                    grid[row][i] *= 2
                    grid[row][col] = 0
                    merged_row = True  # Indiquer la fusion dans la ligne


# Fonction pour inverser la grille
def transpose_grid(grid):
    grid[:] = [list(row) for row in zip(*grid)]


# Fonction pour inverser les lignes de la grille
def reverse_grid(grid):
    for row in grid:
        row.reverse()


# Fonction pour mettre à jour la grille en fonction de la touche pressée
def update_grid(grid, key):
    if key == pygame.K_LEFT:
        move_left(grid)
    elif key == pygame.K_RIGHT:
        # Ajouter le code pour le mouvement vers la droite
        reverse_grid(grid)
        move_left(grid)
        reverse_grid(grid)
    elif key == pygame.K_UP:
        # Ajouter le code pour le mouvement vers le haut
        transpose_grid(grid)
        move_left(grid)
        transpose_grid(grid)
    elif key == pygame.K_DOWN:
        # Ajouter le code pour le mouvement vers le bas
        transpose_grid(grid)
        reverse_grid(grid)
        move_left(grid)
        reverse_grid(grid)
        transpose_grid(grid)


# Fonction pour vérifier si aucun mouvement n'est possible
def is_game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True


# Fonction principale pour jouer au jeu
def play_game():
    grid = init_grid()
    add_new_tile(grid)
    draw_grid(grid)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                elif event.key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ]:
                    prev_grid = [
                        row[:] for row in grid
                    ]  # Copie de la grille précédente
                    update_grid(grid, event.key)
                    if grid != prev_grid:
                        add_new_tile(grid)
                    draw_grid(grid)
                    if is_game_over(grid):
                        grid = init_grid()
                        add_new_tile(grid)
                        draw_grid(grid)


# Fonction principale pour jouer au jeu
play_game()
