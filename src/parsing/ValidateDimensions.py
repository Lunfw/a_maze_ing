from .MazeConfig import MazeConfig

from typing import Dict, Any


class ValidateDimensions(MazeConfig):
    def validate(self, config: Dict[str, Any]) -> None:
        for i in ['WIDTH', 'HEIGHT']:
            value: Any = config[i]
            if not isinstance(value, int):
                raise ValueError(f"{i} must be an integer")
            if value <= 0:
                raise ValueError(f"{i} must be positive, got: {value}")
            if value > 1000:
                raise ValueError(f"{i} too large (max 1000), got: {value}")
        if config['WIDTH'] < 5 or config['HEIGHT'] < 5:
            raise ValueError("Warning: Maze too small for '42' pattern")
