"""
yadr
~~~~

The core of the :mod:`yadr` package, which contains the public API.

##########
Public API
##########

The following are the functions that make up the public API of :mod:`yadr`.


Rolling Dice
============
:class:`yadr.roll` is the main interface to :mod:`yadr`, and in most
cases it's all you need.

.. autofunction:: yadr.roll


Managing Dice Maps
==================
If you're playing a game that uses symbol-based dice rather than ones
with numbers, you may need to use a dice map to translate the dice
rolls into those symbols. You can handle that in :ref:`YADN`, but the
following functions can be useful, too.

.. autofunction:: yadr.add_dice_map
.. autofunction:: yadr.list_dice_maps


#################
Utility Functions
#################

The following functions are used within the API, but they are not intended
for public use. They are only documented here for support purposes.

.. autofunction:: yadr.yadr.get_default_maps
.. autofunction:: yadr.yadr.read_file
.. autofunction:: yadr.yadr.parse_maps

"""
from importlib.resources import files
from pathlib import Path
from typing import Optional

import yadr.data
from yadr import maps as m
from yadr.encode import Encoder
from yadr.lex import Lexer
from yadr.model import CompoundResult, DiceMapping, Result, TokenInfo
from yadr.parser import Parser, dice_map


# Public API.
def add_dice_map(loc: str) -> dict[str, DiceMapping]:
    """Load the dice-maps from a given file.

    :param loc: The location of the file of dice mappings to load.
    :return: None.
    :rtype: NoneType

    Usage::

        >>> from yadr import add_dice_map
        >>>
        >>> path = 'tests/data/__test_dice_map.txt'
        >>> add_dice_map(path)              # doctest: +NORMALIZE_WHITESPACE
        {'spam': {1: 'eggs', 2: 'bacon', 3: 'eggs', 4: 'tomato'}, 'fudge':
        {1: '-', 2: '', 3: '+'}}
    """
    yadn = read_file(loc)
    return parse_map(yadn)


def list_dice_maps() -> str:
    """Get the list of the default dice maps.

    :return: A :class:`str` object.
    :rtype: str

    Usage::

        >>> from yadr import list_dice_maps
        >>>
        >>> list_dice_maps()                # doctest: +ELLIPSIS
        'sweote boost...
    """
    dice_map = get_default_maps()
    maps_ = '\n'.join(dice_map)
    return maps_


def roll(
    yadn: str,
    yadn_out: bool = False,
    dice_map: Optional[dict[str, DiceMapping]] = None
) -> None | Result | CompoundResult:
    """Execute a string of :ref:`YADN` to roll dice.

    :param yadn: A string of :ref:`YADN` that defines the die roll to
        execute.
    :param yadn_out: (Optional.) Whether the output should be in native
        Python objects or :ref:`YADN` notation. The default is native
        Python objects.
    :param dice_map: (Optional.) A dictionary of maps for transforming
        the value rolled. See :ref:`dice_maps` for details.
    :return: The result depends on the details of the die roll.
    :rtype: None, Result, or CompoundResult

    Usage::

        >>> import yadr
        >>>
        >>> yadr.roll('3d6')                        # doctest: +SKIP
        16

    The specific result will depend on the :ref:`YADN` being executed.
    In the example above, it will be an integer in the range of three to
    eighteen that is created by generating three random integers in the
    range of one to six.
    """
    # Get the default dice maps and add any passed into the roll.
    if not dice_map:
        dice_map = {}
    default_maps = get_default_maps()
    default_maps.update(dice_map)

    # Lex the YADN into tokens for parsing.
    lexer = Lexer()
    tokens = lexer.lex(yadn)

    # Parse and execute the YADN tokens.
    parser = Parser()
    parser.dice_map = default_maps
    result: None | Result | CompoundResult = parser.parse(tokens)

    # If needed, encode the result into YADN and return the result.
    if yadn_out:
        encoder = Encoder()
        result = encoder.encode(result)
    return result


# Utility.
def get_default_maps() -> dict[str, DiceMapping]:
    """Get the default dice maps.

    :return: The default dice maps as a :class:`dict` of :class:`dict`
        objects.
    :rtype: dict

    Usage::

        >>> from yadr.yadr import get_default_maps
        >>>
        >>> get_default_maps()              # doctest: +ELLIPSIS
        {'sweote boost': {1: '',...
    """
    data_pkg = files(yadr.data)
    default_file = Path(f'{data_pkg}') / 'dice_maps.yadn'
    with open(default_file) as fh:
        default_maps_yadn = fh.read()
    return parse_map(default_maps_yadn)


def read_file(loc: str | Path) -> str:
    """Read test from a file.

    :param loc: The file system location of the file.
    :return: A :class:str object.
    :rtype: str
    """
    path = Path(loc)
    with open(path) as fh:
        contents = fh.read()
    return contents


def parse_map(yadn: str) -> dict[str, DiceMapping]:
    """Parse the contents of a dice mapping file."""
    if ';' in yadn:
        yadn_parts = yadn.split(';')
        dice_map = {}
        for part in yadn_parts:
            assert ';' not in part
            dice_map.update(parse_map(part))
        return dice_map

    mlexer = m.Lexer()
    mparser = m.Parser()
    tokens = mlexer.lex(yadn)
    name, value = mparser.parse(tokens)
    return {name: value, }
