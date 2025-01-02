import pygame

from grid import Grid

class App:
    def __init__(self, WIDTH: int = 100, HEIGHT = 100, CELL_SIZE = 4):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid(WIDTH, HEIGHT)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("#000000")

            self.update()

            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def update(self):
        pass

pygame.quit()

if __name__ == "__main__":
    App()