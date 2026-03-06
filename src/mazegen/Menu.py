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
        self.check = False

    def display_menu(self) -> None:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Choose seed")
        print("5. Perfect/Imperfect")
        print("6. Edit config")
        print("7. Play")
        print("8. Quit")
        choice = input("Choice? (1-8):")
        if not choice.isdigit():
            print("Error: please enter a number between 1 and 8")
            return
        if int(choice) < 1 or int(choice) > 8:
            print("Error: choice must be between 1 and 8")
            return
        if int(choice) == 1:
            self.generator.solution = False
            self.check = False
            self.generator.generate()
            print("\033[2J\033[H")
            self.generator.display()
            self.generator.solution = False
            self.check = False
        if int(choice) == 2:
            self.check = not self.check
            self.generator.solution = self.check
            if self.check:
                self.generator.bfs()
                self.generator.animate_solution()
            else:
                print("\033[2J\033[H")
                self.generator.display()
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
            self.generator.setColor(color_choice)
            print("\033[2J\033[H")
            self.generator.display()
        if int(choice) == 4:
            print("\n===Choose a seed:===")
            seed = input("Choice: ")
            self.generator = MazeGenerator(self.config, seed)
            self.generator.generate()
            print("\033[2J\033[H")
            self.generator.display()
            self.generator.solution = False
            self.check = False
        if int(choice) == 5:
            self.generator.perfect = not self.generator.perfect
            self.generator.solution = False
            self.check = False
            self.generator.generate()
            print("\033[2J\033[H")
            self.generator.display()
        if int(choice) == 6:
            print("\n===Choose edit config===")
            print(f"1. Width       ({self.config['WIDTH']})")
            print(f"2. Height      ({self.config['HEIGHT']})")
            print(f"3. Entry       {self.config['ENTRY']}")
            print(f"4. Exit        {self.config['EXIT']}")
            print(f"5. Perfect     ({self.config['PERFECT']})")
            CONFIG_MAP = {
                1: "WIDTH",
                2: "HEIGHT",
                3: "ENTRY",
                4: "EXIT",
                5: "PERFECT",
            }
            try:
                edit = int(input("Choice: "))
            except ValueError:
                print("Error: please enter a number")
                return
            if edit in CONFIG_MAP:
                key = CONFIG_MAP[edit]
                new_value = input(f"New value for {key}: ")
                try:
                    if edit in (1, 2):
                        val = int(new_value)
                        if val < 3:
                            raise ValueError("Minimum is 3")
                        self.config[key] = val
                    elif edit in (3, 4):
                        parts = new_value.split(",")
                        if len(parts) != 2:
                            raise ValueError("Format: x,y")
                        self.config[key] = (int(parts[0]), int(parts[1]))
                    elif edit == 5:
                        if new_value.lower() not in ("true", "false"):
                            raise ValueError("Only true or false")
                        self.config[key] = new_value.lower() == "true"
                    self.generator = MazeGenerator(self.config)
                    self.generator.generate()
                    self.generator.display()
                except ValueError as e:
                    print(f"Invalid value: {e}")
        if int(choice) == 7:
            self.generator.play()
            self.generator.generate()
            print("\033[2J\033[H")
            self.generator.display()
        if int(choice) == 8:
            exit()
