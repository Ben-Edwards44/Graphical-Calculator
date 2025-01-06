import gui
import math
import pygame
import calculator_utils


class Axis:
    PIXEL_INDENT_X = 200

    MAIN_AXIS_COLOUR = (100, 100, 100)
    MAIN_AXIS_WIDTH = 2

    BACKGROUND_LINE_COLOUR = (150, 150, 150)
    BACKGROUND_LINE_WIDTH = 1

    DESIRED_NUM_BACKGROUND_LINES = 10

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
        pixel_width = self.width / (gui.SCREEN_WIDTH - Axis.PIXEL_INDENT_X)

        return pixel_width

    def axis_x_to_pixel_x(self, axis_x):
        #convert an x coordinate on the axis to a pixel x coordinate on the pygame window
        fraction_along = (axis_x - self.min_x) / self.width
        scaled_x = fraction_along * (gui.SCREEN_WIDTH - Axis.PIXEL_INDENT_X)

        pixel_x = int(scaled_x) + Axis.PIXEL_INDENT_X

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
        pixel_x -= Axis.PIXEL_INDENT_X
        
        fraction_along = pixel_x / (gui.SCREEN_WIDTH - Axis.PIXEL_INDENT_X)
        axis_x = self.min_x + fraction_along * self.width

        return axis_x
    
    def draw_y_axis(self):
        #draw the y axis if it lies between self.min_x and self.max_x
        if 0 < self.min_x or 0 > self.max_x: return

        origin_x = self.axis_x_to_pixel_x(0)

        pygame.draw.line(self.window, Axis.MAIN_AXIS_COLOUR, (origin_x, 0), (origin_x, gui.SCREEN_HEIGHT), Axis.MAIN_AXIS_WIDTH)

    def draw_x_axis(self):
        #draw the x axis if it lies between self.min_y and self.max_y
        if 0 < self.min_y or 0 > self.max_y: return

        origin_y = self.axis_y_to_pixel_y(0)

        pygame.draw.line(self.window, Axis.MAIN_AXIS_COLOUR, (Axis.PIXEL_INDENT_X, origin_y), (gui.SCREEN_WIDTH, origin_y), Axis.MAIN_AXIS_WIDTH)

    def calculate_line_spacing(self, min, max):
        #choose the spacing of the background lines such that the number is as close to the desired number of lines and each line goes up in 0.1, 1, 10, 100...
        axis_space = max - min
        desired_axis_spacing = axis_space / Axis.DESIRED_NUM_BACKGROUND_LINES

        #choose the nearest power of 10 to the desired axis spacing (because we want to go in steps of 1, 10, 100, 1000...)
        current_power = math.log(desired_axis_spacing, 10)
        lower = 10**int(current_power)
        upper = 10**(int(current_power) + 1)

        diff_lower = desired_axis_spacing - lower
        diff_upper = upper - desired_axis_spacing

        if diff_lower < diff_upper:
            axis_spacing = lower
        else:
            axis_spacing = upper
        
        return axis_spacing
    
    def calculate_start_point(self, axis_spacing, ideal_start):
        #calculate the position of the first background line to be drawn
        threshold_steps = abs(ideal_start) / axis_spacing  #this is the number of axis_spacing steps we need to take to get from the origin to the ideal_start point
        steps = int(threshold_steps)

        start_point = steps * axis_spacing

        if ideal_start < 0: start_point *= -1  #we actually want to start in the other direction

        return start_point

    def draw_vertical_background_lines(self):
        axis_spacing = self.calculate_line_spacing(self.min_x, self.max_x)

        #draw lines from left to right
        line_axis_x = self.calculate_start_point(axis_spacing, self.min_x)
        while line_axis_x <= self.max_x:
            line_pixel_x = self.axis_x_to_pixel_x(line_axis_x)
            pygame.draw.line(self.window, Axis.BACKGROUND_LINE_COLOUR, (line_pixel_x, 0), (line_pixel_x, gui.SCREEN_HEIGHT), Axis.BACKGROUND_LINE_WIDTH)

            line_axis_x += axis_spacing

    def draw_horizontal_background_lines(self):
        axis_spacing = self.calculate_line_spacing(self.min_y, self.max_y)

        #draw lines from top to bottom
        line_axis_y = self.calculate_start_point(axis_spacing, self.max_y)
        while line_axis_y >= self.min_y:
            line_pixel_y = self.axis_y_to_pixel_y(line_axis_y)
            pygame.draw.line(self.window, Axis.BACKGROUND_LINE_COLOUR, (Axis.PIXEL_INDENT_X, line_pixel_y), (gui.SCREEN_WIDTH, line_pixel_y), Axis.BACKGROUND_LINE_WIDTH)

            line_axis_y -= axis_spacing

    def draw(self):
        self.draw_horizontal_background_lines()
        self.draw_vertical_background_lines()

        self.draw_x_axis()
        self.draw_y_axis()


