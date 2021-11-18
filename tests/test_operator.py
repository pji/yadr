"""
test_operator
~~~~~~~~~~~~~

Dice operators for the `yadr` package.
"""
import unittest as ut

from yadr import operator as op


# Test cases.
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
