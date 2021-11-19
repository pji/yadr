"""
parse
~~~~~

Parse dice notation.
"""
from functools import wraps
import operator
from typing import Callable, Optional, Sequence, TypeVar

from yadr import operator as yo
from yadr.model import Token, TokenInfo


# Data.
DICE_OPERATORS = {
    'd': yo.die,
    'dp': yo.dice_pool,
    'd!': yo.exploding_die,
    'dh': yo.keep_high_die,
    'dl': yo.keep_low_die,
}
OPERATORS = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.floordiv,
    '+': operator.add,
    '-': operator.sub,
}
POOL_OPERATORS = {
    'pc': yo.pool_cap,
    'pf': yo.pool_floor,
    'ph': yo.pool_keep_high,
}


# Utility classes and functions.
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
        if self.kind in [Token.NUMBER, Token.POOL]:
            return self.value
        left = self.left.compute()
        right = self.right.compute()
        if self.kind == Token.OPERATOR:
            op = OPERATORS[self.value]
        elif self.kind == Token.DICE_OPERATOR:
            op = DICE_OPERATORS[self.value]
        elif self.kind == Token.POOL_OPERATOR:
            op = POOL_OPERATORS[self.value]
        return op(left, right)


def next_rule(next_rule: Callable) -> Callable:
    """A decorator for simplifying parsing rules."""
    def outer_wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner_wrapper(*args, **kwargs) -> Callable:
            left = next_rule(*args, **kwargs)
            return fn(next_rule, left, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper


# Parsing initiation.
def parse(tokens: Sequence[TokenInfo]) -> int | None:
    """Parse dice notation tokens."""
    trees = [Tree(*token) for token in tokens]
    trees = trees[::-1]
    parsed = add_sub(trees)
    if parsed:
        return parsed.compute()
    return None


# Parsing rules.
def groups_and_numbers(trees: list[Tree]) -> Tree:
    """Final rule, covering numbers and groups."""
    if trees[-1].kind in [Token.NUMBER, Token.POOL]:
        return trees.pop()
    if trees[-1].kind == Token.OPEN_GROUP:
        _ = trees.pop()
    expression = add_sub(trees)
    if trees[-1].kind == Token.CLOSE_GROUP:
        _ = trees.pop()
    return expression


@next_rule(groups_and_numbers)
def pool_operators(next_rule: Callable,
                   left: Tree,
                   trees: list[Tree]):
    """Parse dice operations."""
    while (trees and trees[-1].kind == Token.POOL_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(pool_operators)
def dice_operators(next_rule: Callable,
                   left: Tree,
                   trees: list[Tree]):
    """Parse dice operations."""
    while (trees and trees[-1].kind == Token.DICE_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(dice_operators)
def exponents(next_rule: Callable,
              left: Tree,
              trees: list[Tree]):
    """Parse exponents."""
    while (trees
           and trees[-1].kind == Token.OPERATOR
           and trees[-1].value in '^'):             # type: ignore
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(exponents)
def mul_div(next_rule: Callable,
            left: Tree,
            trees: list[Tree]):
    """Parse multiplication and division."""
    while (trees
           and trees[-1].kind == Token.OPERATOR
           and trees[-1].value in '*/'):            # type: ignore
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(mul_div)
def add_sub(next_rule: Callable,
            left: Tree,
            trees: list[Tree]):
    """Parse addition and subtraction."""
    while (trees
           and trees[-1].kind == Token.OPERATOR
           and trees[-1].value in '+-'):            # type: ignore
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left
