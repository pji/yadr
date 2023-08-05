"""
test_yadr
~~~~~~~~~

Unit tests for the yadr.yadr module.
"""
from yadr import yadr


# Test yadr.roll().
def test_roll(mocker):
    """Execute a YADN string."""
    exp = 11
    yadn = ('3d6',)
    dice = (4, 4, 3)
    roll_test(exp, yadn, dice, mocker)


def test_roll_with_default_dice_map(mocker):
    """Execute a YADN string using a default dice map."""
    exp = '-'
    yadn = ('1d3m"fate"',)
    dice = (1,)
    roll_test(exp, yadn, dice, mocker)


def test_roll_with_yadn_output(mocker):
    """Execute a YADN string returning a YADN string."""
    exp = '11'
    yadn = ('3d6', True)
    dice = (4, 4, 3)
    roll_test(exp, yadn, dice, mocker)


def roll_test(exp, params, dice, mocker):
    mocker.patch('random.randint', side_effect=dice)
    assert yadr.roll(*params) == exp


# Test parse_cli().
def test_parse_cli(mocker, capsys):
    """Execute YADN from the command line."""
    cmd = ['python -m yadr', '3d6']
    dice = (4, 4, 3)
    result = cli_test(cmd, dice, mocker, capsys)
    assert result == '11\n'


def test_parse_cli_with_dice_maps(mocker, capsys):
    """The -m option followed by a file path should load in the
    dice maps at the given location.
    """
    cmd = [
        'python -m yadr',
        '2g3m"fudge"',
        '-m',
        'tests/data/__test_dice_map.txt'
    ]
    dice = (3, 2)
    result = cli_test(cmd, dice, mocker, capsys)
    assert result == '["+", ""]\n'


def test_parse_cli_with_listing_default_maps(mocker, capsys):
    """The -l option will list the default dice maps."""
    cmd = ['python -m yadr', '-l']
    dice = ()
    result = cli_test(cmd, dice, mocker, capsys)

    # Build the expected value.
    default_map_loc = 'yadr/data/dice_maps.yadn'
    with open(default_map_loc) as fh:
        lines = fh.readlines()
    lines = [line for line in lines if '=' in line]
    lines = [line.split('"')[1] for line in lines]
    expected = '\n'.join(lines) + '\n'

    assert result == expected


def cli_test(cmd, dice, mocker, capsys):
    """Test the output of running `yadr` from the command line."""
    # Set up the test.
    mocker.patch('sys.argv', cmd)
    mocker.patch('random.randint', side_effect=dice)

    # Run the test.
    yadr.parse_cli()

    # Capture and return the test result.
    captured = capsys.readouterr()
    return captured.out
