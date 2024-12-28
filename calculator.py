import gui
import pygame
import calculator_utils


class CalculatorMenu:
    EXPRESSION_FONT_SIZE = 40

    CHAR_BUTTONS = ["pi", "ANS", "sqrt", "="]

    CHAR_BUTTON_WIDTH = 50
    CHAR_BUTTON_HEIGHT = 50

    CHAR_BUTTON_TOP_LEFT = (100, 400)  #top left pos of the row of buttons

    BACKGROUND_BOX_TOP_LEFT = (100, 100)
    BACKGROUND_BOX_BORDER_WIDTH = 5
    BACKGROUND_BOX_CORNER_RADIUS = 5

    def __init__(self, window):
        self.window = window

        self.go_back = False

        self.heading_text = self.setup_heading_text()
        self.expression_input_box = self.setup_expression_input()
        self.back_button = self.setup_back_button()
        self.char_buttons = self.setup_char_buttons()

    def setup_heading_text(self):
        heading_text = gui.DisplayText("Calculator", gui.HEADING_CENTER_POS)
        heading_text.set_font_size(gui.HEADING_FONT_SIZE)

        return heading_text
    
    def setup_expression_input(self):
        expression_input_box = gui.TextInput((105, 340), 300, 50, "Enter expression:")
        expression_input_box.set_font_size(CalculatorMenu.EXPRESSION_FONT_SIZE)

        return expression_input_box
    
    def setup_back_button(self):
        back_button = gui.ColourChangeButton(gui.BACK_BUTTON_POS, gui.BACK_BUTTON_WIDTH, gui.BACK_BUTTON_HEIGHT, "<-")

        return back_button
    
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
                    evaluate_expression(self.expression_input_box.get_inputted_text())
                else:
                    self.expression_input_box.input_text(char)

    def draw_background(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        #draw a box in center of the screen around expression input boxes
        border_x = CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[0]
        border_y = CalculatorMenu.BACKGROUND_BOX_TOP_LEFT[1]
        border_width = gui.SCREEN_WIDTH - 2 * border_x
        border_height = gui.SCREEN_HEIGHT - 2 * border_y

        inner_x = border_x + CalculatorMenu.BACKGROUND_BOX_BORDER_WIDTH
        inner_y = border_y + CalculatorMenu.BACKGROUND_BOX_BORDER_WIDTH
        inner_width = gui.SCREEN_WIDTH - 2 * inner_x
        inner_height = gui.SCREEN_HEIGHT - 2 * inner_y

        pygame.draw.rect(self.window, (255, 255, 255), (inner_x, inner_y, inner_width, inner_height))
        pygame.draw.rect(self.window, (0, 0, 0), (border_x, border_y, border_width, border_height), CalculatorMenu.BACKGROUND_BOX_BORDER_WIDTH, CalculatorMenu.BACKGROUND_BOX_CORNER_RADIUS)

    def draw(self):
        self.draw_background()

        self.heading_text.draw(self.window)
        self.expression_input_box.draw(self.window)
        self.back_button.draw(self.window)

        for button in self.char_buttons:
            button.draw(self.window)

        pygame.display.update()


def evaluate_expression(entered_expression):
    expression = calculator_utils.InfixExpression(entered_expression)
    result = expression.evaluate()

    print(result)


def main(window):
    menu = CalculatorMenu(window)

    while not menu.go_back:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()