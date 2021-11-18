"""
model
~~~~~

Common data elements for the yadr package.
"""
from enum import Enum
from typing import Generic, NamedTuple, TypeVar

# Common data.
OPERATORS = '+ - * / ^'.split()
DICE_OPERATORS = 'd d! dh'.split()


class Token(Enum):
    START = 0
    NUMBER = 1
    OPERATOR = 2
    WHITESPACE = 3
    OPEN_GROUP = 4
    CLOSE_GROUP = 5
    DICE_OPERATOR = 6
    END = 7


# Types.
T = TypeVar('T', str, int)
TokenInfo = tuple[Token, T]
