import pygame
import main_menu


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


def create_window():
    #initialise pygame and create the drawing window. This is called on startup
    pygame.init()
    pygame.display.set_caption("Graphical Calculator")

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return window


def main():
    window = create_window()

    main_menu.main(window)  #Enter the main menu


if __name__ == "__main__":
    main()