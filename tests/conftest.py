
from pathlib import Path
from typing import Tuple

import pytest

TEST_ROOT = "tests/output"


@pytest.fixture
def expected_input():
    return {
        'area': [
            {
                'category': [
                    {'name': 'red delicious'}, 
                    {'name': 'granny smith'}
                ], 
                'name': 'apple'
            }, 
            {
                'name': 'banana'
            }, 
            {
                'name': 'pear'
            }
        ]
    }

@pytest.fixture
def actual_input():
    from johnny_decimal.core import Input
    return Input('tests/data/index.toml')

## actual area & categories

@pytest.fixture
def actual_area():
    from johnny_decimal.core import Area
    return Area('test-area')

@pytest.fixture
def actual_category():
    from johnny_decimal.core import Area, Category
    area = Area('test-area')
    return Category(name='test-category', area=area)

## actual registry object

@pytest.fixture
def actual_area_registry():
    from johnny_decimal.core import Area, Category, Registry
    areas = [
        Area('test-area-1', root=Path(TEST_ROOT)),
        Area('test-area-2', root=Path(TEST_ROOT)),
    ]
    return Registry(areas=areas)

@pytest.fixture
def actual_category_registry():
    from johnny_decimal.core import Area, Category, Registry
    areas = [
        Area('test-area-1', root=Path(TEST_ROOT)),
        Area('test-area-2', root=Path(TEST_ROOT)),
    ]
    categories = [
        Category(name='test-category-1', area=areas[0]),
        Category(name='test-category-2', area=areas[1]),
    ]
    return Registry(categories=categories)
