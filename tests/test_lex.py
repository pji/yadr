"""
test_lex
~~~~~~~~

Unit tests for the dice notation lexer.
"""
from collections import namedtuple
from functools import partial
import unittest as ut

import pytest

from tests.common import BaseTests
from yadr import lex
from yadr import model as m


# Registration.
cases = {}


class reg:
    def __init__(self, key):
        self.key = key

    def __call__(self, fn):
        new = partial(fn, token=self.key)
        cases[self.key] = new
        return new


class reg_case:
    def __init__(self, key):
        self.key = key

    def __call__(self, fn):
        cases[self.key] = fn
        return fn


# Common test case utilities.
YADN = namedtuple('YADN', 'yadn tokens')


def get_yadn(token):
    if isinstance(token, YADN):
        return token
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
@reg(m.Token.AS_OPERATOR)
@reg(m.Token.COMPARISON_OPERATOR)
@reg(m.Token.DICE_OPERATOR)
@reg(m.Token.EX_OPERATOR)
@reg(m.Token.MD_OPERATOR)
@reg(m.Token.POOL_OPERATOR)
@reg(m.Token.POOL_GEN_OPERATOR)
@reg(m.Token.ROLL_DELIMITER)
def build_standard_cases(token):
    symbols = m.yadn_symbols_raw[token].split()
    for symbol in symbols:
        yield YADN(f'{symbol}3', (
            (token, symbol),
            (m.Token.NUMBER, 3),
        ))


@reg_case(m.Token.BOOLEAN)
def build_boolean_cases():
    for yadn in get_yadn(m.Token.BOOLEAN):
        yield yadn


@reg_case(m.Token.CHOICE_OPERATOR)
def build_choice_operator_cases():
    yadns = get_yadn(m.Token.CHOICE_OPERATOR)
    for yadn in yadns:
        yield YADN(f'{yadn.yadn}"spam":"eggs"', (
            *yadn.tokens,
            (m.Token.QUALIFIER, 'spam'),
            (m.Token.OPTIONS_OPERATOR, ':'),
            (m.Token.QUALIFIER, 'eggs'),
        ))


@reg_case(m.Token.GROUP_OPEN)
def build_group_cases():
    yield YADN('(3+3)', (
        (m.Token.GROUP_OPEN, '('),
        (m.Token.NUMBER, 3),
        (m.Token.AS_OPERATOR, '+'),
        (m.Token.NUMBER, 3),
        (m.Token.GROUP_CLOSE, ')'),
    ))


@reg_case(m.Token.GROUP_CLOSE)
def build_group_cases():
    yield YADN(')', ((m.Token.GROUP_CLOSE, ')'),))


@reg_case(m.Token.MAPPING_OPERATOR)
def build_mapping_operator_cases():
    for yadn in build_qualifier_cases():
        yield YADN(f'm{yadn.yadn}', (
            (m.Token.MAPPING_OPERATOR, 'm'),
            *yadn.tokens
        ))


@reg_case(m.Token.MAP)
@reg_case(m.Token.MAP_OPEN)
def build_map_cases():
    yield YADN('{"spam"=1:"win",2:"lose"}', ((m.Token.MAP, ('spam', {
        1: 'win',
        2: 'lose',
    })),))


@reg_case(m.Token.NEGATIVE_SIGN)
def build_negative_sign_cases():
    yield YADN('-2', ((m.Token.NUMBER, -2),))


@reg_case(m.Token.NUMBER)
def build_number_cases():
    symbols = m.yadn_symbols_raw[m.Token.NUMBER].split()
    for symbol in symbols:
        yield YADN(symbol, ((m.Token.NUMBER, int(symbol)),))


@reg_case(m.Token.OPTIONS_OPERATOR)
def build_options_operator_cases():
    yield YADN(':"spam"', (
        (m.Token.OPTIONS_OPERATOR, ':'),
        (m.Token.QUALIFIER, 'spam'),
    ))


@reg_case(m.Token.POOL)
@reg_case(m.Token.POOL_OPEN)
def build_pool_cases():
    yield YADN('[3,3]', ((m.Token.POOL, (3, 3)),))


