import gui
import pygame
import calculator_utils


class Axis:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.width = max_x - min_x
        self.height = max_y - min_y

        self.tolerance = self.calculate_tolerance()

    def calculate_tolerance(self):
        pixel_width = self.width / gui.SCREEN_WIDTH
        pixel_height = self.height / gui.SCREEN_HEIGHT

        diagonal_len = (pixel_width**2 + pixel_height**2)**0.5

        #tolerance should be half the length of the diagonal because this is the furthest point from the center of the pixel to another point in the pixel (its corner)
        tolerance = diagonal_len / 2

        return tolerance

    def screen_to_axis_point(self, pixel_x, pixel_y):
        #convert a pixel coordinate point to a point on the axis
        corrected_pixel_y = gui.SCREEN_HEIGHT - pixel_y  #pygame uses the top of the screen as 0, but the axis uses the bottom of the screen as 0

        fraction_along = pixel_x / gui.SCREEN_WIDTH
        fraction_up = corrected_pixel_y / gui.SCREEN_HEIGHT

        x = self.min_x + self.width * fraction_along
        y = self.min_y + self.height * fraction_up

        return x, y


#NOTE: do dry run of graph drawing algorithms - points vs lines
class Graph:
    def __init__(self, window, axis, equation_string):
        self.window = window
        self.axis = axis
        self.equation_string = equation_string
        
        self.left_expression, self.right_expression = self.extract_expression_sides()

    def extract_expression_sides(self):
        #get the expressions to the left and right hand side of the equals sign
        left, right = self.equation_string.split("=")

        return left, right

    def replace_variables(self, x_value, y_value):
        left = ""
        for char in self.left_expression:
            if char == "x":
                left += f"({x_value})"
            elif char == "y":
                left += f"({y_value})"
            else:
                left += char

        right = ""
        for char in self.right_expression:
            if char == "x":
                right += f"({x_value})"
            elif char == "y":
                right += f"({y_value})"
            else:
                right += char

        return left, right

    def is_point_on_graph(self, x, y, tolerance):
        left, right = self.replace_variables(x, y)

        left_result = calculator_utils.evaluate_expression(left)
        right_result = calculator_utils.evaluate_expression(right)
        diff = abs(left_result - right_result)

        return diff < tolerance
    
    def draw(self):
        for pixel_x in range(gui.SCREEN_WIDTH):
            for pixel_y in range(gui.SCREEN_HEIGHT):
                axis_x, axis_y = self.axis.screen_to_axis_point(pixel_x, pixel_y)

                if self.is_point_on_graph(axis_x, axis_y, self.axis.tolerance):
                    pygame.draw.circle(self.window, (255, 0, 0), (pixel_x, pixel_y), 1)


def main(window):
    a = Axis(-10, 10, -10, 10)
    temp = Graph(window, a, "y=x^2")

    print(a.screen_to_axis_point(0, 0))
    print(a.screen_to_axis_point(gui.SCREEN_WIDTH, 0))
    print(a.screen_to_axis_point(0, gui.SCREEN_HEIGHT))
    print(a.screen_to_axis_point(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT))

    window.fill((0, 0, 0))
    temp.draw()
    pygame.display.update()

    while True:
        gui.check_user_quit()