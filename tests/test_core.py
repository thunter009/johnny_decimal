import pdb
from pathlib import Path

import pytest

from johnny_decimal.core import Area, Category, Input, Registry


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

    # TODO: test for raising of AttributeNotDefined -- id/path attributes can only be set in a registry
    # def test_path(self,
    #               actual_area: Area,
    #               expected_area_path: str):
    #     actual = actual_area.path
    #     assert actual == expected_area_path

    # TODO: test for raising of AttributeNotDefined -- id/path attributes can only be set in a registry
    # def test_id(self,
    #               actual_area: Area,
    #               expected_area_id: int):
    #     breakpoint()
    #     # actual = actual_area.id
    #     assert actual == expected_area_id

    def test_root(self,
                  actual_area: Area,
                  expected_area_root: Path):
        actual = actual_area.root
        assert actual == expected_area_root

    # TODO: test that area can create directory for given path
    def test_mkdir(self,
                  actual_area: Area):
                #   expected_area_obj: Area):
        # actual = actual_area.path
        # assert actual == expected_area
        pass

class TestCategory:
    """
    Tests for Category class
    """

class TestReigstry:
    """
    Tests for Registry class
    """

