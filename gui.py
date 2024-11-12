import pygame


class BasicButton:
    #A button that can be clicked

    DEFAULT_BORDER_WIDTH = 4

    DEFAULT_BORDER_COLOUR = (150, 150, 150)
    DEFAULT_BACKGROUND_COLOUR = (255, 255, 255)

    DEFAULT_CORNER_RADIUS = 12  #specifies how rounded the corners should be

    def __init__(self, top_left_pos, width, height):
        self.top_left_x, self.top_left_y = top_left_pos

        self.width = width
        self.height = height

        self.center_x = self.top_left_x + self.width // 2
        self.center_y = self.top_left_y + self.height // 2

        self.border_width = BasicButton.DEFAULT_BORDER_WIDTH

        self.border_colour = BasicButton.DEFAULT_BORDER_COLOUR
        self.background_colour = BasicButton.DEFAULT_BACKGROUND_COLOUR

        self.corner_radius = BasicButton.DEFAULT_CORNER_RADIUS

    def set_border_width(self, new_border_width):
        self.border_width = new_border_width

    def set_border_colour(self, new_border_colour):
        self.border_colour = new_border_colour

    def set_background_colour(self, new_background_colour):
        self.background_colour = new_background_colour

    def set_corner_radius(self, new_corner_radius):
        self.corner_radius = new_corner_radius

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

        #draw the button background
        background_rect_value = (self.top_left_x, self.top_left_y, self.width, self.height)

        pygame.draw.rect(window, self.background_colour, background_rect_value)

        #draw the button border
        border_rect_value = (self.top_left_x - self.border_width, 
                             self.top_left_y - self.border_width, 
                             self.width + self.border_width * 2, 
                             self.height + self.border_width * 2)
        
        pygame.draw.rect(window, self.border_colour, border_rect_value, self.border_width, self.corner_radius)


class TextButton(BasicButton):
    #A button with text on it

    def __init__(self, top_left_pos, width, height, text):
        super().__init__(top_left_pos, width, height)

        self.text = Text(text, self.get_center())

    def set_font_colour(self, new_font_colour):
        self.text.set_font_colour(new_font_colour)

    def set_font_size(self, new_font_size):
        self.text.set_font_size(new_font_size)

    def get_center(self):
        #return the coordinates of the center of the button
        center_x = self.top_left_x + self.width // 2
        center_y = self.top_left_y + self.height // 2

        return center_x, center_y

    def draw(self, window):
        super().draw(window)  #draw the button background
        self.text.draw(window)  #now draw the text on top


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


class Text:
    #Text that can be displayed on screen

    DEFAULT_FONT_SIZE = 32
    DEFAULT_FONT_NAME = "notosansmath"

    DEFAULT_FONT_COLOUR = (0, 0, 0)

    def __init__(self, text, center_pos):
        self.text = text
        self.center_pos = center_pos

        self.font_colour = Text.DEFAULT_FONT_COLOUR

        self.font = pygame.font.SysFont(Text.DEFAULT_FONT_NAME, Text.DEFAULT_FONT_SIZE)

    def set_font_colour(self, new_font_colour):
        self.font_colour = new_font_colour

    def set_font_size(self, new_font_size):
        self.font = pygame.font.SysFont(Text.DEFAULT_FONT_NAME, new_font_size)

    def draw(self, window):
        #draw the text to the screen
        text_surface = self.font.render(self.text, True, self.font_colour)
        text_rect = text_surface.get_rect()

        #ensure text is in correct place
        text_rect.center = self.center_pos

        window.blit(text_surface, text_rect)


#test
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((500, 500))

    b = ColourChangeButton((100, 100), 100, 40, "hello :)")
    b.set_border_colour((255, 0, 0))
    b.set_border_width(10)
    b.set_font(None, 16)
    b.set_font_colour((255, 255, 255))

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