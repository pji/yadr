"""
model
~~~~~

Common data elements for the yadr package.
"""
from collections import UserString
from enum import Enum
from typing import Generic, NamedTuple, Sequence, Tuple, TypeVar


# Tokens.
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
    QUALIFIER_DELIMITER = 19
    QUALIFIER = 20
    QUALIFIER_CLOSE = 21
    OPTIONS_OPERATOR = 22
    COMPARISON_OPERATOR = 23
    BOOLEAN = 24
    CHOICE_OPERATOR = 25
    CHOICE_OPTIONS = 26
    AS_OPERATOR = 27
    MD_OPERATOR = 28
    EX_OPERATOR = 29
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


# Classes.
class Char(UserString):
    """A string with YADN detections."""
    tokens: dict[Token, Sequence[str]] = {
        Token.GROUP_OPEN: '(',
        Token.GROUP_CLOSE: ')',
        Token.MEMBER_DELIMITER: ',',
        Token.AS_OPERATOR: '+-',
        Token.MD_OPERATOR: '*/%',
        Token.EX_OPERATOR: '^',
        Token.DICE_OPERATOR: 'd d! dc dh dl dw'.split(),
        Token.POOL_OPEN: '[',
        Token.POOL_CLOSE: ']',
        Token.POOL_GEN_OPERATOR: 'g g!'.split(),
        Token.POOL_OPERATOR: 'pa pb pc pf ph pl pr p%'.split(),
        Token.U_POOL_DEGEN_OPERATOR: 'C N S'.split(),
        Token.POOL_DEGEN_OPERATOR: 'nb ns'.split(),
        Token.ROLL_DELIMITER: ';',
        Token.NEGATIVE_SIGN: '-',
        Token.QUALIFIER_DELIMITER: '"',
        Token.OPTIONS_OPERATOR: ':',
        Token.COMPARISON_OPERATOR: '< > >= <= != =='.split(),
        Token.BOOLEAN: 'T F'.split(),
        Token.CHOICE_OPERATOR: '?',
    }

    # Change state tests.
    def is_as_op(self) -> bool:
        return self.data in self.tokens[Token.AS_OPERATOR]

    def is_boolean(self) -> bool:
        valid_char = {op[0] for op in self.tokens[Token.BOOLEAN]}
        return self.data in valid_char

    def is_choice_op(self) -> bool:
        return self.data == self.tokens[Token.CHOICE_OPERATOR]

    def is_comparison_op(self) -> bool:
        valid_char = {op[0] for op in self.tokens[Token.COMPARISON_OPERATOR]}
        return self.data in valid_char

    def is_dice_op(self) -> bool:
        return self.data in self.tokens[Token.DICE_OPERATOR]

    def is_ex_op(self) -> bool:
        return self.data in self.tokens[Token.EX_OPERATOR]

    def is_group_open(self) -> bool:
        return self.data in self.tokens[Token.GROUP_OPEN]

    def is_group_close(self) -> bool:
        return self.data in self.tokens[Token.GROUP_CLOSE]

    def is_md_op(self) -> bool:
        return self.data in self.tokens[Token.MD_OPERATOR]

    def is_member_delim(self) -> bool:
        return self.data in self.tokens[Token.MEMBER_DELIMITER]

    def is_number(self) -> bool:
        return self.data.isdigit() or self.is_negative_sign()

    def is_negative_sign(self) -> bool:
        return self.data in self.tokens[Token.NEGATIVE_SIGN]

    def is_options_operator(self) -> bool:
        return self.data == self.tokens[Token.OPTIONS_OPERATOR]

    def is_pool_close(self) -> bool:
        return self.data in self.tokens[Token.POOL_CLOSE]

    def is_pool_degen_op(self) -> bool:
        valid_char = {op[0] for op in self.tokens[Token.POOL_DEGEN_OPERATOR]}
        return self.data in valid_char

    def is_pool_gen_op(self) -> bool:
        return self.data in self.tokens[Token.POOL_GEN_OPERATOR]

    def is_pool_op(self) -> bool:
        valid_char = {op[0] for op in self.tokens[Token.POOL_OPERATOR]}
        return self.data in valid_char

    def is_pool_open(self) -> bool:
        return self.data in self.tokens[Token.POOL_OPEN]

    def is_qualifier_delim(self) -> bool:
        return self.data in self.tokens[Token.QUALIFIER_DELIMITER]

    def is_roll_delim(self) -> bool:
        return self.data in self.tokens[Token.ROLL_DELIMITER]

    def is_u_pool_degen_op(self) -> bool:
        return self.data in self.tokens[Token.U_POOL_DEGEN_OPERATOR]

    # Maintain state tests.
    def still_comparison_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.COMPARISON_OPERATOR][2:]]
        return self.data in valid

    def still_dice_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.DICE_OPERATOR][1:]]
        return self.data in valid

    def still_pool_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_OPERATOR]]
        return self.data in valid

    def still_pool_degen_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_DEGEN_OPERATOR]]
        return self.data in valid

    def still_pool_gen_op(self) -> bool:
        valid = [s[1] for s in self.tokens[Token.POOL_GEN_OPERATOR][1:]]
        return self.data in valid

    def still_qualifier(self) -> bool:
        return (self.data.isalpha()
                or self.data.isdigit()
                or self.data.isspace())


class CompoundResult(Tuple):
    """The result of multiple rolls."""


# Types.
Result = TypeVar('Result', int, Tuple[int], None)
T = TypeVar('T', str, int, Tuple[int])
TokenInfo = tuple[Token, T]
