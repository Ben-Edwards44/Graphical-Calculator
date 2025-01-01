import gui
import pygame

import matrix_utils


DIGITS = "0123456789"


class MatrixMenu:
    def __init__(self):
        pass


class DefinedMatrix:
    INPUT_WIDTH = 50
    INPUT_HEIGHT = 50

    INPUT_PADDING_X = 10
    INPUT_PADDING_Y = 10

    NAME_TEXT_PADDING_Y = 50

    #dimensions for the enter width, enter height and done buttons
    BUTTON_PADDING_X = 50
    BUTTON_PADDING_Y = 50

    BUTTON_WIDTH = 75
    BUTTON_HEIGHT = 50

    def __init__(self, window, name):
        self.window = window

        self.name = name

        self.width = 3
        self.height = 3

        self.is_defined = False

        self.top_left = self.calculate_top_left()

        self.input_grid = self.setup_input_grid()
        self.name_text = self.setup_name_text()
        self.width_input, self.height_input, self.done_button = self.setup_button_row()

    def setup_input_grid(self):
        input_grid = [[None for _ in range(self.width)] for _ in range(self.height)]  #blank 2d array

        for x in range(self.width):
            for y in range(self.height):
                top_left_x = self.top_left[0] + x * (DefinedMatrix.INPUT_WIDTH + DefinedMatrix.INPUT_PADDING_X)
                top_left_y = self.top_left[1] + y * (DefinedMatrix.INPUT_HEIGHT + DefinedMatrix.INPUT_PADDING_Y)

                input_box = gui.TextInput((top_left_x, top_left_y), DefinedMatrix.INPUT_WIDTH, DefinedMatrix.INPUT_HEIGHT, "0")

                input_grid[y][x] = input_box

        return input_grid
    
    def setup_button_row(self):
        total_width = 3 * DefinedMatrix.BUTTON_WIDTH + 2 * DefinedMatrix.BUTTON_PADDING_X

        top_left_x, _ = gui.calculate_centered_top_left(total_width, DefinedMatrix.BUTTON_HEIGHT)
        top_left_y = DefinedMatrix.BUTTON_PADDING_Y
        
        x_step = DefinedMatrix.BUTTON_WIDTH + DefinedMatrix.BUTTON_PADDING_X

        width_input = gui.TextInput((top_left_x, top_left_y), DefinedMatrix.BUTTON_WIDTH, DefinedMatrix.BUTTON_HEIGHT, "Enter width:")
        height_input = gui.TextInput((top_left_x + x_step, top_left_y), DefinedMatrix.BUTTON_WIDTH, DefinedMatrix.BUTTON_HEIGHT, "Enter height:")
        done_button = gui.ColourChangeButton((top_left_x + 2 * x_step, top_left_y), DefinedMatrix.BUTTON_WIDTH, DefinedMatrix.BUTTON_HEIGHT, "done")

        return width_input, height_input, done_button
    
    def setup_name_text(self):
        center_pos = (gui.SCREEN_WIDTH // 2, self.top_left[1] - DefinedMatrix.NAME_TEXT_PADDING_Y)
        name_text = gui.DisplayText(self.name, center_pos)
        name_text.set_font_colour((255, 255, 255))

        return name_text
    
    def calculate_top_left(self):
        total_width = DefinedMatrix.INPUT_WIDTH * self.width + DefinedMatrix.INPUT_PADDING_X * (self.width - 1)
        total_height = DefinedMatrix.INPUT_HEIGHT * self.height + DefinedMatrix.INPUT_PADDING_Y * (self.height - 1)

        top_left = gui.calculate_centered_top_left(total_width, total_height)

        return top_left
    
    def check_entered_num(self, text_input, prev_num):
        entered_text = text_input.get_inputted_text()

        is_int = True
        for i in entered_text:
            if i not in DIGITS: is_int = False

        if len(entered_text) > 0 and is_int:
            entered_num = int(entered_text)
            has_changed = entered_num != prev_num

            return has_changed, entered_num
        else:
            return False, 0
    
    def update_dimensions(self):
        self.width_input.check_user_input()
        self.height_input.check_user_input()

        width_changed, new_width = self.check_entered_num(self.width_input, self.width)
        height_changed, new_height = self.check_entered_num(self.height_input, self.height)

        if width_changed:
            self.width = new_width
        if height_changed:
            self.height = new_height

        needs_update = width_changed or height_changed

        if needs_update:
            #the size of the matrix has changed so we need to move all the gui elements around
            self.top_left = self.calculate_top_left()
            self.input_grid = self.setup_input_grid()
            self.name_text = self.setup_name_text()
    
    def check_user_input(self):
        self.update_dimensions()

        for input_row in self.input_grid:
            for input_box in input_row:
                input_box.check_user_input()

        if self.done_button.is_clicked(): self.is_defined = True

    def draw(self):
        self.name_text.draw(self.window)
        self.width_input.draw(self.window)
        self.height_input.draw(self.window)
        self.done_button.draw(self.window)

        for input_row in self.input_grid:
            for input_box in input_row:
                input_box.draw(self.window)


def main(window):
    temp = DefinedMatrix(window, "Matrix A")

    while True:
        window.fill((0, 0, 0))
        temp.draw()
        temp.check_user_input()
        pygame.display.update()

        gui.check_user_quit()