from .Cell import Cell
from .Color import Color

from typing import Dict, Any, Optional

import random


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
        self.directions = [
            (1,  0, Cell.EAST,  Cell.WEST),
            (-1, 0, Cell.WEST,  Cell.EAST),
            (0,  1, Cell.SOUTH, Cell.NORTH),
            (0, -1, Cell.NORTH, Cell.SOUTH),
        ]
        self.color = Color("1")
        self._apply_colors()

    def _apply_colors(self) -> None:
        self.wall = self.color.get("wall")
        self.cell = self.color.get("cell")
        self.wall_42 = self.color.get("wall_42")
        self.fill_42 = self.color.get("fill_42")
        self.entry_c = self.color.get("entry")
        self.exit_c = self.color.get("exit")
        self.reset = self.color.get("reset")

    def set_color(self, choice: str) -> None:
        self.color = Color(choice)
        self._apply_colors()

    def Draw_42(self) -> set[tuple[int, int]]:
        mid_x = self.width // 2
        mid_y = self.height // 2
        quatre = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 3),
            (2, 4),
        ]
        deux = [
            (4, 0), (5, 0), (6, 0),
                            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        ]
        result = set()
        offset_x = mid_x - 3
        offset_y = mid_y - 2
        for (x, y) in quatre + deux:
            result.add((offset_x + x, offset_y + y))
        return result

    def _cell_content(
        self,
        x: int,
        y: int,
        wall_42: Optional[set[tuple[int, int]]]
    ) -> str:
        if wall_42 and (x, y) in wall_42:
            return self.fill_42
        if (x, y) == (self.entry[0], self.entry[1]):
            return self.entry_c + "  " + self.reset
        if (x, y) == (self.exit[0], self.exit[1]):
            return self.exit_c + "  " + self.reset
        return self.cell

    def corner(
        self,
        x: int,
        y: int,
        wall_42: Optional[set[tuple[int, int]]]
    ) -> str:
        neighbors = [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]
        for nx, ny in neighbors:
            if wall_42 is not None and (nx, ny) in wall_42:
                return self.wall_42
        return self.wall

    def generate(self) -> None:
        self.grid = [
            [Cell(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]
        if self.width >= 10 and self.height >= 10:
            wall_42 = self.Draw_42()
        else:
            wall_42 = None
        if wall_42 is not None:
            for (x, y) in wall_42:
                if self.position_check(x, y):
                    self.grid[x][y].visited = True
        self.dfs(self.entry[0], self.entry[1])
        if wall_42 is not None:
            for (x, y) in wall_42:
                if self.position_check(x, y):
                    self.grid[x][y].walls = 0xF
            for (x, y) in wall_42:
                for nx, ny, wall_here, wall_neighbor in self.directions:
                    if (nx, ny) in wall_42 and self.position_check(nx, ny):
                        self.grid[x][y].remove_wall(wall_here)
                        self.grid[nx][ny].remove_wall(wall_neighbor)
        print(self.wall * (self.width * 2 + 1))
        for y in range(self.height):
            line = self.wall
            bottom = self.wall
            for x in range(self.width):
                cell = self.grid[x][y]
                cell_42 = wall_42 is not None and (x,   y) in wall_42
                cell_east_42 = wall_42 is not None and (x+1, y) in wall_42
                cell_south_42 = wall_42 is not None and (x, y+1) in wall_42
                east = self.wall if cell.has_wall(Cell.EAST) else self.cell
                south = self.wall if cell.has_wall(Cell.SOUTH) else self.cell
                if cell_42 or cell_east_42:
                    if cell_42 and cell_east_42:
                        east = self.fill_42
                    else:
                        east = self.wall_42
                if cell_42 or cell_south_42:
                    if cell_42 and cell_south_42:
                        south = self.fill_42
                    else:
                        south = self.wall_42
                line += self._cell_content(x, y, wall_42) + east
                bottom += south + self.corner(x, y, wall_42)
            print(line)
            print(bottom)

    def position_check(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def dfs(self, x: int, y: int) -> None:
        self.grid[x][y].visited = True
        directions = [
            (x + dx, y + dy, wh, wn)
            for dx, dy, wh, wn in self.directions
        ]
        self.random_seed.shuffle(directions)
        for nx, ny, wall_here, wall_neighbor in directions:
            if self.position_check(nx, ny) and not self.grid[nx][ny].visited:
                self.grid[x][y].remove_wall(wall_here)
                self.grid[nx][ny].remove_wall(wall_neighbor)
                self.dfs(nx, ny)
