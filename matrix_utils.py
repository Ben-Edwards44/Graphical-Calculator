class Matrix:
    def __init__(self, items):
        self.items = items

        self.width = len(items[0])
        self.height = len(items)

    def __mul__(self, other_matrix):
        #this overrides the * operator
        if self.width != other_matrix.height:
            #TODO: show error
            return
        
        result_items = [[None for _ in range(other_matrix.width)] for _ in range(self.height)]  #create blank 2D array

        for row_inx in range(self.height):
            for col_inx in range(other_matrix.width):
                sum = 0
                for element_inx in range(self.width):
                    sum += self.items[row_inx][element_inx] * other_matrix.items[element_inx][col_inx]

                result_items[row_inx][col_inx] = sum

        result_matrix = Matrix(result_items)

        return result_matrix
    

class SquareMatrix(Matrix):
    def __init__(self, items):
        super().__init__(items)

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
    

a = SquareMatrix([[5, 8, 9, 2],
                  [1, 5, 8, 6],
                  [2, 4, 3, 3],
                  [9, 0, 1, 2]])


print(a.determinant())