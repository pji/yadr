"""
test_maps
~~~~~~~~~

Unittests for the yadr.maps module.
"""
import unittest as ut

from tests.common import BaseTests
from yadr import maps
from yadr.model import MapToken


# Test cases.
class MapCloseTestCase(BaseTests.MapLexTestCase):
    def test_map_close(self):
        """Given a map close character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.MAP_CLOSE, '}'),
        )
        yadn = '{}'
        self.lex_test(exp, yadn)


class MapOpenTestCase(BaseTests.MapLexTestCase):
    def test_map_open(self):
        """Given a map open character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
        )
        yadn = '{'
        self.lex_test(exp, yadn)


class QualifierTestCase(BaseTests.MapLexTestCase):
    def test_qualifier(self):
        """Given a qualifier, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.MAP_CLOSE, '}'),
        )
        yadn = '{"spam"}'
        self.lex_test(exp, yadn)
