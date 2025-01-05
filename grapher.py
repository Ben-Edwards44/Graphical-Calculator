import gui
import pygame
import calculator_utils


class Axis:
    MAIN_AXIS_COLOUR = (0, 255, 0)
    MAIN_AXIS_WIDTH = 4

    def __init__(self, window, min_x, max_x, min_y, max_y):
        self.window = window

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

    def axis_x_to_pixel_x(self, axis_x):
        #convert an x coordinate on the axis to a pixel x coordinate on the pygame window
        fraction_along = (axis_x - self.min_x) / self.width
        scaled_x = fraction_along * gui.SCREEN_WIDTH

        pixel_x = int(scaled_x)

        return pixel_x

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
    
    def draw_x_axis(self):
        #draw the x axis if it lies between self.min_x and self.max_x
        if 0 < self.min_x or 0 > self.max_x: return

        origin_x = self.axis_x_to_pixel_x(0)

        pygame.draw.line(self.window, Axis.MAIN_AXIS_COLOUR, (origin_x, 0), (origin_x, gui.SCREEN_HEIGHT), Axis.MAIN_AXIS_WIDTH)

    def draw_y_axis(self):
        #draw the y axis if it lies between self.min_y and self.max_y
        if 0 < self.min_y or 0 > self.max_y: return

        origin_y = self.axis_y_to_pixel_y(0)

        pygame.draw.line(self.window, Axis.MAIN_AXIS_COLOUR, (0, origin_y), (gui.SCREEN_WIDTH, origin_y), Axis.MAIN_AXIS_WIDTH)

    def draw(self):
        self.draw_x_axis()
        self.draw_y_axis()


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
    a = Axis(window, -10, 10, -10, 10)
    temp = ExplicitGraph(window, "y=sin(x^3)", a)

    window.fill((0, 0, 0))
    a.draw()
    temp.draw()
    pygame.display.update()

    while True:
        gui.check_user_quit()