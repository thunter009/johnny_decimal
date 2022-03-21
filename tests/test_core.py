import shutil
from pathlib import Path

import pytest

from johnny_decimal.core import Area, Category, Input, Registry
from johnny_decimal.exceptions import AttributeNotDefined

TEST_ROOT = "tests/output"

@pytest.fixture(scope='module')
def file_system():
    yield file_system
    print('******TEARDOWN******')
    shutil.rmtree(TEST_ROOT)


class TestInput:
    """
    Tests for Input class
    """

    def test_load(self,
                  actual_input: Input,
                  expected_input: Input):
        actual = actual_input.load()
        assert actual == expected_input

class TestArea:
    """
    Tests for Area class
    """

    def test_root(self,
                  actual_area: Area):
        actual = actual_area.root
        assert actual == Path('.')

    def test_id(self,
                  actual_area: Area):
        """
        Test that id attributes is an empty string while defined outside of a registry
        """
        assert actual_area.id == ''

    def test_path(self,
                  actual_area: Area):
        """
        Test that path attributes should raise exception when trying to 
        access outside of registry
        """
        with pytest.raises(AttributeNotDefined, match=r'[.]*id[.]*'):
            actual_area.path

    def test_mkdir(self,
                  actual_area: Category):
        """
        Test that area object can't call mkdir because the ID attribute can only be defined
        in a registry object.
        """
        with pytest.raises(AttributeNotDefined, match=r'[.]*id[.]*'):
            actual_area.mkdir()

class TestCategory:
    """
    Tests for Category class
    """

    def test_id(self,
                actual_category: Category):
        """
        Test that id attributes is an empty string while defined outside of a registry
        """
        assert actual_category.id == ''

    def test_path(self,
                  actual_category: Category):
        """
        Test that path attributes should raise exception when trying to 
        access outside of registry
        """
        with pytest.raises(AttributeNotDefined, match=r'[.]*id[.]*'):
            actual_category.path

    def test_mkdir(self,
                  actual_category: Category):
        """
        Test that category object can't call mkdir because the ID attribute can only be defined
        in a registry object.
        """
        with pytest.raises(AttributeNotDefined, match=r'[.]*id[.]*'):
            actual_category.mkdir()

class TestReigstry:
    """
    Tests for Registry class
    """

    def test__detect_input_style(self, 
                                 actual_area_registry: Registry,
                                 actual_category_registry: Registry):

        assert actual_area_registry._detect_input_style() == 'areas'
        # assert actual_category_registry._detect_input_style() == 'categories'

    def test__get_index_generator(self, 
                                  actual_area_registry: Registry,
                                  actual_category_registry: Registry):

        pass

    def test_get_areas(self, 
                       actual_area_registry: Registry,
                       actual_category_registry: Registry):

        # expected_area_set = {
        #     Area(name='test-area-2'), 
        #     Area(name='test-area-1')
        # }
        # assert actual_area_registry.get_areas() == expected_area_set
        # assert actual_category_registry.get_areas() == expected_area_set
        pass

    def test_area_get_max_id_range(self, actual_area_registry: Registry):

        actual1 = actual_area_registry.areas[0].get_max_id_range()
        assert actual1 == 19

        actual2 = actual_area_registry.areas[1].get_max_id_range()
        assert actual2 == 29

    def test_area_get_max_id_range(self, actual_area_registry: Registry):

        actual1 = actual_area_registry.areas[0].get_min_id_range()
        assert actual1 == 10

        actual2 = actual_area_registry.areas[1].get_min_id_range()
        assert actual2 == 20

    def test_area_id(self, actual_area_registry: Registry):
        """
        Test that id attributes for input areas are defined as expected
        """
        assert actual_area_registry.areas[0].id == '10-19'
        assert actual_area_registry.areas[1].id == '20-29'

    def test_area_path(self, actual_area_registry: Registry):
        """
        Test that path attributes for input areas are defined as expected
        """
        root = actual_area_registry.areas[0].root
        assert actual_area_registry.areas[0].path == Path(f'{root}/10-19_test-area-1')
        assert actual_area_registry.areas[1].path == Path(f'{root}/20-29_test-area-2')

    def test_category_id(self, actual_category_registry: Registry):
        """
        Test that id attributes for input categories are defined as expected
        """
        assert actual_category_registry.categories[0].id == '10'
        assert actual_category_registry.categories[1].id == '21' #TODO: fix this error

    def test_category_path(self, actual_category_registry: Registry):
        """
        Test that path attributes for input categories are defined as expected
        """
        root = actual_category_registry.categories[0].area.root
        assert actual_category_registry.categories[0].path == Path(f'{root}/10-19_test-area-1/10_test-category-1')
        assert actual_category_registry.categories[1].path == Path(f'{root}/20-29_test-area-2/21_test-category-2')

    def test_area_mkdir(self, actual_area_registry: Registry, file_system):
        """
        Test that area object can call mkdir as expected
        """
        root = actual_area_registry.areas[0].root
        actual_area_registry.areas[0].mkdir()
        actual_area_registry.areas[1].mkdir()
        output1 = root / '10-19_test-area-1'
        output2 = root / '20-29_test-area-2'
        assert output1.exists()
        assert output2.exists()

    def test_category_mkdir(self, actual_category_registry: Registry, file_system):
        """
        Test that category object can call mkdir as expected
        """
        root = actual_category_registry.categories[0].area.root
        actual_category_registry.categories[0].mkdir()
        actual_category_registry.categories[1].mkdir()
        output1 = root / '10-19_test-area-1/10_test-category-1'
        output2 = root / '20-29_test-area-2/21_test-category-2'
        assert output1.exists()
        assert output2.exists()

    def test_init(self, 
                  actual_area_registry: Registry, 
                  actual_category_registry: Registry, 
                  file_system):
        """
        Test that area object can call mkdir as expected
        """
        root = actual_area_registry.areas[0].root
        actual_area_registry.init()
        actual_category_registry.init()
        output1 = root / '10-19_test-area-1/10_test-category-1'
        output2 = root / '20-29_test-area-2/21_test-category-2'
        assert output1.exists()
        assert output2.exists()
