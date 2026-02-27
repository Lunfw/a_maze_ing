from ..logique import Cell
from ..logique import MazeGenerator


class BFS(MazeGenerator):
    def __init__(self, maze: MazeGenerator):
        super().__init__(maze.config, maze.seed)
        self.queue = [self.entry]
        self.visit_list = set()

    def add_node(self, node: Node) -> None:
        self.queue.add(node)

    def check_neighbors(self, node: Node) -> None:
        directions: tuple = (1, 2, 4, 8)
        if (node not in visit_list):
            self.visit_list.add(node.cell)
            for i in directions:
                if (cell.has_wall(i)):
                    node.directions.append(i)
                else:
                    continue

    def bfs_runner(self) -> None:
        for i in self.queue:
            pass
