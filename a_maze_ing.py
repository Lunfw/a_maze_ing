from src.parsing.ConfigLoader import ConfigLoader
from src.logique.MazeGenerator import MazeGenerator
from src.logique.Cell import Cell
import sys
from typing import Dict, Any


def main() -> None:
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py <config_file>")
            sys.exit(1)
        config_file: str = sys.argv[1]
        loader = ConfigLoader()
        config: Dict[str, Any] = loader.load(config_file)
        Cell(config['WIDTH'], config['HEIGHT'])
        generator = MazeGenerator(config)
        generator.generate()
        temp: list = []
        for i in generator.grid:
            for j in i:
                temp.append((j.x, j.y))
        print(f'\nCenter: {temp[int(len(temp) / 2)]}\n')
    except ValueError as e:
        print(f"Error: {e}")


if (__name__ == "__main__"):
    main()
