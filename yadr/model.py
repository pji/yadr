"""
model
~~~~~

Common data elements for the yadr package.
"""
from collections import UserString
from enum import Enum, EnumMeta, auto
from typing import Generic, NamedTuple, Sequence, Union, Tuple, TypeVar


# YADN Tokens.
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

    # Dice mapping tokens.
    MAP_OPEN = auto()
    MAP_CLOSE = auto()


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

# Symbols for YADN tokens.
# This maps the symbols used in YADN to tokens for lexing. This isn't
# a direct mapping from the YADN specification document. It's just
# the basic things that can be handled by the lexer easily. More
# complicated things are handled through the lexer itself.
yadn_symbols_raw = {
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
    Token.WHITESPACE: '',

    # Dice mapping symbols.
    Token.MAP_OPEN: '{',
    Token.MAP_CLOSE: '}',
}


# YADN dice mapping tokens.
# These are the YADN tokens that are specific to dice maps. These are
# split out so they won't confuse the main YADN lexer. Dice maps are
# parsed by their own lexer.
class MapToken(Enum):
    START = auto()
    END = auto()
    KEY = auto()
    KV_DELIMITER = auto()
    MAP_CLOSE = auto()
    MAP_OPEN = auto()
    NAME = auto()
    NAME_DELIMITER = auto()
    NEGATIVE_SIGN = auto()
    NUMBER = auto()
    PAIR_DELIMITER = auto()
    QUALIFIER = auto()
    QUALIFIER_DELIMITER = auto()
    QUALIFIER_END = auto()
    VALUE = auto()
    WHITESPACE = auto()


# Symbols for YADN dice mapping tokens.
map_symbols_raw = {
    MapToken.START: '',
    MapToken.END: '',
    MapToken.KEY: '',
    MapToken.KV_DELIMITER: ':',
    MapToken.MAP_CLOSE: '}',
    MapToken.MAP_OPEN: '{',
    MapToken.NAME: '',
    MapToken.NAME_DELIMITER: '=',
    MapToken.NEGATIVE_SIGN: '-',
    MapToken.NUMBER: '0 1 2 3 4 5 6 7 8 9',
    MapToken.PAIR_DELIMITER: ',',
    MapToken.QUALIFIER: '',
    MapToken.QUALIFIER_DELIMITER: '"',
    MapToken.QUALIFIER_END: '',
    MapToken.VALUE: '',
    MapToken.WHITESPACE: '',
}


# Classes.
class CompoundResult(Tuple):
    """The result of multiple rolls."""


# Types.
BaseToken = Union[Token, MapToken]
Result = Union[int, bool, str, Tuple[int], None]
TokenInfo = tuple[BaseToken, Union[Result, CompoundResult]]


# Symbols by token.
def split_symbols(d: dict, enum: EnumMeta) -> dict[BaseToken, list[str]]:
    """Split the symbol strings and add whitespace."""
    split_symbols = {k: v.split() for k, v in d.items()}
    for member in enum:                                     # type: ignore
        if member.name == 'WHITESPACE':
            split_symbols[member] = [' ', '\t', '\n']
            break
    return split_symbols


symbols = split_symbols(yadn_symbols_raw, Token)
map_symbols = split_symbols(map_symbols_raw, MapToken)
