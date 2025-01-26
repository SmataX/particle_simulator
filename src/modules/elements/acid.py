import random

from modules.grid import Grid
from modules.liquid_element import LiquidElement

class Acid(LiquidElement):
    def __init__(self, name="acid", colors=["#006600"], gravity=2, dispersion=2, viscosity=0.3, acid_strength=0.1, inertial_resistance=0.5):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance, viscosity)

        if acid_strength < 0 or acid_strength > 1:
            raise ValueError("Acid Strength value should be between 0 and 1")
        self.acid_strength = acid_strength

    def can_step_on(self, target_cell) -> bool:
        return target_cell is None or type(target_cell).__name__ == 'Stone'
    

    def move(self, grid: Grid, x: int, y: int, target_x: int, target_y: int):
        if self.special_behaviour(grid, x, y, target_x, target_y) and grid.get_value(target_x, target_y) is None:
            grid.swap_values(x, y, target_x, target_y)

    def special_behaviour(self, grid, x1, y1, x2, y2):
        target_cell = grid.get_value(x2, y2)
        if type(target_cell).__name__ == 'Stone' and random.random() < self.acid_strength:
            grid.set_value(x2, y2, None)
            grid.set_value(x1, y1, None)
            return False
        return True
