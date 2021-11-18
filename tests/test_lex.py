"""
test_lex
~~~~~~~~

Unit tests for the dice notation lexer.
"""
import unittest as ut

from yadr import lex


# Test cases.
class LexTestCase(ut.TestCase):
    def lex_test(self, exp, data):
        """Run a basic test on yadr.lex.lex."""
        lexer = lex.Lexer()
        act = lexer.lex(data)
        self.assertTupleEqual(exp, act)

    def test_basic_addition(self):
        """Given a basic addition equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 15),
            (lex.Token.OPERATOR, '+'),
            (lex.Token.NUMBER, 3),
        )
        data = '15+3'
        self.lex_test(exp, data)

    def test_basic_addition_with_spaces(self):
        """Given a basic addition equation containing whitespace,
        return the tokens that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 15),
            (lex.Token.OPERATOR, '+'),
            (lex.Token.NUMBER, 3),
        )
        data = ' 15 + 3 '
        self.lex_test(exp, data)

    def test_basic_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '20d10'
        self.lex_test(exp, data)

    def test_basic_exploding_die(self):
        """Given a basic exploding die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'd!'),
            (lex.Token.NUMBER, 10),
        )
        data = '20d!10'
        self.lex_test(exp, data)

    def test_basic_keep_high_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dh'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dh10'
        self.lex_test(exp, data)

    def test_basic_keep_low_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dl'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dl10'
        self.lex_test(exp, data)

    def test_basic_division(self):
        """Given a basic division equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.OPERATOR, '/'),
            (lex.Token.NUMBER, 10),
        )
        data = '20/10'
        self.lex_test(exp, data)

    def test_basic_exponentiation(self):
        """Given a basic exponentiation equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.OPERATOR, '^'),
            (lex.Token.NUMBER, 10),
        )
        data = '20^10'
        self.lex_test(exp, data)

    def test_basic_multiplication(self):
        """Given a basic multiplication equation, return the tokens
        that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
        )
        data = '2*10'
        self.lex_test(exp, data)

    def test_basic_subtraction(self):
        """Given a basic subtraction equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 200),
            (lex.Token.OPERATOR, '-'),
            (lex.Token.NUMBER, 10),
        )
        data = '200-10'
        self.lex_test(exp, data)

    def test_parentheses(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.OPEN_GROUP, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.CLOSE_GROUP, ')'),
            (lex.Token.OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '(32-5)*21'
        self.lex_test(exp, data)

    def test_parentheses_with_whitespace(self):
        """Given a statement containing parenthesis and whitespace,
        return the tokenized equation.
        """
        exp = (
            (lex.Token.OPEN_GROUP, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.CLOSE_GROUP, ')'),
            (lex.Token.OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '( 32 - 5 ) * 21'
        self.lex_test(exp, data)

    def test_negative_number(self):
        """Tokenize a number that starts with a negative sign."""
        exp = ((lex.Token.NUMBER, -24),)
        data = '-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3+-24'
        self.lex_test(exp, data)

    def test_negative_number_after_operator_with_whitespace(self):
        """Tokenize a number that starts with a negative sign."""
        exp = (
            (lex.Token.NUMBER, 3),
            (lex.Token.OPERATOR, '+'),
            (lex.Token.NUMBER, -24),
        )
        data = '3 + -24'
        self.lex_test(exp, data)
