import pdb

import pytest

from johnny_decimal.core import Input


class TestInput:

    def test_load(self,
                  actual_input: Input,
                  expected_input: Input):
        actual = actual_input.load()
        assert actual == expected_input
