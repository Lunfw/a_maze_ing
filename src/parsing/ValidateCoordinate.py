from .MazeConfig import MazeConfig

from typing import Dict, Any


class ValidateCoordinate(MazeConfig):
    def validate(self, config: Dict[str, Any]) -> None:
        width: int = config['WIDTH']
        height: int = config['HEIGHT']
        for i in ['ENTRY', 'EXIT']:
            if not isinstance(config[i], tuple) or len(config[i]) != 2:
                raise ValueError(f"{i} must be a")
            x: int
            y: int
            x, y = config[i]
            if x < 0 or y < 0:
                raise ValueError(f"{i} coordinates")
            if x >= width:
                raise ValueError(f"{i} x={x} is")
            if y >= height:
                raise ValueError(f"{i} y={y} is")
        if config['ENTRY'] == config['EXIT']:
            raise ValueError("ENTRY and EXIT must be different positions")
