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

        self.pixel_width = self.calculate_pixel_width()

    def calculate_pixel_width(self):
        #calculate the amount of axis space taken up by one pixel - needed for sampling each pixel multiple times
        pixel_width = self.width / gui.SCREEN_WIDTH

        return pixel_width

    def axis_y_to_pixel_y(self, axis_y):
        #convert a y coordinate on the axis to a pixel y coordinate on the pygame window
        fraction_up = (axis_y - self.min_y) / self.height
        scaled_y = gui.SCREEN_HEIGHT * fraction_up

        #pygame uses the top of the screen as 0, but the axis uses the bottom of the screen as 0 so we need to subtract scaled_y from the screen height
        pixel_y = gui.SCREEN_HEIGHT - int(scaled_y)

        return pixel_y
    
    def pixel_x_to_axis_x(self, pixel_x):
        #convert a pixel x coordinate to an x coordinate on the axis - fraction_into_pixel specifes how far from the left of the pixel the coordinate should be
        fraction_along = pixel_x / gui.SCREEN_WIDTH
        axis_x = self.min_x + fraction_along * self.width

        return axis_x


#NOTE: do dry run of graph drawing algorithms - points vs lines
class Graph:
    RESOLUTION = 5  #how many x value samples are taken per pixel

    def __init__(self, window, equation_string, axis):
        self.window = window
        self.equation_string = equation_string
        self.axis = axis

    def draw(self):
        for pixel_x in range(gui.SCREEN_WIDTH):
            axis_x = self.axis.pixel_x_to_axis_x(pixel_x)

            for sample_num in range(Graph.RESOLUTION):
                fraction_into_pixel = sample_num / Graph.RESOLUTION

                x = axis_x + self.axis.pixel_width * fraction_into_pixel
                y = self.get_y_value(x)

                pixel_y = self.axis.axis_y_to_pixel_y(y)

                pygame.draw.circle(self.window, (255, 0, 0), (pixel_x, pixel_y), 1)


class ExplicitGraph(Graph):
    def __init__(self, window, equation_string, axis):
        super().__init__(window, equation_string, axis)

        self.function = self.extract_function()

    def extract_function(self):
        #equation string will be in form y=f(x), we only want the f(x) part
        _, func = self.equation_string.split("=")

        return func
    
    def substitute_variables(self, x_value):
        substituted_expression = ""
        for char in self.function:
            if char == "x":
                substituted_expression += f"({x_value})"
            else:
                substituted_expression += char

        return substituted_expression
    
    def get_y_value(self, x_value):
        substituted_expression = self.substitute_variables(x_value)
        y = calculator_utils.evaluate_expression(substituted_expression)

        return y


def main(window):
    a = Axis(-10, 10, -10, 10)
    temp = ExplicitGraph(window, "y=sin(x^3)", a)

    window.fill((0, 0, 0))
    temp.draw()
    pygame.display.update()

    while True:
        gui.check_user_quit()