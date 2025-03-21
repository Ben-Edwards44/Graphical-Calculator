import gui
import math
import pygame
import random
import equation_utils
import calculator_utils


class Axis:
    PIXEL_INDENT_X = 200

    MAIN_AXIS_WIDTH = 3

    BACKGROUND_LINE_COLOUR = (150, 150, 150)
    BACKGROUND_LINE_WIDTH = 1

    DESIRED_NUM_BACKGROUND_LINES = 10

    ZOOM_FACTOR = 0.9

    MIN_X = -10
    MAX_X = 10
    MIN_Y = -10
    MAX_Y = 10

    def __init__(self, window):
        self.window = window

        self.min_x = Axis.MIN_X
        self.max_x = Axis.MAX_X
        self.min_y = Axis.MIN_Y
        self.max_y = Axis.MAX_Y

        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

        self.prev_mouse_pos = None

        self.view_changed = False

        self.pixel_width = self.calculate_pixel_width()

    get_view_changed = lambda self: self.view_changed

    def calculate_pixel_width(self):
        #calculate the amount of axis space taken up by one pixel
        #this is needed for sampling each pixel multiple times
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

        #pygame uses the top of the screen as 0, but the axis uses the 
        #bottom of the screen as 0, so we need to subtract scaled_y from the screen height
        pixel_y = gui.SCREEN_HEIGHT - int(scaled_y)

        return pixel_y
    
    def pixel_x_to_axis_x(self, pixel_x):
        #convert a pixel x coordinate to an x coordinate on the axis
        pixel_x -= Axis.PIXEL_INDENT_X
        
        fraction_along = pixel_x / (gui.SCREEN_WIDTH - Axis.PIXEL_INDENT_X)
        axis_x = self.min_x + fraction_along * self.width

        return axis_x
    
    def draw_y_axis(self):
        #draw the y axis if it lies between self.min_x and self.max_x
        if 0 < self.min_x or 0 > self.max_x: return

        origin_x = self.axis_x_to_pixel_x(0)

        pygame.draw.line(self.window, 
                         Axis.BACKGROUND_LINE_COLOUR, 
                         (origin_x, 0), 
                         (origin_x, gui.SCREEN_HEIGHT), 
                         Axis.MAIN_AXIS_WIDTH)

    def draw_x_axis(self):
        #draw the x axis if it lies between self.min_y and self.max_y
        if 0 < self.min_y or 0 > self.max_y: return

        origin_y = self.axis_y_to_pixel_y(0)

        pygame.draw.line(self.window, 
                         Axis.BACKGROUND_LINE_COLOUR, 
                         (Axis.PIXEL_INDENT_X, origin_y), 
                         (gui.SCREEN_WIDTH, origin_y), 
                         Axis.MAIN_AXIS_WIDTH)

    def calculate_line_spacing(self, min, max):
        #choose the spacing of the background lines such that the number is as close
        #to the desired number of lines and each line goes up in 0.1, 1, 10, 100...
        axis_space = abs(max - min)
        desired_axis_spacing = axis_space / Axis.DESIRED_NUM_BACKGROUND_LINES

        #choose the nearest power of 10 to the desired axis spacing 
        #(because we want to go in steps of 1, 10, 100, 1000...)
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
    
    def calculate_first_line_pos(self, axis_spacing, ideal_start):
        #calculate the position of the first background line to be drawn

        #this is the number of axis_spacing steps we need to take to 
        #get from the origin to the ideal_start point
        threshold_steps = abs(ideal_start) / axis_spacing
        steps = int(threshold_steps)

        start_point = steps * axis_spacing

        #we actually want to start in the other direction
        if ideal_start < 0: start_point *= -1

        return start_point

    def draw_vertical_background_lines(self):
        axis_spacing = self.calculate_line_spacing(self.min_x, self.max_x)

        #draw lines from left to right
        line_axis_x = self.calculate_first_line_pos(axis_spacing, self.min_x)
        while line_axis_x <= self.max_x:
            line_pixel_x = self.axis_x_to_pixel_x(line_axis_x)

            pygame.draw.line(self.window, 
                             Axis.BACKGROUND_LINE_COLOUR, 
                             (line_pixel_x, 0), 
                             (line_pixel_x, gui.SCREEN_HEIGHT), 
                             Axis.BACKGROUND_LINE_WIDTH)

            line_axis_x += axis_spacing

    def draw_horizontal_background_lines(self):
        axis_spacing = self.calculate_line_spacing(self.min_y, self.max_y)

        #draw lines from top to bottom
        line_axis_y = self.calculate_first_line_pos(axis_spacing, self.max_y)
        while line_axis_y >= self.min_y:
            line_pixel_y = self.axis_y_to_pixel_y(line_axis_y)
            
            pygame.draw.line(self.window, 
                             Axis.BACKGROUND_LINE_COLOUR, 
                             (Axis.PIXEL_INDENT_X, line_pixel_y), 
                             (gui.SCREEN_WIDTH, line_pixel_y), 
                             Axis.BACKGROUND_LINE_WIDTH)

            line_axis_y -= axis_spacing

    def translate(self, x_translation_pixels, y_translation_pixels):
        self.view_changed = True

        #when the user clicks and drags, we need to update the bounds of the axis
        x_translation = x_translation_pixels / (gui.SCREEN_WIDTH - Axis.PIXEL_INDENT_X) * self.width
        y_translation = y_translation_pixels / gui.SCREEN_HEIGHT * self.height

        #x translations are flipped
        self.min_x -= x_translation
        self.max_x -= x_translation

        self.min_y += y_translation
        self.max_y += y_translation

    def zoom(self, mouse_scroll_dir):
        self.view_changed = True

        if mouse_scroll_dir == 1:
            zoom_factor = Axis.ZOOM_FACTOR  #zoom in
        else:
            zoom_factor = 1 / Axis.ZOOM_FACTOR  #zoom out

        self.min_x *= zoom_factor
        self.max_x *= zoom_factor

        self.min_y *= zoom_factor
        self.max_y *= zoom_factor

        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

    def check_mouse_drag(self):
        #check if the user is dragging their mouse
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()

            if self.prev_mouse_pos is not None:
                #the user is dragging their mouse - translate the axis
                delta_x = mouse_pos[0] - self.prev_mouse_pos[0]
                delta_y = mouse_pos[1] - self.prev_mouse_pos[1]

                self.translate(delta_x, delta_y)

            self.prev_mouse_pos = mouse_pos
        else:
            #the user has stopped dragging, so set prev_mouse_pos 
            #to None to stop the axis being translated further
            self.prev_mouse_pos = None

    def check_mouse_scroll(self):
        #check if the user is scrolling
        scroll_events = pygame.event.get(pygame.MOUSEWHEEL)

        for event in scroll_events:
            self.zoom(event.y)

    def check_user_input(self):
        #self.view_changed will be overwritten if 
        #the user scrolls or drags their mouse
        self.view_changed = False

        self.check_mouse_drag()
        self.check_mouse_scroll()

    def draw(self):
        self.draw_horizontal_background_lines()
        self.draw_vertical_background_lines()

        self.draw_x_axis()
        self.draw_y_axis()


