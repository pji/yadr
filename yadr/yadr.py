"""
yadr
~~~~

The core of the yadn package.
"""
from argparse import ArgumentParser

from yadr.lex import Lexer
from yadr.model import CompoundResult, Result
from yadr.parser import parse


# Execute YADN.
def roll(yadn: str) -> Result | CompoundResult:
    """Execute a string of YADN to roll dice.

    :param yadn: A string of YADN that defines the die roll to execute.
        YADN is described here: YADN_
    :return: The result depends on the details of the die roll, but
        could be a :class:int, :class:tuple, or :class:str object.
    :rtype: int or tuple or str

    .. _YADN: https://github.com/pji/yadr/blob/main/docs/dice_notation.rst
    """
    lexer = Lexer()
    tokens = lexer.lex(yadn)
    result = parse(tokens)
    return result


# Command parsing.
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

    # Parse and execute the command.
    args = p.parse_args()
    result = roll(args.yadn)
    print(result)
