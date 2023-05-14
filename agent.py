import pygame
import game
import tensorflow as tf
import numpy as np
import random

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
        grid = game.init_grid()
        while True:
            prev_grid = [row[:] for row in grid]
            key = np.random.choice(MOUVES)
            game.update_grid(grid, key)
            if grid != prev_grid:
                X.append(grid)
                y.append(MOUVES.index(key))
                break
    X = np.array(X)
    y = tf.keras.utils.to_categorical(y)
    return X, y


def train_model(model, X, y):
    model.fit(X, y, epochs=10)

def play_game(model):
    grid = game.init_grid()
    game.add_new_tile(grid)
    game.draw_grid(grid)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                elif event.key in MOUVES:
                    prev_grid = [row[:] for row in grid]
                    game.update_grid(grid, event.key)
                    if grid != prev_grid:
                        game.add_new_tile(grid)
                    game.draw_grid(grid)
                    if game.is_game_over(grid):
                        pygame.quit()
                        return
                    X = np.array([grid])
                    y = model.predict(X)
                    key = MOUVES[np.argmax(y)]
                    prev_grid = [row[:] for row in grid]
                    game.update_grid(grid, key)
                    if grid != prev_grid:
                        game.add_new_tile(grid)
                    game.draw_grid(grid)
                    if game.is_game_over(grid):
                        pygame.quit()
                        return

def main():
    pygame.init()
    window = pygame.display.set_mode((game.WINDOW_SIZE, game.WINDOW_SIZE))
    pygame.display.set_caption("2048")
    model = get_model()
    X, y = get_data()
    train_model(model, X, y)
    play_game(model)

if __name__ == '__main__':
    main()
