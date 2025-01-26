from modules.liquid_element import LiquidElement

from modules.elements.stone import Stone

class Water(LiquidElement):
    def __init__(self, name="water", colors=["#00b1ff", "#0097ff", "#1588ff"], gravity=3, dispersion=3, viscosity=0.1, inertial_resistance=0.5):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance, viscosity)

    def can_step_on(self, target_cell):
        return super().can_step_on(target_cell) or type(target_cell).__name__ == 'Lava'

    def special_behaviour(self, grid, x1, y1, x2, y2):
        if type(grid.get_value(x2, y2)).__name__ == 'Lava':
            for i in range(3):
                if grid.is_within(x1, y1 + i):
                    grid.set_value(x1, y1 + i, Stone())
            grid.set_value(x2, y2, None)
        return True
