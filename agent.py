import pygame
from game import *
import tensorflow as tf
import numpy as np

MOUVES = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

def get_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def get_data():
    X = []
    y = []
    for i in range(1000):
        grid = init_grid()
        while True:
            prev_grid = [row[:] for row in grid]
            key = np.random.choice(MOUVES)
            update_grid(grid, key)
            if grid != prev_grid:
                X.append(grid)
                y.append(MOUVES.index(key))
                break
    X = np.array(X)
    y = tf.keras.utils.to_categorical(y)
    return X, y

def update_data(grid, key, X, y):
    prev_grid = [row[:] for row in grid]
    update_grid(grid, key)
    if grid != prev_grid:
        X.append(grid)
        y.append(MOUVES.index(key))

def train_model(model, X, y):
    model.fit(X, y, epochs=10)

# Appel de la fonction principale pour commencer le jeu
def agent_play_game(model, X, y):
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
        best_move = get_best_move(grid, model)
        if best_move:
            prev_grid = [row[:] for row in grid]
            update_grid(grid, best_move)
            update_data(grid, best_move, X, y)
            if grid != prev_grid:
                add_new_tile(grid)
            draw_grid(grid)
            if is_game_over(grid):
                grid = init_grid()
                add_new_tile(grid)
                draw_grid(grid)

if __name__ == '__main__':
    model = get_model()
    X, y = get_data()
    train_model(model, X, y)
    agent_play_game(model, X, y)
