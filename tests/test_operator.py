"""
test_operator
~~~~~~~~~~~~~

Dice operators for the `yadr` package.
"""
import unittest as ut
from unittest.mock import patch

from yadr import operator as op


# Roll test cases.
class RollTestCase(ut.TestCase):
    def test_derives_value_from_pool(self):
        """Given a dice pool, value is the sum of the numbers in
        the pool.
        """
        # Expected value.
        exp = 10

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)

        # Run test.
        act = roll.value

        # Determine test result.
        self.assertEqual(exp, act)

    def test_addition_with_int_uses_value(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 12

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)
        value = 2

        # Run tests.
        act = roll + 2

        # Determine test result.
        self.assertEqual(exp, act)

    def test_exponentiation_with_int_uses_value(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 100

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)
        value = 2

        # Run tests.
        act = roll ** 2

        # Determine test result.
        self.assertEqual(exp, act)

    def test_floor_division_with_int_uses_value(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 5

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)
        value = 2

        # Run tests.
        act = roll // 2

        # Determine test result.
        self.assertEqual(exp, act)

    def test_multiplication_with_int_uses_value(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 20

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)
        value = 2

        # Run tests.
        act = roll * 2

        # Determine test result.
        self.assertEqual(exp, act)

    def test_subtraction_with_int_uses_value(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 8

        # Test data and state.
        pool = (3, 3, 4)
        roll = op.Roll(pool)
        value = 2

        # Run tests.
        act = roll - 2

        # Determine test result.
        self.assertEqual(exp, act)

    def test_addition_with_class(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 18

        # Test data and state.
        a = op.Roll((3, 3, 4))
        b = op.Roll((5, 3))

        # Run tests.
        act = a + b

        # Determine test result.
        self.assertEqual(exp, act)

    def test_exponentiation_with_class(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 100000000

        # Test data and state.
        a = op.Roll((3, 3, 4))
        b = op.Roll((3, 5))

        # Run tests.
        act = a ** b

        # Determine test result.
        self.assertEqual(exp, act)

    def test_floor_division_with_class(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 3

        # Test data and state.
        a = op.Roll((3, 3, 4))
        b = op.Roll((1, 2))

        # Run tests.
        act = a // b

        # Determine test result.
        self.assertEqual(exp, act)

    def test_multiplication_with_class(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 80

        # Test data and state.
        a = op.Roll((3, 3, 4))
        b = op.Roll((5, 3))

        # Run tests.
        act = a * b

        # Determine test result.
        self.assertEqual(exp, act)

    def test_subtraction_with_class(self):
        """Basic arithmetic with integers uses the value attribute."""
        # Expected value:
        exp = 2

        # Test data and state.
        a = op.Roll((3, 3, 4))
        b = op.Roll((3, 5))

        # Run tests.
        act = a - b

        # Determine test result.
        self.assertEqual(exp, act)


# Dice operation test cases.
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
