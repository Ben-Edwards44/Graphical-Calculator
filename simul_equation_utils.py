class SystemEquations:
    def __init__(self, equation_variables, equation_constants):
        self.equation_variables = equation_variables
        self.equation_constants = equation_constants

    def build_constant_matrix(self):
        constant_matrix_items = [[constant] for constant in self.equation_constants]
        matrix_object = Matrix(constant_matrix_items)

        return matrix_object

    def build_coefficient_matrix(self):
        coefficient_matrix_items = []
        for variables in self.equation_variables:
            coefficient_matrix_items.append(variables)

        matrix_object = SquareMatrix(coefficient_matrix_items)

        return matrix_object
    
    def solve(self):
        coefficient_matrix = self.build_coefficient_matrix()
        constant_matrix = self.build_constant_matrix()

        inv_coefficient_matrix = coefficient_matrix.inverse()

        result_matrix = inv_coefficient_matrix.matrix_multiply(constant_matrix)
        result_values = [row[0] for row in result_matrix.items]

        return result_values
    

class Matrix:
    def __init__(self, items):
        self.items = items

        self.width = len(items[0])
        self.height = len(items)

    def matrix_multiply(self, other_matrix):
        #multiply two matrixes together        
        result_items = [[None for _ in range(other_matrix.width)] for _ in range(self.height)]  #create blank 2D array

        for row_inx in range(self.height):
            for col_inx in range(other_matrix.width):
                sum = 0
                for element_inx in range(self.width):
                    sum += self.items[row_inx][element_inx] * other_matrix.items[element_inx][col_inx]

                result_items[row_inx][col_inx] = sum

        result_matrix = Matrix(result_items)

        return result_matrix
    
    def scalar_multiply(self, scalar):
        #multiply a matrix by a scalar
        scaled_items = [[item * scalar for item in row] for row in self.items]
        scaled_matrix = Matrix(scaled_items)

        return scaled_matrix
    
    def transpose(self):
        new_items = []
        for col_index in range(self.width):
            column = [self.items[row_index][col_index] for row_index in range(self.height)]
            new_items.append(column)  #the columns of the old matrix become the rows of the new ones

        return Matrix(new_items)
    

class SquareMatrix(Matrix):
    def __init__(self, items):
        super().__init__(items)

    def scalar_multiply(self, scalar):
        #polymorphism - overrides the scalar_multiply() method from Matrix
        scaled_items = [[item * scalar for item in row] for row in self.items]
        scaled_matrix = SquareMatrix(scaled_items)

        return scaled_matrix
    
    def transpose(self):
        #polymorphism - overrides the transpose() method from Matrix
        new_items = []
        for col_index in range(self.width):
            column = [self.items[row_index][col_index] for row_index in range(self.height)]
            new_items.append(column)  #the columns of the old matrix become the rows of the new ones

        return SquareMatrix(new_items)

    def get_minor(self, remove_x, remove_y):
        minor_items = []
        for row_index, row in enumerate(self.items):
            if row_index == remove_x: continue

            minor_row = [item for col_index, item in enumerate(row) if col_index != remove_y]
            minor_items.append(minor_row)

        minor = SquareMatrix(minor_items)

        return minor

    def determinant(self):
        #return the determinant of the matrix
        if self.width == 2 and self.height == 2:
            #det = a*d - b*c
            return self.items[0][0] * self.items[1][1] - self.items[0][1] * self.items[1][0]
        
        det = 0
        for remove_y in range(self.width):
            #recursively get the determinants of each matrix minor from the top row
            minor = self.get_minor(0, remove_y)
            minor_det = minor.determinant()

            if remove_y % 2 == 0:
                multiplier = self.items[0][remove_y]
            else:
                multiplier = -self.items[0][remove_y]

            det += multiplier * minor_det

        return det
    
    def get_matrix_minors(self):
        minor_matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                minor = self.get_minor(x, y)
                minor_det = minor.determinant()

                minor_matrix[x][y] = minor_det

        return minor_matrix
    
    def get_cofactor_matrix(self, minor_matrix):
        cofactor_matrix_items = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            sign = 1 if x % 2 == 0 else -1

            for y in range(self.height):
                cofactor_matrix_items[x][y] = sign * minor_matrix[x][y]
                sign *= -1

        return SquareMatrix(cofactor_matrix_items)
    
    def inverse(self):
        if self.width == 2 and self.height == 2:
            new_items = [[self.items[1][1], -self.items[0][1]],
                         [-self.items[1][0], self.items[0][0]]]
            
            scalar = 1 / self.determinant()

            inverse_mat = SquareMatrix(new_items)
            scaled_inverse_mat = inverse_mat.scalar_multiply(scalar)

            return scaled_inverse_mat

        minor_matrix = self.get_matrix_minors()
        cofactor_matrix = self.get_cofactor_matrix(minor_matrix)
        
        adjoint_matrix = cofactor_matrix.transpose()

        scalar = 1 / self.determinant()

        inverse_mat = adjoint_matrix.scalar_multiply(scalar)

        return inverse_mat