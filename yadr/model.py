"""
model
~~~~~

Common data elements for the yadr package.
"""
from collections import UserString
from enum import Enum
from typing import Generic, NamedTuple, Sequence, Tuple, TypeVar

# Common data.
OPERATORS = '+ - * / ^'.split()
DICE_OPERATORS = 'd d! dc dh dl dw'.split()
POOL_GEN_OPERATORS = 'g g!'.split()
POOL_OPERATORS = 'p pa pb pc pf ph pl pr p%'.split()
U_POOL_DEGEN_OPERATORS = 'C N S'.split()
POOL_DEGEN_OPERATORS = 'nb ns'.split()
ROLL_DELIMITER = ';'


class Token(Enum):
    START = 0
    WHITESPACE = 1
    NUMBER = 2
    OPERATOR = 3
    GROUP_OPEN = 4
    GROUP_CLOSE = 5
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
    ROLL_DELIMITER = 17
    NEGATIVE_SIGN = 18
    END = 19


class Char(UserString):
    """A string with YADN detections."""
    tokens: dict[Token, Sequence[str]] = {
        Token.GROUP_OPEN: '(',
        Token.GROUP_CLOSE: ')',
        Token.MEMBER_DELIMITER: ',',
        Token.OPERATOR: '^*/+-',
        Token.DICE_OPERATOR: 'd d! dc dh dl dw'.split(),
        Token.POOL_OPEN: '[',
        Token.POOL_CLOSE: ']',
        Token.POOL_GEN_OPERATOR: 'g g!'.split(),
        Token.POOL_OPERATOR: 'p pa pb pc pf ph pl pr p%'.split(),
        Token.U_POOL_DEGEN_OPERATOR: 'C N S'.split(),
        Token.POOL_DEGEN_OPERATOR: 'nb ns'.split(),
        Token.ROLL_DELIMITER: ';',
        Token.NEGATIVE_SIGN: '-',
    }

    def is_dice_op(self) -> bool:
        return self.data in self.tokens[Token.DICE_OPERATOR]

    def is_group_open(self) -> bool:
        return self.data in self.tokens[Token.GROUP_OPEN]

    def is_group_close(self) -> bool:
        return self.data in self.tokens[Token.GROUP_CLOSE]

    def is_member_delim(self) -> bool:
        return self.data in self.tokens[Token.MEMBER_DELIMITER]

    def is_operator(self) -> bool:
        return self.data in self.tokens[Token.OPERATOR]

    def is_pool_open(self) -> bool:
        return self.data in self.tokens[Token.POOL_OPEN]

    def is_pool_close(self) -> bool:
        return self.data in self.tokens[Token.POOL_CLOSE]

    def is_pool_gen_op(self) -> bool:
        return self.data in self.tokens[Token.POOL_GEN_OPERATOR]

    def is_pool_op(self) -> bool:
        return self.data in self.tokens[Token.POOL_OPERATOR]

    def is_u_pool_degen_op(self) -> bool:
        return self.data in self.tokens[Token.U_POOL_DEGEN_OPERATOR]

    def is_pool_degen_op(self) -> bool:
        return self.data in self.tokens[Token.POOL_DEGEN_OPERATOR]

    def is_roll_delim(self) -> bool:
        return self.data in self.tokens[Token.ROLL_DELIMITER]

    def is_negative_sign(self) -> bool:
        return self.data in self.tokens[Token.NEGATIVE_SIGN]

    def still_dice_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.DICE_OPERATOR][1:]]
        return self.data in valid

    def still_pool_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_OPERATOR][1:]]
        return self.data in valid

    def still_pool_degen_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_DEGEN_OPERATOR]]
        return self.data in valid

    def still_pool_gen_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_GEN_OPERATOR][1:]]
        return self.data in valid


# Types.
Result = TypeVar('Result', int, Tuple[int], None)
T = TypeVar('T', str, int, Tuple[int])
TokenInfo = tuple[Token, T]


class CompoundResult(Tuple):
    """The result of multiple rolls."""
