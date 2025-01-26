class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def is_within(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def set_value(self, x: int, y: int, value):
        self.grid[y][x] = value

    def get_value(self, x: int, y: int):
        return self.grid[y][x]
    
    def swap_values(self, x1: int, y1: int, x2: int, y2: int):
        temp = self.get_value(x1, y1)
        self.set_value(x1, y1, self.get_value(x2, y2))
        self.set_value(x2, y2, temp)