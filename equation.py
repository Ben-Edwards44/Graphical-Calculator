import gui
import pygame
import equation_utils


class EquationMenu:
    EQUATION_FONT_SIZE = 28

    CHAR_BUTTONS = ["π", "e", "sqrt", "solve"]

    CHAR_BUTTON_WIDTH = 90
    CHAR_BUTTON_HEIGHT = 50

    CHAR_BUTTON_TOP_LEFT = (100, gui.SCREEN_HEIGHT - 80)  #top left pos of the row of buttons

    BACKGROUND_BOX_TOP_LEFT = (100, 100)
    BACKGROUND_BOX_BORDER_WIDTH = 6
    BACKGROUND_BOX_CORNER_RADIUS = 12

    NUM_EQUATION_BOXES = 4

    EQUATION_BOX_PADDING_X = 8
    EQUATION_BOX_PADDING_Y = 10

    def __init__(self, window):
        self.window = window

        self.go_back = False

        self.equation_boxes = []

        #create all elements in the GUI
        self.heading_text = self.setup_heading_text()
        self.equation_input_box = self.setup_equation_input()
        self.back_button = gui.create_back_button()
        self.char_buttons = self.setup_char_buttons()
        self.background_rect = self.setup_background_rect()

    def setup_heading_text(self):
        heading_text = gui.DisplayText("Equation", gui.HEADING_CENTER_POS)
        heading_text.set_font_size(gui.HEADING_FONT_SIZE)

        return heading_text
    
    def setup_equation_input(self):
        width, height, top_left_x = self.get_equation_box_dimensions()

        #position the input box at the bottom of the screen
        top_left_y = EquationMenu.BACKGROUND_BOX_TOP_LEFT[1] + EquationMenu.NUM_EQUATION_BOXES * (height + EquationMenu.EQUATION_BOX_PADDING_Y) + EquationMenu.EQUATION_BOX_PADDING_Y

        equation_input_box = gui.TextInput((top_left_x, top_left_y), width, height, "Enter equation:")
        equation_input_box.set_font_size(EquationMenu.EQUATION_FONT_SIZE)

        return equation_input_box
    
    def setup_char_buttons(self):
        total_row_width = gui.SCREEN_WIDTH - 2 * EquationMenu.CHAR_BUTTON_TOP_LEFT[0]
        total_button_width = EquationMenu.CHAR_BUTTON_WIDTH * len(EquationMenu.CHAR_BUTTONS)

        num_gaps = len(EquationMenu.CHAR_BUTTONS) - 1
        padding_x = (total_row_width - total_button_width) // num_gaps

        char_buttons = []
        for index, char in enumerate(EquationMenu.CHAR_BUTTONS):
            top_left_x = EquationMenu.CHAR_BUTTON_TOP_LEFT[0] + index * (EquationMenu.CHAR_BUTTON_WIDTH + padding_x)
            button = gui.ColourChangeButton((top_left_x, EquationMenu.CHAR_BUTTON_TOP_LEFT[1]), EquationMenu.CHAR_BUTTON_WIDTH, EquationMenu.CHAR_BUTTON_HEIGHT, char)

            char_buttons.append(button)

        return char_buttons
    
    def setup_background_rect(self):
        width = gui.SCREEN_WIDTH - 2 * EquationMenu.BACKGROUND_BOX_TOP_LEFT[0]
        height = gui.SCREEN_HEIGHT - 2 * EquationMenu.BACKGROUND_BOX_TOP_LEFT[1]

        #although the background rect is not a button, it will be draw exactly the same as one so it is stored as a button object
        background_rect = gui.BasicButton(EquationMenu.BACKGROUND_BOX_TOP_LEFT, width, height)

        background_rect.set_border_width(EquationMenu.BACKGROUND_BOX_BORDER_WIDTH)
        background_rect.set_corner_radius(EquationMenu.BACKGROUND_BOX_CORNER_RADIUS)

        return background_rect
    
    def get_equation_box_dimensions(self):
        #get the width, height and x coordinate of the top left pos of the equation boxes
        top_left_x = EquationMenu.BACKGROUND_BOX_TOP_LEFT[0] + EquationMenu.EQUATION_BOX_PADDING_X
        width = gui.SCREEN_WIDTH - 2 * top_left_x

        available_height = gui.SCREEN_HEIGHT - 2 * EquationMenu.BACKGROUND_BOX_TOP_LEFT[1] - EquationMenu.EQUATION_BOX_PADDING_Y
        total_height = available_height // (EquationMenu.NUM_EQUATION_BOXES + 1)  #we need to +1 to the number of equation boxes because the input box at the bottom also takes up space
        box_height = total_height - EquationMenu.EQUATION_BOX_PADDING_Y

        return width, box_height, top_left_x
    
    def get_char_button_text(self, char_button):
        #get the text to add to the input box when a char button is pressed
        match char_button:
            case "sqrt":
                return "sqrt("
            case _:
                return char_button

    def check_user_input(self):
        self.equation_input_box.check_user_input()  #check if user is entering equation
        if self.back_button.is_clicked(): self.go_back = True  #check if user has pressed back
    
        #check if user has pressed any of the char buttons
        for index, button in enumerate(self.char_buttons):
            already_been_clicked = button.get_has_been_clicked()
            clicked = button.is_clicked()
            
            if clicked and not already_been_clicked:
                char = EquationMenu.CHAR_BUTTONS[index]

                if char == "solve":
                    new_expression_box = EquationBox(self.window, self.equation_input_box.get_inputted_text())
                    self.equation_boxes.append(new_expression_box)
                else:
                    text_to_add = self.get_char_button_text(char)
                    self.equation_input_box.input_text(text_to_add)

        gui.check_user_quit()

    def draw_equation_boxes(self):
        width, height, top_left_x = self.get_equation_box_dimensions()

        most_recent_boxes = self.equation_boxes[-EquationMenu.NUM_EQUATION_BOXES:]  #only draw the most recent equation boxes

        for index, box in enumerate(most_recent_boxes):
            top_left_y = EquationMenu.BACKGROUND_BOX_TOP_LEFT[1] + EquationMenu.EQUATION_BOX_PADDING_Y + index * (height + EquationMenu.EQUATION_BOX_PADDING_Y)
            box.draw((top_left_x, top_left_y), width, height)

    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.background_rect.draw(self.window)
        self.heading_text.draw(self.window)
        self.equation_input_box.draw(self.window)
        self.back_button.draw(self.window)

        for button in self.char_buttons:
            button.draw(self.window)

        self.draw_equation_boxes()

        pygame.display.update()


