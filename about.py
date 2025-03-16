import gui
import pygame


ABOUT_TEXT = """
This is a graphical calculator emulator.
It is intended to help with revision for A level
maths and further maths, but can be
useful for any level of maths.

The calculator has four main modes:
- Calculator: Performs simple calculations
and evaluates expressions
- 2D grapher: Draws graphs of 2D funcitons
- Simul equation: Solves systems of linear
simultaneous equations
- Equation: Finds approximate solutions to a
single equation
"""

FONT_SIZE = 30

TEXT_Y = 60

LINE_PADDING_Y = 36


def setup_heading_text():
    heading_text = gui.DisplayText("About", gui.HEADING_CENTER_POS)
    heading_text.set_font_size(gui.HEADING_FONT_SIZE)

    return heading_text


def setup_about_text():
    #pygame cannot render newlines, so a new text object
    #needs to be created for each line
    lines = ABOUT_TEXT.splitlines()

    text_objects = []
    for inx, line in enumerate(lines):
        text_object = gui.DisplayText(line, (0, 0))
        text_object.set_font_size(FONT_SIZE)
        
        width = text_object.get_width()

        y = TEXT_Y + inx * LINE_PADDING_Y
        x, _ = gui.calculate_centered_top_left(width, 0)

        text_object.set_top_left_pos((x, y))

        text_objects.append(text_object)

    return text_objects


def draw(window, text_objects, back_button):
    window.fill(gui.BACKGROUND_COLOUR)

    back_button.draw(window)

    for text in text_objects:
        text.draw(window)

    pygame.display.update()


def main(window):
    text_objects = setup_about_text()
    heading_text = setup_heading_text()

    text_objects.append(heading_text)

    back_button = gui.create_back_button()

    while not back_button.is_clicked():
        draw(window, text_objects, back_button)

        gui.check_user_quit()