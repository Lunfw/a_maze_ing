from .Color import Color

from typing import Dict, Any, Optional
from collections import deque

import random
import pyfiglet  # type: ignore
import shutil
import sys
import tty
import termios
import time

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

PATH_COLOR = "\033[42m  \033[0m"
PLAYER_COLOR = "\033[43m  \033[0m"


class Cell:
    def __init__(self) -> None:
        self.walls: int = 0b1111
        self.visited: bool = False


class MazeGenerator:
    def __init__(
        self,
        config: Dict[str, Any],
        seed: Optional[str] = None,
        solution: bool = False
    ) -> None:
        self.width: int = config['WIDTH']
        self.height: int = config['HEIGHT']
        self.entry = config['ENTRY']
        self.exit = config['EXIT']
        self.perfect = config['PERFECT']
        self.output_file = config['OUTPUT_FILE']
        self.seed = seed
        self.path: list[tuple[int, int]] = []
        self.solution = solution
        self.wall_42_cells: Optional[set[tuple[int, int]]] = None
        self.random_seed = random.Random(seed)
        self.grid = [
            [Cell() for x in range(self.width)]
            for y in range(self.height)
        ]
        self.directions = [
            (0, -1, NORTH, SOUTH),
            (1,  0, EAST,  WEST),
            (0,  1, SOUTH, NORTH),
            (-1, 0, WEST,  EAST),
        ]
        self.setColor("1")

    def setColor(self, choice: str) -> None:
        self.color = Color(choice)
        self.wall = self.color.get("wall")
        self.cell = self.color.get("cell")
        self.wall_42 = self.color.get("wall_42")
        self.fill_42 = self.color.get("fill_42")
        self.entry_c = self.color.get("entry")
        self.exit_c = self.color.get("exit")
        self.reset = self.color.get("reset")

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        return bool(self.grid[y][x].walls & direction)

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        self.grid[y][x].walls &= ~direction

    def Draw_42(self) -> Optional[set[tuple[int, int]]]:
        quatre = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
        deux = [
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (4, 2),
            (5, 2),
            (6, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4)
        ]
        x = self.width // 2 - 3
        y = self.height // 2 - 2
        result = set()
        for i, j in quatre + deux:
            result.add((x + i, y + j))
        return result

    def display(self) -> None:
        print(self.wall * (self.width * 2 + 1))
        wall_42: Optional[set[tuple[int, int]]] = self.wall_42_cells
        for y in range(self.height):
            line = self.wall
            bottom = self.wall
            for x in range(self.width):
                content = self.cell
                if self.has_wall(x, y, EAST):
                    east = self.wall
                else:
                    east = self.cell
                if self.has_wall(x, y, SOUTH):
                    south = self.wall
                else:
                    south = self.cell
                corner = self.wall
                if (x, y) == (self.entry[0], self.entry[1]):
                    content = self.entry_c + "  " + self.reset
                if (x, y) == (self.exit[0], self.exit[1]):
                    content = self.exit_c + "  " + self.reset
                if self.solution:
                    if (x, y) in self.path:
                        if (x, y) != (self.entry[0], self.entry[1]):
                            if (x, y) != (self.exit[0], self.exit[1]):
                                content = PATH_COLOR
                        east_in_path = (x + 1, y) in self.path
                        if east_in_path and not self.has_wall(x, y, EAST):
                            east = PATH_COLOR
                        south_in_path = (x, y + 1) in self.path
                        if south_in_path and not self.has_wall(x, y, SOUTH):
                            south = PATH_COLOR
                if wall_42 and (x, y) in wall_42:
                    content = self.fill_42
                if wall_42 and ((x, y) in wall_42 or (x+1, y) in wall_42):
                    east = self.wall_42
                if wall_42 and ((x, y) in wall_42 and (x+1, y) in wall_42):
                    east = self.fill_42
                if wall_42 and ((x, y) in wall_42 or (x, y+1) in wall_42):
                    south = self.wall_42
                if wall_42 and ((x, y) in wall_42 and (x, y+1) in wall_42):
                    south = self.fill_42
                if wall_42:
                    for i, j in [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]:
                        if (i, j) in wall_42:
                            corner = self.wall_42
                line += content + east
                bottom += south + corner
            print(line)
            print(bottom)

    def animate_solution(self, delay: float = 0.03) -> None:
        if not self.path:
            self.bfs()
        if not self.path:
            return
        old = self.solution
        self.solution = False
        print("\033[2J\033[H", end="", flush=True)
        self.display()
        self.solution = old
        entry = (self.entry[0], self.entry[1])
        exit_ = (self.exit[0], self.exit[1])
        for i, (x, y) in enumerate(self.path):
            if (x, y) != entry and (x, y) != exit_:
                print(f"\033[{2 + y * 2};{3 + x * 4}H{PATH_COLOR}",
                      end="", flush=True)
            if i + 1 < len(self.path):
                nx, ny = self.path[i + 1]
                if nx == x + 1:
                    r, c = 2 + y * 2, 5 + x * 4
                elif nx == x - 1:
                    r, c = 2 + y * 2, 5 + nx * 4
                elif ny == y + 1:
                    r, c = 3 + y * 2, 3 + x * 4
                else:
                    r, c = 3 + ny * 2, 3 + x * 4
                print(f"\033[{r};{c}H{PATH_COLOR}",
                      end="", flush=True)
            time.sleep(delay)
        print(f"\033[{2 + self.height * 2};1H", flush=True)

    def position_check(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def generate(self) -> Optional[set[tuple[int, int]]]:
        self.random_seed = random.Random(self.seed)
        self.grid = [
            [Cell() for x in range(self.width)]
            for y in range(self.height)
        ]
        wall_42 = None
        if self.width >= 10 and self.height >= 10:
            wall_42 = self.Draw_42()
        if wall_42 is not None:
            if tuple(self.exit) in wall_42 or tuple(self.entry) in wall_42:
                print("Error: Exit or Entry is inside the 42")
                exit()
            for x, y in wall_42:
                if self.position_check(x, y):
                    self.grid[y][x].visited = True
        self.dfs(self.entry[0], self.entry[1])
        if not self.perfect:
            self.imperfect()
        if wall_42 is not None:
            for x, y in wall_42:
                if self.position_check(x, y):
                    self.grid[y][x].walls = 0xF
            for x, y in wall_42:
                for i, j, wall_here, wall_neighbor in self.directions:
                    k, m = x + i, y + j
                    if (k, m) in wall_42 and self.position_check(k, m):
                        self.remove_wall(x, y, wall_here)
                        self.remove_wall(k, m, wall_neighbor)
        self.wall_42_cells = wall_42
        if self.solution:
            self.bfs()
        return wall_42

    def imperfect(self) -> None:
        total = self.width * (self.height - 1) + self.height * (self.width - 1)
        count = int(total * 0.3)
        for i in range(count):
            x = self.random_seed.randint(0, self.width - 1)
            y = self.random_seed.randint(0, self.height - 1)
            choice = self.random_seed.choice(self.directions)
            j, k, wall_here, wall_neighbor = choice
            m, n = x + j, y + k
            if self.position_check(m, n):
                self.remove_wall(x, y, wall_here)
                self.remove_wall(m, n, wall_neighbor)

    def dfs(self, x: int, y: int) -> None:
        stack = [(x, y)]
        self.grid[y][x].visited = True
        while stack:
            x, y = stack[-1]
            neighbors = []
            for j, k, wall_here, wall_neighbor in self.directions:
                m, n = x + j, y + k
                if self.position_check(m, n):
                    if not self.grid[n][m].visited:
                        neighbors.append((m, n, wall_here, wall_neighbor))
            self.random_seed.shuffle(neighbors)
            moved = False
            for m, n, wall_here, wall_neighbor in neighbors:
                if not self.grid[n][m].visited:
                    self.remove_wall(x, y, wall_here)
                    self.remove_wall(m, n, wall_neighbor)
                    self.grid[n][m].visited = True
                    stack.append((m, n))
                    moved = True
                    break
            if not moved:
                stack.pop()

    def bfs(self) -> Optional[list[tuple[int, int]]]:
        visited = set()
        queue: deque[tuple[int, int]] = deque()
        parents: dict[tuple[int, int], tuple[int, int]] = {}
        visited.add(self.entry)
        queue.append(self.entry)
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                self.path = list(self.reconstruct(parents))
                return self.path
            for j, k, wall_here, wall_neighbor in self.directions:
                m, n = x + j, y + k
                neighbour = (m, n)
                if not self.position_check(m, n):
                    continue
                if neighbour in visited:
                    continue
                if self.has_wall(x, y, wall_here):
                    continue
                visited.add(neighbour)
                parents[neighbour] = (x, y)
                queue.append(neighbour)
        return None

    def reconstruct(
        self,
        parents: dict[tuple[int, int], tuple[int, int]]
    ) -> list[tuple[int, int]]:
        path = []
        current = self.exit
        while current != self.entry:
            path.append(current)
            current = parents[current]
        path.append(self.entry)
        path.reverse()
        return path

    def save(self) -> None:
        with open(self.output_file, 'w') as f:
            for y in range(self.height):
                for x in range(self.width):
                    f.write(format(self.grid[y][x].walls, 'X'))
                f.write("\n")
            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            for i in range(len(self.path) - 1):
                x, y = self.path[i]
                nx, ny = self.path[i + 1]
                if nx == x + 1:
                    f.write("E")
                elif nx == x - 1:
                    f.write("W")
                elif ny == y + 1:
                    f.write("S")
                elif ny == y - 1:
                    f.write("N")
            f.write("\n")

    @staticmethod
    def getKey() -> Optional[int]:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\033':
                ch2 = sys.stdin.read(2)
                if ch2 == '[A':
                    return NORTH
                if ch2 == '[B':
                    return SOUTH
                if ch2 == '[C':
                    return EAST
                if ch2 == '[D':
                    return WEST
            if ch == 'q':
                return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return 0

    def play(self) -> None:
        px, py = self.entry[0], self.entry[1]
        print("\033[?25l", end="", flush=True)
        print("\033[2J\033[H", end="", flush=True)
        self.display()
        print(f"\033[{2 + py * 2};{3 + px * 4}H{PLAYER_COLOR}")
        while True:
            direction = self.getKey()
            if direction is None:
                break
            if direction == 0:
                continue
            if self.has_wall(px, py, direction):
                continue
            print(f"\033[{2 + py * 2};{3 + px * 4}H{self.cell}")
            for j, k, wall, wall_neighbor in self.directions:
                if wall == direction:
                    px, py = px + j, py + k
                    break
            print(f"\033[{2 + py * 2};{3 + px * 4}H{PLAYER_COLOR}")
            if (px, py) == (self.exit[0], self.exit[1]):
                print(f"\033[{2 + self.height * 2};1H", flush=True)
                print("\033[2J\033[H", end="", flush=True)
                columns = shutil.get_terminal_size().columns
                ascii_banner = pyfiglet.figlet_format("Y O U W I N !")
                for line in ascii_banner.split("\n"):
                    print(line.center(columns))
                print("\033[?25h", end="", flush=True)
                time.sleep(2)
                break
