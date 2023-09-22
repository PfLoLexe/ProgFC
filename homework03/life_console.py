import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for rows in range(self.life.cols):
            for cols in range(self.life.rows):
                try:

                    if self.life.curr_generation[rows][cols]:
                        screen.addch(rows + 1, cols + 1, "*")

                except:
                    pass

    def run(self) -> None:
        screen = curses.initscr()
        pause = False

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()

        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife((24, 80), max_generations=50)
    ui = Console(game)
    ui.run()