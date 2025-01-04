import random

from grid import Grid

class Particle:
    def __init__(self, name: str = "particle", colors: list = ["#ffffff"]):
        self.__colors = colors
        self.color = random.choice(colors)
    
    def step(self, grid: Grid, x: int, y: int):
        pass

class MoveableParticle(Particle):
    def __init__(self, name = "particle", colors = ["#ffffff"], gravity: int = 1):
        super().__init__(name, colors)
        self.gravity = gravity

    def move_verticaly(self, grid: Grid, x: int, y: int):
        velocity = 0
        for i in range(self.gravity):
            if not grid.is_within(x, y + i + 1):
                return velocity
            
            if grid.get_value(x, y + i + 1) != None:
                return velocity
            
            velocity += 1
        
        return velocity

    def move_diagonally():
        pass

    def move_horizontally():
        pass

class PowderParticle(MoveableParticle):
    def __init__(self, name="particle", colors=["#ffffff"], gravity = 1):
        super().__init__(name, colors, gravity)

    def move_verticaly(self, grid, x, y):
        velocity = 0
        for i in range(self.gravity):
            if not grid.is_within(x, y + i + 1):
                return velocity
            
            target_cell = grid.get_value(x, y + i + 1)
            if target_cell != None and type(target_cell) != LiquidParticle:
                return velocity
            
            velocity += 1
        
        return velocity

    def step(self, grid: Grid, x: int, y: int):
        velocity_y = self.move_verticaly(grid, x, y)
        if velocity_y != 0:
            grid.swap_values(x, y, x, y + velocity_y)
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


class LiquidParticle(MoveableParticle):
    def __init__(self, name="particle", colors=["#ffffff"], gravity = 1, dispersion: int = 1):
        super().__init__(name, colors, gravity)
        self.dispersion = dispersion

    def move_horizontally(self, grid: Grid, x: int, y: int, direction: int = -1):
        velocity = 0
        for i in range(self.dispersion):
            if not grid.is_within(x + (i + 1)*direction, y):
                break

            target_cell = grid.get_value(x + (i + 1)*direction, y)
            if target_cell is not None:
                return velocity    
            velocity += direction
        
        return velocity
    
    def step(self, grid: Grid, x: int, y: int):
        velocity_y = self.move_verticaly(grid, x, y)
        if velocity_y != 0:
            grid.swap_values(x, y, x, y + velocity_y)
        else:
            # Spread horizontally
            velocities = [self.move_horizontally(grid, x, y, -1), self.move_horizontally(grid, x, y, 1)]
            sides = [r for r in velocities if velocities != 0]
            if sides:
                velocity = random.choice(sides)
                grid.swap_values(x, y, x + velocity, y)
