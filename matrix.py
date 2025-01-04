import gui
import pygame

import matrix_utils


DIGITS = "0123456789"


class MatrixMenu:
    def __init__(self):
        pass


class DisplayMatrix:
    NUM_WIDTH = 50
    NUM_HEIGHT = 50

    NUM_PADDING_X = 10
    NUM_PADDING_Y = 10

    NAME_TEXT_PADDING_Y = 50

    def __init__(self, window, name, matrix):
        self.window = window

        self.name = name

        self.matrix = matrix  #matrix_utils.Matrix object

        self.go_back = False

        self.top_left = self.calculate_top_left()

        self.num_grid = self.setup_num_grid()
        self.name_text = self.setup_name_text()
        self.back_button = gui.create_back_button()

    def setup_num_grid(self):
        num_grid = [[None for _ in range(self.matrix.width)] for _ in range(self.matrix.height)]  #blank 2d array

        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                num = self.matrix.items[y][x]

                top_left_x = self.top_left[0] + x * (DisplayMatrix.NUM_WIDTH + DisplayMatrix.NUM_PADDING_X)
                top_left_y = self.top_left[1] + y * (DisplayMatrix.NUM_HEIGHT + DisplayMatrix.NUM_PADDING_Y)

                #Text inputs are used to display each number so that the numbers can be edited in the DefinedMatrix class
                input_box = gui.TextInput((top_left_x, top_left_y), DisplayMatrix.NUM_WIDTH, DisplayMatrix.NUM_HEIGHT, str(num))

                num_grid[y][x] = input_box

        return num_grid
    
    def setup_name_text(self):
        center_pos = (gui.SCREEN_WIDTH // 2, self.top_left[1] - DisplayMatrix.NAME_TEXT_PADDING_Y)
        name_text = gui.DisplayText(self.name, center_pos)
        name_text.set_font_colour((255, 255, 255))

        return name_text
    
    def calculate_top_left(self):
        total_width = DisplayMatrix.NUM_WIDTH * self.matrix.width + DisplayMatrix.NUM_PADDING_X * (self.matrix.width - 1)
        total_height = DisplayMatrix.NUM_HEIGHT * self.matrix.height + DisplayMatrix.NUM_PADDING_Y * (self.matrix.height - 1)

        top_left = gui.calculate_centered_top_left(total_width, total_height)

        return top_left
    
    def check_user_input(self):
        if self.back_button.is_clicked():
            self.go_back = True

    def draw(self):
        self.name_text.draw(self.window)
        self.back_button.draw(self.window)

        for num_row in self.num_grid:
            for num in num_row:
                num.draw(self.window)


class DefinedMatrix(DisplayMatrix):
    DEFAULT_WIDTH = 3
    DEFAULT_HEIGHT = 3

    #dimensions for the enter width and enter height buttons
    BUTTON_PADDING_X = 50
    BUTTON_PADDING_Y = 50

    BUTTON_WIDTH = 75
    BUTTON_HEIGHT = 50

    def __init__(self, window, name):
        super().__init__(window, name, self.create_blank_matrix(DefinedMatrix.DEFAULT_WIDTH, DefinedMatrix.DEFAULT_HEIGHT))        

        self.is_defined = False

        self.width_input, self.height_input = self.setup_dimension_change_buttons()
    
    def create_blank_matrix(self, width, height):
        items = [[0 for _ in range(width)] for _ in range(height)]
        matrix_object = matrix_utils.Matrix(items)

        return matrix_object

    def setup_dimension_change_buttons(self):
        #the dimension change buttons are centered vertically, but placed DefinedMatrix.BUTTON_PADDING_X away from the left of the screen
        total_height = 2 * DefinedMatrix.BUTTON_HEIGHT + DefinedMatrix.BUTTON_PADDING_Y
        _, top_left_y = gui.calculate_centered_top_left(DefinedMatrix.BUTTON_WIDTH, total_height)
        top_left_x = DefinedMatrix.BUTTON_PADDING_X
        
        y_step = DefinedMatrix.BUTTON_HEIGHT + DefinedMatrix.BUTTON_PADDING_Y

        width_input = gui.TextInput((top_left_x, top_left_y), DefinedMatrix.BUTTON_WIDTH, DefinedMatrix.BUTTON_HEIGHT, "Enter width:")
        height_input = gui.TextInput((top_left_x, top_left_y + y_step), DefinedMatrix.BUTTON_WIDTH, DefinedMatrix.BUTTON_HEIGHT, "Enter height:")

        return width_input, height_input
    
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

        width_changed, new_width = self.check_entered_num(self.width_input, self.matrix.width)
        height_changed, new_height = self.check_entered_num(self.height_input, self.matrix.height)

        if not width_changed:
            new_width = self.matrix.width  #just use the previous width
        if not height_changed:
            new_height = self.matrix.height  #just use the previous height

        needs_update = width_changed or height_changed

        if needs_update:
            #the size of the matrix has changed so we need to move all the gui elements around
            self.matrix = self.create_blank_matrix(new_width, new_height)

            self.top_left = self.calculate_top_left()
            self.num_grid = self.setup_num_grid()
            self.name_text = self.setup_name_text()
    
    def check_user_input(self):
        #overrides DisplayMatrix.check_user_input()
        super().check_user_input()

        self.update_dimensions()

        for input_row in self.num_grid:
            for input_box in input_row:
                input_box.check_user_input()

    def draw(self):
        #overrides DisplayMatrix.draw()
        super().draw()

        self.width_input.draw(self.window)
        self.height_input.draw(self.window)


def main(window):
    #m = matrix_utils.Matrix([[1, 2],
    #                         [3, 4]])
    #temp = DisplayMatrix(window, "Matrix A", m)
    temp = DefinedMatrix(window, "test")

    while True:
        window.fill((0, 0, 0))
        temp.draw()
        temp.check_user_input()
        pygame.display.update()

        gui.check_user_quit()