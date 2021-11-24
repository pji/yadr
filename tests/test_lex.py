"""
test_lex
~~~~~~~~

Unit tests for the dice notation lexer.
"""
import unittest as ut

from yadr import lex
from yadr import model as m


# Base test case.
class BasicOperatorTestCase(ut.TestCase):
    def setUp(self):
        self.lexer = lex.Lexer()

    def tearDown(self):
        self.lexer = None

    def lex_test(self, exp, data):
        """Run a basic test on yadr.lex.lex."""
        act = self.lexer.lex(data)
        self.assertTupleEqual(exp, act)


# Symbol test cases.
class BooleanTestCase(BasicOperatorTestCase):
    def test_boolean_true(self):
        """Lex a boolean."""
        exp = (
            (lex.Token.BOOLEAN, True),
        )
        data = 'T'
        self.lex_test(exp, data)

    def test_boolean_false(self):
        """Lex a boolean."""
        exp = (
            (lex.Token.BOOLEAN, True),
        )
        data = 'T'
        self.lex_test(exp, data)


class ChoiceTestCase(BasicOperatorTestCase):
    def test_choice(self):
        """Lex a choice operator."""
        exp = (
            (lex.Token.BOOLEAN, True),
            (lex.Token.CHOICE_OPERATOR, '?'),
            (lex.Token.QUALIFIER, 'spam'),
            (lex.Token.OPTIONS_OPERATOR, ':'),
            (lex.Token.QUALIFIER, 'eggs'),
        )
        data = 'T?"spam":"eggs"'
        self.lex_test(exp, data)


class ComparisonOperatorTestCase(BasicOperatorTestCase):
    def test_basic_equal(self):
        """Lex equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '=='),
            (lex.Token.NUMBER, 20),
        )
        data = '21==20'
        self.lex_test(exp, data)

    def test_basic_greater_than(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>'),
            (lex.Token.NUMBER, 20),
        )
        data = '21>20'
        self.lex_test(exp, data)

    def test_basic_greater_than_or_equal(self):
        """Lex greater than or equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>='),
            (lex.Token.NUMBER, 20),
        )
        data = '21>=20'
        self.lex_test(exp, data)

    def test_basic_greater_than_whitspace(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '>'),
            (lex.Token.NUMBER, 20),
        )
        data = '21 > 20'
        self.lex_test(exp, data)

    def test_basic_less_than(self):
        """Lex greater than."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '<'),
            (lex.Token.NUMBER, 20),
        )
        data = '21<20'
        self.lex_test(exp, data)

    def test_basic_less_than_or_equal(self):
        """Lex less than or equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '<='),
            (lex.Token.NUMBER, 20),
        )
        data = '21<=20'
        self.lex_test(exp, data)

    def test_basic_not_equal(self):
        """Lex not equal."""
        exp = (
            (lex.Token.NUMBER, 21),
            (lex.Token.COMPARISON_OPERATOR, '!='),
            (lex.Token.NUMBER, 20),
        )
        data = '21!=20'
        self.lex_test(exp, data)


