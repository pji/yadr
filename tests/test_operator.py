"""
test_operator
~~~~~~~~~~~~~

Dice operators for the `yadr` package.
"""
import unittest as ut
from unittest.mock import patch

from yadr import operator as op


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


# Dice operation test cases.
class DieTestCase(ut.TestCase):
    def die_test(self, exp, args=None, kwargs=None, seed='spam'):
        """Common test for the die function."""
        if not args:
            args = []
        if not kwargs:
            kwargs = {}
        op._seed(seed)
        act = op.die(*args, **kwargs)
        self.assertEqual(exp, act)

    def test_die(self):
        """Given a number of dice and the size of the die,
        roll that many dice and return the result.
        """
        exp = 4
        kwargs = {
            'num': 1,
            'size': 6,
        }
        seed = 'spam12'
        self.die_test(exp, kwargs=kwargs, seed=seed)


class ExplodingDie(ut.TestCase):
    def exploding_die_test(self, exp, num, size):
        """Common test for the die function."""
        act = op.exploding_die(num, size)
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_exploding_die(self, mock_randint):
        """Given a number of dice and the size of the die,
        roll that many exploding dice and return the result.
        """
        exp = 25
        mock_randint.side_effect = [2, 1, 4, 4, 3, 1, 4, 4, 2]
        num = 5
        size = 4
        self.exploding_die_test(exp, num, size)


class KeepHighDie(ut.TestCase):
    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        # Expected value.
        exp = 18

        # Test data and state.
        mock_randint.side_effect = [15, 3, 6, 18, 10]
        num = 5
        size = 20

        # Run test.
        act = op.keep_high_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


class KeepLowDie(ut.TestCase):
    @patch('random.randint')
    def test_keep_high_die(self, mock_randint):
        # Expected value.
        exp = 3

        # Test data and state.
        mock_randint.side_effect = [15, 3, 6, 18, 10]
        num = 5
        size = 20

        # Run test.
        act = op.keep_low_die(num, size)

        # Determine test result.
        self.assertEqual(exp, act)


# Pool operation test cases.
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
