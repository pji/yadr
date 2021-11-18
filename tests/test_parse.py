"""
test_parse
~~~~~~~~~~

Unit tests for the yadr.parse module.
"""
import unittest as ut

from yadr import parse as p
from yadr.model import Token


# Test cases.
class ParserTestCase(ut.TestCase):
    def parser_test(self, exp, tokens):
        """The standard Parse test case."""
        parser = p.Parser()
        act = parser.parse(tokens)
        self.assertEqual(exp, act)

    # Test basic operations.
    def test_addition(self):
        "Perform basic addition."
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '+'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_division(self):
        "Perform basic division."
        exp = 2
        tokens = (
            (Token.NUMBER, 4),
            (Token.OPERATOR, '/'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_division_rounds_down(self):
        "Division rounds down to the nearest integer (floor division)."
        exp = 2
        tokens = (
            (Token.NUMBER, 5),
            (Token.OPERATOR, '/'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_exponentiation(self):
        "Perform basic division."
        exp = 9
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '^'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_multiplication(self):
        "Perform basic multiplication."
        exp = 6
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '*'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    def test_subtraction(self):
        "Perform basic subtraction."
        exp = 1
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '-'),
            (Token.NUMBER, 2),
        )
        self.parser_test(exp, tokens)

    # Test order of precedence.
    def test_can_perform_multiple_operations(self):
        """The parser can parse statements with multiple operators."""
        exp = 9
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '+'),
            (Token.NUMBER, 2),
            (Token.OPERATOR, '+'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_exponentiation_before_multiplication(self):
        """Multiplication should occur before addition."""
        exp = 48
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '*'),
            (Token.NUMBER, 2),
            (Token.OPERATOR, '^'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_multiplication_before_addition(self):
        """Multiplication should occur before addition."""
        exp = 11
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '+'),
            (Token.NUMBER, 2),
            (Token.OPERATOR, '*'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    def test_parens_before_multiplication(self):
        """Parentheses should occur before multiplication."""
        exp = 18
        tokens = (
            (Token.NUMBER, 3),
            (Token.OPERATOR, '*'),
            (Token.OPEN_GROUP, '('),
            (Token.NUMBER, 2),
            (Token.OPERATOR, '+'),
            (Token.NUMBER, 4),
            (Token.CLOSE_GROUP, ')'),
        )
        self.parser_test(exp, tokens)
