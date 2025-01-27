import gui
import pygame
import calculator_utils


class CalculatorMenu:
    EXPRESSION_FONT_SIZE = 28

    CHAR_BUTTONS = ["π", "e", "ANS", "sqrt", "="]

    CHAR_BUTTON_WIDTH = 90
    CHAR_BUTTON_HEIGHT = 50

    CHAR_BUTTON_TOP_LEFT = (100, gui.SCREEN_HEIGHT - 80)  #top left pos of the row of buttons

    BACKGROUND_BOX_TOP_LEFT = (100, 100)
    BACKGROUND_BOX_BORDER_WIDTH = 6
    BACKGROUND_BOX_CORNER_RADIUS = 12

    NUM_EXPRESSION_BOXES = 4

    EXPRESSION_BOX_PADDING_X = 8
    EXPRESSION_BOX_PADDING_Y = 10

    def __init__(self, window):
        self.window = window

        self.go_back = False

        self.expression_boxes = []

        #create all elements in the GUI
        self.heading_text = self.setup_heading_text()
        self.expression_input_box = self.setup_expression_input()
        self.back_button = gui.create_back_button()
        self.char_buttons = self.setup_char_buttons()
        self.background_rect = self.setup_background_rect()

    def setup_heading_text(self):
        heading_text = gui.DisplayText("Calculator", gui.HEADING_CENTER_POS)
        heading_text.set_font_size(gui.HEADING_FONT_SIZE)

        return heading_text
    
    def setup_expression_input(self):
        width, height, top_left_x = self.get_expression_box_dimensions()

        #position the input box at the bottom of the screen
        top_left_y = CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[1] + CalculatorMenu.NUM_EXPRESSION_BOXES * (height + CalculatorMenu.EXPRESSION_BOX_PADDING_Y) + CalculatorMenu.EXPRESSION_BOX_PADDING_Y

        expression_input_box = gui.TextInput((top_left_x, top_left_y), width, height, "Enter expression:")
        expression_input_box.set_font_size(CalculatorMenu.EXPRESSION_FONT_SIZE)

        return expression_input_box
    
    def setup_char_buttons(self):
        total_row_width = gui.SCREEN_WIDTH - 2 * CalculatorMenu.CHAR_BUTTON_TOP_LEFT[0]
        total_button_width = CalculatorMenu.CHAR_BUTTON_WIDTH * len(CalculatorMenu.CHAR_BUTTONS)

        num_gaps = len(CalculatorMenu.CHAR_BUTTONS) - 1
        padding_x = (total_row_width - total_button_width) // num_gaps

        char_buttons = []
        for index, char in enumerate(CalculatorMenu.CHAR_BUTTONS):
            top_left_x = CalculatorMenu.CHAR_BUTTON_TOP_LEFT[0] + index * (CalculatorMenu.CHAR_BUTTON_WIDTH + padding_x)
            button = gui.ColourChangeButton((top_left_x, CalculatorMenu.CHAR_BUTTON_TOP_LEFT[1]), CalculatorMenu.CHAR_BUTTON_WIDTH, CalculatorMenu.CHAR_BUTTON_HEIGHT, char)

            char_buttons.append(button)

        return char_buttons
    
    def setup_background_rect(self):
        width = gui.SCREEN_WIDTH - 2 * CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[0]
        height = gui.SCREEN_HEIGHT - 2 * CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[1]

        #although the background rect is not a button, it will be draw exactly the same as one so it is stored as a button object
        background_rect = gui.BasicButton(CalculatorMenu.BACKGROUND_BOX_TOP_LEFT, width, height)

        background_rect.set_border_width(CalculatorMenu.BACKGROUND_BOX_BORDER_WIDTH)
        background_rect.set_corner_radius(CalculatorMenu.BACKGROUND_BOX_CORNER_RADIUS)

        return background_rect
    
    def get_expression_box_dimensions(self):
        #get the width, height and x coordinate of the top left pos of the expression boxes
        top_left_x = CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[0] + CalculatorMenu.EXPRESSION_BOX_PADDING_X
        width = gui.SCREEN_WIDTH - 2 * top_left_x

        available_height = gui.SCREEN_HEIGHT - 2 * CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[1] - CalculatorMenu.EXPRESSION_BOX_PADDING_Y
        total_height = available_height // (CalculatorMenu.NUM_EXPRESSION_BOXES + 1)  #we need to +1 to the number of expression boxes because the input box at the bottom also takes up space
        box_height = total_height - CalculatorMenu.EXPRESSION_BOX_PADDING_Y

        return width, box_height, top_left_x
    
    def get_char_button_text(self, char_button):
        #get the text to add to the input box when a char button is pressed
        match char_button:
            case "ANS":
                if len(self.expression_boxes) > 0:
                    last_expression = self.expression_boxes[-1]
                    prev_ans = last_expression.answer_string
                else:
                    prev_ans = "0"

                return prev_ans
            case "sqrt":
                return "sqrt("
            case _:
                return char_button
    
    def check_user_input(self):
        self.expression_input_box.check_user_input()  #check if user is entering expression
        if self.back_button.is_clicked(): self.go_back = True  #check if user has pressed back
    
        #check if user has pressed any of the char buttons
        for index, button in enumerate(self.char_buttons):
            already_been_clicked = button.get_has_been_clicked()
            clicked = button.is_clicked()
            
            if clicked and not already_been_clicked:
                char = CalculatorMenu.CHAR_BUTTONS[index]

                if char == "=":
                    new_expression_box = ExpressionBox(self.window, self.expression_input_box.get_inputted_text())
                    self.expression_boxes.append(new_expression_box)
                else:
                    text_to_add = self.get_char_button_text(char)
                    self.expression_input_box.input_text(text_to_add)

    def draw_expression_boxes(self):
        width, height, top_left_x = self.get_expression_box_dimensions()

        most_recent_boxes = self.expression_boxes[-CalculatorMenu.NUM_EXPRESSION_BOXES:]  #only draw the most recent expression boxes

        for index, box in enumerate(most_recent_boxes):
            top_left_y = CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[1] + CalculatorMenu.EXPRESSION_BOX_PADDING_Y + index * (height + CalculatorMenu.EXPRESSION_BOX_PADDING_Y)
            box.draw((top_left_x, top_left_y), width, height)

    def draw(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.background_rect.draw(self.window)
        self.heading_text.draw(self.window)
        self.expression_input_box.draw(self.window)
        self.back_button.draw(self.window)

        for button in self.char_buttons:
            button.draw(self.window)

        self.draw_expression_boxes()

        pygame.display.update()


class ExpressionBox:
    DECIMAL_PLACES = 5

    def __init__(self, window, expression_string):
        self.window = window
        self.expression_string = expression_string

        self.answer_string = self.evaluate_expression()

    def answer_to_string(self, answer):
        correct_dp = round(answer, ExpressionBox.DECIMAL_PLACES)
        string = str(correct_dp)

        return string

    def evaluate_expression(self):
        try:
            answer = calculator_utils.evaluate_expression(self.expression_string)
            answer_string = self.answer_to_string(answer)
        except:
            #the user has entered an invalid expression: an error will be displayed
            answer_string = "ERROR"

        return answer_string
    
    def draw(self, top_left_pos, width, height):
        background_rect = gui.BasicButton(top_left_pos, width, height)

        expression_text = gui.DisplayText(self.expression_string, top_left_pos)
        answer_text = gui.DisplayText(self.answer_string, top_left_pos)

        expression_text.set_top_left_pos(top_left_pos)  #put the expression on the left of the box
        answer_text.set_top_right_pos((top_left_pos[0] + width, top_left_pos[1]))  #put the answer on the right of the box

        background_rect.draw(self.window)
        expression_text.draw(self.window)
        answer_text.draw(self.window)


def main(window):
    menu = CalculatorMenu(window)

    while not menu.go_back:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()