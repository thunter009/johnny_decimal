import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, Iterable, List, MutableSet

import pytoml as toml

from johnny_decimal.exceptions import AttributeNotDefined, InvalidIDException
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


@dataclass()
class Base:
    name: str = field()
    id: str = default_field('', init=False)
    # TODO: replace with InitVar
    _path: Path = default_field(None, init=False, repr=False)


@dataclass
class Area(Base, DirectoryMixin):
    """
    Areas group categories together.

    id is defined when passed to a Registry object.
    """
    root: Path = default_field(Path('.'), repr=False)

    def __hash__(self):
        return hash(self.id)

    @property
    def path(self) -> Path:
        if self.id == '':
            raise AttributeNotDefined(
                'Define instance id before accessing path property')

        if not self._path:
            path = Path(self.root) / Path(f'{self.id}_{self.name}')

        return path

    def get_max_id_range(self) -> int:
        """
        Get's the maximum range of id's for a given Area id
        """
        if self.id == '':
            raise AttributeNotDefined(
                'Define id before computing max id range')
        return int(self.id[3:5])

    def get_min_id_range(self) -> int:
        if self.id == '':
            raise AttributeNotDefined(
                'Define id before computing max id range')
        return int(self.id[0:2])


@dataclass
class Category(Base, DirectoryMixin):
    """
    Categories within each area
    """
    area: Area = field(repr=False)

    def __hash__(self):
        return hash(self.id)

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

    def _detect_input_style(self) -> str:
        if self.areas:
            return 'areas'
        if self.categories:
            return 'categories'

    @staticmethod
    def _get_index_generator(style: str, iterable: Iterable) -> Generator:
        if style == 'categories':
            return range(0, len(iterable) + 1)
        elif style == 'areas':
            return range(1, len(iterable) + 1)

    def get_areas(self) -> MutableSet[Area]:
        """
        Returns set of all configured Area objects in this Reigstry
        """
        temp = [cat.area for cat in self.categories]
        return set(c for c in temp)

    def get_area_ids(self) -> List[Area]:
        """
        Takes a list areas and generates ids.
        """
        if not self.areas:
            areas = self.get_areas()
        else:
            areas = self.areas
        index = self._get_index_generator(style='areas', iterable=areas)
        for x in zip(areas, index):
            area = x[0]
            index_value = x[1]
            area.id = f'{index_value}0-{index_value}9'
        return areas

    def get_category_ids(self):
        categories = self.categories
        index = self._get_index_generator(style='categories', iterable=categories)
        for x in zip(categories, index):
            category = x[0]
            index_value = x[1]
            min_value = category.area.get_min_id_range()
            new_value = min_value + index_value

            if new_value > category.area.get_max_id_range():
                raise InvalidIDException()

            category.id = f'{new_value}'
        
        return categories

    def init(self):

        if self.style == 'ares':
            for area in self.areas:
                area.mkdir()

        if self.style == 'categories':
            for category in self.categories:
                category.mkdir()
