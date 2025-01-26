import random

from modules.grid import Grid
from modules.movable_element import MoveableElement
from modules.liquid_element import LiquidElement

class PowderElement(MoveableElement):
    def __init__(self, name="particle", colors=["#ffffff"], gravity = 1, dispersion = 1, inertial_resistance = 0.5):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance)

    def can_step_on(self, target_cell) -> bool:
        return target_cell is None or isinstance(target_cell, LiquidElement)

    def step(self, grid: Grid, x: int, y: int):
        new_y = self.look_vertically(grid, x, y)
        if y != new_y:
            self.move(grid, x, y, x, new_y)
            self.is_free_falling = True
        elif self.is_free_falling:
            new_x, new_y = self.look_diagonally(grid, x, y)
            if new_x != x:
                self.move(grid, x, y, new_x, new_y)
            elif random.random() < self.inertial_resistance:
                    self.is_free_falling = False
                