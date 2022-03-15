from pathlib import Path

import pytest


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
    return Input('tests/index.toml')

@pytest.fixture
def expected_area_id():
    return 123

@pytest.fixture
def expected_area_path():
    return 'tests/'

@pytest.fixture
def expected_area_root():
    return Path('.')

@pytest.fixture
def actual_area():
    from johnny_decimal.core import Area
    return Area('test-area')
