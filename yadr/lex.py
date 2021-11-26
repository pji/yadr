"""
lex
~~~

A lexer for `yadr` dice notation.
"""
from functools import wraps
from typing import Callable, Optional

from yadr.base import BaseLexer
from yadr.model import (
    BaseToken,
    CompoundResult,
    Result,
    Token,
    TokenInfo,
    tokens
)


# Lexers.
class Lexer(BaseLexer):
    """A state-machine to lex dice notation."""
    def __init__(self) -> None:
        bracket_states: dict[BaseToken, BaseToken] = {
            Token.NEGATIVE_SIGN: Token.NUMBER,
            Token.QUALIFIER_DELIMITER: Token.QUALIFIER,
            Token.POOL_OPEN: Token.POOL,
        }
        state_map: dict[BaseToken, Callable] = {
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
        tokens_: dict[BaseToken, list[str]] = tokens
        result_map: dict[BaseToken, Callable] = {
            Token.BOOLEAN: self._tf_boolean,
            Token.NUMBER: self._tf_number,
            Token.POOL: self._tf_pool,
            Token.QUALIFIER: self._tf_qualifier,
        }
        no_store: list[BaseToken] = [
            Token.WHITESPACE,
            Token.START,
            Token.POOL_END,
            Token.QUALIFIER_END,
        ]
        super().__init__(
            bracket_states,
            state_map,
            tokens_,
            result_map,
            no_store
        )
        self.process = self._start

    # Value transforms.
    def _tf_boolean(self, value: str) -> bool:
        if value == 'T':
            return True
        return False

    def _tf_number(self, value: str) -> int:
        return int(value)

    def _tf_pool(self, value: str) -> tuple[int, ...]:
        plexer = PoolLexer()
        lexed = plexer.lex(value)
        gen = (L[1] for L in lexed if L[0] == Token.NUMBER)
        return tuple(gen)                           # type: ignore

    def _tf_qualifier(self, value: str) -> str:
        return value[1:-1]

    # Lexing rules.
    def _as_operator(self, char: str) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _boolean(self, char: str) -> None:
        """Processing a boolean."""
        can_follow = [
            Token.CHOICE_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _choice_operator(self, char: str) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.QUALIFIER,
            Token.QUALIFIER_DELIMITER,
            Token.CHOICE_OPTIONS,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _comparison_operator(self, char: str) -> None:
        """Processing a comparison operator."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NEGATIVE_SIGN,
            Token.NUMBER,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _dice_operator(self, char: str) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _ex_operator(self, char: str) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _group_close(self, char: str) -> None:
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

    def _group_open(self, char: str) -> None:
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

    def _map_close(self, char: str) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _map_open(self, char: str) -> None:
        """Processing a choice operator."""
        can_follow = [
            Token.MAP_CLOSE,
            Token.QUALIFIER,
            Token.QUALIFIER_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _md_operator(self, char: str) -> None:
        """Processing an operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _number(self, char: str) -> None:
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

    def _options_operator(self, char: str) -> None:
        """Processing an options operator."""
        can_follow = [
            Token.QUALIFIER_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool(self, char: str) -> None:
        """Processing a pool."""
        self.buffer += char
        if self._is_token_start(Token.POOL_CLOSE, char):
            new_state = Token.POOL_END
            self._change_state(new_state, char)

    def _pool_end(self, char: str) -> None:
        """Processing after a pool."""
        can_follow = [
            Token.GROUP_CLOSE,
            Token.POOL_DEGEN_OPERATOR,
            Token.POOL_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_gen_operator(self, char: str) -> None:
        """Processing an pool generation operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _qualifier(self, char: str) -> None:
        """Processing a qualifier."""
        self.buffer += char
        if self._is_token_start(Token.QUALIFIER_DELIMITER, char):
            new_state = Token.QUALIFIER_END
            self._change_state(new_state, char)

    def _qualifier_end(self, char: str) -> None:
        """Process after a qualifier."""
        can_follow = [
            Token.OPTIONS_OPERATOR,
            Token.ROLL_DELIMITER,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_degen_operator(self, char: str) -> None:
        """Processing a pool degeneration operator."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.GROUP_OPEN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _pool_operator(self, char: str) -> None:
        """Lex pool operators."""
        can_follow = [
            Token.GROUP_OPEN,
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.U_POOL_DEGEN_OPERATOR,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _roll_delimiter(self, char: str) -> None:
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

    def _start(self, char: str) -> None:
        """The starting state."""
        if self.tokens:
            self.tokens = []
        self._roll_delimiter(char)

    def _u_pool_degen_operator(self, char: str) -> None:
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

    def _whitespace(self, char: str) -> None:
        if char.isspace():
            return None
        prev_state: BaseToken = Token.START
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
        bracket_states: dict[BaseToken, BaseToken] = {
            Token.NEGATIVE_SIGN: Token.NUMBER,
            Token.QUALIFIER_DELIMITER: Token.QUALIFIER,
            Token.POOL_OPEN: Token.POOL,
        }
        state_map: dict[BaseToken, Callable] = {
            Token.NUMBER: self._number,
            Token.MEMBER_DELIMITER: self._member_delimiter,
            Token.POOL: self._pool,
            Token.POOL_CLOSE: self._pool_close,
            Token.START: self._start,
            Token.WHITESPACE: self._whitespace,
            Token.END: self._start,
        }
        tokens_: dict[BaseToken, list[str]] = tokens
        result_map: dict[BaseToken, Callable] = {
            Token.NUMBER: self._tf_number,
        }
        no_store: list[BaseToken] = [
            Token.POOL_OPEN,
            Token.POOL_CLOSE,
            Token.WHITESPACE,
        ]
        super().__init__(
            bracket_states,
            state_map,
            tokens,
            result_map,
            no_store
        )
        self.process = self._start

    # Value transforms.
    def _tf_number(self, value: str) -> int:
        return int(value)

    # Lexing rules.
    def _member_delimiter(self, char: str) -> None:
        """Lex a member delimiter."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _number(self, char: str) -> None:
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

    def _pool_close(self, char: str) -> None:
        """Lex a pool close."""
        msg = '[ cannot follow a ]'
        raise ValueError(msg)

    def _pool(self, char: str) -> None:
        """Lex a pool open."""
        can_follow = [
            Token.NUMBER,
            Token.NEGATIVE_SIGN,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _start(self, char: str) -> None:
        """Start lexing the string."""
        can_follow = [
            Token.POOL_OPEN,
        ]
        self._check_char(char, can_follow)

    def _whitespace(self, char: str) -> None:
        """Processing whitespace."""
        can_follow = [
            Token.NUMBER,
            Token.MEMBER_DELIMITER,
            Token.NEGATIVE_SIGN,
            Token.POOL_CLOSE,
            Token.WHITESPACE,
        ]
        self._check_char(char, can_follow)
