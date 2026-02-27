from .MazeGenerator import MazeGenerator


class Menu:
    def __init__(self, generator: MazeGenerator) -> None:
        self.generator = generator

    def display_menu(self) -> None:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4):")
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
            exit()
