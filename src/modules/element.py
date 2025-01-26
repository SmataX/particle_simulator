import random

from modules.grid import Grid

class Element:
    def __init__(self, name: str = "particle", colors: list = ["#ffffff"]):
        self.name = name
        self.color = random.choice(colors)
    
    def step(self, grid: Grid, x: int, y: int):
        pass