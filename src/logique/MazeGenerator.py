from .Cell import Cell

from typing import Dict, Any, Optional

import random


WALL = "\033[107m  \033[0m"
WHITE = "\033[0m"
CELL = "  "
PINK = "\033[105m"
RED  = "\033[101m"


class MazeGenerator:
    def __init__(
        self,
        config: Dict[str, Any],
        seed: Optional[int] = None
    ) -> None:

        self.width: int = config['WIDTH']
        self.height: int = config['HEIGHT']
        self.entry: tuple[int, int] = config['ENTRY']
        self.exit: tuple[int, int] = config['EXIT']
        self.perfect: bool = config['PERFECT']
        self.output_file: str = config['OUTPUT_FILE']
        self.seed: Optional[int] = seed
        self.random_seed = random.Random(seed)
        self.grid = [
            [Cell(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]

    def generate(self) -> None:
        self.dfs(self.entry[0], self.entry[1])
        top = WALL * (self.width * 2 + 1)
        print(top)
        for y in range(self.height):
            line = WALL
            bottom = WALL
            for x in range(self.width):
                cell = self.grid[x][y]
                if cell.has_wall(Cell.EAST):
                    east = WALL
                else:
                    east = CELL
                if cell.has_wall(Cell.SOUTH):
                    south = WALL
                else:
                    south = CELL
                if (x, y) == (self.entry[0], self.entry[1]):
                    line += PINK + CELL + WHITE + east
                elif (x, y) == (self.exit[0], self.exit[1]):
                    line += RED + CELL + WHITE + east
                else: 
                    line += CELL + east
                bottom += south + WALL
            print(line)
            print(bottom)

    def position_check(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def dfs(self, x: int, y: int) -> None:
        self.grid[x][y].visited = True
        directions = [
                (x, y-1, Cell.NORTH, Cell.SOUTH),
                (x, y+1, Cell.SOUTH, Cell.NORTH),
                (x+1, y, Cell.EAST, Cell.WEST),
                (x-1, y, Cell.WEST, Cell.EAST),
            ]
        self.random_seed.shuffle(directions)
        for nx, ny, wall_here, wall_neighbor in directions:
            if self.position_check(nx, ny) and not self.grid[nx][ny].visited:
                self.grid[x][y].remove_wall(wall_here)
                self.grid[nx][ny].remove_wall(wall_neighbor)
                self.dfs(nx, ny)
