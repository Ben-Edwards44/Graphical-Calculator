import gui
import pygame
import calculator_utils


class CalculatorMenu:
    EXPRESSION_FONT_SIZE = 40

    def __init__(self, window):
        self.window = window

        self.go_back = False

        self.heading_text = self.setup_heading_text()
        self.expression_input_box = self.setup_expression_input()
        self.back_button = self.setup_back_button()

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
    
    def check_user_input(self):
        self.expression_input_box.check_user_input()  #check if user is entering expression
        if self.back_button.is_clicked(): self.go_back = True  #check if user has pressed back
    
    def draw_background(self):
        self.window.fill(gui.BACKGROUND_COLOUR)

        #draw box around expression input boxes
        pygame.draw.rect(self.window, (0, 0, 0), (100, 100, 300, 300))
        pygame.draw.rect(self.window, (255, 255, 255), (105, 105, 290, 290))

    def draw(self):
        self.draw_background()

        self.heading_text.draw(self.window)
        self.expression_input_box.draw(self.window)
        self.back_button.draw(self.window)

        pygame.display.update()

def main(window):
    menu = CalculatorMenu(window)

    while not menu.go_back:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()