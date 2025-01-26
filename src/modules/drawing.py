import random
import pygame

from modules.grid import Grid

# Powders
from modules.elements.sand import Sand
from modules.elements.wet_sand import WetSand
from modules.elements.ash import Ash

# Liquids
from modules.elements.water import Water
from modules.elements.lava import Lava
from modules.elements.acid import Acid

# Static
from modules.elements.stone import Stone

class Drawing:
    list_of_elements = [Sand, WetSand, Ash, Water, Lava, Acid, Stone]
    selected_element = 0

    last_mouse_position = None

    def place_elements(grid: Grid, cell_size: int):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = round(mouse_x / cell_size), round(mouse_y / cell_size)

        if True in pygame.mouse.get_pressed():
            if not grid.is_within(grid_x, grid_y):
                return
            
            if Drawing.last_mouse_position == None:
                Drawing.last_mouse_position = (grid_x, grid_y)

            if pygame.mouse.get_pressed()[0] and grid.get_value(grid_x, grid_y) is None:
                Drawing.draw_between_two_points(grid, grid_x, grid_y, Drawing.last_mouse_position[0], Drawing.last_mouse_position[1])
            elif pygame.mouse.get_pressed()[2]:
                Drawing.draw_between_two_points(grid, grid_x, grid_y, Drawing.last_mouse_position[0], Drawing.last_mouse_position[1], set_none = True)
            Drawing.last_mouse_position = (grid_x, grid_y)
        else:
            Drawing.last_mouse_position = None
            
            
            

    def draw_between_two_points(grid: Grid, x1: int, y1: int, x2: int, y2: int, set_none = False):
        dx = x1 - x2
        dy = y1 - y2
        distance = max(abs(dx), abs(dy))
            
        for i in range(distance + 1):
            step_x = x2 + i * (dx / distance if distance else 0)
            step_y = y2 + i * (dy / distance if distance else 0)
            step_x, step_y = round(step_x), round(step_y)
                
            if grid.is_within(step_x, step_y):
                if set_none == True:
                    value = None
                else:
                    value = Drawing.list_of_elements[Drawing.selected_element]()
                grid.set_value(step_x, step_y, value)
                    


    def change_element(id: int):
        Drawing.selected_element = id