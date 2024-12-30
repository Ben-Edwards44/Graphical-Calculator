import gui
import pygame
import simul_equation_utils


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class SimulEquationMenu:
    TOP_LEFT = (100, 100)

    WIDTH = gui.SCREEN_WIDTH - 2 * TOP_LEFT[0]
    HEIGHT = gui.SCREEN_HEIGHT - 2 * TOP_LEFT[1]

    EQUATION_PADDING_X = 5
    EQUATION_PADDING_Y = 5

    def __init__(self, window):
        self.window = window

        self.equations = self.create_equations(4)

    def create_equations(self, num_equations):
        #the number of variables in each equation is the same as the number of equations
        top_left_x = SimulEquationMenu.TOP_LEFT[0] + SimulEquationMenu.EQUATION_PADDING_X

        equation_width = SimulEquationMenu.WIDTH - 2 * SimulEquationMenu.EQUATION_PADDING_X
        equation_height = (SimulEquationMenu.HEIGHT - SimulEquationMenu.EQUATION_PADDING_Y * num_equations) // num_equations  #ensures equations take up all available space regardless of how many there are

        equations = []
        for i in range(num_equations):
            top_left_y = (equation_height + SimulEquationMenu.EQUATION_PADDING_Y) * i
            equation = Equation(self.window, equation_width, equation_height, (top_left_x, top_left_y), num_equations)

            equations.append(equation)

        return equations
    
    def check_user_input(self):
        for equation in self.equations:
            equation.check_user_input()
    
    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        for equation in self.equations:
            equation.draw()

        pygame.display.update()


class Equation:
    def __init__(self, window, width, height, top_left, num_variables):
        self.window = window

        self.width = width
        self.height = height

        self.top_left = top_left

        self.variables = self.create_variables(num_variables)

    def create_variables(self, num_variables):
        x_step = self.width // (num_variables + 1)  #the +1 is because there is a constant at the end of the equation

        variables = []
        for i in range(num_variables):
            variable_name = ALPHABET[i]
            top_left = (self.top_left[0] + i * x_step, self.top_left[1])

            variables.append(Variable(self.window, variable_name, top_left))

        return variables
    
    def check_user_input(self):
        for variable in self.variables:
            variable.check_user_input()

    def draw(self):
        for variable in self.variables:
            variable.draw()


class Variable:
    INPUT_WIDTH = 50
    INPUT_HEIGHT = 50

    TEXT_PADDING = 5

    FONT_SIZE = 32

    def __init__(self, window, name, top_left):
        self.window = window
        self.name = name
        self.top_left = top_left

        self.input = self.setup_input()
        self.name_text = self.setup_text()

    def setup_input(self):
        input_box = gui.TextInput(self.top_left, Variable.INPUT_WIDTH, Variable.INPUT_HEIGHT, "...")
        input_box.set_font_size(Variable.FONT_SIZE)

        return input_box

    def setup_text(self):
        center_x = self.top_left[0] + Variable.INPUT_WIDTH + Variable.TEXT_PADDING
        center_y = self.top_left[1] + Variable.INPUT_HEIGHT // 2

        text = gui.DisplayText(self.name, (center_x, center_y))
        text.set_font_size(Variable.FONT_SIZE)

        return text
    
    def check_user_input(self):
        self.input.check_user_input()
    
    def draw(self):
        self.input.draw(self.window)
        self.name_text.draw(self.window)


def main(window):
    menu = SimulEquationMenu(window)

    while True:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()