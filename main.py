from Maze import Maze, maze_list
from Genetic_algorithm import Genetic_algorithm as GA
from Genetic_algorithm import Direction
import pygame
import time

def display_code(maze: Maze, individuals: list[list[Direction]]):
    pygame.init()
    array = maze.get_array()

    wall_size = 5
    size_y = len(array)
    size_x = len(array[0])
    square_size = 50
    screen = pygame.display.set_mode((square_size * ((size_x + 1) // 2) + wall_size * ((size_x - 1) // 2), square_size * ((size_y + 1) // 2) + wall_size * ((size_y - 1) // 2)))
    pygame.display.set_caption("Maze")

    screen.fill((255, 255, 255))  # Fill the screen with white
    last_flip_time = pygame.time.get_ticks()
    for individual in individuals:
        array = maze.get_array()
        x, y = maze.START
        array[y][x] = 3
        for direction in individual:
            x_inc = 0
            y_inc = 0
            match direction:
                case Direction.Up:
                    y_inc = -1
                case Direction.Down:
                    y_inc = 1
                case Direction.Left:
                    x_inc = -1
                case Direction.Right:
                    x_inc = 1
            array[y + y_inc][x + x_inc] = 3
            array[y + y_inc * 2][x + x_inc * 2] = 3
            x += x_inc * 2
            y += y_inc * 2

        current_y_pixel = 0
        for row in range(size_y):
            current_x_pizel = 0
            for col in range(size_x):
                color: int
                match array[row][col]:
                    case 0:
                        color = 255, 255, 255
                    case 1:
                        color = 0, 0, 0
                    case 2:
                        color = 0, 255, 0
                    case 3:
                        color = 255, 0, 0
                x_size = square_size if not col % 2 else wall_size
                y_size = square_size if not row % 2 else wall_size
                pygame.draw.rect(
                    screen,
                    color,
                    (current_x_pizel, current_y_pixel, x_size, y_size),
                )
                current_x_pizel += x_size
            current_y_pixel += y_size


        pygame.display.flip()

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            if (current_time - last_flip_time) >= 500:
                last_flip_time = current_time
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

def main():
    maze = Maze(maze_list, (36,12))
    ga = GA(maze, 100, 1000, 0.1, 0.1)
    maze.print_array()
    best_solutions = ga.run()
    display_code(maze, best_solutions)

if __name__ == "__main__":
    main()