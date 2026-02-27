class Cell:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls = 0xF
        self.visited = False

    def has_wall(self, direction: int) -> bool:
        return (self.walls & direction) != 0

    def remove_wall(self, direction: int) -> None:
        self.walls &= ~direction

    def add_wall(self, direction: int) -> None:
        self.walls |= direction
