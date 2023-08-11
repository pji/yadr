"""
test_maps
~~~~~~~~~

Unittests for the yadr.maps module.
"""
from collections import namedtuple
from functools import partial

import pytest

from yadr import maps
from yadr import model as m
from yadr.model import Token


# Registration.
cases = {}


class reg:
    def __init__(self, key):
        self.key = key

    def __call__(self, fn):
        new = partial(fn, token=self.key)
        cases[self.key] = new
        return fn


# Common test case utilities.
YADN = namedtuple('YADN', 'yadn tokens')


def get_yadn(token):
    """Build a :class:`YADN` object for each valid symbol for the token."""
    # If a YADN object was passed, just yield it back.
    if isinstance(token, YADN):
        yield token

    # Otherwise get the symbols for the token type, build and then
    # yield the YADN object for each of the symbols.
    else:
        symbols = m.yadn_symbols_raw[token].split()
        for symbol in symbols:
            yadn = symbol
            value = symbol
            if token == m.Token.NUMBER:
                value = int(value)
            elif token == m.Token.BOOLEAN:
                value = True
                if symbol == 'F':
                    value = False
            yield YADN(yadn, ((token, value),))


# Build the test data for testing each type of token.
@reg(m.Token.KV_DELIMITER)
def build_kv_delimiter_cases(token):
    yadns = get_yadn(token)
    for yadn in yadns:
        yield YADN(f'{yadn.yadn}"spam"}}', (
            *yadn.tokens,
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.MAP_CLOSE, '}'),
        ))


@reg(m.Token.NEGATIVE_SIGN)
def build_negative_sign_cases(token):
    yield YADN('-2', ((m.Token.NUMBER, -2),))


@reg(m.Token.NAME_DELIMITER)
def build_name_delimiter_cases(token):
    yadns = get_yadn(token)
    for yadn in yadns:
        yield YADN(f'{yadn.yadn}2:"spam"}}', (
            *yadn.tokens,
            (m.Token.NUMBER, 2),
            (m.Token.KV_DELIMITER, ':'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.MAP_CLOSE, '}'),
        ))


@reg(m.Token.PAIR_DELIMITER)
def build_pair_delimiter_cases(token):
    yadns = get_yadn(token)
    for yadn in yadns:
        yield YADN(f'{yadn.yadn}2:"spam"}}', (
            *yadn.tokens,
            (m.Token.NUMBER, 2),
            (m.Token.KV_DELIMITER, ':'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.MAP_CLOSE, '}'),
        ))


@reg(m.Token.QUALIFIER)
@reg(m.Token.QUALIFIER_DELIMITER)
def build_qualifier_cases(token=None):
    yield YADN('"spam"', ((m.Token.QUALIFIER, 'spam'),))


@reg(m.Token.MAP_CLOSE)
@reg(m.Token.NUMBER)
def build_token_only_case(token):
    for yadn in get_yadn(token):
        yield yadn


# Core test code.
def allowed_test(symbol, before, after):
    """Test a token that is allowed to follow the given symbol."""
    expected = (
        *before.tokens,
        *symbol.tokens,
        *after.tokens,
    )

    lexer = maps.Lexer()
    yadns = [
        f'{before.yadn}{symbol.yadn}{after.yadn}',
        f'{before.yadn}{symbol.yadn} {after.yadn}',
    ]

    for yadn in yadns:
        actual = lexer.lex(yadn)
        try:
            assert actual == expected
        except AssertionError as ex:
            cls = ex.__class__
            msg = f'{ex}\n{yadn}'
            raise cls(msg)


def disallowed_test(symbol, before, after):
    """Test a token that is not allowed to follow the given symbol"""
    expected = ValueError

    lexer = maps.Lexer()
    yadns = [
        f'{before.yadn}{symbol.yadn}{after.yadn}',
        f'{before.yadn}{symbol.yadn} {after.yadn}',
    ]

    for yadn in yadns:
        try:
            pytest.raises(expected, lexer.lex, yadn)
        except BaseException as ex:
            cls = ex.__class__
            msg = f'{ex}\n{yadn}'
            raise cls(msg)


def lexer_test(token, before, alloweds):
    """Common test of :meth:`Lexer.lex` for a token."""
    # Build list of disallowed tokens.
    disalloweds = [token for token in cases if token not in alloweds]

    # Since AS_OPERATORS contain -, the NEGATIVE_SIGN will be allowed
    # if AS_OPERATORS are allowed.
    if m.Token.AS_OPERATOR in alloweds:
        disalloweds = [
            token for token in disalloweds
            if token != m.Token.NEGATIVE_SIGN
        ]

    # Since AS_OPERATORS contain -, that AS_OPERATOR is allowed when
    # NEGATIVE_SIGN is allowed. This change does prevent us from testing
    # whether + is allowed, though.
    if m.Token.NEGATIVE_SIGN in alloweds:
        disalloweds = [
            token for token in disalloweds
            if token != m.Token.AS_OPERATOR
        ]

    # NUMBERS next to NUMBERS aren't separate tokens.
    if (
        token == m.Token.NUMBER
        or (
            isinstance(token, YADN)
            and token.tokens
            and token.tokens[0][0] == m.Token.NUMBER
        )
    ):
        disalloweds = [
            token for token in disalloweds
            if token != m.Token.NUMBER
        ]

    # Test each of the possible symbols for the token.
    symbols = get_yadn(token)
    for symbol in symbols:

        # Test alloweds.
        for key in alloweds:
            afters = cases[key]()
            for after in afters:
                allowed_test(symbol, before, after)

        # Test disalloweds.
        for key in disalloweds:
            afters = cases[key]()
            for after in afters:
                disallowed_test(symbol, before, after)


