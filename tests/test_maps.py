"""
test_maps
~~~~~~~~~

Unittests for the yadr.maps module.
"""
import unittest as ut

from tests.common import BaseTests
from yadr import maps


# Test cases.
@ut.skip
class MapOpenTestCase(BaseTests.MapLexTestCase):
    def test_map_open(self):
        """Given a map open character, return the proper tokens."""
        exp = (
            (maps.Token.MAP_OPEN, '('),
        )
        yadn = '{'
        self.lex_test(exp, yadn)
