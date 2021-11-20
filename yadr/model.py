"""
model
~~~~~

Common data elements for the yadr package.
"""
from enum import Enum
from typing import Generic, NamedTuple, Tuple, TypeVar

# Common data.
OPERATORS = '+ - * / ^'.split()
DICE_OPERATORS = 'd d! dc dh dl dp'.split()
POOL_OPERATORS = 'p pa pb pc pf ph pl pr'.split()
U_POOL_DEGEN_OPERATORS = 'N S'.split()
POOL_DEGEN_OPERATORS = 'nb ns'.split()


class Token(Enum):
    START = 0
    WHITESPACE = 1
    NUMBER = 2
    OPERATOR = 3
    OPEN_GROUP = 4
    CLOSE_GROUP = 5
    MEMBER_DELIMITER = 6
    MEMBER = 7
    POOL_OPEN = 8
    POOL_CLOSE = 9
    POOL = 10
    DICE_OPERATOR = 11
    POOL_GEN_OPERATOR = 12
    POOL_OPERATOR = 13
    U_POOL_DEGEN_OPERATOR = 14
    POOL_DEGEN_OPERATOR = 15
    POOL_END = 16
    END = 17


# Types.
T = TypeVar('T', str, int, Tuple[int])
TokenInfo = tuple[Token, T]
