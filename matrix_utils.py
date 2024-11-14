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
    pass