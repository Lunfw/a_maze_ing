from src.parsing.ConfigLoader import ConfigLoader
from src.mazegen.MazeGenerator import MazeGenerator
from src.mazegen.Menu import Menu


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
        generator = MazeGenerator(config)
        generator.generate()
        generator.bfs()
        generator.display()
        menu = Menu(config, generator)
        generator.save()
        while True:
            menu.display_menu()
    except ValueError as e:
        print(f"Error: {e}")


main()
