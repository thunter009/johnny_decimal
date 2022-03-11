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
