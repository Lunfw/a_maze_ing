#!/usr/bin/env python3

from typing import Dict, Any, List

from .ValidateCoordinate import ValidateCoordinate
from .ValidateDimensions import ValidateDimensions
from .MazeConfig import MazeConfig


class ConfigLoader:
    """Orchestrator that uses validators."""

    def __init__(self) -> None:
        self.validators: List[MazeConfig] = [
            ValidateDimensions(),
            ValidateCoordinate()
        ]

    def load(self, file_name: str) -> Dict[str, Any]:
        """Load and validate configuration using all validators."""
        first_validator = self.validators[0]
        lines = first_validator.open_file(file_name)
        if lines is None:
            print("Error: Could not read configuration file")
            return {}
        config: Dict[str, Any] = self.validators[0].parsing(lines)
        self.validators[0].requirement(config)

        for validator in self.validators:
            validator.validate(config)
        return config


'''def main() -> None:
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py <config_file>")
            sys.exit(1)
        config_file: str = sys.argv[1]
        loader = ConfigLoader()
        config: Dict[str, Any] = loader.load(config_file)
        print(config)
    except ValueError as e:
        print(f"Error: {e}")


main()'''