class EquationBox:
    DECIMAL_PLACES = 4

    SOLUTION_MIN_X = -100
    SOLUTION_MAX_X = 100

    def __init__(self, window, equation_string):
        self.window = window
        self.equation_string = equation_string

        self.solution_string = self.get_solution_string()

    def solution_to_string(self, solution):
        correct_dp = round(solution, EquationBox.DECIMAL_PLACES)
        string = str(correct_dp)

        return string

    def get_solution_string(self):
        solutions = self.solve_equation()

        if len(solutions) == 0:
            return f"none for {EquationBox.SOLUTION_MIN_X}<x<{EquationBox.SOLUTION_MAX_X}"
        
        solutions_strings = [self.solution_to_string(solution) for solution in solutions]
        solution_text = f"x={','.join(solutions_strings)}"

        return solution_text

    def solve_equation(self):
        try:
            solutions = equation_utils.solve_equation(self.equation_string, EquationBox.SOLUTION_MIN_X, EquationBox.SOLUTION_MAX_X)
        except:
            #the user has entered an invalid equation: no solutions will be displayed
            solutions = []

        return solutions
    
    def draw(self, top_left_pos, width, height):
        background_rect = gui.BasicButton(top_left_pos, width, height)

        equation_text = gui.DisplayText(self.equation_string, top_left_pos)
        solution_text = gui.DisplayText(self.solution_string, top_left_pos)

        equation_text.set_top_left_pos(top_left_pos)  #put the equation on the left of the box
        solution_text.set_top_right_pos((top_left_pos[0] + width, top_left_pos[1]))  #put the answer on the right of the box

        background_rect.draw(self.window)
        equation_text.draw(self.window)
        solution_text.draw(self.window)


def main(window):
    menu = EquationMenu(window)

    while not menu.go_back:
        menu.check_user_input()
        menu.draw()