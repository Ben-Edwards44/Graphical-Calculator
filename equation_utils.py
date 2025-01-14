import calculator_utils


class ArbitraryEquation:
    SMALL_X_STEP = 0.01

    NUM_NEWTON_RAPHSON_STEPS = 20

    SOLUTION_SEARCH_RESOLUTION = 50

    TOLERANCE = 0.001

    def __init__(self, equation_string):
        self.equation_string = equation_string
        self.lhs, self.rhs = self.extract_sides()

    def extract_sides(self):
        #extract the left hand side and right hand side of the equation
        left, right = self.equation_string.split("=")

        return left, right
    
    def substitute_variable(self, expression, x_value):
        substituted_expression = ""
        for char in expression:
            if char == "x":
                substituted_expression += f"({x_value})"
            else:
                substituted_expression += char

        return substituted_expression
    
    def evaluate_equals_zero(self, x_value):
        #evaluate the equation as if it was in the form f(x)=0
        left_substituted = self.substitute_variable(self.lhs, x_value)
        right_substituted = self.substitute_variable(self.rhs, x_value)

        left = calculator_utils.evaluate_expression(left_substituted)
        right = calculator_utils.evaluate_expression(right_substituted)

        #the equation is in form lhs=rhs, but we want it to be f(x)=0. Subtracting rhs gives lhs-rhs=0, which is in the right form
        evaluation = left - right

        return evaluation

    def differentiate(self, x_value):
        y1 = self.evaluate_equals_zero(x_value)
        y2 = self.evaluate_equals_zero(x_value + ArbitraryEquation.SMALL_X_STEP)

        gradient = (y2 - y1) / ArbitraryEquation.SMALL_X_STEP

        return gradient
    
    def solve(self, start_x_value):
        x = start_x_value

        #apply the Newton-Raphson method to solve the equation
        for _ in range(ArbitraryEquation.NUM_NEWTON_RAPHSON_STEPS):
            print(x)
            x = x - self.evaluate_equals_zero(x) / self.differentiate(x)

        return x
    
    def find_all_solutions(self, min_x, max_x):
        #find all the solutions to the equation in the range min_x <= x <= max_x
        x_step = (max_x - min_x) / ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION

        solutions = []
        for step in range(ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION):
            start_x = min_x + step * x_step
            solution = self.solve(start_x)
            is_actual_solution = abs(self.evaluate_equals_zero(solution)) < ArbitraryEquation.TOLERANCE  #the Newton-Raphson method does not always converge, so sometimes gives numbers that are not solutions

            if min_x <= solution <= max_x and is_new_element(solutions, solution, ArbitraryEquation.TOLERANCE) and is_actual_solution:
                solutions.append(solution)

        return solutions


def is_new_element(list, num, tolerance):
    #determine if the num is in the list, within a given tolerance (e.g. 5.001 should not be new to [3, 4, 5])
    for element in list:
        if abs(element - num) < tolerance:
            return False  #already in list

    return True