class DiceOperatorTestCase(BasicOperatorTestCase):
    def test_basic_concat(self):
        """Given a basic concat equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dc'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dc10'
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

    def test_basic_wild_die(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dw'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dw10'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_group_can_follow_dice_operator(self):
        """Numbers can follow dice operators."""
        exp = (
            (lex.Token.NUMBER, 10),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '10d(10*10)'
        self.lex_test(exp, data)

    def test_group_can_follow_dice_operator_whitespace(self):
        """Numbers can follow dice operators."""
        exp = (
            (lex.Token.NUMBER, 10),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '10d (10*10)'
        self.lex_test(exp, data)

    def test_qualifier_cannot_follow_dice_operator(self):
        """Qualifiers cannot follow dice operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a dice operator.'

        # Test data and state.
        data = '3d"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_dice_operator_whitespace(self):
        """Qualifiers cannot follow dice operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a dice operator.'

        # Test data and state.
        data = '3d "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class GroupingOperatorTestCase(BasicOperatorTestCase):
    def test_parentheses(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '(32-5)*21'
        self.lex_test(exp, data)

    def test_parentheses_with_whitespace(self):
        """Given a statement containing parenthesis and whitespace,
        return the tokenized equation.
        """
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 32),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 5),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 21),
        )
        data = '( 32 - 5 ) * 21'
        self.lex_test(exp, data)

    # Allowed interior symbol.
    def test_operator_cannot_follow_group_open(self):
        """An operator cannot follow a group open."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow \\(.'

        # Test data and state.
        data = '(+2)'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_follow_group_open_whitespace(self):
        """An operator cannot follow a group open."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow \\(.'

        # Test data and state.
        data = '( +2)'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_unary_pool_degen_can_follow_group_open(self):
        """Unary pool degeneration operators can follow group open."""
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (1, 2, 3)),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '(S[1,2,3])'
        self.lex_test(exp, data)

    def test_unary_pool_degen_can_follow_group_open_whitespace(self):
        """Unary pool degeneration operators can follow group open."""
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (1, 2, 3)),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '( S[1,2,3])'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_dice_operator_can_follow_group(self):
        """Dice operators can follow groups."""
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '(10*10)d10'
        self.lex_test(exp, data)

    def test_dice_operator_can_follow_group_whitespace(self):
        """Dice operators can follow groups."""
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '(10*10) d10'
        self.lex_test(exp, data)

    def test_number_cannot_follow_group(self):
        """Numbers cannot follow groups."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '4 cannot follow a group.'

        # Test data and state.
        data = '(3+2) 4'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_qualifier_cannot_follow_group(self):
        """Qualifiers cannot follow groups."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a group.'

        # Test data and state.
        data = '(3d10+5)"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_group_whitespace(self):
        """Qualifiers cannot follow groups."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a group.'

        # Test data and state.
        data = '(3d10+5) "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_roll_delimiter_can_follow_group(self):
        """A roll delimiter can follow a close group delimiter."""
        exp = (
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 2),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 1),
            (lex.Token.GROUP_CLOSE, ')'),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '(2d10+1);5d10'
        self.lex_test(exp, data)


