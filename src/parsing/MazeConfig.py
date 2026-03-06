from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple


class MazeConfig(ABC):
    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}

    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> None:
        pass

    @staticmethod
    def open_file(file_name: str) -> List[str] | None:
        try:
            with open(file_name, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            print("File not found")
        return None

    def parsing(self, lines: List[str]) -> Dict[str, Any]:
        """Parse configuration lines into config dictionary."""
        self.config = {}
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if line.startswith('#'):
                continue
            self.validate_line_format(line, line_number)
            key, value_str = self.extract_key_value(line, line_number)
            if key in self.config:
                raise ValueError(f"Line {line_number}: Duplicate key '{key}'")
            value = self.parse_value(key, value_str, line_number)
            self.config[key] = value
        return self.config

    def validate_line_format(
        self,
        line: str,
        line_number: int
    ) -> None:
        """Validate basic line format (KEY=VALUE)."""
        if '=' not in line:
            raise ValueError(f"Line {line_number}: Missing '='")
        if line.count('=') > 1:
            raise ValueError(f"Line {line_number}: Multiple '=' found")

    def extract_key_value(
        self,
        line: str,
        line_number: int
    ) -> Tuple[str, str]:
        """Extract and validate key and value from line."""
        key, value_str = line.split('=', 1)
        key = key.strip().upper()
        value_str = value_str.strip()
        if not key:
            raise ValueError(f"Line {line_number}: Empty key")
        if not key.replace('_', '').isalnum():
            raise ValueError(
                f"Line {line_number}: Invalid key '{key}'"
            )
        if not value_str:
            raise ValueError(
                f"Line {line_number}: Empty value for key '{key}'"
            )
        return key, value_str

    def parse_value(
        self,
        key: str,
        value_str: str,
        line_number: int
    ) -> Any:
        """Parse value string based on key type."""
        if key in ['ENTRY', 'EXIT']:
            return self.parse_coordinates(key, value_str, line_number)
        elif key == 'PERFECT':
            return self.parse_boolean(key, value_str, line_number)
        elif key == 'OUTPUT_FILE':
            return value_str
        else:
            return self.parse_integer(key, value_str, line_number)

    def parse_coordinates(
        self,
        key: str,
        value_str: str,
        line_number: int
    ) -> Tuple[int, int]:
        """Parse coordinate string 'x,y' to tuple."""
        if ',' not in value_str:
            raise ValueError(
                f"Line {line_number}: {key} must be in format 'x,y'"
            )
        parts = value_str.split(',')
        if len(parts) != 2:
            raise ValueError(
                f"Line {line_number}: {key} must have exactly 2 coordinates"
            )
        if not parts[0].strip() or not parts[1].strip():
            raise ValueError(
                f"Line {line_number}: {key} coordinates cannot be empty"
            )
        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
            return (x, y)
        except ValueError:
            raise ValueError(
                f"Line {line_number}: {key} coordinates must be integers"
            )

    def parse_integer(
        self,
        key: str,
        value_str: str,
        line_number: int
    ) -> int:
        """Parse integer value."""
        try:
            return int(value_str)
        except ValueError:
            raise ValueError(
                f"Line {line_number}: {key} must be an integer, "
                f"got: '{value_str}'"
            )

    def parse_boolean(
        self,
        key: str,
        value_str: str,
        line_number: int
    ) -> bool:
        """Parse boolean value (True/False)."""
        if value_str not in ['True', 'False']:
            raise ValueError(
                f"Line {line_number}: {key} must be 'True' or 'False', "
                f"got: '{value_str}'"
            )
        return value_str == 'True'

    def requirement(self, config: Dict[str, Any]) -> None:
        """Check required keys are present."""
        list_requirement: List[str] = [
            'WIDTH',
            'HEIGHT',
            'ENTRY',
            'EXIT',
            'OUTPUT_FILE',
            'PERFECT'
        ]
        missing = [
            key for key in list_requirement if key not in self.config
        ]
        if missing:
            raise ValueError(
                f"Missing required keys: {', '.join(missing)}"
            )
        return None
