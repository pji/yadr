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
class KVDelimiterTestCase(BaseTests.MapLexTestCase):
    def test_kv_delimiter(self):
        """Given a key-value delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.QUALIFIER, 'key'),
            (MapToken.KV_DELIMITER, ':'),
        )
        yadn = '{"spam"="key":'
        self.lex_test(exp, yadn)

    def test_kv_delimiter_whitespace(self):
        """Given a key-value delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.QUALIFIER, 'key'),
            (MapToken.KV_DELIMITER, ':'),
        )
        yadn = '{"spam"="key" :'
        self.lex_test(exp, yadn)


class MapCloseTestCase(BaseTests.MapLexTestCase):
    def test_map_close(self):
        """Given a map close character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.MAP_CLOSE, '}'),
        )
        yadn = '{}'
        self.lex_test(exp, yadn)

    def test_map_close_whitespace(self):
        """Given a map close character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.MAP_CLOSE, '}'),
        )
        yadn = '{ }'
        self.lex_test(exp, yadn)


class MapOpenTestCase(BaseTests.MapLexTestCase):
    def test_map_open(self):
        """Given a map open character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
        )
        yadn = '{'
        self.lex_test(exp, yadn)


class NameDelimiterTestCase(BaseTests.MapLexTestCase):
    def test_name_delimiter(self):
        """Given a name delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '=')
        )
        yadn = '{"spam"='
        self.lex_test(exp, yadn)

    def test_name_delimiter_whitespace(self):
        """Given a name delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '=')
        )
        yadn = '{"spam" ='
        self.lex_test(exp, yadn)


class QualifierTestCase(BaseTests.MapLexTestCase):
    def test_qualifier(self):
        """Given a qualifier, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam')
        )
        yadn = '{"spam"'
        self.lex_test(exp, yadn)

    def test_qualifier_whitespace(self):
        """Given a qualifier, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam')
        )
        yadn = '{ "spam"'
        self.lex_test(exp, yadn)
