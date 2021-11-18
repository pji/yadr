"""
lex
~~~

A lexer for `yadr` dice notation.
"""
from yadr.model import OPERATORS, Token, TokenInfo


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
            Token.WHITESPACE: self._whitespace,
            Token.OPEN_GROUP: self._open_group,
            Token.CLOSE_GROUP: self._close_group,
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
            value: str | int = self.buffer
            if self.state == Token.NUMBER:
                value = int(value)
            token_info = (self.state, value)
            self.tokens.append(token_info)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    # Private state methods.
    def _close_group(self, char: str) -> None:
        """Processing a close group token."""
        if char.isdigit():
            new_state = Token.NUMBER
        elif char.isspace():
            char = ''
            new_state = Token.WHITESPACE
        elif char in OPERATORS:
            new_state = Token.OPERATOR
        else:
            msg = f'An open group cannot be followed by {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _number(self, char: str) -> None:
        """Processing a number."""
        new_state: Token | None = None
        if char.isdigit():
            self.buffer += char
        elif char.isspace():
            char = ''
            new_state = Token.WHITESPACE
        elif char in OPERATORS:
            new_state = Token.OPERATOR
        elif char == '(':
            new_state = Token.OPEN_GROUP
        elif char == ')':
            new_state = Token.CLOSE_GROUP
        else:
            msg = f'{char} cannot follow digit.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char)

    def _open_group(self, char: str) -> None:
        """Processing an open group token."""
        if char.isdigit():
            new_state = Token.NUMBER
        elif char.isspace():
            char = ''
            new_state = Token.WHITESPACE
        else:
            msg = f'An open group cannot be followed by {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _operator(self, char: str) -> None:
        """Processing an operator."""
        if char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char.isspace():
            char = ''
            new_state = Token.WHITESPACE
        else:
            msg = f'{char} cannot follow operator.'
            raise ValueError(msg)
        self._change_state(new_state, char)

    def _start(self, char: str) -> None:
        """The starting state."""
        if self.tokens:
            self.tokens = []
        if char.isspace():
            char = ''
            new_state = Token.WHITESPACE
        elif char.isdigit() or char == '-':
            new_state = Token.NUMBER
        elif char == '(':
            new_state = Token.OPEN_GROUP
        else:
            msg = f'Cannot start with {char}.'
            raise ValueError(msg)
        self._change_state(new_state, char, store=False)

    def _whitespace(self, char: str) -> None:
        """Processing whitespace."""
        if self.tokens:
            previous, _ = self.tokens[-1]
        else:
            previous = Token.START
        new_state: Token | None = None
        if char.isdigit() and previous == Token.OPERATOR:
            new_state = Token.NUMBER
        elif char.isdigit() and previous == Token.OPEN_GROUP:
            new_state = Token.NUMBER
        elif char.isdigit() and previous == Token.START:
            new_state = Token.NUMBER
        elif char == '-' and previous == Token.OPERATOR:
            new_state = Token.NUMBER
        elif char == '-' and previous == Token.START:
            new_state = Token.NUMBER
        elif char in OPERATORS and previous == Token.NUMBER:
            new_state = Token.OPERATOR
        elif char in OPERATORS and previous == Token.CLOSE_GROUP:
            new_state = Token.OPERATOR
        elif char == ')' and previous == Token.NUMBER:
            new_state = Token.CLOSE_GROUP
        elif char.isspace():
            ...
        else:
            msg = f'{char} cannot follow a {previous} token.'
            raise ValueError(msg)
        if new_state:
            self._change_state(new_state, char, store=False)