@reg_case(m.Token.QUALIFIER)
@reg_case(m.Token.QUALIFIER_DELIMITER)
def build_qualifier_cases():
    yadns = [
        YADN('"spam"', ((m.Token.QUALIFIER, 'spam'),)),
    ]
    for yadn in yadns:
        yield yadn


@reg_case(m.Token.U_POOL_DEGEN_OPERATOR)
def build_u_pool_degeneration_operator_cases():
    symbols = m.yadn_symbols_raw[m.Token.U_POOL_DEGEN_OPERATOR].split()
    for symbol in symbols:
        yadn = f'{symbol}[3, 3]'
        yield YADN(yadn, (
            (m.Token.U_POOL_DEGEN_OPERATOR, symbol),
            (m.Token.POOL, (3, 3)),
        ))


# Core test code.
def allowed_test(symbol, before, after):
    expected = (
        *before.tokens,
        *symbol.tokens,
        *after.tokens,
    )

    lexer = lex.Lexer()

    # Test without whitespace.
    yadn = f'{before.yadn}{symbol.yadn}{after.yadn}'
    actual = lexer.lex(yadn)
    assert actual == expected

    # Test with whitespace.
    yadn = f'{before.yadn}{symbol.yadn} {after.yadn}'
    actual = lexer.lex(yadn)
    assert actual == expected


def disallowed_test(symbol, before, after):
    expected = ValueError

    lexer = lex.Lexer()

    # Test without whitespace.
    yadn = f'{before.yadn}{symbol.yadn}{after.yadn}'
    pytest.raises(expected, lexer.lex, yadn)

    # Test with whitespace.
    yadn = f'{before.yadn}{symbol.yadn} {after.yadn}'
    pytest.raises(expected, lexer.lex, yadn)


