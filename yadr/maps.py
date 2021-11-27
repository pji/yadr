"""
maps
~~~~

A module for handling YADN dice maps.
"""
from typing import Callable

from yadr.base import BaseLexer
from yadr.model import BaseToken, MapToken, map_symbols


# Lexing.
class Lexer(BaseLexer):
    def __init__(self) -> None:
        bracket_states: dict[BaseToken, BaseToken] = {
            MapToken.QUALIFIER_DELIMITER: MapToken.QUALIFIER,
        }
        bracket_ends: dict[BaseToken, BaseToken] = {
            MapToken.QUALIFIER: MapToken.QUALIFIER_END,
        }
        state_map: dict[BaseToken, Callable] = {
            MapToken.START: self._start,
            MapToken.END: self._start,
            MapToken.MAP_CLOSE: self._map_close,
            MapToken.MAP_OPEN: self._map_open,
            MapToken.NAME_DELIMITER: self._name_delimiter,
            MapToken.QUALIFIER: self._qualifier,
            MapToken.QUALIFIER_END: self._qualifier_end,
            MapToken.WHITESPACE: self._whitespace,
        }
        symbol_map: dict[BaseToken, list[str]] = map_symbols
        result_map: dict[BaseToken, Callable] = {
            MapToken.QUALIFIER: self._tf_qualifier,
        }
        no_store: list[BaseToken] = [
            MapToken.START,
            MapToken.QUALIFIER_END,
            MapToken.WHITESPACE,
        ]
        init_state: BaseToken = MapToken.START
        super().__init__(
            bracket_states,
            state_map,
            symbol_map,
            result_map,
            no_store,
            init_state,
            bracket_ends
        )

    # Result transformation rules.
    def _tf_qualifier(self, value: str) -> str:
        return value[1:-1]

    # Lexing rules.
    def _map_close(self, char: str) -> None:
        """Lex a map close symbol."""
        can_follow: list[BaseToken] = []
        self._check_char(char, can_follow)

    def _map_open(self, char: str) -> None:
        """Lex a map open symbol."""
        can_follow = [
            MapToken.MAP_CLOSE,
            MapToken.QUALIFIER_DELIMITER,
            MapToken.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _name_delimiter(self, char: str) -> None:
        """Lex a map open symbol."""
        can_follow = [
            MapToken.QUALIFIER_DELIMITER,
            MapToken.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _qualifier(self, char: str) -> None:
        """Lex a qualifier."""
        self.buffer += char
        if self._is_token_start(MapToken.QUALIFIER_DELIMITER, char):
            new_state = MapToken.QUALIFIER_END
            self._change_state(new_state, char)

    def _qualifier_end(self, char: str) -> None:
        can_follow = [
            MapToken.MAP_CLOSE,
            MapToken.NAME_DELIMITER,
            MapToken.WHITESPACE,
        ]
        self._check_char(char, can_follow)

    def _start(self, char: str) -> None:
        """Initial lexer state."""
        can_follow = [
            MapToken.MAP_OPEN,
            MapToken.WHITESPACE,
        ]
        self._check_char(char, can_follow)
