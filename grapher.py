import gui
import math
import pygame
import random
import equation_utils
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
    RESOLUTION = 10  #how many x value samples taken per pixel

    def __init__(self, window, axis, colour):
        self.window = window
        self.axis = axis
        self.colour = colour

        self.equation_string = ""

        self.pixel_points_on_graph = None

    def set_equation_string(self, new_equation_string):
        self.equation_string = new_equation_string
        self.pixel_points_on_graph = None  #because we have updated the equation of the graph, we need to draw it again

    def check_valid_equation(self, equation_string):
        #check whether the graph's equation string is valid
        prev_equation_string = self.equation_string

        test_value_x = random.uniform(0, 100)

        try:
            self.set_equation_string(equation_string)

            test_y = self.get_y_values(test_value_x)
            valid = test_y is not None  #if a number is returned (not a None value), the equation must be valid
        except:
            #there was an error when evaluating the graph's equation, so it must be invalid
            valid = False

        self.set_equation_string(prev_equation_string)  #reset the graphs equation string

        return valid
    
    def get_points_on_graph(self):
        points_on_graph = set()  #a set is used to remove duplicates (no need to draw a pixel twice)
        for pixel_x in range(Axis.PIXEL_INDENT_X, gui.SCREEN_WIDTH):
            axis_x = self.axis.pixel_x_to_axis_x(pixel_x)

            for sample_num in range(Graph.RESOLUTION):
                fraction_into_pixel = sample_num / Graph.RESOLUTION

                x = axis_x + self.axis.pixel_width * fraction_into_pixel
                y_values = self.get_y_values(x)

                if y_values is None: continue  #this x value results in an error, like dividing by 0

                for y in y_values:
                    pixel_y = self.axis.axis_y_to_pixel_y(y)

                    coordinate = (pixel_x, pixel_y)
                    points_on_graph.add(coordinate)

        return points_on_graph

    def draw(self):
        if self.equation_string == "": return  #graph equation has not yet been set

        if self.pixel_points_on_graph is None:
            #we need to calcluate what points are on the graph because this has not yet been done
            self.pixel_points_on_graph = self.get_points_on_graph()

        for x, y in self.pixel_points_on_graph:
            #draw a rectangle one pixel wide at each coordinate on the graph
            pygame.draw.rect(self.window, self.colour, (x, y, 1, 1))


class ExplicitGraph(Graph):
    def __init__(self, window, axis, colour):
        super().__init__(window, axis, colour)

        self.function_expression = None

    def set_equation_string(self, new_equation_string):
        #overrides Graph.set_equation_string()
        super().set_equation_string(new_equation_string)

        function = self.extract_function()

        self.function_expression = calculator_utils.AlgebraicInfixExpression(function)

    def extract_function(self):
        #equation string will be in form y=f(x), we only want the f(x) part
        if self.equation_string == "": return ""  #equation of graph has not yet been set

        _, func = self.equation_string.split("=")

        return func
    
    def get_y_values(self, x_value):
        if self.function_expression is None: return None

        substitution = {"x" : x_value}

        try:
            y = self.function_expression.evaluate(substitution)
        except ZeroDivisionError:
            #for graphs like y=1/x, substituting x=0 gives a divide by zero error
            y = None

        if y is None: return None  #this can occur if the equation is y= (nothing given on right hand side)

        return [y]
    

class ImplicitGraph(Graph):
    def __init__(self, window, axis, colour):
        super().__init__(window, axis, colour)

        self.equation_solver = None

    def set_equation_string(self, new_equation_string):
        #overrides Graph.set_equation_string()
        super().set_equation_string(new_equation_string)

        if new_equation_string == "":
            #equation has not yet been set
            self.equation_solver = None
            return

        left_string, right_string = new_equation_string.split("=")

        lhs_expression = calculator_utils.AlgebraicInfixExpression(left_string)
        rhs_expression = calculator_utils.AlgebraicInfixExpression(right_string)

        self.equation_solver = equation_utils.ArbitraryEquation(lhs_expression, rhs_expression, "y")

    def get_y_values(self, x_value):
        known_substitutions = {"x" : x_value}

        try:
            y_values = self.equation_solver.find_all_solutions(self.axis.min_y, self.axis.max_y, known_substitutions)
        except Exception as e:
            #if an equation has not solutions, there may be a division by zero error when trying to solve it
            return None
        
        return y_values


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

        self.go_back = False

        self.axis = self.setup_axis()
        self.graph_inputs = self.setup_graph_inputs()
        self.graphs = self.setup_graphs()
        self.back_button = gui.create_back_button()

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
            graph = ImplicitGraph(self.window, self.axis, colour)
            graphs.append(graph)

        return graphs
        
    def update_graphs(self):
        for input_box, graph in zip(self.graph_inputs, self.graphs):
            inputted_equation = input_box.get_inputted_text()

            if inputted_equation != "" and inputted_equation != graph.equation_string and graph.check_valid_equation(inputted_equation):
                #the user has entered a different graph equation
                graph.set_equation_string(inputted_equation)

    def check_user_input(self):
        if self.back_button.is_clicked(): self.go_back = True

        for input_box in self.graph_inputs:
            input_box.check_user_input()

        self.update_graphs()
        
    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.axis.draw()

        for graph in self.graphs:
            graph.draw()

        for input_box in self.graph_inputs:
            input_box.draw(self.window)

        self.back_button.draw(self.window)

        pygame.display.update()


def get_graph_type(equation_string):
    #determine whether a graph is implicit or explicit
    lhs, rhs = equation_string.split("=")

    if lhs == "y" and "y" not in rhs:
        return ExplicitGraph
    elif rhs == "y" and "y" not in lhs:
        return ExplicitGraph
    else:
        return ImplicitGraph


def main(window):
    menu = GrapherMenu(window)

    while not menu.go_back:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()