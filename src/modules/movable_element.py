import random

from modules.grid import Grid
from modules.element import Element

class MoveableElement(Element):
    def __init__(self, name = "particle", colors = ["#ffffff"], gravity: int = 1, dispersion: int = 1, inertial_resistance: float = 0.5):
        super().__init__(name, colors)
        
        if gravity < 0:
            raise ValueError("Gravity value should be greater or equal 0")

        if dispersion < 0:
            raise ValueError("Dispersion value should be greater or equal 0")
        
        if inertial_resistance < 0 or inertial_resistance > 1:
            raise ValueError("Inertial Resistance value should be between 0 and 1")
        
        self.gravity = gravity
        self.dispersion = dispersion
        self.inertial_resistance = inertial_resistance
        self.is_free_falling = True

    def can_step_on(self, target_cell) -> bool:
        return target_cell is None
    

    def set_sides_free_fall(self, grid: Grid, x: int, y: int):
        for direction in [-1, 1]:
            if grid.is_within(x + direction, y):
                target_cell = grid.get_value(x + 1, y)
                if target_cell and hasattr(target_cell, "is_free_falling") and not target_cell.is_free_falling and random.random() > target_cell.inertial_resistance:
                    target_cell.is_free_falling = True

    
    def calculate_velocity(self, grid: Grid, x: int, y: int, dir_x: int, dir_y: int, max_steps: int) -> int:
        velocity = 0
        for step in range(1, max_steps + 1):
            step_x = x + dir_x * step
            step_y = y + dir_y * step
            if not grid.is_within(step_x, step_y) or not self.can_step_on(grid.get_value(step_x, step_y)):
                break
            velocity += 1
        return velocity


    def look_vertically(self, grid: Grid, x: int, y: int) -> int:
        return y + self.calculate_velocity(grid, x, y, 0, 1, self.gravity)


    def look_diagonally(self, grid: Grid, x: int, y: int) -> int:
        velocity =  [
            -self.calculate_velocity(grid, x, y, -1, 1, self.dispersion),
            self.calculate_velocity(grid, x, y, 1, 1, self.dispersion)
        ]
        sides = [v for v in velocity if v != 0]
        if sides:
            random_velocity = random.choice(sides)
            return x + random_velocity, y + abs(random_velocity)
        return x, y


    def look_horizontally(self, grid: Grid, x: int, y: int) -> int:
        velocity = [
            -self.calculate_velocity(grid, x, y, -1, 0, self.dispersion),
            self.calculate_velocity(grid, x, y, 1, 0, self.dispersion)
        ]

        sides = [v for v in velocity if v != 0]
        if sides:
            random_velocity = random.choice(sides)
            return x + random_velocity
        return x

    def special_behaviour(self, grid: Grid, x1: int, y1: int, x2: int, y2: int):
        return True
    

    def move(self, grid: Grid, x: int, y: int, target_x: int, target_y: int):
        if self.special_behaviour(grid, x, y, target_x, target_y):
            grid.swap_values(x, y, target_x, target_y)