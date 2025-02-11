"""
__main__
~~~~~~~~

Mainline for the CLI interface of the :mod:`yadr` package.

.. autofunction:: yadr.__main__.parse_cli
"""
from argparse import ArgumentParser

from yadr.yadr import add_dice_map, list_dice_maps, roll


def parse_cli() -> None:
    """Parse command line options and execute those commands.

    :returns: `None`.
    :rtype: NoneType

    Invoking :mod:`yadr`
    --------------------
    After installing :mod:`yadr` with :mod:`pip` or similar process,
    you can run it from the command line with the following::

        $ yadr

    Options can be passed into :mod:`yadr` to alter its behavior. The
    easiest way to view these options is to invoke the help::

        $ yadr -h
    """
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
        nargs='?',
        type=str
    )
    p.add_argument(
        '--list_dice_maps', '-l',
        help='List the names of the default dice maps.',
        action='store_true'
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
    result = 'Use `yadr -h` to view the available options for running yadr.\n'
    dice_map = {}
    if args.add_dice_map:
        dice_map = add_dice_map(args.add_dice_map[0])
    elif args.list_dice_maps:
        result = list_dice_maps()
    if args.yadn:
        raw_result = roll(args.yadn, True, dice_map)
        result = str(raw_result)
    print(result)


if __name__ == '__main__':
    parse_cli()
