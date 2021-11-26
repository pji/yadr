"""
model
~~~~~

Common data elements for the yadr package.
"""
from collections import UserString
from enum import Enum
from typing import Generic, NamedTuple, Sequence, Union, Tuple, TypeVar


# Tokens.
class Token(Enum):
    START = 0
    AS_OPERATOR = 1
    BOOLEAN = 2
    CHOICE_OPERATOR = 3
    CHOICE_OPTIONS = 4
    COMPARISON_OPERATOR = 5
    DICE_OPERATOR = 6
    EX_OPERATOR = 7
    GROUP_OPEN = 8
    GROUP_CLOSE = 9
    MD_OPERATOR = 10
    MEMBER = 11
    MEMBER_DELIMITER = 12
    NEGATIVE_SIGN = 13
    NUMBER = 14
    OPERATOR = 15
    OPTIONS_OPERATOR = 16
    POOL = 17
    POOL_CLOSE = 18
    POOL_DEGEN_OPERATOR = 19
    POOL_END = 20
    POOL_GEN_OPERATOR = 21
    POOL_OPEN = 22
    POOL_OPERATOR = 23
    QUALIFIER = 24
    QUALIFIER_END = 25
    QUALIFIER_DELIMITER = 26
    ROLL_DELIMITER = 27
    U_POOL_DEGEN_OPERATOR = 28
    WHITESPACE = 29
    END = 30


op_tokens = (
    Token.CHOICE_OPERATOR,
    Token.COMPARISON_OPERATOR,
    Token.DICE_OPERATOR,
    Token.POOL_GEN_OPERATOR,
    Token.POOL_DEGEN_OPERATOR,
    Token.POOL_OPERATOR,
    Token.U_POOL_DEGEN_OPERATOR,
    Token.OPTIONS_OPERATOR,
    Token.OPERATOR,
    Token.AS_OPERATOR,
    Token.MD_OPERATOR,
    Token.EX_OPERATOR,
)
id_tokens = (
    Token.BOOLEAN,
    Token.NUMBER,
    Token.POOL,
    Token.QUALIFIER,
)
symbols = {
    Token.START: '',
    Token.AS_OPERATOR: '+ -',
    Token.BOOLEAN: 'T F',
    Token.CHOICE_OPERATOR: '?',
    Token.CHOICE_OPTIONS: '',
    Token.COMPARISON_OPERATOR: '< > >= <= != ==',
    Token.DICE_OPERATOR: 'd d! dc dh dl dw',
    Token.EX_OPERATOR: '^',
    Token.GROUP_OPEN: '(',
    Token.GROUP_CLOSE: ')',
    Token.MEMBER_DELIMITER: ',',
    Token.MD_OPERATOR: '* / %',
    Token.NEGATIVE_SIGN: '-',
    Token.NUMBER: '0 1 2 3 4 5 6 7 8 9',
    Token.OPTIONS_OPERATOR: ':',
    Token.POOL_CLOSE: ']',
    Token.POOL: '',
    Token.POOL_END: '',
    Token.POOL_OPEN: '[',
    Token.POOL_DEGEN_OPERATOR: 'nb ns',
    Token.POOL_GEN_OPERATOR: 'g g!',
    Token.POOL_OPERATOR: 'pa pb pc pf ph pl pr p%',
    Token.QUALIFIER: '',
    Token.QUALIFIER_DELIMITER: '"',
    Token.QUALIFIER_END: '',
    Token.ROLL_DELIMITER: ';',
    Token.U_POOL_DEGEN_OPERATOR: 'C N S',
}
tokens = {k: v.split() for k,v in symbols.items()}
tokens[Token.WHITESPACE] = [' ', '\t', '\n']


# Classes.
class Char(UserString):
    """A string with YADN detections."""
    tokens = tokens

    def is_start(self, token: Token) -> bool:
        valid = {s[0] for s in self.tokens[token]}
        return self.data in valid

    def is_still(self, token: Token) -> bool:
        tokens = self.tokens[token]
        relevant = [item for item in tokens if len(item) > 1]
        if relevant:
            valid = {s[1] for s in relevant}
            return self.data in valid
        return False


class CompoundResult(Tuple):
    """The result of multiple rolls."""


# Types.
Result = Union[int, Tuple[int], None]
T = TypeVar('T', str, int, Tuple[int])
TokenInfo = tuple[Token, T]
