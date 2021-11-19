"""
test_parse
~~~~~~~~~~

Unit tests for the yadr.parse module.
"""
import unittest as ut
from unittest.mock import patch

from yadr import parse as p
from yadr.model import Token
from yadr import operator as yo


# Test cases.
class ParseTestCase(ut.TestCase):
    def parser_test(self, exp, tokens):
        """The standard Parse test case."""
        act = p.parse(tokens)
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

    # Test dice operators.
    def test_die(self):
        """Roll a die."""
        yo._seed('spam')
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'd'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    def test_exploding_die(self):
        """Roll an exploding die."""
        yo._seed('spam')
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'd!'),
            (Token.NUMBER, 4),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        """Roll dice and keep the highest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 5
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dh'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    @patch('random.randint')
    def test_keep_low_die(self, mock_randint):
        """Roll dice and keep the lowest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = 1
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dl'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)

    # Test pool generation operators.
    @patch('random.randint')
    def test_dice_pool(self, mock_randint):
        """Roll dice and keep the highest."""
        mock_randint.side_effect = [1, 5, 3]
        exp = (1, 5, 3)
        tokens = (
            (Token.NUMBER, 3),
            (Token.DICE_OPERATOR, 'dp'),
            (Token.NUMBER, 6),
        )
        self.parser_test(exp, tokens)
    
    #Test pool operators.
    def test_pool_cap(self):
        """Cap the values in a pool at a given value."""
        exp = (5, 7, 1, 7)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pc'),
            (Token.NUMBER, 7),
        )
        self.parser_test(exp, tokens)
    
    def test_pool_floor(self):
        """Floor the values in a pool at a given value."""
        exp = (8, 8, 8, 9)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'pf'),
            (Token.NUMBER, 8),
        )
        self.parser_test(exp, tokens)
    
    def test_pool_keep_high(self):
        """Keep a number of highest values from the pool."""
        exp = (9, 8)
        tokens = (
            (Token.POOL, (5, 8, 1, 9)),
            (Token.POOL_OPERATOR, 'ph'),
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
