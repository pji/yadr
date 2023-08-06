"""
test_operator
~~~~~~~~~~~~~

Dice operators for the `yadr` package.
"""
import unittest as ut
from unittest.mock import patch

from yadr import operator as op


# Choice test cases.
def test_choice_options():
    """Generate choice options."""
    a = 'spam'
    b = 'eggs'
    assert op.choice_options(a, b) == (a, b,)


def test_choice():
    """Make a choice."""
    boolean = True
    options = ('spam', 'eggs')
    assert op.choice(boolean, options) == 'spam'


# Dice operation test cases.
def test_concat(mocker):
    """Concatenate the least significant digit of the dice."""
    mocker.patch('random.randint', side_effect=(3, 10, 4))
    num = 3
    size = 10
    assert op.concat(num, size) == 304


def test_die(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and return the result.
    """
    mocker.patch('random.randint', side_effect=(4, 2, 1))
    num = 2
    size = 6
    assert op.die(num, size) == 6


def test_exploding_die(mocker):
    """Given a number of dice and the size of the die, roll that many
    exploding dice and return the result.
    """
    mocker.patch('random.randint', side_effect=[2, 1, 4, 4, 3, 1, 4, 4, 2])
    num = 5
    size = 4
    assert op.exploding_die(num, size) == 25


def test_keep_high_die(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and keep the highest.
    """
    mocker.patch('random.randint', side_effect=[15, 3, 6, 18, 10, 20])
    num = 5
    size = 20
    assert op.keep_high_die(num, size) == 18


def test_keep_low_die(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and keep the lowest.
    """
    mocker.patch('random.randint', side_effect=[15, 3, 6, 18, 10, 1])
    num = 5
    size = 20
    assert op.keep_low_die(num, size) == 3


def test_wild_die(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and add them together. If the first die rolled doesn't roll
    the highest number possible for that die, it is counted like any
    other die.
    """
    mocker.patch('random.randint', side_effect=[3, 4, 1, 5, 4, 2])
    num = 5
    size = 6
    assert op.wild_die(num, size) == 17


def test_wild_die_explodes(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and add them together. If the first die rolled rolls the
    highest number possible for that die, it explodes.
    """
    mocker.patch('random.randint', side_effect=[6, 2, 4, 1, 5, 4, 3])
    num = 5
    size = 6
    assert op.wild_die(num, size) == 22


def test_wild_die_is_one(mocker):
    """Given a number of dice and the size of the die, roll that many
    dice and add them together. If the first die rolled rolls the
    a one, the roll is zero.
    """
    mocker.patch('random.randint', side_effect=[1, 4, 1, 5, 4])
    num = 5
    size = 6
    assert op.wild_die(num, size) == 0


# Pool degeneration test cases.
class PoolConcatenateTestCase(ut.TestCase):
    def test_pool_concatenate(self):
        """Concatenate the members in the pool."""
        exp = 314
        pool = (3, 1, 4)
        act = op.pool_concatenate(pool)
        self.assertEqual(exp, act)


class PoolCountTestCase(ut.TestCase):
    def test_pool_count(self):
        """Count the members in the pool."""
        exp = 3
        pool = (3, 1, 4)
        act = op.pool_count(pool)
        self.assertEqual(exp, act)


class PoolSumTestCase(ut.TestCase):
    def test_pool_count(self):
        """Sum the members in the pool."""
        exp = 8
        pool = (3, 1, 4)
        act = op.pool_sum(pool)
        self.assertEqual(exp, act)


class CountSuccessesTestCase(ut.TestCase):
    def test_count_successes(self):
        """Count the number of values above or equal to a target."""
        # Expected value.
        exp = 5

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        target = 5

        # Run test.
        act = op.count_successes(pool, target)

        # Determine test result.
        self.assertEqual(exp, act)


class CountSuccessesWithBotchesTestCase(ut.TestCase):
    def test_count_successes_with_botch(self):
        """Count the number of values above or equal to a target and
        remove botches.
        """
        # Expected value.
        exp = 3

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        target = 5

        # Run test.
        act = op.count_successes_with_botch(pool, target)

        # Determine test result.
        self.assertEqual(exp, act)


# Pool generation operation test cases.
class DicePoolTestCase(ut.TestCase):
    @patch('random.randint')
    def test_dice_pool(self, mock_randint):
        """Generate a dice pool."""
        # Expected value.
        exp = (3, 5, 1, 10, 8, 4, 3)

        # Test data and state.
        mock_randint.side_effect = exp
        num = 7
        size = 10

        # Run test.
        act = op.dice_pool(num, size)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class ExplodingPoolTestCase(ut.TestCase):
    @patch('random.randint')
    def test_exploding_pool(self, mock_randint):
        """Generate a dice pool."""
        # Expected value.
        exp = (2, 9, 1, 1, 13, 3)

        # Test data and state.
        mock_randint.side_effect = (2, 6, 1, 1, 6, 3, 3, 6, 1)
        num = 6
        size = 6

        # Run test.
        act = op.exploding_pool(num, size)

        # Determine test result.
        self.assertTupleEqual(exp, act)


# Pool operation test cases.
class PoolKeepAbove(ut.TestCase):
    def test_pool_keep_above(self):
        """Keep dice equal to or below above the given value from the
        pool.
        """
        # Expected value.
        exp = (5, 6, 4, 5, 6, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 4

        # Run test.
        act = op.pool_keep_above(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepBelow(ut.TestCase):
    def test_pool_keep_below(self):
        """Keep dice equal to or below the given value from the pool."""
        # Expected value.
        exp = (1, 2, 4, 1, 3)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        ceiling = 4

        # Run test.
        act = op.pool_keep_below(pool, ceiling)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolCapTestCase(ut.TestCase):
    def test_pool_cap(self):
        """Dice in the pool are capped at the given value."""
        # Expected value.
        exp = (1, 2, 3, 7, 5, 6, 7, 7, 7, 4)

        # Test data and state.
        pool = (1, 2, 3, 10, 5, 6, 7, 8, 9, 4)
        cap = 7

        # Run test.
        act = op.pool_cap(pool, cap)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolFloorTestCase(ut.TestCase):
    def test_pool_floor(self):
        """Dice in the pool are floored at the given value."""
        # Expected value.
        exp = (3, 3, 3, 10, 5, 6, 7, 8, 9, 4)

        # Test data and state.
        pool = (1, 2, 3, 10, 5, 6, 7, 8, 9, 4)
        cap = 3

        # Run test.
        act = op.pool_floor(pool, cap)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepHigh(ut.TestCase):
    def test_pool_keep_high(self):
        """Keep the given number of highest dice from the pool."""
        # Expected value.
        exp = (5, 6, 5, 6, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 5

        # Run test.
        act = op.pool_keep_high(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolKeepLow(ut.TestCase):
    def test_pool_keep_low(self):
        """Keep the given number of highest dice from the pool."""
        # Expected value.
        exp = (1, 2, 1)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        keep = 3

        # Run test.
        act = op.pool_keep_low(pool, keep)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolModulo(ut.TestCase):
    def test_pool_keep_below(self):
        """Perform a modulo on all members."""
        # Expected value.
        exp = (1, 2, 2, 0, 1, 2, 1, 0, 0, 0)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        divisor = 3

        # Run test.
        act = op.pool_modulo(pool, divisor)

        # Determine test result.
        self.assertTupleEqual(exp, act)


class PoolRemove(ut.TestCase):
    def test_pool_keep_below(self):
        """Keep dice equal to or below the given value from the pool."""
        # Expected value.
        exp = (1, 2, 6, 4, 1, 6, 3, 6)

        # Test data and state.
        pool = (1, 2, 5, 6, 4, 5, 1, 6, 3, 6)
        cut = 5

        # Run test.
        act = op.pool_remove(pool, cut)

        # Determine test result.
        self.assertTupleEqual(exp, act)
