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

    # Identity.
    def test_pool(self):
        """A pool of dice."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '{5,1,9}'
        self.lex_test(exp, data)

    def test_pool_with_whitespace(self):
        """A pool of dice that has whitespace."""
        exp = ((
            lex.Token.POOL,
            (5, 1, 9),
        ),)
        data = '{ 5 , 1 , 9 }'
        self.lex_test(exp, data)

    # Operators.
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

    def test_operator_can_be_followed_by_unary_pool_degen(self):
        """Subtraction can be followed by a unary pool degeneration
        operator.
        """
        exp = (
            (lex.Token.NUMBER, 200),
            (lex.Token.OPERATOR, '-'),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (2, 3, 4)),
        )
        data = '200-S{2,3,4}'
        self.lex_test(exp, data)

    def test_operator_cannot_be_followed_by_an_operator(self):
        """And operator cannot be followed by and operator."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow operator.'
        
        # Test data and state.
        data = '3-+2'
        lexer = lex.Lexer()
        
        # Run test and determine the result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    # Dice operators.
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

    # Pool generation operator.
    def test_basic_dice_pool(self):
        """Given a basic die equation, return the tokens that
        represent the equation.
        """
        exp = (
            (lex.Token.NUMBER, 20),
            (lex.Token.DICE_OPERATOR, 'dp'),
            (lex.Token.NUMBER, 10),
        )
        data = '20dp10'
        self.lex_test(exp, data)

    # Pool operators.
    def test_basic_pool_keep_above(self):
        """Given a basic pool keep above statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pa'),
            (lex.Token.NUMBER, 2),
        )
        data = '{5,1,9}pa2'
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
        data = '{5,1,9}pb2'
        self.lex_test(exp, data)

    def test_basic_pool_cap(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pc'),
            (lex.Token.NUMBER, 7),
        )
        data = '{5,1,9}pc7'
        self.lex_test(exp, data)

    def test_basic_pool_floor(self):
        """Floor the minimum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pf'),
            (lex.Token.NUMBER, 2),
        )
        data = '{5,1,9}pf2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_high(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'ph'),
            (lex.Token.NUMBER, 2),
        )
        data = '{5,1,9}ph2'
        self.lex_test(exp, data)

    def test_basic_pool_keep_low(self):
        """Cap the maximum value in a pool."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_OPERATOR, 'pl'),
            (lex.Token.NUMBER, 2),
        )
        data = '{5,1,9}pl2'
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
        data = '{5,1,9}pr5'
        self.lex_test(exp, data)

    # Unary pool degeneration operator.
    def test_basic_pool_count(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N{3,1,7}'
        self.lex_test(exp, data)

    def test_basic_pool_count_with_space(self):
        """Given a basic pool count statement with white space, return
        the tokens in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'N {3,1,7}'
        self.lex_test(exp, data)

    def test_basic_pool_sum(self):
        """Given a basic pool count statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'S'),
            (lex.Token.POOL, (3, 1, 7))
        )
        data = 'S{3,1,7}'
        self.lex_test(exp, data)

    # Binary pool degeneration operator.
    def test_basic_count_successes(self):
        """Given a basic count successes statement, return the tokens
        in the statement.
        """
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.NUMBER, 5),
        )
        data = '{5,1,9}ns5'
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
        data = '{5,1,9}nb5'
        self.lex_test(exp, data)

    def test_count_successes_before_group(self):
        """Groups can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.OPEN_GROUP, '('),
            (lex.Token.NUMBER, 3),
            (lex.Token.OPERATOR, '+'),
            (lex.Token.NUMBER, 2),
            (lex.Token.CLOSE_GROUP, ')'),
        )
        data = '{5,1,9}ns(3+2)'
        self.lex_test(exp, data)

    def test_count_successes_before_unary_pool_degen(self):
        """Unary pool degens can follow pool degeneration operators."""
        exp = (
            (lex.Token.POOL, (5, 1, 9)),
            (lex.Token.POOL_DEGEN_OPERATOR, 'ns'),
            (lex.Token.U_POOL_DEGEN_OPERATOR, 'N'),
            (lex.Token.POOL, (5, 1, 9)),
        )
        data = '{5,1,9}nsN{5,1,9}'
        self.lex_test(exp, data)

    def test_count_successes_before_operator(self):
        """Operators cannot occur after pool degen operators."""
        # Expected values.
        exp_ex = ValueError
        exp_msg = '\\+ cannot follow pool degeneration operator.'

        # Test data and state.
        data = '{5,1,9}ns+'
        lexer = lex.Lexer()

        # Run test and determine results.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            _ = lexer.lex(data)

    # Grouping.
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

    # Order of operations.
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
