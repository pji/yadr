"""
base
~~~~

Base classes for the yadr package.
"""
from typing import Callable, Optional

from yadr.model import BaseToken, CompoundResult, Result, Token, TokenInfo


# Utility functions.
def _mutable(value, type_=list):
    """Return an empty mutable type to avoid bugs where you put a
    mutable in the signature.
    """
    if not value:
        value = type_()
    return value


# Base classes.
class BaseLexer:
    def __init__(self,
                 bracket_states: Optional[dict[BaseToken, BaseToken]] = None,
                 state_map: Optional[dict[BaseToken, Callable]] = None,
                 symbol_map: Optional[dict[BaseToken, list[str]]] = None,
                 result_map: Optional[dict[BaseToken, Callable]] = None,
                 no_store: Optional[list[BaseToken]] = None,
                 init_state: BaseToken = Token.START,
                 bracket_ends: Optional[dict[BaseToken, BaseToken]] = None
                 ) -> None:
        self.bracket_states = _mutable(bracket_states, dict)
        self.bracket_ends = _mutable(bracket_ends, dict)
        self.state_map = _mutable(state_map, dict)
        self.symbol_map = _mutable(symbol_map, dict)
        self.result_map = _mutable(result_map, dict)
        self.no_store = _mutable(no_store)
        self.init_state = init_state
        self.state = init_state

        self.process = self._start
        self.buffer = ''
        self.tokens: list[TokenInfo] = []

    # Public methods.
    def lex(self, text: str) -> tuple[TokenInfo, ...]:
        """Lex a dice notation string."""
        for char in text:
            self.process(char)
        else:
            self._change_state(self.init_state, '')
        return tuple(self.tokens)

    # Private operation method.
    def _is_token_start(self, token: BaseToken, char: str) -> bool:
        """Is the given character the start of a new token."""
        valid = {s[0] for s in self.symbol_map[token]}
        return char in valid

    def _is_token_still(self, char: str) -> bool:
        """Is the given character still a part of the current token."""
        index = len(self.buffer)
        tokens = [t for t in self.symbol_map[self.state] if len(t) > index]
        if tokens:
            valid = {s[index] for s in tokens}
            return char in valid
        return False

    def _cannot_follow(self, char: str) -> None:
        """The character is not allowed by the current state."""
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

    def _change_state(self, new_state: BaseToken, char: str) -> None:
        """Terminate the previous token and start a new one."""
        # Terminate and store the old token.
        if self.state not in self.no_store:
            value: Result | CompoundResult = self.buffer
            if self.state in self.result_map:
                transform = self.result_map[self.state]
                value = transform(value)
            token_info = (self.state, value)
            self.tokens.append(token_info)

        # Set new state.
        self.buffer = char
        self.state = new_state
        self.process = self.state_map[new_state]

    def _check_char(self, char: str, can_follow: list) -> None:
        """Determine how to process a character."""
        new_state: Optional[BaseToken] = None

        # If the character doesn't change the state, add it to the
        # buffer and stop processing.
        if self._is_token_still(char):
            self.buffer += char
            return None

        # Check to see if the character starts a token that is allowed
        # to follow the current token. Stop looking once you find one.
        for token in can_follow:
            if self._is_token_start(token, char):
                new_state = token
                break

        # If not, throw an exception. Since whitespace isn't a token in
        # YADN, an exception saying a character can't follow WHITESPACE
        # isn't useful. Therefore handle that case by looking at the
        # last stored token.
        else:
            self._cannot_follow(char)

        # Some tokens start a state that doesn't match the token.
        if new_state in self.bracket_states:
            new_state = self.bracket_states[new_state]

        # If the state changed, change the state.
        if new_state:
            self._change_state(new_state, char)

    # Lexing rules.
    def _start(self, char: str) -> None:
        ...

    def _whitespace(self, char: str) -> None:
        """Lex white space."""
        if char.isspace():
            return None
        prev_state = self.init_state
        if self.tokens:
            prev_state = self.tokens[-1][0]
        if prev_state in self.bracket_ends:
            prev_state = self.bracket_ends[prev_state]
        process = self.state_map[prev_state]
        process(char)
