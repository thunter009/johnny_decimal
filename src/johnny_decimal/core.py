from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from johnny_decimal.utils import default_field


@dataclass
class Area:
    """
        Areas group categories together.
    """
    number: int = field()
    name: str = field()


@dataclass
class Category:
    """
        Categories within each area
    """
    number: int = field()
    name: str = field()
    area: Area = field(init=False)
