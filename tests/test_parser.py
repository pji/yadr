"""
test_parse
~~~~~~~~~~

Unit tests for the yadr.parse module.
"""
from yadr import operator as yo
from yadr import parser as p
from yadr.model import Token


# Core test functions.
def parser_test(expected, tokens):
    parser = p.Parser()
    assert parser.parse(tokens) == expected


# Identity test cases.
def test_boolean():
    """Parse a boolean."""
    exp = True
    tokens = (
        (Token.BOOLEAN, True),
    )
    parser_test(exp, tokens)


def test_number():
    "Parse a number."
    exp = 5
    tokens = (
        (Token.NUMBER, 5),
    )
    parser_test(exp, tokens)


def test_pool():
    "Parse a pool."
    exp = (3, 3, 4)
    tokens = (
        (Token.POOL, (3, 3, 4)),
    )
    parser_test(exp, tokens)


def test_quantifier():
    """Parse a qualifier."""
    exp = 'spam'
    tokens = (
        (Token.QUALIFIER, 'spam'),
    )
    parser_test(exp, tokens)


# Basic arithmetic tests.
def test_addition():
    """Parse basic addition."""
    exp = 5
    tokens = (
        (Token.NUMBER, 3),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_division():
    "Perform basic division."
    exp = 2
    tokens = (
        (Token.NUMBER, 4),
        (Token.MD_OPERATOR, '/'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_division_rounds_down():
    "Division rounds down to the nearest integer (floor division)."
    exp = 2
    tokens = (
        (Token.NUMBER, 5),
        (Token.MD_OPERATOR, '/'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_exponentiation():
    "Perform basic division."
    exp = 9
    tokens = (
        (Token.NUMBER, 3),
        (Token.EX_OPERATOR, '^'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_modulo():
    "Perform basic modulo."
    exp = 1
    tokens = (
        (Token.NUMBER, 3),
        (Token.MD_OPERATOR, '%'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_multiplication():
    "Perform basic multiplication."
    exp = 6
    tokens = (
        (Token.NUMBER, 3),
        (Token.MD_OPERATOR, '*'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_subtraction():
    "Perform basic subtraction."
    exp = 1
    tokens = (
        (Token.NUMBER, 3),
        (Token.AS_OPERATOR, '-'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


# Choice and related operator tests.
def test_choice():
    """Perform choice operation."""
    exp = 'eggs'
    tokens = (
        (Token.BOOLEAN, False),
        (Token.CHOICE_OPERATOR, '?'),
        (Token.QUALIFIER, 'spam'),
        (Token.OPTIONS_OPERATOR, ':'),
        (Token.QUALIFIER, 'eggs'),
    )
    parser_test(exp, tokens)


def test_greater_than():
    """Perform greater than comparison."""
    exp = True
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '>'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_greater_than_or_equal():
    """Perform greater than or equal comparison."""
    exp = True
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '>='),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_less_than():
    """Perform less than comparison."""
    exp = False
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '<'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_less_than_or_equal():
    """Perform less than comparison."""
    exp = False
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '<='),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_equal():
    """Perform less than comparison."""
    exp = False
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '=='),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_not_equal():
    """Perform less than comparison."""
    exp = True
    tokens = (
        (Token.NUMBER, 3),
        (Token.COMPARISON_OPERATOR, '!='),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_options_operator():
    """Create a choice options."""
    exp = ('spam', 'eggs')
    tokens = (
        (Token.QUALIFIER, 'spam'),
        (Token.OPTIONS_OPERATOR, ':'),
        (Token.QUALIFIER, 'eggs'),
    )
    parser_test(exp, tokens)


# Dice operator tests.
def test_concat(mocker):
    """Concatenate dice rolls."""
    mocker.patch('random.randint', side_effect=[1, 11, 3])
    exp = 113
    tokens = (
        (Token.NUMBER, 3),
        (Token.DICE_OPERATOR, 'dc'),
        (Token.NUMBER, 12),
    )
    parser_test(exp, tokens)


def test_die(mocker):
    """Roll a die."""
    mocker.patch('random.randint', side_effect=[1, 2, 2])
    exp = 5
    tokens = (
        (Token.NUMBER, 3),
        (Token.DICE_OPERATOR, 'd'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_exploding_die(mocker):
    """Roll an exploding die."""
    mocker.patch('random.randint', side_effect=[1, 2, 4, 2, 2])
    exp = 11
    tokens = (
        (Token.NUMBER, 4),
        (Token.DICE_OPERATOR, 'd!'),
        (Token.NUMBER, 4),
    )
    parser_test(exp, tokens)


def test_keep_high_die(mocker):
    """Roll dice and keep the highest."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = 5
    tokens = (
        (Token.NUMBER, 3),
        (Token.DICE_OPERATOR, 'dh'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_keep_low_die(mocker):
    """Roll dice and keep the lowest."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = 1
    tokens = (
        (Token.NUMBER, 3),
        (Token.DICE_OPERATOR, 'dl'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_wild_die(mocker):
    """Roll dice and keep the lowest."""
    mocker.patch('random.randint', side_effect=[4, 2, 1, 6])
    exp = 13
    tokens = (
        (Token.NUMBER, 4),
        (Token.DICE_OPERATOR, 'dw'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


# Pool generation operator tests.
def test_dice_pool(mocker):
    """Roll dice and keep the highest."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = (1, 5, 3)
    tokens = (
        (Token.NUMBER, 3),
        (Token.POOL_GEN_OPERATOR, 'g'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_exploding_pool(mocker):
    """Roll an exploding dice pool."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = (1, 5, 3)
    tokens = (
        (Token.NUMBER, 3),
        (Token.POOL_GEN_OPERATOR, 'g!'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


# Unary pool degeneration operator tests.
def test_pool_concatenate(mocker):
    """Concatenate the dice in a pool."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = 153
    tokens = (
        (Token.U_POOL_DEGEN_OPERATOR, 'C'),
        (Token.NUMBER, (1, 5, 3)),
    )
    parser_test(exp, tokens)


def test_pool_count(mocker):
    """Count the dice in a pool."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = 3
    tokens = (
        (Token.U_POOL_DEGEN_OPERATOR, 'N'),
        (Token.NUMBER, (1, 5, 3)),
    )
    parser_test(exp, tokens)


def test_pool_sum(mocker):
    """Count the dice in a pool."""
    mocker.patch('random.randint', side_effect=[1, 5, 3])
    exp = 9
    tokens = (
        (Token.U_POOL_DEGEN_OPERATOR, 'S'),
        (Token.NUMBER, (1, 5, 3)),
    )
    parser_test(exp, tokens)


# Pool degeneration operators.
def test_count_successes():
    """Keep a values that aren't a given number in the pool."""
    exp = 2
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_DEGEN_OPERATOR, 'ns'),
        (Token.NUMBER, 8),
    )
    parser_test(exp, tokens)


def test_count_successes_with_botch():
    """Keep a values that aren't a given number in the pool."""
    exp = 1
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_DEGEN_OPERATOR, 'nb'),
        (Token.NUMBER, 8),
    )
    parser_test(exp, tokens)


# Pool operators.
def test_pool_keep_above():
    """Keep a values above a given number in the pool."""
    exp = (8, 9)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pa'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_pool_keep_below():
    """Keep a values below a given number in the pool."""
    exp = (5, 1)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pb'),
        (Token.NUMBER, 6),
    )
    parser_test(exp, tokens)


def test_pool_cap():
    """Cap the values in a pool at a given value."""
    exp = (5, 7, 1, 7)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pc'),
        (Token.NUMBER, 7),
    )
    parser_test(exp, tokens)


def test_pool_floor():
    """Floor the values in a pool at a given value."""
    exp = (8, 8, 8, 9)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pf'),
        (Token.NUMBER, 8),
    )
    parser_test(exp, tokens)


def test_pool_keep_high():
    """Keep a number of highest values from the pool."""
    exp = (8, 9)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'ph'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_pool_keep_low():
    """Keep a number of highest values from the pool."""
    exp = (5, 1)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pl'),
        (Token.NUMBER, 2),
    )
    parser_test(exp, tokens)


def test_pool_modulo():
    """Perform a modulo on each member."""
    exp = (0, 3, 1, 4)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'p%'),
        (Token.NUMBER, 5),
    )
    parser_test(exp, tokens)


def test_pool_remove():
    """Keep a values that aren't a given number in the pool."""
    exp = (5, 1, 9)
    tokens = (
        (Token.POOL, (5, 8, 1, 9)),
        (Token.POOL_OPERATOR, 'pr'),
        (Token.NUMBER, 8),
    )
    parser_test(exp, tokens)


# Dice mapping tests.
def test_map():
    """Parse and store a dice map."""
    # Expected value.
    exp = 'success'

    # Test data and state.
    parser = p.Parser()
    tokens = (
        (Token.MAP, ('spam', {1: 'none', 2: 'success'})),
    )
    _ = parser.parse(tokens)

    # Run test.
    assert parser.dice_map['spam'][2] == exp


# Mapping operator tests.
def test_map_result(mocker):
    """Given a map and a roll with a dice map operator, return the
    correct result.
    """
    # Expected value.
    exp = 'success'

    # Test data and state.
    parser = p.Parser()
    mocker.patch('random.randint', side_effect=(3, ))
    parser.dice_map['_test_map_result'] = {
        1: 'none',
        2: 'success',
        3: 'success',
        4: 'success success',
    }
    tokens = (
        (Token.NUMBER, 1),
        (Token.DICE_OPERATOR, 'd'),
        (Token.NUMBER, 4),
        (Token.MAPPING_OPERATOR, 'm'),
        (Token.QUALIFIER, '_test_map_result'),
    )

    # Run test.
    assert parser.parse(tokens) == exp


def test_map_result_pool(mocker):
    """Given a map and a roll with a dice map operator, return the
    correct result.
    """
    # Expected value.
    exp = ('success', 'none')

    # Test data and state.
    parser = p.Parser()
    mocker.patch('random.randint', side_effect=(3, 1, ))
    parser.dice_map['_test_map_result'] = {
        1: 'none',
        2: 'success',
        3: 'success',
        4: 'success success',
    }
    tokens = (
        (Token.NUMBER, 2),
        (Token.DICE_OPERATOR, 'g'),
        (Token.NUMBER, 4),
        (Token.MAPPING_OPERATOR, 'm'),
        (Token.QUALIFIER, '_test_map_result'),
    )

    # Run test.
    assert parser.parse(tokens) == exp


# Test rolls and result tests.
def test_roll_delimiter(mocker):
    """Return the result of two rolls."""
    mocker.patch('random.randint', side_effect=(1, 1, 3, 8))
    exp = ((1, 1, 3), 10)
    tokens = (
        (Token.NUMBER, 3),
        (Token.POOL_GEN_OPERATOR, 'g'),
        (Token.NUMBER, 8),
        (Token.ROLL_DELIMITER, ';'),
        (Token.NUMBER, 1),
        (Token.DICE_OPERATOR, 'd'),
        (Token.NUMBER, 10),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 2)
    )
    parser_test(exp, tokens)


def test_roll_delimiter_remove_none_result(mocker):
    """Return the result of two rolls."""
    mocker.patch('random.randint', side_effect=(2,))
    exp = 'lose'
    tokens = (
        (Token.MAP, (
            'spam',
            {1: "win", 2: "lose"}
        )),
        (Token.ROLL_DELIMITER, ';'),
        (Token.NUMBER, 1),
        (Token.DICE_OPERATOR, 'd'),
        (Token.NUMBER, 2),
        (Token.MAPPING_OPERATOR, 'm'),
        (Token.QUALIFIER, 'spam')
    )
    parser_test(exp, tokens)


# Test order of precedence.
def test_can_perform_multiple_operations():
    """The parser can parse statements with multiple operators."""
    exp = 9
    tokens = (
        (Token.NUMBER, 3),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 2),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 4),
    )
    parser_test(exp, tokens)


def test_exponentiation_before_multiplication():
    """Multiplication should occur before addition."""
    exp = 48
    tokens = (
        (Token.NUMBER, 3),
        (Token.MD_OPERATOR, '*'),
        (Token.NUMBER, 2),
        (Token.EX_OPERATOR, '^'),
        (Token.NUMBER, 4),
    )
    parser_test(exp, tokens)


def test_multiplication_before_addition():
    """Multiplication should occur before addition."""
    exp = 11
    tokens = (
        (Token.NUMBER, 3),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 2),
        (Token.MD_OPERATOR, '*'),
        (Token.NUMBER, 4),
    )
    parser_test(exp, tokens)


def test_parens_before_multiplication():
    """Parentheses should occur before multiplication."""
    exp = 18
    tokens = (
        (Token.NUMBER, 3),
        (Token.MD_OPERATOR, '*'),
        (Token.GROUP_OPEN, '('),
        (Token.NUMBER, 2),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 4),
        (Token.GROUP_CLOSE, ')'),
    )
    parser_test(exp, tokens)


def test_pool_generation_happens_before_pool_degeneration(mocker):
    """Pool generation should happen before pool degeneration
    in order of operations.
    """
    # Expected value.
    exp = 20

    # Test data and state.
    rand_results = [5, 4, 6, 2, 3]
    mocker.patch('random.randint', side_effect=rand_results)
    tokens = (
        (Token.U_POOL_DEGEN_OPERATOR, 'S'),
        (Token.NUMBER, 5),
        (Token.POOL_GEN_OPERATOR, 'g'),
        (Token.NUMBER, 6),
    )

    # Run test.
    parser_test(exp, tokens)


def test_unary_pool_degeneration_happens_before_operators(mocker):
    """Unary pool degeneration should happen before operators
    in order of operations.
    """
    # Expected value.
    exp = 25

    # Test data and state.
    rand_results = [5, 4, 6, 2, 3]
    mocker.patch('random.randint', side_effect=rand_results)
    tokens = (
        (Token.U_POOL_DEGEN_OPERATOR, 'S'),
        (Token.NUMBER, 5),
        (Token.POOL_GEN_OPERATOR, 'g'),
        (Token.NUMBER, 6),
        (Token.AS_OPERATOR, '+'),
        (Token.NUMBER, 5),
    )

    # Run test.
    parser_test(exp, tokens)


def test_pool_operation_happens_before_pool_degeneration():
    """Pool operations should happen before pool degeneration
    in order of operations.
    """
    # Expected value.
    exp = 1

    # Test data and state.
    tokens = (
        (Token.POOL, (5, 4, 6, 2, 3)),
        (Token.POOL_OPERATOR, 'pb'),
        (Token.NUMBER, 5),
        (Token.POOL_DEGEN_OPERATOR, 'ns'),
        (Token.NUMBER, 5),
    )

    # Run test.
    parser_test(exp, tokens)
