import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed

        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        self.width = self.cell_size * self.life.cols
        self.height = self.cell_size * self.life.rows

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                Rect = (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size)
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), Rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), Rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        runing = True
        pause = False

        while runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:  # type: ignore
                        pause = not pause

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posittion = pygame.mouse.get_pos()

                    self.life.curr_generation[posittion[1] // self.cell_size][
                        posittion[0] // self.cell_size
                    ] ^= 1

            self.draw_grid()
            self.draw_lines()

            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

if __name__ == "__main__":
    life = GameOfLife((21, 23))
    gui = GUI(life)
    gui.run()