class NumberTestCase(BasicOperatorTestCase):
    # Allowed next symbol.
    def test_group_cannot_follow_number(self):
        """Groups cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\( cannot follow a number.'

        # Test data and state.
        data = '3(3+2)'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_group_cannot_follow_number_after_whitespace(self):
        """Groups cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\( cannot follow a number.'

        # Test data and state.
        data = '3 (3+2)'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_number_cannot_follow_number(self):
        """Numbers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '4 cannot follow a number.'

        # Test data and state.
        data = '3 4'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_pool_degen_operator_can_follow_number(self):
        """Dice operators can follow groups."""
        exp = (
            (lex.Token.NUMBER, 5),
            (lex.Token.POOL_GEN_OPERATOR, 'g'),
            (lex.Token.NUMBER, 6),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.NUMBER, 7),
        )
        data = '5g6ns7'
        self.lex_test(exp, data)

    def test_pool_degen_operator_can_follow_number_whitespace(self):
        """Dice operators can follow groups."""
        exp = (
            (lex.Token.NUMBER, 5),
            (lex.Token.POOL_GEN_OPERATOR, 'g'),
            (lex.Token.NUMBER, 6),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.NUMBER, 7),
        )
        data = '5g6 ns7'
        self.lex_test(exp, data)

    def test_qualifier_cannot_follow_number(self):
        """Qualifiers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a number.'

        # Test data and state.
        data = '5"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_number_whitespace(self):
        """Qualifiers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a number.'

        # Test data and state.
        data = '5 "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class OperatorTestCase(BasicOperatorTestCase):
    def test_basic_addition(self):
        """Given a basic addition equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 15),
            (lex.Token.AS_OPERATOR, '+'),
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
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 3),
        )
        data = ' 15 + 3 '
        self.lex_test(exp, data)

    def test_basic_division(self):
        """Given a basic division equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.MD_OPERATOR, '/'),
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

    def test_basic_modulo(self):
        """Given a basic modulo equation, return the tokens
        that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.MD_OPERATOR, '%'),
            (lex.Token.NUMBER, 10),
        )
        data = '2%10'
        self.lex_test(exp, data)

    def test_basic_multiplication(self):
        """Given a basic multiplication equation, return the tokens
        that represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.MD_OPERATOR, '*'),
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
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.NUMBER, 10),
        )
        data = '200-10'
        self.lex_test(exp, data)

    # Allowed next operator.
    def test_group_can_follow_operator(self):
        """Numbers can follow operators."""
        exp = (
            (lex.Token.NUMBER, 10),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '10+(10*10)'
        self.lex_test(exp, data)

    def test_group_can_follow_operator_whitespace(self):
        """Numbers can follow operators."""
        exp = (
            (lex.Token.NUMBER, 10),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 10),
            (lex.Token.MD_OPERATOR, '*'),
            (lex.Token.NUMBER, 10),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '10+ (10*10)'
        self.lex_test(exp, data)

    def test_operator_cannot_follow_operator(self):
        """And operator cannot be followed by an operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow an operator.'

        # Test data and state.
        data = '3-+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_follow_operator_whitespace(self):
        """And operator cannot be followed by an operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow an operator.'

        # Test data and state.
        data = '3- +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_pool_cannot_follow_operator(self):
        """A pool cannot follow a operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\[ cannot follow an operator.'

        # Test data and state.
        data = '3+[2,3]'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_pool_cannot_follow_operator_whitespace(self):
        """A pool cannot follow a operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\[ cannot follow an operator.'

        # Test data and state.
        data = '3+ [2,3]'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_unary_pool_degen_can_follow_operator(self):
        """Subtraction can be followed by a unary pool degeneration
        operator.
        """
        exp = (
            (lex.Token.NUMBER, 200),
            (lex.Token.AS_OPERATOR, '-'),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (2, 3, 4)),
        )
        data = '200-S[2,3,4]'
        self.lex_test(exp, data)

    def test_qualifier_cannot_follow_operator(self):
        """Qualifiers cannot follow operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow an operator.'

        # Test data and state.
        data = '5+"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_operator_whitespace(self):
        """Qualifiers cannot follow operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow an operator.'

        # Test data and state.
        data = '5+ "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class OptionsOperatorTestCase(BasicOperatorTestCase):
    def test_basic_options_operator(self):
        """Lex choice options."""
        exp = (
            (lex.Token.QUALIFIER, 'spam'),
            (lex.Token.OPTIONS_OPERATOR, ':'),
            (lex.Token.QUALIFIER, 'eggs'),
        )
        data = '"spam":"eggs"'
        self.lex_test(exp, data)


class PoolDegenerationOperatorTestCase(BasicOperatorTestCase):
    def test_basic_count_successes(self):
        """Given a basic count successes statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]ns5'
        self.lex_test(exp, data)

    def test_basic_count_successes_with_botch(self):
        """Given a basic count successes with botches statement, return
        the tokens in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'nb'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]nb5'
        self.lex_test(exp, data)

    def test_count_successes_before_group(self):
        """Groups can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.GROUP_OPEN, '('),
            (lex.Token.NUMBER, 3),
            (lex.Token.AS_OPERATOR, '+'),
            (lex.Token.NUMBER, 2),
            (lex.Token.GROUP_CLOSE, ')'),
        )
        data = '[5,1,9]ns(3+2)'
        self.lex_test(exp, data)

    def test_count_successes_before_unary_pool_degen(self):
        """Unary pool degens can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (5, 1, 9)),
        )
        data = '[5,1,9]nsN[5,1,9]'
        self.lex_test(exp, data)

    def test_count_successes_before_operator(self):
        """Operators cannot occur after pool degen operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a pool degeneration operator.'

        # Test data and state.
        data = '[5,1,9]ns+'
        lexer = lex.Lexer()

        # Run test and determine results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    # Allowed next symbol.
    def test_operator_cannot_follow_pool_degen_operator(self):
        """And operator follow by a pool degen operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a pool degeneration operator.'

        # Test data and state.
        data = '[1,2,3]ns+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_follow_pool_degen_operator_whitespace(self):
        """And operator follow by a pool degen operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a pool degeneration operator.'

        # Test data and state.
        data = '[1,2,3]ns +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_qualifier_cannot_follow_pool_degen_op(self):
        """Qualifiers cannot follow pool degeneration operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool degeneration operator.'

        # Test data and state.
        data = '5g6ns"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_pool_degen_op_whitespace(self):
        """Qualifiers cannot follow pool degeneration operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool degeneration operator.'

        # Test data and state.
        data = '5g6ns "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class PoolGenerationOperatorTestCase(BasicOperatorTestCase):
    def test_basic_dice_pool(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.POOL_GEN_OPERATOR, 'g'),
            (lex.Token.NUMBER, 10),
        )
        data = '20g10'
        self.lex_test(exp, data)

    def test_basic_expolding_pool(self):
        """Given a basic pool generation, return the tokens that
        represent the generation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.POOL_GEN_OPERATOR, 'g!'),
            (lex.Token.NUMBER, 10),
        )
        data = '20g!10'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_qualifier_cannot_follow_pool_gen_op(self):
        """Qualifiers cannot follow pool generation operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool generation operator.'

        # Test data and state.
        data = '5g"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_pool_gen_op_whitespace(self):
        """Qualifiers cannot follow pool generation operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool generation operator.'

        # Test data and state.
        data = '5g "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class PoolOperatorTestCase(BasicOperatorTestCase):
    def test_basic_pool_keep_above(self):
        """Given a basic pool keep above statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pa'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pa2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_below(self):
        """Given a basic pool keep below statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pb'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pb2'
        self.lex_test(exp, data)

    def test_basic_pool_cap(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pc'),
            (lex.Token.NUMBER, 7),
        )
        data = '[5,1,9]pc7'
        self.lex_test(exp, data)

    def test_basic_pool_floor(self):
        """Floor the minimum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pf'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pf2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_high(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'ph'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]ph2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_low(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pl'),
            (lex.Token.NUMBER, 2),
        )
        data = '[5,1,9]pl2'
        self.lex_test(exp, data)

    def test_basic_pool_modulo(self):
        """Given a basic pool modulo statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'p%'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]p%5'
        self.lex_test(exp, data)

    def test_basic_pool_remove(self):
        """Given a basic pool remove statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pr'),
            (lex.Token.NUMBER, 5),
        )
        data = '[5,1,9]pr5'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_operator_cannot_follow_pool_operator(self):
        """And operator follow by a pool operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a pool operator.'

        # Test data and state.
        data = '[1,2,3]ph+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_follow_pool_operator_whitespace(self):
        """And operator follow by a pool operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow a pool operator.'

        # Test data and state.
        data = '[1,2,3]ph +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_qualifier_cannot_follow_pool_op(self):
        """Qualifiers cannot follow pool operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool operator.'

        # Test data and state.
        data = '[1,2,3]pa"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_pool_op_whitespace(self):
        """Qualifiers cannot follow pool operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool operator.'

        # Test data and state.
        data = '[1,2,3]pa "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class PoolTestCase(BasicOperatorTestCase):
    def test_pool(self):
        """A pool of dice."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '[5,1,9]'
        self.lex_test(exp, data)

    def test_pool_with_whitespace(self):
        """A pool of dice that has whitespace."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '[ 5 , 1 , 9 ]'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_number_cannot_follow_pool(self):
        """Numbers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '4 cannot follow a pool.'

        # Test data and state.
        data = '[1,2,3]4'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_number_cannot_follow_pool_whitespace(self):
        """Numbers cannot follow numbers."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '4 cannot follow a pool.'

        # Test data and state.
        data = '[1,2,3] 4'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_qualifier_cannot_follow_pool(self):
        """Qualifiers cannot follow pool."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool.'

        # Test data and state.
        data = '[1,2,3]"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_pool_whitespace(self):
        """Qualifiers cannot follow pool."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a pool.'

        # Test data and state.
        data = '[1,2,3] "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_roll_delimiter_can_follow_pool(self):
        """A roll delimiter can follow a close group delimiter."""
        exp = (
            (lex.Token.POOL, (1, 2, 3)),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '[1, 2, 3];5d10'
        self.lex_test(exp, data)


class QualifierTestCase(BasicOperatorTestCase):
    def test_quotation_marks(self):
        """Given a statement containing quotation marks, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.QUALIFIER, 'spam'),
        )
        data = '"spam"'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_qualifier_cannot_follow_qualifier(self):
        """Qualifiers cannot follow qualifier."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a qualifier.'

        # Test data and state.
        data = '"eggs""spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_qualifier_whitespace(self):
        """Qualifiers cannot follow qualifier."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow a qualifier.'

        # Test data and state.
        data = '"eggs" "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


class ResultsRollTestCase(BasicOperatorTestCase):
    def test_roll_delimiter(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '2d10;5d10'
        self.lex_test(exp, data)

    def test_roll_delimiter_whitespace(self):
        """Given a statement containing parenthesis, return the
        tokenized equation.
        """
        exp = (
            (lex.Token.NUMBER, 2),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
            (lex.Token.ROLL_DELIMITER, ';'),
            (lex.Token.NUMBER, 5),
            (lex.Token.DICE_OPERATOR, 'd'),
            (lex.Token.NUMBER, 10),
        )
        data = '2d10 ; 5d10'
        self.lex_test(exp, data)


class UnaryPoolDegenerationOperatorTestCase(BasicOperatorTestCase):
    def test_basic_pool_concatente(self):
        """Given a basic pool concatenate statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'C'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'C[3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_count(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N[3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_count_with_space(self):
        """Given a basic pool count statement with white space, return
        the tokens in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N [3,1,7]'
        self.lex_test(exp, data)

    def test_basic_pool_sum(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'S[3,1,7]'
        self.lex_test(exp, data)

    # Allowed next symbol.
    def test_dice_operator_cannot_follow_unary_pool_degen(self):
        """And operator cannot be followed by a unary pool degen."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'd cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'Sd20'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_dice_operator_cannot_follow_unary_pool_degen_whitespace(self):
        """And operator cannot be followed by a unary pool degen."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = 'd cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'S d20'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def Test_number_can_follow_unary_pool_degen(self):
        """A number can follow an unary pool degen."""
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.NUMBER, 3),
            (lex.Token.POOL_GEN_OPERATOR, 'dp'),
            (lex.Token.NUMBER, 3),
        )
        data = 'S3dp3'
        self.lex_test(exp, data)

    def Test_number_can_follow_unary_pool_degen_whitespace(self):
        """A number can follow an unary pool degen."""
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.NUMBER, 3),
            (lex.Token.POOL_GEN_OPERATOR, 'dp'),
            (lex.Token.NUMBER, 3),
        )
        data = 'S 3dp3'
        self.lex_test(exp, data)

    def test_operator_cannot_follow_unary_pool_degen(self):
        """And operator cannot be followed by a unary pool degen."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'S+2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_operator_cannot_follow_unary_pool_degen_whitespace(self):
        """And operator cannot be followed by a unary pool degen."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'S +2'
        lexer = lex.Lexer()

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    def test_qualifier_cannot_follow_u_pool_degen(self):
        """Qualifiers cannot follow unary pool degeneration operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'S"spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)

    def test_qualifier_cannot_follow_u_pool_degen_whitespace(self):
        """Qualifiers cannot follow unary pool degeneration operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '" cannot follow an unary pool degeneration operator.'

        # Test data and state.
        data = 'S "spam"'

        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = self.lex_test(None, data)


# Roll test case.
class StartRollTestCase(BasicOperatorTestCase):
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
class OrderOfOperationsTestCase(BasicOperatorTestCase):
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
