"""
model
~~~~~

Common data elements for the yadr package.
"""
from enum import Enum
from typing import Generic, NamedTuple, TypeVar

# Common data.
OPERATORS = '+ - * / ^ d'.split()


class Token(Enum):
    START = 0
    NUMBER = 1
    OPERATOR = 2
    WHITESPACE = 3
    OPEN_GROUP = 4
    CLOSE_GROUP = 5
    END = 6


# Types.
T = TypeVar('T', str, int)
TokenInfo = tuple[Token, T]
