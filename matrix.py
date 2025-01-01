import gui
import pygame

import matrix_utils


class MatrixMenu:
    def __init__(self):
        pass


class NewMatrix:
    INPUT_WIDTH = 50
    INPUT_HEIGHT = 50

    PADDING_X = 10
    PADDING_Y = 10

    def __init__(self, window, width, height):
        self.window = window

        self.width = width
        self.height = height

        self.top_left = self.calculate_top_left()
        self.input_grid = self.setup_input_grid()

    def calculate_top_left(self):
        total_width = NewMatrix.INPUT_WIDTH * self.width + NewMatrix.PADDING_X * (self.width - 1)
        total_height = NewMatrix.INPUT_HEIGHT * self.height + NewMatrix.PADDING_Y * (self.height - 1)

        top_left = gui.calculate_centered_top_left(total_width, total_height)

        return top_left

    def setup_input_grid(self):
        input_grid = [[None for _ in range(self.width)] for _ in range(self.height)]  #blank 2d array

        for x in range(self.width):
            for y in range(self.height):
                top_left_x = self.top_left[0] + x * (NewMatrix.INPUT_WIDTH + NewMatrix.PADDING_X)
                top_left_y = self.top_left[1] + y * (NewMatrix.INPUT_HEIGHT + NewMatrix.PADDING_Y)

                input_box = gui.TextInput((top_left_x, top_left_y), NewMatrix.INPUT_WIDTH, NewMatrix.INPUT_HEIGHT, "...")

                input_grid[y][x] = input_box

        return input_grid
    
    def check_user_input(self):
        for input_row in self.input_grid:
            for input_box in input_row:
                input_box.check_user_input()

    def draw(self):
        for input_row in self.input_grid:
            for input_box in input_row:
                input_box.draw(self.window)


def main(window):
    temp = NewMatrix(window, 5, 5)

    while True:
        window.fill((0, 0, 0))
        temp.draw()
        temp.check_user_input()
        pygame.display.update()

        gui.check_user_quit()