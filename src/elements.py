import random
import math

from grid import Grid

class Element:
    def __init__(self, name: str = "particle", colors: list = ["#ffffff"], explosion_resistance: float = 0.5):
        self.color = random.choice(colors)

        if explosion_resistance < 0 or explosion_resistance > 1:
            raise ValueError("Explosion Resistance value mus be between 0 and 1")
        self.explosion_resistance = explosion_resistance
    
    def step(self, grid: Grid, x: int, y: int):
        pass

class MoveableElement(Element):
    def __init__(self, name = "particle", colors = ["#ffffff"], explosion_resistance = 0.5, gravity: int = 1, dispersion: int = 1, inertial_resistance: float = 0.5):
        super().__init__(name, colors, explosion_resistance)
        
        if gravity < 0:
            raise ValueError("Gravity value should be greater or equal 0")
        self.gravity = gravity

        if dispersion < 0:
            raise ValueError("Dispersion value should be greater or equal 0")
        self.dispersion = dispersion

        if inertial_resistance < 0 or inertial_resistance > 1:
            raise ValueError("Inertial Resistance value should be between 0 and 1")
        self.inertial_resistance = inertial_resistance

        self.is_free_falling = True

    def can_step_on(self, target_cell) -> bool:
        if target_cell == None:
            return True
        return False
    
    def set_sides_free_fall(self, grid: Grid, x: int, y: int):
        if grid.is_within(x + 1, y):
            target_cell = grid.get_value(x + 1, y)
            if target_cell is not None and hasattr(target_cell, "is_free_falling") and not target_cell.is_free_falling and random.random() > target_cell.inertial_resistance:
                target_cell.is_free_falling = True

        if grid.is_within(x - 1, y):
            target_cell = grid.get_value(x - 1, y)

            if target_cell is not None and hasattr(target_cell, "is_free_falling") and not target_cell.is_free_falling and random.random() > target_cell.inertial_resistance:
                target_cell.is_free_falling = True
                    # target_cell.color = "#00ff00"

    def look_vertically(self, grid: Grid, x: int, y: int):
        velocity = 0
        for i in range(1, self.gravity + 1):
            if grid.is_within(x, y + i) == False:
                break

            target_cell = grid.get_value(x, y + i)
            if self.can_step_on(target_cell) == False:
                break
            self.set_sides_free_fall(grid, x, y + i)
            
            velocity += 1
        return y + velocity

    def look_diagonally(self, grid: Grid, x: int, y: int):
        velocity = [0, 0]
        loop = math.floor((self.gravity + self.dispersion) / 2)
        for i in range(1, loop + 1):
            if grid.is_within(x + i, y + i) == False:
                break

            target_cell = grid.get_value(x + i, y + i)
            if self.can_step_on(target_cell) == False:
                break
            
            velocity[1] += 1

        for i in range(1, loop + 1):
            if grid.is_within(x - i, y + i) == False:
                break

            target_cell = grid.get_value(x - i, y + i)
            if self.can_step_on(target_cell) == False:
                break

            velocity[1] -= 1

        selected_side_value = random.choice([v for v in velocity if velocity != 0])

        for i in range(selected_side_value):
            self.set_sides_free_fall(grid, x + i, y + abs(i))

        return x + selected_side_value, y + abs(selected_side_value)


    def look_horizontally(self, grid: Grid, x: int, y: int):
        velocity = [0, 0]
        for i in range(1, self.dispersion + 1):
            if grid.is_within(x + i, y) == False:
                break

            target_cell = grid.get_value(x + i, y)
            if self.can_step_on(target_cell) == False:
                break
            velocity[1] += 1

        for i in range(1, self.dispersion + 1):
            if grid.is_within(x - i, y) == False:
                break

            target_cell = grid.get_value(x - i, y)
            if self.can_step_on(target_cell) == False:
                break
            velocity[0] -= 1

        selected_side_value = random.choice([v for v in velocity if velocity != 0])
        for i in range(selected_side_value):
            self.set_sides_free_fall(grid, x + i, y)
        return x + selected_side_value
    

    def special_behaviour(self, grid: Grid, x1: int, y1: int, x2: int, y2: int):
        return True

class PowderElement(MoveableElement):
    def __init__(self, name="particle", colors=["#ffffff"], explosion_resistance=0.5, gravity = 1, dispersion = 1, inertial_resistance = 0.5):
        super().__init__(name, colors, explosion_resistance, gravity, dispersion, inertial_resistance)

    def can_step_on(self, target_cell) -> bool:
        if target_cell == None:
            return True
        else:
            if type(target_cell) == LiquidElement:
                return True
        return False

    def step(self, grid: Grid, x: int, y: int):
        new_y = self.look_vertically(grid, x, y)
        if y != new_y:
            grid.swap_values(x, y, x, new_y)
            self.is_free_falling = True
        elif self.is_free_falling:
            new_x, new_y = self.look_diagonally(grid, x, y)
            if new_x != x:
                grid.swap_values(x, y, new_x, new_y)
            else:
                if random.random() < self.inertial_resistance:
                    self.is_free_falling = False



class LiquidElement(MoveableElement):
    def __init__(self, name="particle", colors=["#ffffff"], explosion_resistance=0.5, gravity = 1, dispersion = 1, inertial_resistance = 0.5, viscosity: int = 0.1):
        super().__init__(name, colors, explosion_resistance, gravity, dispersion, inertial_resistance)
        self.viscosity = viscosity
    
    def step(self, grid: Grid, x: int, y: int):
        new_y = self.look_vertically(grid, x, y)
        if self.special_behaviour(grid, x, y, x, new_y):
            grid.swap_values(x, y, x, new_y)
        if new_y == y:
            if random.random() > self.viscosity:
                new_x = self.look_horizontally(grid, x, y)
                if self.special_behaviour(grid, x, y, new_x, y):
                    grid.swap_values(x, y, new_x, y)


class AcidElement(LiquidElement):
    def __init__(self, name="particle", colors=["#ffffff"], explosion_resistance=0.5, gravity=1, dispersion=1, inertial_resistance=0.5):
        super().__init__(name, colors, explosion_resistance, gravity, dispersion, inertial_resistance)

    def can_step_on(self, target_cell):
        if target_cell == None:
            return True
        else:
            if type(target_cell) == Element:
                return True
        return False
    
    def special_behaviour(self, grid, x1, y1, x2, y2):
        target_cell = grid.get_value(x2, y2)
        if target_cell is not None:
            if type(target_cell) == Element and random.random() > 0.65:
                grid.set_value(x1, y1, None)
                grid.set_value(x2, y2, None)
            return False
        return True
        
