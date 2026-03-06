from typing import Dict, Any, List

from .ValidateCoordinate import ValidateCoordinate
from .ValidateDimensions import ValidateDimensions
from .MazeConfig import MazeConfig


class ConfigLoader:
    def __init__(self) -> None:
        self.validators: List[MazeConfig] = [
            ValidateDimensions(),
            ValidateCoordinate()
        ]

    def load(self, file_name: str) -> Dict[str, Any]:
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
