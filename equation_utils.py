class ArbitraryEquation:
    SMALL_X_STEP = 0.01

    NUM_NEWTON_RAPHSON_STEPS = 6

    SOLUTION_SEARCH_RESOLUTION = 12

    TOLERANCE = 0.01

    def __init__(self, lhs_expression, rhs_expression, variable_to_solve_for):
        self.lhs = lhs_expression
        self.rhs = rhs_expression

        self.variable_name = variable_to_solve_for
    
    def evaluate_equals_zero(self, variable_value, known_variable_substitutions):
        #evaluate the equation as if it was in the form f(x)=0
        known_variable_substitutions[self.variable_name] = variable_value

        left = self.lhs.evaluate(known_variable_substitutions)
        right = self.rhs.evaluate(known_variable_substitutions)

        #the equation is in form lhs=rhs, but we want it to be f(x)=0. Subtracting rhs gives lhs-rhs=0, which is in the right form
        evaluation = left - right

        return evaluation

    def differentiate(self, variable_value, known_variable_substitutions):
        y1 = self.evaluate_equals_zero(variable_value, known_variable_substitutions)
        y2 = self.evaluate_equals_zero(variable_value + ArbitraryEquation.SMALL_X_STEP, known_variable_substitutions)

        gradient = (y2 - y1) / ArbitraryEquation.SMALL_X_STEP

        return gradient
    
    def solve(self, start_variable_value, known_variable_substitutions):
        variable = start_variable_value

        #apply the Newton-Raphson method to solve the equation
        for _ in range(ArbitraryEquation.NUM_NEWTON_RAPHSON_STEPS):
            variable = variable - self.evaluate_equals_zero(variable, known_variable_substitutions) / self.differentiate(variable, known_variable_substitutions)

        return variable
    
    def find_all_solutions(self, min, max, known_variable_substitutions):
        #find all the solutions to the equation in the range min <= solution <= max
        x_step = (max - min) / ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION

        solutions = []
        for step in range(ArbitraryEquation.SOLUTION_SEARCH_RESOLUTION):
            start_x = min + step * x_step
            solution = self.solve(start_x, known_variable_substitutions)
            is_actual_solution = abs(self.evaluate_equals_zero(solution, known_variable_substitutions)) < ArbitraryEquation.TOLERANCE  #the Newton-Raphson method does not always converge, so sometimes gives numbers that are not solutions

            if min <= solution <= max and is_new_element(solutions, solution, ArbitraryEquation.TOLERANCE) and is_actual_solution:
                solutions.append(solution)

        return solutions


def is_new_element(list, num, tolerance):
    #determine if the num is in the list, within a given tolerance (e.g. 5.001 should not be new to [3, 4, 5])
    for element in list:
        if abs(element - num) < tolerance:
            return False  #already in list

    return True