# Symbol unit tests.
def test_kv_delimiter():
    """Given a key-value delimiter, return the proper tokens."""
    token = Token.KV_DELIMITER
    before = YADN(
        '{"spam"=1',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.NAME_DELIMITER, '='),
            (m.Token.NUMBER, 1),
        )
    )
    alloweds = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
        Token.QUALIFIER,
        Token.QUALIFIER_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_map_close():
    """Given a map close character, return the proper tokens."""
    token = Token.MAP_CLOSE
    before = YADN(
        '{"spam"=1:"eggs"',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.NAME_DELIMITER, '='),
            (m.Token.NUMBER, 1),
            (m.Token.KV_DELIMITER, ':'),
            (m.Token.QUALIFIER, 'eggs'),
        )
    )
    alloweds = []
    lexer_test(token, before, alloweds)


def test_map_open():
    """Given a map open character, return the proper tokens."""
    token = Token.MAP_OPEN
    before = YADN('', ())
    alloweds = [
        Token.MAP_CLOSE,
        Token.QUALIFIER,
        Token.QUALIFIER_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_name_delimiter():
    """Given a name delimiter character, return the proper tokens."""
    token = Token.NAME_DELIMITER
    before = YADN(
        '{"spam"',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
        )
    )
    alloweds = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
    ]
    lexer_test(token, before, alloweds)


def test_number():
    """Given a number, return the proper tokens."""
    token = m.Token.NUMBER
    before = YADN(
        '{"spam"=',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.NAME_DELIMITER, '='),
        )
    )
    alloweds = [
        Token.KV_DELIMITER,
        Token.MAP_CLOSE,
        Token.PAIR_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_number_with_negative_sign():
    """Given a negative sign character, return the proper tokens."""
    token = YADN('-2', ((m.Token.NUMBER, -2),))
    before = YADN(
        '{"spam"=',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.NAME_DELIMITER, '='),
        )
    )
    alloweds = [
        Token.KV_DELIMITER,
        Token.MAP_CLOSE,
        Token.PAIR_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_pair_delimiter():
    """Given a pair delimiter, return the proper tokens."""
    token = m.Token.PAIR_DELIMITER
    before = YADN(
        '{"spam"=1:"eggs"',
        (
            (m.Token.MAP_OPEN, '{'),
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.NAME_DELIMITER, '='),
            (m.Token.NUMBER, 1),
            (m.Token.KV_DELIMITER, ':'),
            (m.Token.QUALIFIER, 'eggs'),
        )
    )
    alloweds = [
        Token.NEGATIVE_SIGN,
        Token.NUMBER,
    ]
    lexer_test(token, before, alloweds)


def test_qualifier():
    """Given a qualifier, return the proper tokens."""
    token = m.Token.QUALIFIER
    before = YADN('{', ((m.Token.MAP_OPEN, '{'),))
    alloweds = [
        Token.MAP_CLOSE,
        Token.NAME_DELIMITER,
        Token.PAIR_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


# Parsing test cases.
def test_parser():
    """A basic dice mapping can be parsed."""
    tokens = (
        (Token.MAP_OPEN, '{'),
        (Token.QUALIFIER, 'name'),
        (Token.NAME_DELIMITER, '='),
        (Token.NUMBER, 1),
        (Token.KV_DELIMITER, ':'),
        (Token.QUALIFIER, 'none'),
        (Token.PAIR_DELIMITER, ','),
        (Token.NUMBER, 2),
        (Token.KV_DELIMITER, ':'),
        (Token.QUALIFIER, 'success'),
        (Token.PAIR_DELIMITER, ','),
        (Token.NUMBER, 3),
        (Token.KV_DELIMITER, ':'),
        (Token.QUALIFIER, 'success'),
        (Token.PAIR_DELIMITER, ','),
        (Token.NUMBER, 4),
        (Token.KV_DELIMITER, ':'),
        (Token.QUALIFIER, 'success success'),
        (Token.PAIR_DELIMITER, ','),
        (Token.MAP_CLOSE, '}'),
    )
    parser = maps.Parser()
    assert parser.parse(tokens) == (
        'name',
        {
            1: "none",
            2: "success",
            3: "success",
            4: "success success",
        }
    )


def test_parser_with_numbers():
    """A basic dice mapping can be parsed."""
    tokens = (
        (Token.MAP_OPEN, '{'),
        (Token.QUALIFIER, 'name'),
        (Token.NAME_DELIMITER, '='),
        (Token.NUMBER, 1),
        (Token.KV_DELIMITER, ':'),
        (Token.NUMBER, -1),
        (Token.PAIR_DELIMITER, ','),
        (Token.NUMBER, 2),
        (Token.KV_DELIMITER, ':'),
        (Token.NUMBER, 0),
        (Token.PAIR_DELIMITER, ','),
        (Token.NUMBER, 3),
        (Token.KV_DELIMITER, ':'),
        (Token.NUMBER, 1),
        (Token.MAP_CLOSE, '}'),
    )
    parser = maps.Parser()
    assert parser.parse(tokens) == (
        'name',
        {
            1: -1,
            2: 0,
            3: 1,
        }
    )
