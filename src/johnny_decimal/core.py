import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pytoml as toml

from johnny_decimal.exceptions import AttributeNotDefined
from johnny_decimal.mixins import DirectoryMixin
from johnny_decimal.utils import default_field


@dataclass
class Input:
    """
        Handles user input
    """
    _path: str = field()

    # @classmethod
    def load(self):
        path = Path(self._path)
        with open(str(path.resolve()), 'rb') as f:
            config = toml.load(f)
        return config


@dataclass
class Area(DirectoryMixin):
    """
        Areas group categories together.

        id is defined when passed to an AreaRegistry object.
    """
    name: str = field()
    id: str = default_field('', init=False)
    _path: Path = default_field(None, init=False, repr=False)
    root: Path = default_field(Path('.'), repr=False)

    @property
    def path(self) -> Path:
        if self.id == '':
            raise AttributeNotDefined(
                'Define instance id before accessing path property')

        if not self._path:
            path = Path(self.root) / Path(f'{self.id}_{self.name}')

        return path


@dataclass
class AreaRegistry:
    """
        Area Registry for collecting individual Area objects and
        assigning them id's and full file paths
    """
    areas: List[Area] = field()

    def __post_init__(self):
        self.areas = self._get_ids()
        self._get_paths()

    def __getitem__(self, index):
        return self.areas[index]

    def _get_ids(self):
        areas = self.areas
        index = range(1, len(areas) + 1)
        for x in zip(areas, index):
            area = x[0]
            index_value = x[1]
            area.id = f'{index_value}0-{index_value}9'
        return areas

    def _get_paths(self):
        areas = self.areas
        return (area.path for area in areas)

    def init(self):
        for area in self.areas:
            area.mkdir()


@dataclass
class Category:
    """
        Categories within each area
    """
    number: int = field()
    name: str = field()
    area: Area = field(init=False)
