import gui
import pygame


class MainMenu:
    def __init__(self, window):
        self.window = window

        self.setup_gui()

    def setup_gui(self):
        #initialise all of the gui elements present in the main menu
        self.heading_text = gui.Text("Calculator Modes", (250, 250))
        self.heading_text.set_font_size(52)

        self.calculator_mode = gui.ColourChangeButton((300, 300), 100, 50, "Calculator")

    def check_user_input(self):
        if self.calculator_mode.is_clicked():
            print("calculator mode")

    def draw(self):
        gui_elements = (self.heading_text,
                        self.calculator_mode)
        
        self.window.fill((200, 200, 200))

        for element in gui_elements:
            element.draw(self.window)

        pygame.display.update()


def main(window):
    menu = MainMenu(window)

    while True:
        menu.check_user_input()
        menu.draw()

        #check if user has pressed the quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()