import random

from grid import Grid

class PowderParticle:
    def __init__(self, colors: list, density: int = 10):
        self.__colors = colors
        self.color = random.choice(self.__colors)
        self.density = density

    def step(self, grid: Grid, x: int, y: int):
        if not grid.is_within(x, y + 1):
            return
        
        target_cell = grid.get_value(x, y + 1)
        if target_cell == None or type(target_cell) == LiquidParticle:
            grid.swap_values(x, y, x, y + 1)
            return
        else:
            if not grid.is_within(x - 1, y + 1):
                return
            target_cell = grid.get_value(x - 1, y + 1)
            if target_cell == None:
                grid.swap_values(x, y, x - 1, y + 1)
                return
            
            if not grid.is_within(x + 1, y - 1):
                return
            target_cell = grid.get_value(x + 1, y + 1)
            if target_cell == None:
                grid.swap_values(x, y, x + 1, y + 1)
                return

class LiquidParticle:
    def __init__(self, colors: list, density: int = 10):
        self.__colors = colors
        self.color = random.choice(self.__colors)
        self.density = density
    
    def step(self, grid: Grid, x: int, y: int):
        if grid.is_within(x, y + 1):
            target_cell = grid.get_value(x, y + 1)
            if target_cell == None:
                grid.swap_values(x, y, x, y + 1)
                return
        
        # Spread diagonally downwards if possible
        downward_sides = []
        if grid.is_within(x - 1, y + 1) and grid.get_value(x - 1, y + 1) is None:
            downward_sides.append((x - 1, y + 1))
        if grid.is_within(x + 1, y + 1) and grid.get_value(x + 1, y + 1) is None:
            downward_sides.append((x + 1, y + 1))
        if downward_sides:
            target = random.choice(downward_sides)
            grid.swap_values(x, y, target[0], target[1])
            return

        # Spread horizontally
        sides = []
        if grid.is_within(x - 1, y) and grid.get_value(x - 1, y) is None:
            sides.append((x - 1, y))
        if grid.is_within(x + 1, y) and grid.get_value(x + 1, y) is None:
            sides.append((x + 1, y))
        if sides:
            target = random.choice(sides)
            grid.swap_values(x, y, target[0], target[1])
