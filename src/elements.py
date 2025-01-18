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
        try:
            if grid.is_within(x - 1, y):
                target_cell = grid.get_value(x - 1, y)

                if random.random() > target_cell.inertial_resistance:
                    target_cell.is_free_falling = True

            if grid.is_within(x + 1, y):
                target_cell = grid.get_value(x + 1, y)
                if random.random() > target_cell.inertial_resistance:
                    target_cell.is_free_falling = True
        except:
            pass

    def look_vertically(self, grid: Grid, x: int, y: int):
        velocity = 0
        for i in range(1, self.gravity + 1):
            if grid.is_within(x, y + i) == False:
                break

            target_cell = grid.get_value(x, y + i)
            if self.can_step_on(target_cell) == False:
                break
            
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
        return x + selected_side_value

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
            self.set_sides_free_fall(grid, x, new_y)
        elif self.is_free_falling:
            new_x, new_y = self.look_diagonally(grid, x, y)
            if new_x != x:
                grid.swap_values(x, y, new_x, new_y)
                self.set_sides_free_fall(grid, new_x, new_y)
            else:
                self.is_free_falling = False



class LiquidElement(MoveableElement):
    def __init__(self, name="particle", colors=["#ffffff"], explosion_resistance=0.5, gravity = 1, dispersion = 1):
        super().__init__(name, colors, explosion_resistance, gravity, dispersion)
    
    def step(self, grid: Grid, x: int, y: int):
        new_y = self.look_vertically(grid, x, y)
        grid.swap_values(x, y, x, new_y)
        if new_y == y:
            new_x = self.look_horizontally(grid, x, y)
            grid.swap_values(x, y, new_x, y)
        
