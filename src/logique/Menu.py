from .MazeGenerator import MazeGenerator

from typing import Dict, Any


class Menu:
    def __init__(
        self,
        config: Dict[str, Any],
        generator: MazeGenerator
    ) -> None:
        self.generator = generator
        self.config = config

    def display_menu(self) -> None:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Choose seed")
        print("5. Quit")
        choice = input("Choice? (1-5):")
        if int(choice) == 1:
            self.generator.generate()
        if int(choice) == 3:
            print("\n===Choose a color theme:===")
            print("1. Classic  (white)")
            print("2. Matrix   (green)")
            print("3. Ocean    (blue)")
            print("4. Violet   (magenta)")
            print("5. Cyan     (cyan)")
            print("6. Fire (fire)")
            print("7. Sunset (sunset)")
            color_choice = input("Choice: ")
            self.generator.set_color(color_choice)
            self.generator.generate()
        if int(choice) == 4:
            print("\n===Choose a seed:===")
            seed = input("Choice: ")
            self.generator = MazeGenerator(self.config, seed)
            self.generator.generate()
        if int(choice) == 5:
            exit()
