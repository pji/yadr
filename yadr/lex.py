"""
lex
~~~

A lexer for `yadr` dice notation.
"""
from functools import wraps
from typing import Callable

from yadr.model import (
    DICE_OPERATORS,
    OPERATORS,
    POOL_OPERATORS,
    Token,
    TokenInfo,
    U_POOL_DEGEN_OPERATORS,
    POOL_DEGEN_OPERATORS
)


# Utility.
def ignore_whitespace(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(self, char: str) -> None:
        if char.isspace():
            return None
        fn(self, char)
    return wrapper


# Classes.
class Lexer:
    """A state-machine to lex dice notation."""
    def __init__(self) -> None:
        self.buffer = ''
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
            Token.OPEN_GROUP: self._open_group,
            Token.CLOSE_GROUP: self._close_group,
            Token.DICE_OPERATOR: self._dice_operator,
            Token.POOL: self._pool,
            Token.POOL_OPERATOR: self._pool_operator,
            Token.U_POOL_DEGEN_OPERATOR: self._u_pool_degen_operator,
            Token.POOL_DEGEN_OPERATOR: self._pool_degen_operator,
            Token.END: self._start
        }
        self.process = self._start

    # Public methods.
    def lex(self, text: str) -> tuple[TokenInfo, ...]:
        """Lex a dice notation string."""
        for char in text:
            self.process(char)
        else:
            args = [Token.END, '']
            if self.state == Token.WHITESPACE:
                args.append(False)
            self._change_state(*args)               # type: ignore
        return tuple(self.tokens)

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: str,
                      store: bool = True) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if store:
            value: str | int | tuple[int, ...] = self.buffer
            if self.state == Token.NUMBER and isinstance(value, str):
                value = int(value)
            elif self.state == Token.POOL and isinstance(value, str):
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
    @ignore_whitespace
    def _close_group(self, char: str) -> None:
        """Processing a close group token."""
        if char.isdigit():
            new_state = Token.NUMBER
        elif char in OPERATORS:
            new_state = Token.OPERATOR
        elif char == 'd':
            new_state = Token.DICE_OPERATOR
        else:
            msg = f'An open group cannot be followed by {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    @ignore_whitespace
    def _dice_operator(self, char: str) -> None:
        """Processing an operator."""
        valid_char = [s[1] for s in DICE_OPERATORS[1:]]
        new_state: Token | None = None
        if char in valid_char:
            self.buffer += char
        elif char.isdigit() or char == '-':
            new_state = Token.NUMBER
        else:
            msg = f'{char} cannot follow dice operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    @ignore_whitespace
    def _number(self, char: str) -> None:
        """Processing a number."""
        new_state: Token | None = None
        if char.isdigit():
            self.buffer += char
        elif char in OPERATORS:
            new_state = Token.OPERATOR
        elif char == 'd':
            new_state = Token.DICE_OPERATOR
        elif char == '(':
            new_state = Token.OPEN_GROUP
        elif char == ')':
            new_state = Token.CLOSE_GROUP
        else:
            msg = f'{char} cannot follow digit.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    @ignore_whitespace
    def _open_group(self, char: str) -> None:
        """Processing an open group token."""
        if char.isdigit():
            new_state = Token.NUMBER
        else:
            msg = f'An open group cannot be followed by {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    @ignore_whitespace
    def _operator(self, char: str) -> None:
        """Processing an operator."""
        if char.isdigit() or char == '-':
            new_state = Token.NUMBER
        else:
            msg = f'{char} cannot follow operator.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    @ignore_whitespace
    def _pool(self, char: str) -> None:
        """Processing a pool open."""
        new_state = None
        if (char.isdigit() or char in '-,}'):
            self.buffer += char
        elif char == 'p':
            new_state = Token.POOL_OPERATOR
        elif char == 'n':
            new_state = Token.POOL_DEGEN_OPERATOR
        else:
            msg = f'{char} cannot be in a pool.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    @ignore_whitespace
    def _u_pool_degen_operator(self, char: str) -> None:
        """Processing a unary pool degeneration operator."""
        if char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char == '{':
            new_state = Token.POOL
        else:
            msg = f'{char} cannot follow unary pool degeneration operator.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    @ignore_whitespace
    def _pool_degen_operator(self, char: str) -> None:
        """Processing a pool degeneration operator."""
        valid_char = [s[1] for s in POOL_DEGEN_OPERATORS]
        new_state: Token | None = None
        if char in valid_char:
            self.buffer += char
        elif char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char in U_POOL_DEGEN_OPERATORS:
            new_state = Token.U_POOL_DEGEN_OPERATOR
        elif char == '(':
            new_state = Token.OPEN_GROUP
        else:
            msg = f'{char} cannot follow pool degeneration operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    @ignore_whitespace
    def _pool_operator(self, char: str) -> None:
        """Lex pool operators."""
        new_state = None
        valid_char = [s[1] for s in POOL_OPERATORS[1:]]
        if char in valid_char:
            self.buffer += char
        elif char.isdigit() or char == '-':
            new_state = Token.NUMBER
        else:
            msg = f'{char} cannot follow dice operator.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    @ignore_whitespace
    def _start(self, char: str) -> None:
        """The starting state."""
        if self.tokens:
            self.tokens = []
        if char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char == '(':
            new_state = Token.OPEN_GROUP
        elif char == '{':
            new_state = Token.POOL
        elif char in U_POOL_DEGEN_OPERATORS:
            new_state = Token.U_POOL_DEGEN_OPERATOR
        else:
            msg = f'Cannot start with {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char, store=False)


class PoolLexer:
    def __init__(self) -> None:
        self.buffer = ''
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
    def lex(self, text: str) -> tuple[int, ...]:
        """Lex a pool string from dice notation."""
        for char in text:
            self.process(char)
        return tuple(self.pool)

    # Private operation methods.
    def _change_state(self, new_state: Token,
                      char: str,
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
    def _member(self, char:str) -> None:
        """Lex a member."""
        new_state = None
        if char == ',':
            new_state = Token.MEMBER_DELIMITER
        elif char == '}':
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

    def _member_delimiter(self, char: str) -> None:
        """Lex a member delimiter."""
        if char.isdigit() or char == '-':
            new_state = Token.MEMBER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow a ,'
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _pool_close(self, char: str) -> None:
        """Lex a pool close."""
        msg = '{} cannot follow a \x007d'.format(char)
        raise ValueError(msg)

    def _pool_open(self, char: str) -> None:
        """Lex a pool open."""
        if char.isdigit() or char == '-':
            new_state = Token.MEMBER
        elif char.isspace():
            new_state = Token.WHITESPACE
        else:
            msg = '{} cannot follow a \x007b'.format(char)
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _start(self, char: str) -> None:
        """Start lexing the string."""
        if char == '{':
            new_state = Token.POOL_OPEN
        else:
            msg = f'{char} cannot start a pool.'
            raise ValueError(msg)
        self._change_state(new_state, char, False)

    def _whitespace(self, char: str) -> None:
        """Processing whitespace."""
        new_state = None
        if char.isdigit() or char == '-':
            new_state = Token.MEMBER
        elif char == ',':
            new_state = Token.MEMBER_DELIMITER
        elif char == '}':
            new_state = Token.POOL_CLOSE
        else:
            msg = f'{char} cannot follow white space.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char, False)
