"""
lex
~~~

A lexer for `yadr` dice notation.
"""
from functools import wraps
from typing import Callable, Optional

from yadr.model import (
    Char,
    CompoundResult,
    Result,
    Token,
    TokenInfo,
)


# Base class.
class BaseLexer:
    def __init__(self) -> None:
        self.buffer = Char('')
        self.tokens: list[TokenInfo] = []
        self.state = Token.START
        self.state_map: dict[Token, Callable] = {}
        self.process = self._start

    # Public methods.
    def lex(self, text: str | Char) -> tuple[TokenInfo, ...]:
        """Lex a dice notation string."""
        chars = [Char(c) for c in text]
        for char in chars:
            self.process(char)
        else:
            self._change_state(Token.START, Char(''))
        return tuple(self.tokens)

    # Private operation method.
    def _change_state(self, new_state: Token, char: Char) -> None:
        ...

    def _check_char(self, char: Char, can_follow: list[Token]) -> None:
        """Determine how to process a character."""
        new_state: Optional[Token] = None

        # If the character doesn't change the state, add it to the
        # buffer and stop processing.
        if char.is_still(self.state):
            self.buffer += char
            return None

        # Check to see if the character starts a token that is allowed
        # to follow the current token. Stop looking once you find one.
        for token in can_follow:
            if char.is_start(token):
                new_state = token
                break

        # If not, throw an exception. Since whitespace isn't a token in
        # YADN, an exception saying a character can't follow WHITESPACE
        # isn't useful. Therefore handle that case by looking at the
        # last stored token.
        else:
            state = self.state.name
            if state == 'WHITESPACE' and self.tokens:
                state = self.tokens[-1][0].name
            elif state == 'WHITESPACE':
                state = 'START'
            if state == 'QUALIFIER_END':
                state = 'QUALIFIER'

            if state == 'START':
                msg = f'Cannot start with {char}.'
            else:
                article = 'a'
                if state[0] in 'AEIOU':
                    article = 'an'
                msg = f'{char} cannot follow {article} {state}.'

            raise ValueError(msg)

        # Some tokens start a state that doesn't match the token.
        if new_state == Token.NEGATIVE_SIGN:
            new_state = Token.NUMBER
        elif new_state == Token.QUALIFIER_DELIMITER:
            new_state = Token.QUALIFIER
        elif new_state == Token.POOL_OPEN:
            new_state = Token.POOL

        # If the state changed, change the state.
        if new_state:
            self._change_state(new_state, char)

    # Lexing rules.
    def _start(self, char: Char) -> None:
        ...


# Lexers.
class Lexer(BaseLexer):
    """A state-machine to lex dice notation."""
    def __init__(self) -> None:
        super().__init__()
        self.state_map = {
            Token.START: self._start,
            Token.AS_OPERATOR: self._as_operator,
            Token.BOOLEAN: self._boolean,
            Token.CHOICE_OPERATOR: self._choice_operator,
            Token.COMPARISON_OPERATOR: self._comparison_operator,
            Token.DICE_OPERATOR: self._dice_operator,
            Token.EX_OPERATOR: self._ex_operator,
            Token.GROUP_OPEN: self._group_open,
            Token.GROUP_CLOSE: self._group_close,
            Token.MD_OPERATOR: self._md_operator,
            Token.NUMBER: self._number,
            Token.OPTIONS_OPERATOR: self._options_operator,
            Token.POOL: self._pool,
            Token.POOL_DEGEN_OPERATOR: self._pool_degen_operator,
            Token.POOL_END: self._pool_end,
            Token.POOL_GEN_OPERATOR: self._pool_gen_operator,
            Token.POOL_OPERATOR: self._pool_operator,
            Token.QUALIFIER: self._qualifier,
            Token.QUALIFIER_END: self._qualifier_end,
            Token.ROLL_DELIMITER: self._roll_delimiter,
            Token.U_POOL_DEGEN_OPERATOR: self._u_pool_degen_operator,
            Token.WHITESPACE: self._whitespace,
            Token.END: self._start,

            # Mapping tokens.
            Token.MAP_OPEN: self._map_open,
            Token.MAP_CLOSE: self._map_close,
        }
        self.process = self._start

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: Char) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if self.state not in [Token.WHITESPACE,
                              Token.START,
                              Token.POOL_END,
                              Token.QUALIFIER_END]:
            value: Char | str | int | bool | tuple[int, ...] = self.buffer
            if self.state == Token.NUMBER and isinstance(value, Char):
                value = int(value)
            elif self.state == Token.QUALIFIER and isinstance(value, Char):
                value = str(value[1:])
            elif self.state == Token.POOL and isinstance(value, Char):
                plexer = PoolLexer()
                lexed = plexer.lex(value)
                value = tuple(L[1] for L in lexed if L[0] == Token.NUMBER)
