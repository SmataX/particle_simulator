from modules.liquid_element import LiquidElement

from modules.elements.water import Water
from modules.elements.stone import Stone

class Lava(LiquidElement):
    def __init__(self, name="lava", colors=["#EC753A", "#D73F24"], gravity=1, dispersion=1, viscosity=0.75, inertial_resistance=0.5):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance, viscosity)

    def can_step_on(self, target_cell):
        return super().can_step_on(target_cell) or type(target_cell).__name__ == 'Water'

    def special_behaviour(self, grid, x1, y1, x2, y2):
        if type(grid.get_value(x2, y2)).__name__ == 'Water':
            for i in range(3):
                if grid.is_within(x1, y1 + i):
                    grid.set_value(x1, y1 + i, Stone())
            grid.set_value(x2, y2, None)
        return True

