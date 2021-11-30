"""
test_yadr
~~~~~~~~~

Unit tests for the yadr.yadr module.
"""
from io import StringIO
import sys
import unittest as ut
from unittest.mock import patch

from yadr import yadr


# Test cases.
class ParseCliTestCase(ut.TestCase):
    def setUp(self):
        self.argv_buffer = sys.argv

    def tearDown(self):
        sys.argv = self.argv_buffer

    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint')
    def test_yadn(self, mock_randint, mock_stdout):
        """Execute YADN from the command line."""
        # Expected value.
        exp = '11\n'

        # Test data and state.
        sys.argv = ['python -m yadr', '3d6']
        mock_randint.side_effect = (4, 4, 3)

        # Run test.
        yadr.parse_cli()

        # Extract actual result and determine success.
        act = mock_stdout.getvalue()
        self.assertEqual(exp, act)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint')
    def test_yadn_dice_maps(self, mock_randint, mock_stdout):
        """The -m option followed by a file path should load in the
        dice maps at the given location.
        """
        # Expected value.
        exp = '["+", ""]\n'

        # Test data and state.
        sys.argv = [
            'python -m yadr',
            '2g3m"fudge"',
            '-m',
            'tests/data/__test_dice_map.txt'
        ]
        mock_randint.side_effect = (3, 2)

        # Run test.
        yadr.parse_cli()

        # Extract actual result and determine success.
        act = mock_stdout.getvalue()
        self.assertEqual(exp, act)


class RollTestCase(ut.TestCase):
    @patch('random.randint')
    def test_roll(self, mock_randint):
        """Execute a YADN string."""
        # Expected value.
        exp = 11

        # Test data and state.
        mock_randint.side_effect = (4, 4, 3)
        yadn = '3d6'

        # Run test.
        act = yadr.roll(yadn)

        # Determine test results.
        self.assertEqual(exp, act)

    @patch('random.randint')
    def test_roll_yadn_out(self, mock_randint):
        """Execute a YADN string."""
        # Expected value.
        exp = '11'

        # Test data and state.
        mock_randint.side_effect = (4, 4, 3)
        yadn = '3d6'
        yadn_out = True

        # Run test.
        act = yadr.roll(yadn, yadn_out)

        # Determine test results.
        self.assertEqual(exp, act)