#                 value = plexer.lex(value)
            elif self.state in [Token.POOL, Token.NUMBER]:
                msg = f'value must be str, was {type(value)}'
                raise TypeError(msg)
            elif self.state == Token.BOOLEAN:
                value = False
                if self.buffer == 'T':
                    value = True
            token_info = (self.state, value)
            self.tokens.append(token_info)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    # Lexing rules.
    def _as_operator(self, char: Char) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _boolean(self, char: Char) -> None:
        """Processing a boolean."""
        can_follow = [
            Token.CHOICE_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _choice_operator(self, char: Char) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.QUALIFIER,
            Token.QUALIFIER_DELIMITER,
            Token.CHOICE_OPTIONS,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _comparison_operator(self, char: Char) -> None:
        """Processing a comparison operator."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NEGATIVE_SIGN,
            Token.NUMBER,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _dice_operator(self, char: Char) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _ex_operator(self, char: Char) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _group_close(self, char: Char) -> None:
        """Processing a close group token."""
        can_follow = [
            Token.AS_OPERATOR,
            Token.MD_OPERATOR,
            Token.EX_OPERATOR,
            Token.DICE_OPERATOR,
            Token.GROUP_CLOSE,
            Token.POOL_OPERATOR,
            Token.POOL_GEN_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _group_open(self, char: Char) -> None:
        """Processing an open group token."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.POOL_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _map_close(self, char: Char) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _map_open(self, char: Char) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.MAP_CLOSE,
            Token.QUALIFIER,
            Token.QUALIFIER_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _md_operator(self, char: Char) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _number(self, char: Char) -> None:
        """Processing a number."""
        can_follow = [
            Token.AS_OPERATOR,
            Token.COMPARISON_OPERATOR,
            Token.DICE_OPERATOR,
            Token.EX_OPERATOR,
            Token.GROUP_CLOSE,
            Token.MD_OPERATOR,
            Token.POOL_GEN_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]

        # Check here if the character is a digit because the checks in
        # Char are currently limited to tokens that no longer than two
        # characters. Check if the state is a number because white
        # space also ends up here, and we want white space to separate
        # numbers.
        if char.isdigit() and self.state == Token.NUMBER:
            self.buffer += char
        else:
            self._check_char(char, can_follow)

    def _options_operator(self, char: Char) -> None:
        """Processing an options operator."""
        can_follow = [
            Token.QUALIFIER_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool(self, char: Char) -> None:
        """Processing a pool."""
        self.buffer += char
        if char.is_start(Token.POOL_CLOSE):
            new_state = Token.POOL_END
            self._change_state(new_state, char)

    def _pool_end(self, char: Char) -> None:
        """Processing after a pool."""
        can_follow = [
            Token.GROUP_CLOSE,
            Token.POOL_DEGEN_OPERATOR,
            Token.POOL_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_gen_operator(self, char: Char) -> None:
        """Processing an pool generation operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _qualifier(self, char: Char) -> None:
        """Processing a qualifier."""
        if not char.is_start(Token.QUALIFIER_DELIMITER):
            self.buffer += char
        else:
            new_state = Token.QUALIFIER_END
            self._change_state(new_state, char)

    def _qualifier_end(self, char: Char) -> None:
        """Process after a qualifier."""
        can_follow = [
            Token.OPTIONS_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_degen_operator(self, char: Char) -> None:
        """Processing a pool degeneration operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_operator(self, char: Char) -> None:
        """Lex pool operators."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _roll_delimiter(self, char: Char) -> None:
        """Lex roll delimiters."""
        can_follow = [
            Token.MAP_OPEN,
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.BOOLEAN,
            Token.GROUP_OPEN,
            Token.POOL_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.QUALIFIER_DELIMITER,
            Token.BOOLEAN,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _start(self, char: Char) -> None:
        """The starting state."""
        if self.tokens:
            self.tokens = []
        self._roll_delimiter(char)

    def _u_pool_degen_operator(self, char: Char) -> None:
        """Processing a unary pool degeneration operator."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.POOL_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _whitespace(self, char: Char) -> None:
        if char.isspace():
            return None
        prev_state = Token.START
        if self.tokens:
            prev_state = self.tokens[-1][0]
        if prev_state == Token.POOL:
            prev_state = Token.POOL_END
        elif prev_state == Token.QUALIFIER:
            prev_state = Token.QUALIFIER_END
        self.ws_process = self.state_map[prev_state]
        self.ws_process(char)


class PoolLexer(BaseLexer):
    def __init__(self) -> None:
        super().__init__()
        self.state_map = {
            Token.NUMBER: self._number,
            Token.MEMBER_DELIMITER: self._member_delimiter,
            Token.POOL: self._pool,
            Token.POOL_CLOSE: self._pool_close,
            Token.START: self._start,
            Token.WHITESPACE: self._whitespace,
            Token.END: self._start,
        }
        self.process = self._start

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: Char) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if self.state in [Token.NUMBER, Token.MEMBER_DELIMITER]:
            value: int | Char = self.buffer
            if self.state == Token.NUMBER:
                value = int(value)
            token_info = (self.state, value)
            self.tokens.append(token_info)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    # Lexing rules.
    def _member_delimiter(self, char: Char) -> None:
        """Lex a member delimiter."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _number(self, char: Char) -> None:
        """Lex a member."""
        can_follow = [
            Token.MEMBER_DELIMITER,
            Token.POOL_CLOSE,
            Token.WHITESPACE,
        ]

        # Check here if the character is a digit because the checks in
        # Char are currently limited to tokens that no longer than two
        # characters. Check if the state is a number because white
        # space also ends up here, and we want white space to separate
        # numbers.
        if char.isdigit() and self.state == Token.NUMBER:
            self.buffer += char
        else:
            self._check_char(char, can_follow)

    def _pool_close(self, char: Char) -> None:
        """Lex a pool close."""
        msg = '[ cannot follow a ]'
        raise ValueError(msg)

    def _pool(self, char: Char) -> None:
        """Lex a pool open."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _start(self, char: Char) -> None:
        """Start lexing the string."""
        can_follow = [
            Token.POOL_OPEN,
        ]
        self._check_char(char, can_follow)

    def _whitespace(self, char: Char) -> None:
        """Processing whitespace."""
        can_follow = [
            Token.NUMBER,
            Token.MEMBER_DELIMITER,
            Token.NEGATIVE_SIGN,
            Token.POOL_CLOSE,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)
