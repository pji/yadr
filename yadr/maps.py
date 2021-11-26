"""
maps
~~~~

A module for handling YADN dice maps.
"""
from yadr.base import BaseLexer
from yadr.model import MapToken


# Data.
symbols = {
    MapToken.MAP_OPEN: '{',
}
token_map = {k: v.split() for k,v in symbols.items()}


# Lexing.
class Lexer(BaseLexer):
    ...
