"""
test_maps
~~~~~~~~~

Unittests for the yadr.maps module.
"""
import unittest as ut

from tests.common import BaseTests
from yadr import maps
from yadr.model import MapToken


# Lexing test cases.
class KVDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.KV_DELIMITER
    allowed = [
        MapToken.NUMBER,
        MapToken.QUALIFIER_DELIMITER,
        MapToken.WHITESPACE,
    ]

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


class MapCloseTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.MAP_CLOSE
    allowed = []

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


class MapOpenTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.MAP_OPEN
    allowed = [
        MapToken.MAP_CLOSE,
        MapToken.QUALIFIER_DELIMITER,
        MapToken.WHITESPACE,
    ]

    def test_map_open(self):
        """Given a map open character, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
        )
        yadn = '{'
        self.lex_test(exp, yadn)


class NameDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.NAME_DELIMITER
    allowed = [
        MapToken.NUMBER,
        MapToken.WHITESPACE,
    ]

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


class NegativeSignTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.NEGATIVE_SIGN
    allowed = [
        MapToken.NUMBER,
    ]

    def test_negative_sign(self):
        """Given a negative sign, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.NUMBER, -1),
        )
        yadn = '{"spam"=-1'
        self.lex_test(exp, yadn)


class NumberTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.NUMBER
    allowed = [
        MapToken.KV_DELIMITER,
        MapToken.MAP_CLOSE,
        MapToken.PAIR_DELIMITER,
    ]

    def test_number(self):
        """Given a number, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.NUMBER, 1),
        )
        yadn = '{"spam"=1'
        self.lex_test(exp, yadn)

    def test_number_whitespace(self):
        """Given a number, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.NUMBER, 1),
        )
        yadn = '{"spam"= 1'
        self.lex_test(exp, yadn)


class PairDelimiterTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.NAME_DELIMITER
    allowed = [
        MapToken.NUMBER,
        MapToken.WHITESPACE,
    ]

    def test_kv_delimiter(self):
        """Given a pair delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.QUALIFIER, 'key'),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'value'),
            (MapToken.PAIR_DELIMITER, ','),
        )
        yadn = '{"spam"="key":"value",'
        self.lex_test(exp, yadn)

    def test_kv_delimiter_whitespace(self):
        """Given a pair delimiter, return the proper tokens."""
        exp = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'spam'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.QUALIFIER, 'key'),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'value'),
            (MapToken.PAIR_DELIMITER, ','),
        )
        yadn = '{"spam"="key":"value" ,'
        self.lex_test(exp, yadn)


class QualifierTestCase(BaseTests.MapLexTokenTestCase):
    token = MapToken.QUALIFIER
    allowed = [
        MapToken.MAP_CLOSE,
        MapToken.NAME_DELIMITER,
        MapToken.PAIR_DELIMITER,
        MapToken.WHITESPACE,
    ]

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


# Parsing test cases.
class ParseTestCase(ut.TestCase):
    def setUp(self):
        self.parser = maps.Parser()

    def tearDown(self):
        self.parser = None

    def parser_test(self, exp, tokens):
        act = self.parser.parse(tokens)
        self.assertEqual(exp, act)

    # Test cases.
    def test_parser(self):
        """A basic dice mapping can be parsed."""
        exp = (
            'name',
            {
                1: "none",
                2: "success",
                3: "success",
                4: "success success",
            }
        )
        tokens = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'name'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.NUMBER, 1),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'none'),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.NUMBER, 2),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'success'),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.NUMBER, 3),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'success'),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.NUMBER, 4),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.QUALIFIER, 'success success'),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.MAP_CLOSE, '}'),
        )
        self.parser_test(exp, tokens)

    def test_parser_with_numbers(self):
        """A basic dice mapping can be parsed."""
        exp = (
            'name',
            {
                1: -1,
                2: 0,
                3: 1,
            }
        )
        tokens = (
            (MapToken.MAP_OPEN, '{'),
            (MapToken.QUALIFIER, 'name'),
            (MapToken.NAME_DELIMITER, '='),
            (MapToken.NUMBER, 1),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.NUMBER, -1),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.NUMBER, 2),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.NUMBER, 0),
            (MapToken.PAIR_DELIMITER, ','),
            (MapToken.NUMBER, 3),
            (MapToken.KV_DELIMITER, ':'),
            (MapToken.NUMBER, 1),
            (MapToken.MAP_CLOSE, '}'),
        )
        self.parser_test(exp, tokens)
