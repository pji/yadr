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


# Lexers.
class Lexer:
    """A state-machine to lex dice notation."""
    def __init__(self) -> None:
        self.buffer = Char('')
        self.tokens: list[TokenInfo] = []

        # Lexer is a state machine, so its behavior changes based on its
        # current state. This is implemented by assigning the `process`
        # method to the private processing method associated with the
        # state. The initial state of the Lexer is "START".
        self.state = Token.START
        self.state_map = {
            Token.START: self._start,
            Token.NUMBER: self._number,
            Token.OPERATOR: self._operator,
            Token.GROUP_OPEN: self._open_group,
            Token.GROUP_CLOSE: self._close_group,
            Token.DICE_OPERATOR: self._dice_operator,
            Token.POOL: self._pool,
            Token.POOL_END: self._pool_end,
            Token.POOL_OPERATOR: self._pool_operator,
            Token.U_POOL_DEGEN_OPERATOR: self._u_pool_degen_operator,
            Token.POOL_GEN_OPERATOR: self._pool_gen_operator,
            Token.POOL_DEGEN_OPERATOR: self._pool_degen_operator,
            Token.ROLL_DELIMITER: self._roll_delimiter,
            Token.WHITESPACE: self._whitespace,
            Token.END: self._start
        }
        self.process = self._start

    # Public methods.
    def lex(self, text: str) -> tuple[TokenInfo, ...]:
        """Lex a dice notation string."""
        chars = [Char(c) for c in text]
        for char in chars:
            self.process(char)
        else:
            self._change_state(Token.END, Char(''))
        return tuple(self.tokens)

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: Char) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if self.state not in [Token.WHITESPACE, Token.START, Token.POOL_END]:
            value: Char | int | tuple[int, ...] = self.buffer
            if self.state == Token.NUMBER and isinstance(value, Char):
                value = int(value)
            elif self.state == Token.POOL and isinstance(value, Char):
                plexer = PoolLexer()
                value = plexer.lex(value)
            elif self.state in [Token.POOL, Token.NUMBER]:
                msg = f'value must be str, was {type(value)}'
                raise TypeError(msg)
            token_info = (self.state, value)
            self.tokens.append(token_info)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    # Lexing rules.
    def _close_group(self, char: Char) -> None:
        """Processing a close group token."""
        if char.is_operator():
            new_state = Token.OPERATOR
        elif char.is_dice_op():
            new_state = Token.DICE_OPERATOR
        elif char.isspace():
            new_state = Token.WHITESPACE
        elif char.is_roll_delim():
            new_state = Token.ROLL_DELIMITER
        else:
            msg = f'{char} cannot follow a group.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _dice_operator(self, char: Char) -> None:
        """Processing an operator."""
        new_state: Token | None = None
        if char.still_dice_op():
            self.buffer += char
        elif char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char == '(':
            new_state = Token.GROUP_OPEN
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow dice operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _open_group(self, char: Char) -> None:
        """Processing an open group token."""
        if char.isdigit():
            new_state = Token.NUMBER
        elif char.is_u_pool_degen_op():
            new_state = Token.U_POOL_DEGEN_OPERATOR
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow (.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _number(self, char: Char) -> None:
        """Processing a number."""
        new_state: Token | None = None

        # Have to check state to avoid adding white space to the
        # number.
        if char.isdigit() and self.state == Token.NUMBER:
            self.buffer += char
        elif char.is_operator():
            new_state = Token.OPERATOR
        elif char.is_dice_op():
            new_state = Token.DICE_OPERATOR
        elif char.is_pool_gen_op():
            new_state = Token.POOL_GEN_OPERATOR
        elif char.is_group_close():
            new_state = Token.GROUP_CLOSE
        elif char.is_roll_delim():
            new_state = Token.ROLL_DELIMITER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a number.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _operator(self, char: Char) -> None:
        """Processing an operator."""
        if char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.is_group_open():
            new_state = Token.GROUP_OPEN
        elif char.is_u_pool_degen_op():
            new_state = Token.U_POOL_DEGEN_OPERATOR
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow an operator.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _pool(self, char: Char) -> None:
        """Processing a pool open."""
        new_state = None
        if char.isdigit():
            self.buffer += char
        elif char.is_negative_sign():
            self.buffer += char
        elif char.is_member_delim():
            self.buffer += char
        elif char.isspace():
            self.buffer += char
        elif char.is_pool_close():
            self.buffer += char
            new_state = Token.POOL_END
        else:
            msg = f'{char} cannot be in a pool.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _pool_end(self, char: Char) -> None:
        """Processing after a pool."""
        if char == 'p':
            new_state = Token.POOL_OPERATOR
        elif char == 'n':
            new_state = Token.POOL_DEGEN_OPERATOR
        elif char == ')':
            new_state = Token.GROUP_CLOSE
        elif char == ';':
            new_state = Token.ROLL_DELIMITER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a pool.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _pool_gen_operator(self, char: Char) -> None:
        """Processing an operator."""
        new_state: Token | None = None
        if char.still_pool_gen_op():
            self.buffer += char
        elif char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.is_group_open():
            new_state = Token.GROUP_OPEN
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow pool gen operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _u_pool_degen_operator(self, char: Char) -> None:
        """Processing a unary pool degeneration operator."""
        if char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.is_pool_open():
            new_state = Token.POOL
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow an unary pool degeneration operator.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _pool_degen_operator(self, char: Char) -> None:
        """Processing a pool degeneration operator."""
        new_state: Token | None = None
        if char.still_pool_degen_op():
            self.buffer += char
        elif char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.is_u_pool_degen_op():
            new_state = Token.U_POOL_DEGEN_OPERATOR
        elif char.is_group_open():
            new_state = Token.GROUP_OPEN
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a pool degeneration operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _pool_operator(self, char: Char) -> None:
        """Lex pool operators."""
        new_state = None
        if char.still_pool_op():
            self.buffer += char
        elif char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a pool operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _roll_delimiter(self, char: Char) -> None:
        """Lex roll delimiters."""
        if char.isdigit() or char.is_negative_sign():
            new_state = Token.NUMBER
        elif char.is_group_open():
            new_state = Token.GROUP_OPEN
        elif char.is_pool_open():
            new_state = Token.POOL
        elif char.is_u_pool_degen_op():
            new_state = Token.U_POOL_DEGEN_OPERATOR
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'Cannot start with {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _start(self, char: Char) -> None:
        """The starting state."""
        if self.tokens:
            self.tokens = []
        self._roll_delimiter(char)

    def _whitespace(self, char: Char) -> None:
        if char.isspace():
            return None
        prev_state = Token.START
        if self.tokens:
            prev_state = self.tokens[-1][0]
        if prev_state == Token.POOL:
            prev_state = Token.POOL_END
        self.ws_process = self.state_map[prev_state]
        self.ws_process(char)


class PoolLexer:
    def __init__(self) -> None:
        self.buffer = Char('')
        self.pool: list[int] = []
        self.state = Token.START
        self.state_map = {
            Token.MEMBER: self._member,
            Token.MEMBER_DELIMITER: self._member_delimiter,
            Token.POOL_CLOSE: self._pool_close,
            Token.POOL_OPEN: self._pool_open,
            Token.START: self._start,
            Token.WHITESPACE: self._whitespace,
        }
        self.process = self._start

    # Public methods.
    def lex(self, text: Char) -> tuple[int, ...]:
        """Lex a pool string from dice notation."""
        for char in text:
            self.process(Char(char))
        return tuple(self.pool)

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: Char,
                      store: bool = True) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if store:
            value = int(self.buffer)
            self.pool.append(value)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    # Lexing rules.
    def _member(self, char: Char) -> None:
        """Lex a member."""
        new_state = None
        if char.is_member_delim():
            new_state = Token.MEMBER_DELIMITER
        elif char.is_pool_close():
            new_state = Token.POOL_CLOSE
        elif char.isdigit():
            self.buffer += char
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a member'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _member_delimiter(self, char: Char) -> None:
        """Lex a member delimiter."""
        if char.isdigit() or char == '-':
            new_state = Token.MEMBER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a ,'
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _pool_close(self, char: Char) -> None:
        """Lex a pool close."""
        msg = '[ cannot follow a ]'
        raise ValueError(msg)

    def _pool_open(self, char: Char) -> None:
        """Lex a pool open."""
        if char.isdigit() or char == '-':
            new_state = Token.MEMBER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = '{} cannot follow a \x007b'.format(char)
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _start(self, char: Char) -> None:
        """Start lexing the string."""
        if char.is_pool_open():
            new_state = Token.POOL_OPEN
        else:
            msg = f'{char} cannot start a pool.'
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _whitespace(self, char: Char) -> None:
        """Processing whitespace."""
        new_state = None
        if char.isdigit() or char.is_negative_sign():
            new_state = Token.MEMBER
        elif char.is_member_delim():
            new_state = Token.MEMBER_DELIMITER
        elif char.is_pool_close():
            new_state = Token.POOL_CLOSE
        else:
            msg = f'{char} cannot follow white space.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char, False)


# Delexer.
class Encoder:
    def __init__(self, yadn: str = '') -> None:
        self.yadn = yadn

    # Public methods.
    def encode(self, data: Result) -> str:
        """Turn computed Python object results into a YADN string."""
        if isinstance(data, int):
            self._encode_int(data)
        elif isinstance(data, CompoundResult):
            self._encode_compound_result(data)
        elif isinstance(data, tuple):
            self._encode_tuple(data)
        return self.yadn

    # Private methods.
    def _encode_compound_result(self, data: CompoundResult) -> None:
        for result in data[:-1]:
            self.encode(result)
            self.yadn += '; '
        else:
            self.encode(data[-1])

    def _encode_int(self, data: int) -> None:
        self.yadn = f'{self.yadn}{data}'

    def _encode_tuple(self, data: tuple) -> None:
        members = ', '.join(str(m) for m in data)
        self.yadn = f'{self.yadn}[{members}]'
