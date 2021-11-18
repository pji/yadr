"""
parse
~~~~~

Parse dice notation.
"""
import operator
from typing import Optional, Sequence

from yadr import operator as yo
from yadr.model import Token, TokenInfo


# Data.
DICE_OPERATORS = {
    'd': yo.die,
    'd!': yo.exploding_die,
}
OPERATORS = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.floordiv,
    '+': operator.add,
    '-': operator.sub,
}


# Classes.
class Parser:
    """Parser for dice notation."""
    def parse(self, tokens: Sequence[TokenInfo]) -> int | None:
        """Parse dice notation tokens."""
        trees = [Tree(*token) for token in tokens]
        trees = trees[::-1]
        parsed = self._rule_1(trees)
        if parsed:
            return parsed.compute()
        return None

    # Grammar rules.
    def _rule_1(self, trees: list['Tree']) -> 'Tree':
        left = self._rule_2(trees)

        while (trees
               and trees[-1].kind == Token.OPERATOR
               and trees[-1].value in '+-'):            # type: ignore
            tree = trees.pop()
            tree.left = left
            tree.right = self._rule_2(trees)
            left = tree

        return left

    def _rule_2(self, trees: list['Tree']) -> 'Tree':
        """Rule for multiplication and division."""
        left = self._rule_3(trees)

        while (trees
               and trees[-1].kind == Token.OPERATOR
               and trees[-1].value in '*/'):            # type: ignore
            tree = trees.pop()
            tree.left = left
            tree.right = self._rule_3(trees)
            left = tree

        return left

    def _rule_3(self, trees: list['Tree']) -> 'Tree':
        """Rule for exponentiation."""
        left = self._rule_4(trees)

        while (trees
               and trees[-1].kind == Token.OPERATOR
               and trees[-1].value in '^'):             # type: ignore
            tree = trees.pop()
            tree.left = left
            tree.right = self._rule_4(trees)
            left = tree

        return left

    def _rule_4(self, trees: list['Tree']) -> 'Tree':
        """Rule for dice operators."""
        left = self._rule_5(trees)

        while (trees and trees[-1].kind == Token.DICE_OPERATOR):
            tree = trees.pop()
            tree.left = left
            tree.right = self._rule_5(trees)
            left = tree

        return left

    def _rule_5(self, trees: list['Tree']) -> 'Tree':
        """Rule for numbers and groups."""

        if trees[-1].kind == Token.NUMBER:
            return trees.pop()

        if trees[-1].kind == Token.OPEN_GROUP:
            _ = trees.pop()

        expression = self._rule_1(trees)

        if trees[-1].kind == Token.CLOSE_GROUP:
            _ = trees.pop()

        return expression


class Tree:
    """A binary tree."""
    def __init__(self,
                 kind: Token,
                 value: int | str,
                 left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None) -> None:
        self.kind = kind
        self.value = value
        self.left = left
        self.right = right

    def compute(self):
        if self.kind == Token.NUMBER:
            return self.value
        left = self.left.compute()
        right = self.right.compute()
        if self.kind == Token.OPERATOR:
            op = OPERATORS[self.value]
        elif self.kind == Token.DICE_OPERATOR:
            op = DICE_OPERATORS[self.value]
        return op(left, right)
