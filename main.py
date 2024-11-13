import gui
import pygame
import calculator


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class MainMenu:
    def __init__(self, window):
        self.window = window

        #for the self.mode_button_click_events dictionary - key is the button object, value is the function to be called when the button is clicked
        self.all_gui_elements, self.mode_button_click_events = self.setup_gui()

    def setup_gui(self):
        #initialise all of the gui elements present in the main menu and add them to self.all_gui_elements and self.button_click_events
        heading_text = gui.Text("Calculator Modes", (250, 250))
        heading_text.set_font_size(52)

        calculator_mode = gui.ColourChangeButton((300, 300), 100, 50, "Calculator")

        all_gui_elements = [
            heading_text,
            calculator_mode
        ]

        mode_button_click_events = {
            calculator_mode : calculator.main
        }

        return all_gui_elements, mode_button_click_events

    def check_user_input(self):
        #check if the user has clicked any buttons
        for button, click_function in self.mode_button_click_events.items():
            if button.is_clicked():
                #if the button has been clicked, move into the next mode by calling the corresponding function
                click_function(self.window)

    def draw(self):        
        self.window.fill((200, 200, 200))

        for element in self.all_gui_elements:
            element.draw(self.window)

        pygame.display.update()


def create_window():
    #initialise pygame and create the drawing window. This is called on startup
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

        #check if user has pressed the quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()