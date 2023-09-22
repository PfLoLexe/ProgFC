import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:

        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [0] * self.rows
        
        for i in range(self.rows):
            grid[i] = [0] * self.cols
            if(randomize):
                for j in range(self.cols):
                    grid[i][j] = random.choice((0, 1))

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        addcell = []
        row = cell[0]
        col = cell[1]
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if not (0 <= i <= self.rows - 1 and 0 <= j <= self.cols - 1) or (
                    i == row and j == col
                ):
                    continue
                addcell.append(self.curr_generation[i][j])
        return addcell

    def get_next_generation(self) -> Grid:
        subgrid = self.create_grid(False)

        for i in range(self.rows):
            for j in range(self.cols):
                cell = (i, j)
                if (self.curr_generation[i][j] == 0) and sum(self.get_neighbours(cell)) == 3:
                    subgrid[i][j] = 1
                elif (self.curr_generation[i][j] == 1) and (
                    2 <= sum(self.get_neighbours(cell)) <= 3
                ):
                    subgrid[i][j] = 1
        self.curr_generation = subgrid
        return subgrid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations <= self.generations:  # type: ignore
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        fileforopen = open(filename, "r")
        filetext = [[int(col) for col in row.strip()] for row in fileforopen]
        fileforopen.close()
        gamefromfile = GameOfLife((len(filetext), len(filetext[0])))
        gamefromfile.curr_generation = filetext
        return gamefromfile

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        fileforsave = open(filename, "w")

        for rows in self.curr_generation:
            for cols in rows:
                fileforsave.write(str(cols))

            fileforsave.write("\n")

        fileforsave.close()