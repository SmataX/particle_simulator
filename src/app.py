import pygame
import random

from modules.grid import Grid
from modules.drawing import Drawing
from user_interface import Button, get_inputs, draw_ui

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
            Button(value="sand", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 0, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=0),
            Button(value="wet sand", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 25, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=1),
            Button(value="ash", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 50, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=2),
            Button(value="water", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 75, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=3),
            Button(value="lava", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 100, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=4),
            Button(value="acid", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 125, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=5),
            Button(value="stone", rect=pygame.Rect(WIDTH*CELL_SIZE + 10, 150, 80, 20), background_color="#ffffff", background_color_hover="#ff0000", action=Drawing.change_element, action_args=6)
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
        Drawing.place_elements(self.grid, self.cell_size)

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