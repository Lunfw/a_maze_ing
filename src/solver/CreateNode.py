from ..logique.Cell import Cell
from .BFS import BFS


class Node(BFS):
    def __init__(self, cell: Cell) -> None:
        self.cell: Cell = cell
        self.directions: list = []
        super().add_node(self)
        
