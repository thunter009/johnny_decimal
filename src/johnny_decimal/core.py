import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pytoml as toml

from johnny_decimal.exceptions import AttributeNotDefined, NotDefined
from johnny_decimal.mixins import DirectoryMixin
from johnny_decimal.utils import default_field


@dataclass
class Input:
    """
    Handles user input
    """
    _path: str = field()

    def load(self):
        path = Path(self._path)
        with open(str(path.resolve()), 'rb') as f:
            config = toml.load(f)
        return config


@dataclass
class Base:
    name: str = field()
    id: str = default_field('', init=False)
    # TODO: replace with InitVar
    _path: Path = default_field(None, init=False, repr=False)


@dataclass
class Area(Base, DirectoryMixin):
    """
    Areas group categories together.

    id is defined when passed to an AreaRegistry object.
    """
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
class Category(Base):
    """
    Categories within each area
    """
    area: Area = field(repr=False)

    @property
    def path(self) -> Path:
        if self.id == '':
            raise AttributeNotDefined(
                'Define instance id before accessing path property')

        if not self._path:
            root = self.area.path
            path = Path(root) / Path(f'{self.id}_{self.name}')

        return path


@dataclass
class Registry:
    """
    Generic Registry for collecting individual Area/Category objects and
    performing operations on the collected Registry object, assigning
    them id's and full file paths
    """
    areas: List[Area] = default_field(None)
    categories: List[Category] = default_field(None)
    style: str = default_field(None, init=False)

    def __post_init__(self):
        self.style = self._detect_input_style()
        if self.style == 'areas':
            self.areas = self.get_area_ids()
        elif self.style == 'categories':
            self.areas = self.get_area_ids()
            self.categories = self.get_category_ids()

    def __getitem__(self, index):
        if self.style == 'areas':
            return self.areas[index]
        if self.style == 'categories':
            return self.categories[index]

    def _detect_input_style(self):
        if self.areas:
            return 'areas'
        if self.categories:
            return 'categories'

    @staticmethod
    def _get_index_generator(iterable):
        return range(1, len(iterable) + 1)

    def get_areas(self):
        """
        Returns set of all configured Area objects in this Reigstry
        """
        temp = [cat.area for cat in self.categories]
        return (c for c in temp)

    def get_area_ids(self, areas: List[Area]) -> List[Area]:
        """
        Takes a list of 
        """
        if not self.areas:
            areas = self.get_areas()
        else:
            areas = self.areas
        index = self._get_index_generator(areas)
        for x in zip(areas, index):
            area = x[0]
            index_value = x[1]
            area.id = f'{index_value}0-{index_value}9'
        return areas

    def get_category_ids(self):
        categories = self.categories
        index = self._get_index_generator(categories)
        for x in zip(categories, index):
            category = x[0]
            index_value = x[1]
            category.id = f'{index_value}0-{index_value}9'
        return categories

    def init(self):
        for area in self.areas:
            area.mkdir()
