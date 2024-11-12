import pygame


class BasicButton:
    #A button that can be clicked

    def __init__(self, top_left_pos, width, height, background_colour):
        self.top_left_x, self.top_left_y = top_left_pos

        self.width = width
        self.height = height

        self.background_colour = background_colour

        self.center_x = self.top_left_x + self.width // 2
        self.center_y = self.top_left_y + self.height // 2

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

    def __init__(self, top_left_pos, width, height, background_colour, text, text_colour):
        super().__init__(top_left_pos, width, height, background_colour)

        self.text = text
        self.text_colour = text_colour

        self.set_font(TextButton.DEFAULT_FONT_NAME, TextButton.DEFUALT_FONT_SIZE)

    def set_font(self, new_font_name, new_font_size):
        #create a pygame font object
        self.font = pygame.font.Font(new_font_name, new_font_size)

    def draw(self, window):
        super().draw(window)  #draw the button background

        #now draw the text on top
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect()

        text_rect.centerx = self.center_x
        text_rect.centery = self.center_y

        window.blit(text_surface, text_rect)





#test
pygame.init()
window = pygame.display.set_mode((500, 500))

b = TextButton((100, 100), 100, 40, (255, 0, 0), "hello!", (0, 0, 255))

n = 0
while True:
    b.draw(window)
    pygame.display.update()

    if b.is_hovered():
        print(n)
        n += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()