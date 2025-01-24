import pygame
import random

from grid import Grid
from elements import Element, PowderElement, LiquidElement, AcidElement

from user_interface import draw_ui, Button, get_inputs

class ToolBar:
    current_particle = 0
    brush_radius = 5

    def draw(grid: Grid, pos_x: int, pos_y: int):
        center_x = (pos_x - round(ToolBar.brush_radius / 2))
        center_y = (pos_y - round(ToolBar.brush_radius / 2))
        for x in range(ToolBar.brush_radius):
            for y in range(ToolBar.brush_radius):
                if grid.is_within(center_x + x, center_y + y):
                    grid.set_value(center_x + x, center_y + y, ToolBar.get_particle())

    def get_particle():
        particles_list = [
            PowderElement(name="sand", colors=["#f6d7b0", "#f2d2a9", "#eccca2"], gravity=2, dispersion=1, inertial_resistance=0.3), 
            PowderElement(name="wet_sand", colors=["#997B5B", "#997B5B"], gravity=2, dispersion=1, inertial_resistance=0.7), 
            PowderElement(name="ash", colors=["#868683", "#B4B4B4"], gravity=1, dispersion=3, inertial_resistance=0.05),
            LiquidElement(name="water", colors=["#00b1ff", "#0097ff", "#1588ff"], gravity=3, dispersion=3, viscosity=0.1),
            LiquidElement(name="lava", colors=["#EC753A", "#D73F24"], gravity=1, dispersion=2, viscosity=0.7),
            Element()
        ]
        return particles_list[ToolBar.current_particle]
    
    def change_element(id: int):
        ToolBar.current_particle = id

class App:
    def __init__(self, WIDTH: int = 100, HEIGHT = 100, CELL_SIZE = 4):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH * CELL_SIZE + 100, HEIGHT * CELL_SIZE))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid(WIDTH, HEIGHT)
        self.cell_size = CELL_SIZE


        # UI
        buttons = [
            Button(value="sand", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 0, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=ToolBar.change_element, action_args=0),
            Button(value="wet sand", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 25, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=ToolBar.change_element, action_args=1),
            Button(value="ash", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 50, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=ToolBar.change_element, action_args=2),
            Button(value="water", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 75, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=ToolBar.change_element, action_args=3),
            Button(value="lava", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 100, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=ToolBar.change_element, action_args=4)
        ]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    

            self.screen.fill("#000000")

            # UI
            draw_ui(self.screen, buttons)
            get_inputs(buttons)

            self.update()

            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def get_position_in_grid(self, position: tuple):
        return [round(position[0] / self.cell_size), round(position[1] / self.cell_size)]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            ToolBar.current_particle = 0
        elif keys[pygame.K_2]:
            ToolBar.current_particle = 1
        elif keys[pygame.K_3]:
            ToolBar.current_particle = 2
        elif keys[pygame.K_4]:
            ToolBar.current_particle = 3
        elif keys[pygame.K_5]:
            ToolBar.current_particle = 4
        elif keys[pygame.K_6]:
            ToolBar.current_particle = 5

        if pygame.mouse.get_pressed()[0]:
            mouse_pos_in_grid = self.get_position_in_grid(pygame.mouse.get_pos())
            if self.grid.is_within(mouse_pos_in_grid[0], mouse_pos_in_grid[1]):
                ToolBar.draw(self.grid, mouse_pos_in_grid[0], mouse_pos_in_grid[1])

        for y in range(self.grid.height - 1, -1, -1):
            random_row = list(range(self.grid.width))
            random.shuffle(random_row)
            for x in random_row:
                target_cell = self.grid.get_value(x, y)
                if target_cell:
                    target_cell.step(self.grid, x, y)

        self.render_particles()

    def render_particles(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                target_cell = self.grid.get_value(x, y)
                if target_cell:
                    pygame.draw.rect(self.screen, target_cell.color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

pygame.quit()

if __name__ == "__main__":
    App()