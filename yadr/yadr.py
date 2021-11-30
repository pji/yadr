"""
yadr
~~~~

The core of the yadn package.
"""
from argparse import ArgumentParser
from pathlib import Path

from yadr.encode import Encoder
from yadr.lex import Lexer
from yadr.model import CompoundResult, Result
from yadr.parser import parse


# Execute YADN.
def roll(yadn: str, yadn_out: bool = False) -> str | Result | CompoundResult:
    """Execute a string of YADN to roll dice.

    :param yadn: A string of YADN that defines the die roll to execute.
        YADN is described here: YADN_
    :param yadn_out: (Optional.) Whether the output should be in native
        Python objects or YADN notation. The default is native Python
        objects.
    :return: The result depends on the details of the die roll, but
        could be a :class:int, :class:tuple, or :class:str object.
    :rtype: int or tuple or str

    .. _YADN: https://github.com/pji/yadr/blob/main/docs/dice_notation.rst

    Usage::

        >>> import yadr
        >>>
        >>> yadr.roll('3d6')                        # doctest: +SKIP
        16

    The specific result will depend on the YADN being executed. In the
    example above, it will be an integer in the range of three to
    eighteen that is created by generating three random integers in the
    range of one to six.
    """
    lexer = Lexer()
    tokens = lexer.lex(yadn)
    result: Result | CompoundResult = parse(tokens)
    if yadn_out:
        encoder = Encoder()
        result = encoder.encode(result)
    return result


# Command parsing.
def add_dice_map(loc: str) -> None:
    """Load the dice-maps in the given file into memory."""
    path = Path(loc)
    with open(path) as fh:
        yadn = fh.read()
    _ = roll(yadn)


def parse_cli() -> None:
    """Parse command line options."""
    # Stand up the parser.
    p = ArgumentParser(
        description='Execute YADN syntax to roll dice.',
        prog='yadr'
    )

    # Define the command line arguments.
    p.add_argument(
        'yadn',
        help='A string of YADN describing the die roll.',
        action='store',
        type=str
    )
    p.add_argument(
        '--add_dice_map', '-m',
        help='Load the dice mappings at the given file location.',
        nargs=1,
        action='store',
        type=str
    )

    # Parse and execute the command.
    args = p.parse_args()
    if args.add_dice_map:
        add_dice_map(args.add_dice_map[0])
    result = roll(args.yadn, True)
    print(result)