class Graph:
    RESOLUTION = 4  #how many x value samples taken per pixel

    LINE_WIDTH = 2

    def __init__(self, equation_string, window, axis, colour):
        self.window = window
        self.axis = axis
        self.colour = colour

        self.equation_string = equation_string

        self.pixel_points_on_graph = None

    def check_valid_equation(self):
        #check whether the graph's equation string is valid by testing a random x value
        test_value_x = random.uniform(0, 100)

        try:
            test_y = self.get_y_values(test_value_x)

            #if a number is returned (not a None value), the equation must be valid
            valid = test_y is not None
        except:
            #there was an error when evaluating the graph's equation, so it must be invalid
            valid = False

        return valid
    
    def get_points_on_graph(self):
        #a set is used to remove duplicates (no need to draw a pixel twice)
        points_on_graph = set()
        for pixel_x in range(Axis.PIXEL_INDENT_X, gui.SCREEN_WIDTH):
            axis_x = self.axis.pixel_x_to_axis_x(pixel_x)

            for sample_num in range(Graph.RESOLUTION):
                fraction_into_pixel = sample_num / Graph.RESOLUTION

                x = axis_x + self.axis.pixel_width * fraction_into_pixel
                y_values = self.get_y_values(x)

                #check if this x value results in an error, like dividing by 0
                if y_values is None: continue

                for y in y_values:
                    pixel_y = self.axis.axis_y_to_pixel_y(y)

                    coordinate = (pixel_x, pixel_y)
                    points_on_graph.add(coordinate)

        return points_on_graph

    def draw(self):
        if self.equation_string == "": return  #graph equation has not yet been set

        if self.pixel_points_on_graph is None or self.axis.get_view_changed():
            #we need to calcluate what points are on the graph 
            #because this has not yet been done, or the axis has changed
            self.pixel_points_on_graph = self.get_points_on_graph()

        for x, y in self.pixel_points_on_graph:
            #draw a rectangle one pixel wide at each coordinate on the graph
            pygame.draw.rect(self.window, 
                             self.colour, 
                             (x, y, Graph.LINE_WIDTH, Graph.LINE_WIDTH))


class ExplicitGraph(Graph):
    def __init__(self, equation_string, window, axis, colour):
        super().__init__(equation_string, window, axis, colour)

        self.function_expression = self.extract_function()

    def extract_function(self):
        #equation string will be in form y=f(x), we only want the f(x) part
        lhs, rhs = self.equation_string.split("=")

        if lhs == "y":
            func = rhs  #y=f(x)
        else:
            func = lhs  #f(x)=y

        func_expression = calculator_utils.AlgebraicInfixExpression(func)

        return func_expression
    
    def get_y_values(self, x_value):
        substitution = {"x" : x_value}

        try:
            y = self.function_expression.evaluate(substitution)
        except ZeroDivisionError:
            #for graphs like y=1/x, substituting x=0 gives a divide by zero error
            y = None

        #y can be None if the equation is y= (nothing given on right hand side)
        if y is None: return None

        return [y]
    

