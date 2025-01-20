import gui
import pygame

import about
import grapher
import equation
import calculator
import simul_equation


class MainMenu:
    #specifies the names of the modes as well as the order in which the buttons appear
    MODE_NAMES = [
        ["Calculator", "2D grapher"],
        ["Equation", "Simul Equation"],
        ["About"]
    ]

    #the functions called when the corresponding mode button is clicked - needs to match up with MODE_NAMES
    MODE_CLICK_EVENTS = [
        [calculator.main, grapher.main],
        [equation.main, simul_equation.main],
        [about.main]
    ]

    BUTTON_WIDTH = 250
    BUTTON_HEIGHT = 60

    BUTTON_PADDING_X = 10  #distance between each mode button in the grid
    BUTTON_PADDING_Y = 10  #distance between each mode button in the grid

    def __init__(self, window):
        self.window = window

        self.heading_text = self.setup_heading_text()
        self.mode_buttons = self.setup_mode_buttons()

    def setup_heading_text(self):
        heading_text = gui.DisplayText("Calculator Modes", gui.HEADING_CENTER_POS)
        heading_text.set_font_size(gui.HEADING_FONT_SIZE)

        return heading_text
    
    def calculate_grid_top_left(self):
        buttons_per_row = len(MainMenu.MODE_NAMES[0])
        total_width = MainMenu.BUTTON_WIDTH * buttons_per_row + MainMenu.BUTTON_PADDING_X * (buttons_per_row - 1)

        buttons_per_col = len(MainMenu.MODE_NAMES)
        total_height = MainMenu.BUTTON_HEIGHT * buttons_per_col + MainMenu.BUTTON_PADDING_Y * (buttons_per_col - 1)

        top_left = gui.calculate_centered_top_left(total_width, total_height)

        return top_left

    def setup_mode_buttons(self):
        top_left_x, top_left_y = self.calculate_grid_top_left()

        mode_buttons = [[None for _ in i] for i in MainMenu.MODE_NAMES]  #create a blank 2D array to store the mode buttons

        for grid_y in range(len(mode_buttons)):
            for grid_x in range(len(mode_buttons[grid_y])):
                mode_name = MainMenu.MODE_NAMES[grid_y][grid_x]

                button_top_left_x = top_left_x + (MainMenu.BUTTON_WIDTH + MainMenu.BUTTON_PADDING_X) * grid_x
                button_top_left_y = top_left_y + (MainMenu.BUTTON_HEIGHT + MainMenu.BUTTON_PADDING_Y) * grid_y

                button = gui.ColourChangeButton((button_top_left_x, button_top_left_y), MainMenu.BUTTON_WIDTH, MainMenu.BUTTON_HEIGHT, mode_name)

                mode_buttons[grid_y][grid_x] = button

        return mode_buttons

    def check_user_input(self):
        #loop through all of the buttons to check if the user has clicked any
        for grid_y, button_row in enumerate(self.mode_buttons):
            for grid_x, button in enumerate(button_row):
                if button.is_clicked():
                    #if the button has been clicked, call the corresponding function (this should enter the new mode)
                    click_event_function = MainMenu.MODE_CLICK_EVENTS[grid_y][grid_x]
                    click_event_function(self.window)

    def draw(self):        
        self.window.fill(gui.BACKGROUND_COLOUR)

        self.heading_text.draw(self.window)

        for button_row in self.mode_buttons:
            for button in button_row:
                button.draw(self.window)

        pygame.display.update()


def create_window():
    #initialise pygame and create the drawing window - called on startup
    pygame.init()
    pygame.display.set_caption("Graphical Calculator")

    window = pygame.display.set_mode((gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT))

    return window


def main():
    window = create_window()
    menu = MainMenu(window)

    while True:
        menu.check_user_input()
        menu.draw()

        gui.check_user_quit()


if __name__ == "__main__":
    main()