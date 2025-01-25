import calculator_utils


class ArbitraryEquation:
    SMALL_X_STEP = 0.01

    NUM_NEWTON_RAPHSON_STEPS = 6

    SOLUTION_SEARCH_RESOLUTION = 12

    TOLERANCE = 0.01

    def __init__(self, lhs_expression, rhs_expression, variable_to_solve_for):
        self.lhs = lhs_expression
        self.rhs = rhs_expression

        self.variable_name = variable_to_solve_for

        self.variable_substitutions = {}

    def set_variable_substitutions(self, new_variable_substitutions):
        self.variable_substitutions = new_variable_substitutions
    
    def evaluate_equals_zero(self, variable_value):
        #evaluate the equation as if it was in the form f(x)=0
        all_substitutions = self.variable_substitutions.copy()
        all_substitutions[self.variable_name] = variable_value

        left = self.lhs.evaluate(all_substitutions)
        right = self.rhs.evaluate(all_substitutions)

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
    
    def find_all_solutions(self, min, max, known_variable_substitutions):
        #find all the solutions to the equation in the range min <= solution <= max
        self.set_variable_substitutions(known_variable_substitutions)

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


def solve_equation(equation_string, min, max):
    lhs, rhs = equation_string.split("=")

    lhs_expression = calculator_utils.AlgebraicInfixExpression(lhs)
    rhs_expression = calculator_utils.AlgebraicInfixExpression(rhs)

    equation_solver = ArbitraryEquation(lhs_expression, rhs_expression, "x")

    solutions = equation_solver.find_all_solutions(min, max, {})

    return solutions