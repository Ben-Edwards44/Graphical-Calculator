import gui
import pygame
import calculator_utils
import simul_equation_utils


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class SimulEquationMenu:
    EQUATIONS_TOP_LEFT = (100, 100)

    SOLVE_BUTTON_TOP_LEFT = (20, 20)
    SOLVE_BUTTON_WIDTH = 80
    SOLVE_BUTTON_HEIGHT = 50


    def __init__(self, window):
        self.window = window

        self.solve_button = self.setup_solve_button()
        
        self.equations = self.create_equations(3)

    def setup_solve_button(self):
        solve_button = gui.ColourChangeButton(SimulEquationMenu.SOLVE_BUTTON_TOP_LEFT, SimulEquationMenu.SOLVE_BUTTON_WIDTH, SimulEquationMenu.SOLVE_BUTTON_HEIGHT, "Solve")

        return solve_button

    def create_equations(self, num_equations):
        #the number of variables in each equation is the same as the number of equations
        equations = []
        for i in range(num_equations):
            equation = Equation(self.window, i, num_equations)

            equations.append(equation)

        return equations
    
    def solve_equations(self):
        equation_variables = [equation.get_variable_coefficients() for equation in self.equations]
        equation_constants = [equation.get_constant() for equation in self.equations]

        equation_system = simul_equation_utils.SystemEquations(equation_variables, equation_constants)
        solutions = equation_system.solve()

        print(solutions)
    
    def check_user_input(self):
        for equation in self.equations:
            equation.check_user_input()

        if self.solve_button.is_clicked(): self.solve_equations()
    
    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.solve_button.draw(self.window)

        for equation in self.equations:
            equation.draw()

        pygame.display.update()


class Equation:
    FIRST_EQUATION_POS = (100, 100)  #top left of the first equation

    HEIGHT = 50

    PADDING_Y = 10  #gap between equations

    def __init__(self, window, equation_index, num_variables):
        self.window = window

        self.top_left = self.calculate_top_left(equation_index)

        self.variables, self.constant = self.create_elements(num_variables)

    def calculate_top_left(self, equation_index):
        y_step = Equation.HEIGHT + Equation.PADDING_Y
        y_pos = Equation.FIRST_EQUATION_POS[1] + equation_index * y_step

        return (Equation.FIRST_EQUATION_POS[0], y_pos)

    def create_elements(self, num_variables):
        #setup the variables and the constant used by the equation
        x_step = Variable.INPUT_WIDTH + Variable.TEXT_WIDTH

        variables = []
        for i in range(num_variables):
            variable_name = ALPHABET[i]
            top_left = (self.top_left[0] + i * x_step, self.top_left[1])

            variables.append(Variable(self.window, variable_name, top_left))

        top_left = (self.top_left[0] + num_variables * x_step, self.top_left[1])
        constant = Constant(self.window, top_left)

        return variables, constant
    
    def get_variable_coefficients(self):
        #evaluate the coefficients of each variable
        coefficients = [variable.get_coefficient() for variable in self.variables]

        return coefficients
    
    def get_constant(self):
        constant = self.constant.get_coefficient()

        return constant
    
    def check_user_input(self):
        for variable in self.variables:
            variable.check_user_input()

        self.constant.check_user_input()

    def draw(self):
        for variable in self.variables:
            variable.draw()

        self.constant.draw()


class Variable:
    INPUT_WIDTH = 50
    INPUT_HEIGHT = 50

    TEXT_WIDTH = 50

    FONT_SIZE = 32

    def __init__(self, window, name, top_left):
        self.window = window
        self.name = name
        self.top_left = top_left

        self.input_box = self.setup_input()
        self.name_text = self.setup_text()

    def setup_input(self):
        input_box = gui.TextInput(self.top_left, Variable.INPUT_WIDTH, Variable.INPUT_HEIGHT, "...")
        input_box.set_font_size(Variable.FONT_SIZE)

        return input_box

    def setup_text(self):
        center_x = self.top_left[0] + Variable.INPUT_WIDTH + Variable.TEXT_WIDTH // 2
        center_y = self.top_left[1] + Variable.INPUT_HEIGHT // 2

        text = gui.DisplayText(self.name, (center_x, center_y))
        text.set_font_size(Variable.FONT_SIZE)

        return text
    
    def get_coefficient(self):
        #evaluate the expression entered into the coefficient input box and return it
        expression = self.input_box.get_inputted_text()
        coefficient = calculator_utils.evaluate_expression(expression)

        return coefficient
    
    def check_user_input(self):
        self.input_box.check_user_input()
    
    def draw(self):
        self.input_box.draw(self.window)
        self.name_text.draw(self.window)


class Constant(Variable):
    #The constant will draw a "=" symbol in front of the input box

    def __init__(self, window, top_left):
        super().__init__(window, "=", top_left)

    def setup_input(self):
        #overrides Variable.setup_input()
        top_left_x = self.top_left[0] + Variable.TEXT_WIDTH
        top_left_y = self.top_left[1]

        input_box = gui.TextInput((top_left_x, top_left_y), Variable.INPUT_WIDTH, Variable.INPUT_HEIGHT, "...")
        input_box.set_font_size(Variable.FONT_SIZE)

        return input_box

    def setup_text(self):
        #overrides Variable.setup_text()
        center_x = self.top_left[0] + Variable.TEXT_WIDTH // 2
        center_y = self.top_left[1] + Variable.INPUT_HEIGHT // 2

        text = gui.DisplayText(self.name, (center_x, center_y))
        text.set_font_size(Variable.FONT_SIZE)

        return text


def main(window):
    menu = SimulEquationMenu(window)

    while True:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()