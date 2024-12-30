import matrix_utils


class SystemEquations:
    def __init__(self, equation_variables, equation_constants):
        self.equation_variables = equation_variables
        self.equation_constants = equation_constants

    def build_constant_matrix(self):
        constant_matrix_items = [[constant] for constant in self.equation_constants]
        matrix_object = matrix_utils.Matrix(constant_matrix_items)

        return matrix_object

    def build_coefficient_matrix(self):
        coefficient_matrix_items = []
        for variables in self.equation_variables:
            coefficient_matrix_items.append(variables)

        matrix_object = matrix_utils.SquareMatrix(coefficient_matrix_items)

        return matrix_object
    
    def solve(self):
        coefficient_matrix = self.build_coefficient_matrix()
        constant_matrix = self.build_constant_matrix()

        inv_coefficient_matrix = coefficient_matrix.inverse()

        result_matrix = inv_coefficient_matrix.matrix_multiply(constant_matrix)
        result_values = [row[0] for row in result_matrix.items]

        return result_values