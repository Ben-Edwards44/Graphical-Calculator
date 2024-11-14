import gui
import pygame

import matrix
import grapher
import equation
import calculator


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class MainMenu:
    BACKGROUND_COLOUR = (200, 200, 200)

    HEADING_CENTER_POS = (SCREEN_WIDTH // 2, 50)

    #specifies the names of the modes as well as the order in which the buttons appear
    MODE_NAMES = [
        ["Calculator", "2D grapher"],
        ["Equation", "Matrix"]
    ]

    #the functions called when the corresponding mode button is clicked - needs to match up with MODE_NAMES
    MODE_CLICK_EVENTS = [
        [calculator.main, grapher.main],
        [equation.main, matrix.main]
    ]

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    BUTTON_PADDING_X = 10  #distance between each mode button in the grid
    BUTTON_PADDING_Y = 10  #distance between each mode button in the grid

    BUTTON_GRID_TOP_LEFT = (50, 250)

    def __init__(self, window):
        self.window = window

        #self.mode_buttons is a 2D array of gui.ColourChangeButton objects that match up with each mode from MODE_NAMES and MODE_CLICK_EVENTS
        self.all_gui_elements, self.mode_buttons = self.setup_gui()

    def setup_gui(self):
        #initialise all of the gui elements present in the main menu
        all_gui_elements = []

        heading_text = gui.DisplayText("Calculator Modes", MainMenu.HEADING_CENTER_POS)
        heading_text.set_font_size(52)

        all_gui_elements.append(heading_text)

        #create the mode buttons grid
        mode_buttons = [[None for _ in i] for i in MainMenu.MODE_NAMES]  #create a blank 2D array to store the mode buttons

        for grid_y in range(len(mode_buttons)):
            for grid_x in range(len(mode_buttons[grid_y])):
                mode_name = MainMenu.MODE_NAMES[grid_y][grid_x]

                button_top_left_x = MainMenu.BUTTON_GRID_TOP_LEFT[0] + (MainMenu.BUTTON_WIDTH + MainMenu.BUTTON_PADDING_X) * grid_x
                button_top_left_y = MainMenu.BUTTON_GRID_TOP_LEFT[1] + (MainMenu.BUTTON_HEIGHT + MainMenu.BUTTON_PADDING_Y) * grid_y

                button = gui.ColourChangeButton((button_top_left_x, button_top_left_y), MainMenu.BUTTON_WIDTH, MainMenu.BUTTON_HEIGHT, mode_name)

                mode_buttons[grid_y][grid_x] = button  #add the button to the mode buttons
                all_gui_elements.append(button)        #also add the button to the list of all gui elements

        return all_gui_elements, mode_buttons

    def check_user_input(self):
        #loop through all of the buttons to check if the user has clicked any
        for grid_y, button_row in enumerate(self.mode_buttons):
            for grid_x, button in enumerate(button_row):
                if button.is_clicked():
                    #if the button has been clicked, call the corresponding function (this should enter the new mode)
                    click_event_function = MainMenu.MODE_CLICK_EVENTS[grid_y][grid_x]
                    click_event_function(self.window)

    def draw(self):        
        self.window.fill(MainMenu.BACKGROUND_COLOUR)

        for element in self.all_gui_elements:
            element.draw(self.window)

        pygame.display.update()


def create_window():
    #initialise pygame and create the drawing window - called on startup
    pygame.init()
    pygame.display.set_caption("Graphical Calculator")

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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