def lexer_test(token, before, alloweds):
    """Common test of :meth:`Lexer.lex` for a token."""
    # Build list of disallowed tokens.
    disalloweds = [token for token in cases if token not in alloweds]

    # Since AS_OPERATORS contain -, the NEGATIVE_SIGN will be allowed
    # if AS_OPERATORS is allowed.
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
    if token == m.Token.NUMBER:
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
def test_as_operator():
    """Given an addition or subtraction operator, return the correct
    tokens for the YADN.
    """
    token = m.Token.AS_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_boolean():
    """Given an addition or subtraction operator, return the correct
    tokens for the YADN.
    """
    token = m.Token.BOOLEAN
    before = YADN('', ())
    alloweds = [
        m.Token.CHOICE_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_choice_operator():
    """Given a choice, return the correct tokens for the YADN.
    """
    token = m.Token.CHOICE_OPERATOR
    before = YADN('T', ((m.Token.BOOLEAN, True),))
    alloweds = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_comparison_operator():
    """Given a comparison operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.COMPARISON_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_dice_operator():
    """Given a comparison operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.DICE_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_ex_operator():
    """Given a exponentiation operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.EX_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_group():
    """Given a group close, return the correct tokens for the YADN."""
    token = m.Token.GROUP_CLOSE
    before = YADN('(3', (
        (m.Token.GROUP_OPEN, '('),
        (m.Token.NUMBER, 3),
    ))
    alloweds = [
        m.Token.AS_OPERATOR,
        m.Token.MD_OPERATOR,
        m.Token.EX_OPERATOR,
        m.Token.DICE_OPERATOR,
        m.Token.GROUP_CLOSE,
        m.Token.POOL_OPERATOR,
        m.Token.ROLL_DELIMITER,
        m.Token.POOL_GEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_group_open():
    """Given a group open, return the correct tokens for the YADN."""
    token = m.Token.GROUP_OPEN
    before = YADN('', ())
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_map():
    """Given a map, return the correct tokens for the YADN."""
    token = YADN(
        '{"name"=1:"none",2:"success",3:"success",4:"success success"}',
        ((m.Token.MAP, ('name', {
            1: "none",
            2: "success",
            3: "success",
            4: "success success",
        })),)
    )
    before = YADN('', ())
    alloweds = [
        m.Token.ROLL_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_mapping_operator():
    """Given a mapping operator, return the correct tokens for the YADN."""
    token = m.Token.MAPPING_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_number():
    """Given a number, return the correct tokens for the YADN."""
    token = m.Token.NUMBER
    before = YADN('', ())
    alloweds = [
        m.Token.AS_OPERATOR,
        m.Token.COMPARISON_OPERATOR,
        m.Token.EX_OPERATOR,
        m.Token.DICE_OPERATOR,
        m.Token.GROUP_CLOSE,
        m.Token.MAPPING_OPERATOR,
        m.Token.MD_OPERATOR,
        m.Token.POOL_GEN_OPERATOR,
        m.Token.ROLL_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_number_multiple_digits():
    """Given a number with multiple digits, return the correct tokens
    for the YADN.
    """
    token = YADN('34', ((m.Token.NUMBER, 34)))
    before = YADN('', ())
    alloweds = [
        m.Token.AS_OPERATOR,
        m.Token.COMPARISON_OPERATOR,
        m.Token.EX_OPERATOR,
        m.Token.DICE_OPERATOR,
        m.Token.GROUP_CLOSE,
        m.Token.MAPPING_OPERATOR,
        m.Token.MD_OPERATOR,
        m.Token.POOL_GEN_OPERATOR,
        m.Token.ROLL_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_options_operator():
    """Given a options operator, return the correct tokens for the YADN."""
    token = m.Token.OPTIONS_OPERATOR
    before = YADN('"spam"', ((m.Token.QUALIFIER, 'spam'),))
    alloweds = [
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_pool_degen_operator():
    """Given a pool degeneration operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.POOL_DEGEN_OPERATOR
    before = YADN('[3,3]', ((m.Token.POOL, (3, 3)),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_pool_gen_operator():
    """Given a pool generation operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.POOL_GEN_OPERATOR
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_pool_operator():
    """Given a pool operator, return the correct tokens for
    the YADN.
    """
    token = m.Token.POOL_OPERATOR
    before = YADN('[3,3]', ((m.Token.POOL, (3, 3)),))
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_pool():
    """Given a pool, return the correct tokens for the YADN."""
    token = YADN('[3,3]', ((m.Token.POOL, (3, 3)),))
    before = YADN('', ())
    alloweds = [
        m.Token.GROUP_CLOSE,
        m.Token.POOL_OPERATOR,
        m.Token.POOL_DEGEN_OPERATOR,
        m.Token.ROLL_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_qualifier():
    """Given a qualifier, return the correct tokens for the YADN."""
    token = YADN('"spam"', ((m.Token.QUALIFIER, 'spam'),))
    before = YADN('', ())
    alloweds = [
        m.Token.OPTIONS_OPERATOR,
        m.Token.ROLL_DELIMITER,
    ]
    lexer_test(token, before, alloweds)


def test_roll_delimiter():
    """Given a roll delimiter, return the correct tokens for the YADN."""
    token = m.Token.ROLL_DELIMITER
    before = YADN('3', ((m.Token.NUMBER, 3),))
    alloweds = [
        m.Token.BOOLEAN,
        m.Token.GROUP_OPEN,
        m.Token.MAP_OPEN,
        m.Token.MAP,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.QUALIFIER,
        m.Token.QUALIFIER_DELIMITER,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


def test_u_pool_degen_operator():
    """Given an unary pool degeneration operator, return the correct
    tokens for the YADN.
    """
    token = m.Token.U_POOL_DEGEN_OPERATOR
    before = YADN('', ())
    alloweds = [
        m.Token.GROUP_OPEN,
        m.Token.NEGATIVE_SIGN,
        m.Token.NUMBER,
        m.Token.POOL,
        m.Token.POOL_OPEN,
        m.Token.U_POOL_DEGEN_OPERATOR,
    ]
    lexer_test(token, before, alloweds)


# Roll test case.
class StartRollTestCase(BaseTests.LexTestCase):
    def test_operator_cannot_start_roll(self):
        """An operator cannot start an expression."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'Cannot start with \\+.'

        # Test data and state.
        data = '+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_start_roll_whitespace(self):
        """An operator cannot start an expression."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'Cannot start with \\+.'

        # Test data and state.
        data = ' +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)


# Order of operations test case.
class OrderOfOperationsTestCase(BaseTests.LexTestCase):
    def test_negative_number(self):
        """Tokenize a number that starts with a negative sign."""
        exp = ((lex.Token.NUMBER, -24),)
        data = '-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3+-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator_with_whitespace(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3 + -24'
        self.lex_test(exp, data)