#NOTE: do dry run of graph drawing algorithms - points vs lines (good continuity vs not right for discontinuous curves)
class Graph:
    RESOLUTION = 5  #how many x value samples taken per pixel

    def __init__(self, window, equation_string, axis, colour):
        self.window = window
        self.equation_string = equation_string
        self.axis = axis
        self.colour = colour

    def set_equation_string(self, new_equation_string):
        self.been_drawn = False  #because we have updated the equation of the graph, we need to draw it again
        self.equation_string = new_equation_string

    def check_valid_equation(self, equation_string):
        #check whether the graph's equation string is valid
        prev_equation_string = self.equation_string

        try:
            self.set_equation_string(equation_string)
            test_y = self.get_y_value(0)

            valid = test_y is not None  #if a number is returned (not a None value), the equation must be valid
        except:
            #there was an error when evaluating the graph's equation, so it must be invalid
            valid = False

        self.set_equation_string(prev_equation_string)  #reset the graphs equation string

        return valid

    def substitute_variables(self, x_value):
        substituted_expression = ""
        for char in self.function:
            if char == "x":
                substituted_expression += f"({x_value})"
            else:
                substituted_expression += char

        return substituted_expression

    def draw(self):
        for pixel_x in range(Axis.PIXEL_INDENT_X, gui.SCREEN_WIDTH):
            axis_x = self.axis.pixel_x_to_axis_x(pixel_x)

            for sample_num in range(Graph.RESOLUTION):
                fraction_into_pixel = sample_num / Graph.RESOLUTION

                x = axis_x + self.axis.pixel_width * fraction_into_pixel
                y = self.get_y_value(x)

                pixel_y = self.axis.axis_y_to_pixel_y(y)

                pygame.draw.circle(self.window, self.colour, (pixel_x, pixel_y), 1)


class ExplicitGraph(Graph):
    def __init__(self, window, equation_string, axis, colour):
        super().__init__(window, equation_string, axis, colour)

        self.function = self.extract_function()

    def set_equation_string(self, new_equation_string):
        #overrides Graph.set_equation_string()
        super().set_equation_string(new_equation_string)

        self.function = self.extract_function()

    def extract_function(self):
        #equation string will be in form y=f(x), we only want the f(x) part
        _, func = self.equation_string.split("=")

        return func
    
    def get_y_value(self, x_value):
        substituted_expression = self.substitute_variables(x_value)
        y = calculator_utils.evaluate_expression(substituted_expression)

        return y


class GrapherMenu:
    GRAPH_COLOURS = (
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (252, 219, 5),
        (252, 5, 236),
        (252, 120, 5)
    )

    GRAPH_INPUT_PADDING_X = 10
    GRAPH_INPUT_PADDING_Y = 10

    GRAPH_INPUT_WIDTH = Axis.PIXEL_INDENT_X - 2 * GRAPH_INPUT_PADDING_X

    def __init__(self, window):
        self.window = window

        self.needs_redraw = True

        self.axis = self.setup_axis()
        self.graph_inputs = self.setup_graph_inputs()
        self.graphs = self.setup_graphs()

        self.redraw_entire_screen()  #we need to draw everything from scratch when the menu is first created

    def setup_graph_inputs(self):
        num_boxes = len(GrapherMenu.GRAPH_COLOURS)

        box_height = (gui.SCREEN_HEIGHT - GrapherMenu.GRAPH_INPUT_PADDING_Y * (num_boxes + 1)) // num_boxes

        graph_inputs = []
        for i in range(num_boxes):
            top_left_y = GrapherMenu.GRAPH_INPUT_PADDING_Y + i * (box_height + GrapherMenu.GRAPH_INPUT_PADDING_Y)
            top_left = (GrapherMenu.GRAPH_INPUT_PADDING_X, top_left_y)

            input_box = gui.TextInput(top_left, GrapherMenu.GRAPH_INPUT_WIDTH, box_height, "...")

            graph_inputs.append(input_box)

        return graph_inputs
    
    def setup_axis(self):
        axis = Axis(self.window, -10, 10, -10, 10)

        return axis
    
    def setup_graphs(self):
        graphs = []
        for colour in GrapherMenu.GRAPH_COLOURS:
            graph = ExplicitGraph(self.window, "y=x", self.axis, colour)
            graphs.append(graph)

        return graphs
        
    def update_graphs(self):
        self.needs_redraw = False

        for input_box, graph in zip(self.graph_inputs, self.graphs):
            inputted_equation = input_box.get_inputted_text()

            if inputted_equation != "" and inputted_equation != graph.equation_string and graph.check_valid_equation(inputted_equation):
                #the user has entered a different graph equation
                graph.set_equation_string(inputted_equation)
                self.needs_redraw = True  #because a graph has been changed, we must redraw the entire screen (including all graphs)

    def check_user_input(self):
        for input_box in self.graph_inputs:
            input_box.check_user_input()

        self.update_graphs()

    def partial_clear_screen(self):
        #we want to clear the section of the screen containing the inputs, but not the graphs because these are only drawn once
        rect = (0, 0, Axis.PIXEL_INDENT_X, gui.SCREEN_HEIGHT)
        pygame.draw.rect(self.window, gui.BACKGROUND_COLOUR, rect)

    def redraw_entire_screen(self):
        #should be called when the equation of a graph has changed
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.axis.draw()

        for graph in self.graphs:
            graph.draw()

    def draw(self):
        if self.needs_redraw:
            self.redraw_entire_screen()
        else:
            self.partial_clear_screen()

        for input_box in self.graph_inputs:
            input_box.draw(self.window)

        pygame.display.update()

def main(window):
    menu = GrapherMenu(window)

    while True:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()