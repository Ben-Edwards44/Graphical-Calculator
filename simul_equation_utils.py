import matrix_utils


class LinearEquation:
    def __init__(self, unknown_coefficients, constant):
        self.unknown_coefficients = unknown_coefficients
        self.constant = constant


class SystemEquations:
    def __init__(self, equations):
        self.equations = equations

    def build_constant_matrix(self):
        constant_matrix_items = [[equation.constant] for equation in self.equations]
        matrix_object = matrix_utils.Matrix(constant_matrix_items)

        return matrix_object

    def build_coefficient_matrix(self):
        coefficient_matrix_items = []
        for equation in self.equations:
            coefficient_row = equation.unknown_coefficients

            coefficient_matrix_items.append(coefficient_row)

        matrix_object = matrix_utils.SquareMatrix(coefficient_matrix_items)

        return matrix_object
    
    def solve(self):
        coefficient_matrix = self.build_coefficient_matrix()
        constant_matrix = self.build_constant_matrix()

        inv_coefficient_matrix = coefficient_matrix.inverse()

        result_matrix = inv_coefficient_matrix.matrix_multiply(constant_matrix)
        result_values = [row[0] for row in result_matrix.items]

        return result_values