class ImplicitGraph(Graph):
    def __init__(self, equation_string, window, axis, colour):
        super().__init__(equation_string, window, axis, colour)

        self.equation_solver = self.get_equation_solver()

    def get_equation_solver(self):
        left_string, right_string = self.equation_string.split("=")

        lhs_expression = calculator_utils.AlgebraicInfixExpression(left_string)
        rhs_expression = calculator_utils.AlgebraicInfixExpression(right_string)

        #we need the equation to be solved quickly, 
        #not very accurately (so set fast_solve to True)
        equation_solver = equation_utils.ArbitraryEquation(lhs_expression, 
                                                           rhs_expression, 
                                                           "y", 
                                                           True)

        return equation_solver

    def get_y_values(self, x_value):
        known_substitutions = {"x" : x_value}

        try:
            y_values = self.equation_solver.find_all_solutions(self.axis.min_y, 
                                                               self.axis.max_y, 
                                                               known_substitutions)
        except:
            #if an equation has not solutions, there may be 
            #a division by zero error when trying to solve it
            return None
        
        return y_values


class GrapherMenu:
    GRAPH_COLOURS = (
        (0, 255, 0),
        (0, 0, 255),
        (255, 0, 0),
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

        #create all elements in the GUI
        self.axis = self.setup_axis()
        self.graph_inputs = self.setup_graph_inputs()
        self.graphs = self.setup_graphs()
        self.back_button = gui.create_back_button()

    get_go_back = lambda self: self.go_back

    def setup_graph_inputs(self):
        num_boxes = len(GrapherMenu.GRAPH_COLOURS)

        back_button_space = (gui.BACK_BUTTON_POS[1] * 2 
                             + gui.BACK_BUTTON_HEIGHT)
        
        box_height = (gui.SCREEN_HEIGHT - 
                      back_button_space - 
                      GrapherMenu.GRAPH_INPUT_PADDING_Y * 
                      (num_boxes + 1)) // num_boxes

        graph_inputs = []
        for i in range(num_boxes):
            top_left_y = (back_button_space + 
                          GrapherMenu.GRAPH_INPUT_PADDING_Y + 
                          i * (box_height + GrapherMenu.GRAPH_INPUT_PADDING_Y))
            
            top_left = (GrapherMenu.GRAPH_INPUT_PADDING_X, top_left_y)

            input_box = gui.TextInput(top_left, 
                                      GrapherMenu.GRAPH_INPUT_WIDTH, 
                                      box_height, 
                                      "...")

            graph_inputs.append(input_box)

        return graph_inputs
    
    def setup_axis(self):
        axis = Axis(self.window)

        return axis
    
    def setup_graphs(self):
        graphs = []
        for _ in GrapherMenu.GRAPH_COLOURS:
            graphs.append(None)

        return graphs
        
    def update_graphs(self):
        for inx, input_box in enumerate(self.graph_inputs):
            inputted_equation = input_box.get_inputted_text()
            
            #check if the graph's equation has not yet been set
            if inputted_equation == "": continue

            prev_graph = self.graphs[inx]

            if prev_graph is None or inputted_equation != prev_graph.equation_string:
                #the graph's equation has changed, so
                #replace the graph object with a new one
                new_graph = create_new_graph(inputted_equation, 
                                             self.window, 
                                             self.axis, 
                                             GrapherMenu.GRAPH_COLOURS[inx])

                self.graphs[inx] = new_graph

    def check_user_input(self):
        if self.back_button.is_clicked(): self.go_back = True

        self.axis.check_user_input()

        for input_box in self.graph_inputs:
            input_box.check_user_input()

        self.update_graphs()

        gui.check_user_quit()
        
    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.axis.draw()

        for graph in self.graphs:
            #a graph will be None if it has not yet 
            #been set, or has an invalid equation
            if graph is not None:
                graph.draw()

        for input_box in self.graph_inputs:
            input_box.draw(self.window)

        self.back_button.draw(self.window)

        pygame.display.update()


def is_explicit_function(equation_string):
    if "=" not in equation_string: return False

    lhs, rhs = equation_string.split("=")

    if lhs == "y":
        return "y" not in rhs
    elif rhs == "y":
        return "y" not in lhs
    else:
        return False


def create_new_graph(equation_string, window, axis, colour):
    #return a graph object with the equation string as its 
    #equation. If the equation string is invalid, return None
    if "=" not in equation_string: return None

    #try the explicit graph fist because this is more performant
    if is_explicit_function(equation_string):
        explicit = ExplicitGraph(equation_string, window, axis, colour)

        if explicit.check_valid_equation():
            return explicit
    
    #the explicit did not work, so the equation may be implicit
    implicit = ImplicitGraph(equation_string, window, axis, colour)
    if implicit.check_valid_equation():
        return implicit
    
    #None of the graphs worked, so this equation must be invalid
    return None


def main(window):
    menu = GrapherMenu(window)

    while not menu.get_go_back():
        menu.check_user_input()
        menu.draw()
