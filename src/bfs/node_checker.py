from ..logique.Cell import Cell


class Node:
    def __init__(self, cell: Cell, previous: Node = None) -> None:
        self.origin: (Node or None) = previous
        self.cell: Cell = cell
        self.can_access: list = []
        self.closed: bool = False
        temp: tuple = (1, 2, 4, 8)
        for i in temp:
            self.can_access.append(self.node_checker(cell, i))
        if (not True in self.can_access):
            self.closed = True

    def node_checker(self, cell: Cell, direction: int) -> bool:
        if (not cell.has_wall(direction)):
            return (direction)
