import gui
import pygame


def main(window):
    temp = gui.Text("matrix", (250, 250))
    temp.set_font_colour((255, 255, 255))

    window.fill((0, 0, 0))
    temp.draw(window)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()