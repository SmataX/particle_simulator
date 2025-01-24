import pygame

class Button:
    def __init__(
            self, 
            rect: pygame.Rect,
            value: str = "button", 
            action = None, 
            action_args = None,
            background_color: str = "#ffffff", 
            background_color_hover: str = "#dddddd",
            text_color: str = "#000000"
            ):
        
        self.rect = rect
        self.value = value
        self.action = action
        self.action_args = action_args
        self.background_color = background_color
        self.background_color_hover = background_color_hover
        self.text_color = text_color

        self.font = pygame.font.SysFont(None, 24)
        self.hover: bool = False


    def on_click(self):
        if self.action:
            self.action(self.action_args)


    def draw(self, screen):
        bg_color = self.background_color if not self.hover else self.background_color_hover
        pygame.draw.rect(screen, bg_color, self.rect)
        text_surface = self.font.render(self.value, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


def get_inputs(buttons: list[Button]):
    mouse_x, mouse_y = pygame.mouse.get_pos()
        
    for btn in buttons:
        if mouse_x > btn.rect.x and mouse_x < btn.rect.x + btn.rect.width and mouse_y > btn.rect.y and mouse_y < btn.rect.y + btn.rect.height:
            btn.hover = True
            if pygame.mouse.get_pressed()[0]:
                btn.on_click()
        else:
            btn.hover = False


def draw_ui(screen, buttons: list[Button]):
    for btn in buttons:
        btn.draw(screen)