import pygame


class BasicButton:
    #A button that can be clicked

    DEFAULT_BACKGROUND_COLOUR = (255, 255, 255)

    def __init__(self, top_left_pos, width, height):
        self.top_left_x, self.top_left_y = top_left_pos

        self.width = width
        self.height = height

        self.center_x = self.top_left_x + self.width // 2
        self.center_y = self.top_left_y + self.height // 2

        self.background_colour = BasicButton.DEFAULT_BACKGROUND_COLOUR

    def set_background_colour(self, new_colour):
        self.background_colour = new_colour

    def is_hovered(self):
        #returns whether the user is currently hovering the mouse over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()

        is_over_x = self.top_left_x <= mouse_x <= self.top_left_x + self.width
        is_over_y = self.top_left_y <= mouse_y <= self.top_left_y + self.height

        return is_over_x and is_over_y
    
    def is_clicked(self):
        #returns whether the user is currently clicking the button
        mouse_pressed = pygame.mouse.get_pressed()[0]  #index 0 corresponds to left mouse button
        hovering = self.is_hovered()

        return mouse_pressed and hovering
    
    def draw(self, window):
        #draw the button as a rectangle onto the passed in window
        rect_value = (self.top_left_x, self.top_left_y, self.width, self.height)

        pygame.draw.rect(window, self.background_colour, rect_value)


class TextButton(BasicButton):
    #A button with text on it

    DEFAULT_FONT_NAME = None
    DEFUALT_FONT_SIZE = 32

    DEFAULT_FONT_COLOUR = (0, 0, 0)

    def __init__(self, top_left_pos, width, height, text):
        super().__init__(top_left_pos, width, height)

        self.text = text

        self.font_colour = TextButton.DEFAULT_FONT_COLOUR

        self.set_font(TextButton.DEFAULT_FONT_NAME, TextButton.DEFUALT_FONT_SIZE)

    def set_font_colour(self, new_font_colour):
        self.font_colour = new_font_colour

    def set_font(self, new_font_name, new_font_size):
        self.font = pygame.font.Font(new_font_name, new_font_size)

    def draw_text(self):
        text_surface = self.font.render(self.text, True, self.font_colour)
        text_rect = text_surface.get_rect()

        #make sure the text is in the middle of the button
        text_rect.centerx = self.center_x
        text_rect.centery = self.center_y

        window.blit(text_surface, text_rect)

    def draw(self, window):
        super().draw(window)  #draw the button background
        self.draw_text()  #now draw the text on top


class ColourChangeButton(TextButton):
    #A button that displays text, and changes colour when hovered and clicked

    DEFAULT_NORMAL_COLOUR = (255, 0, 0)
    DEFAULT_HOVERED_COLOUR = (0, 255, 0)
    DEFAULT_CLICKED_COLOUR = (0, 0, 255)

    def __init__(self, top_left_pos, width, height, text):
        super().__init__(top_left_pos, width, height, text)

        self.normal_colour = ColourChangeButton.DEFAULT_NORMAL_COLOUR
        self.hovered_colour = ColourChangeButton.DEFAULT_HOVERED_COLOUR
        self.clicked_colour = ColourChangeButton.DEFAULT_CLICKED_COLOUR

    def set_normal_colour(self, new_colour):
        self.normal_colour = new_colour

    def set_hovered_colour(self, new_colour):
        self.hovered_colour = new_colour

    def set_clicked_colour(self, new_colour):
        self.clicked_colour = new_colour

    def draw(self, window):
        if self.is_clicked():
            self.background_colour = self.clicked_colour
        elif self.is_hovered():
            self.background_colour = self.hovered_colour
        else:
            self.background_colour = self.normal_colour

        super().draw(window)


#test
pygame.init()
window = pygame.display.set_mode((500, 500))

b = ColourChangeButton((100, 100), 100, 40, "hello!")

n = 0
while True:
    b.draw(window)
    pygame.display.update()

    if b.is_clicked():
        print(n)
        n += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()