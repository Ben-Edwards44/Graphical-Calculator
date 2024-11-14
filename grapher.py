import gui
import pygame


def main(window):
    temp = gui.Text("2D grapher", (250, 250))
    temp.set_font_colour((255, 255, 255))

    window.fill((0, 0, 0))
    temp.draw(window)
    pygame.display.update()

    while True:
        gui.check_user_quit()