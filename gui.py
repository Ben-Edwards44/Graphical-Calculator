import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

HEADING_FONT_SIZE = 52
HEADING_CENTER_POS = (SCREEN_WIDTH // 2, 50)

BACK_BUTTON_POS = (20, 20)
BACK_BUTTON_WIDTH = 40
BACK_BUTTON_HEIGHT = 40

BACKGROUND_COLOUR = (200, 200, 200)


class BasicButton:
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

        self.has_been_clicked = False

    def set_border_width(self, new_border_width):
        self.border_width = new_border_width

    def set_border_colour(self, new_border_colour):
        self.border_colour = new_border_colour

    def set_background_colour(self, new_background_colour):
        self.background_colour = new_background_colour

    def set_corner_radius(self, new_corner_radius):
        self.corner_radius = new_corner_radius

    def get_has_been_clicked(self):
        #if the user clicks on a button for multiple frames, we may not want to register multiple clicks so we check if the button has already been clicked
        return self.has_been_clicked

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

        clicked = mouse_pressed and hovering
        self.has_been_clicked = clicked

        return clicked
    
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
    def __init__(self, top_left_pos, width, height, text):
        super().__init__(top_left_pos, width, height)

        self.text = DisplayText(text, self.get_center())

    def set_font_colour(self, new_font_colour):
        self.text.set_font_colour(new_font_colour)

    def set_font_size(self, new_font_size):
        self.text.set_font_size(new_font_size)

    def set_displayed_text(self, new_displayed_text):
        self.text.set_displayed_text(new_displayed_text)

    def get_center(self):
        #return the coordinates of the center of the button
        center_x = self.top_left_x + self.width // 2
        center_y = self.top_left_y + self.height // 2

        return center_x, center_y

    def draw(self, window):
        super().draw(window)  #draw the button background
        self.text.draw(window)  #now draw the text on top


class ColourChangeButton(TextButton):
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


class DisplayText:
    DEFAULT_FONT_SIZE = 32
    DEFAULT_FONT_NAME = "notosansmath"

    DEFAULT_FONT_COLOUR = (0, 0, 0)

    def __init__(self, displayed_text, center_pos):
        self.displayed_text = displayed_text
        self.center_pos = center_pos

        self.font_colour = DisplayText.DEFAULT_FONT_COLOUR

        self.font = pygame.font.SysFont(DisplayText.DEFAULT_FONT_NAME, DisplayText.DEFAULT_FONT_SIZE)

    def set_font_colour(self, new_font_colour):
        self.font_colour = new_font_colour

    def set_font_size(self, new_font_size):
        self.font = pygame.font.SysFont(DisplayText.DEFAULT_FONT_NAME, new_font_size)

    def set_displayed_text(self, new_displayed_text):
        self.displayed_text = new_displayed_text

    def set_top_left_pos(self, new_top_left_pos):
        #we need to convert the top left pos into a center pos
        text_surface = self.font.render(self.displayed_text, False, self.font_colour)
        text_rect = text_surface.get_rect()

        new_center_x = new_top_left_pos[0] + text_rect.width // 2
        new_center_y = new_top_left_pos[1] + text_rect.height // 2

        self.center_pos = (new_center_x, new_center_y)

    def set_top_right_pos(self, new_top_left_pos):
        #we need to convert the top left pos into a center pos
        text_surface = self.font.render(self.displayed_text, False, self.font_colour)
        text_rect = text_surface.get_rect()

        new_center_x = new_top_left_pos[0] - text_rect.width // 2
        new_center_y = new_top_left_pos[1] + text_rect.height // 2

        self.center_pos = (new_center_x, new_center_y)

    def draw(self, window):
        text_surface = self.font.render(self.displayed_text, True, self.font_colour)
        text_rect = text_surface.get_rect()

        text_rect.center = self.center_pos

        window.blit(text_surface, text_rect)  #draw the text to the screen


class TextInput:
    DEFAULT_SELECTED_COLOUR = (100, 100, 100)
    DEFAULT_NON_SELECTED_COLOUR = (200, 200, 200)

    def __init__(self, top_left_pos, width, height, prompt_text):
        self.prompt_text = prompt_text
        self.inputted_text = ""

        self.selected = False
        self.can_update_selected = True

        self.selected_colour = TextInput.DEFAULT_SELECTED_COLOUR
        self.non_selected_colour = TextInput.DEFAULT_NON_SELECTED_COLOUR

        self.button = ColourChangeButton(top_left_pos, width, height, prompt_text)

    def set_selected_colour(self, new_colour):
        self.selected_colour = new_colour

    def set_non_selected_colour(self, new_colour):
        self.non_selected_colour = new_colour

    def set_font_size(self, new_font_size):
        self.button.set_font_size(new_font_size)

    def get_inputted_text(self):
        return self.inputted_text

    def update_selected(self):
        if self.button.is_clicked():
            if self.can_update_selected:
                self.selected = not self.selected
                self.can_update_selected = False  #make sure we don't toggle self.selected again until the user has stopped clicking the button
        else:
            self.can_update_selected = True  #user has stopped clicking, so we should update self.selected next time they click

            if pygame.mouse.get_pressed()[0]:
                #user has clicked somewhere else, so we no longer want this text input to be selected
                self.selected = False

    def input_text(self, inputted_text):
        self.inputted_text += inputted_text

    def update_inputted_text(self):
        #check if the user is currently typing text into the input box. If so, get the typed text
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.inputted_text = self.inputted_text[:-1]  #remove the last character of the inputted text
                else:
                    self.input_text(event.unicode)  #add the typed character to the inputted text

    def check_user_input(self):
        self.update_selected()

        if self.selected:
            self.update_inputted_text()

    def draw(self, window):
        if self.selected:
            button_colour = self.selected_colour
        else:
            button_colour = self.non_selected_colour

        if self.inputted_text == "":
            button_text = self.prompt_text
        else:
            button_text = self.inputted_text

        self.button.set_displayed_text(button_text)
        self.button.set_normal_colour(button_colour)

        self.button.draw(window)


def create_back_button():
    #create a back button in the top left of the screen (same for all modes)
    back_button = ColourChangeButton(BACK_BUTTON_POS, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "<-")

    return back_button


def check_user_quit():
    #check whether the user has pressed the quit button in the top right of the window
    quit_events = pygame.event.get(pygame.QUIT)

    if len(quit_events) > 0:
        quit()