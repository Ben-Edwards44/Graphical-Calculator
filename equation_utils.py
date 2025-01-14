import calculator_utils


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class ArbitraryEquation:
    SMALL_X_STEP = 0.01

    NUM_NEWTON_RAPHSON_STEPS = 20

    SOLUTION_SEARCH_RESOLUTION = 50

    TOLERANCE = 0.001

    def __init__(self, equation_string):
        self.equation_string = equation_string

        self.lhs, self.rhs = self.extract_sides()
        self.variable_name = self.extract_variable_name()

    def extract_sides(self):
        #extract the left hand side and right hand side of the equation
        left, right = self.equation_string.split("=")

        return left, right
    
    def extract_variable_name(self):
        #most of the time, the variable name will be 'x' or 'y'. By convention, variable names are only a single character
        for char in self.equation_string:
            if char in ALPHABET:
                return char
    
    def substitute_variable(self, expression, variable_value):
        substituted_expression = ""
        for char in expression:
            if char == self.variable_name:
                substituted_expression += f"({variable_value})"
            else:
                substituted_expression += char

        return substituted_expression
    
    def evaluate_equals_zero(self, variable_value):
        #evaluate the equation as if it was in the form f(x)=0
        left_substituted = self.substitute_variable(self.lhs, variable_value)
        right_substituted = self.substitute_variable(self.rhs, variable_value)

        left = calculator_utils.evaluate_expression(left_substituted)
        right = calculator_utils.evaluate_expression(right_substituted)

        #the equation is in form lhs=rhs, but we want it to be f(x)=0. Subtracting rhs gives lhs-rhs=0, which is in the right form
        evaluation = left - right

        return evaluation

    def differentiate(self, variable_value):
        y1 = self.evaluate_equals_zero(variable_value)
        y2 = self.evaluate_equals_zero(variable_value + ArbitraryEquation.SMALL_X_STEP)

        gradient = (y2 - y1) / ArbitraryEquation.SMALL_X_STEP

        return gradient
    
    def solve(self, start_variable_value):
        variable = start_variable_value

        #apply the Newton-Raphson method to solve the equation
        for _ in range(ArbitraryEquation.NUM_NEWTON_RAPHSON_STEPS):
            variable = variable - self.evaluate_equals_zero(variable) / self.differentiate(variable)

        return variable
    
    def find_all_solutions(self, min, max):
        #find all the solutions to the equation in the range min <= solution <= max
        x_step = (max - min) / ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION

        solutions = []
        for step in range(ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION):
            start_x = min + step * x_step
            solution = self.solve(start_x)
            is_actual_solution = abs(self.evaluate_equals_zero(solution)) < ArbitraryEquation.TOLERANCE  #the Newton-Raphson method does not always converge, so sometimes gives numbers that are not solutions

            if min <= solution <= max and is_new_element(solutions, solution, ArbitraryEquation.TOLERANCE) and is_actual_solution:
                solutions.append(solution)

        return solutions


def is_new_element(list, num, tolerance):
    #determine if the num is in the list, within a given tolerance (e.g. 5.001 should not be new to [3, 4, 5])
    for element in list:
        if abs(element - num) < tolerance:
            return False  #already in list

    return True