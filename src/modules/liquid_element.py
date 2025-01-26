import random

from modules.grid import Grid
from modules.element import Element
from modules.movable_element import MoveableElement

class LiquidElement(MoveableElement):
    def __init__(self, name="particle", colors=["#ffffff"], gravity = 1, dispersion = 1, inertial_resistance = 0.5, viscosity: int = 0.1):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance)
        self.viscosity = viscosity
    
    def step(self, grid: Grid, x: int, y: int):
        new_y = self.look_vertically(grid, x, y)
        
        if new_y != y:
            self.move(grid, x, y, x, new_y)
        elif random.random() > self.viscosity:
            new_x = self.look_horizontally(grid, x, y)
            self.move(grid, x, y, new_x, y)
                