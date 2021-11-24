"""
parse
~~~~~

Parse dice notation.
"""
from functools import wraps
import operator
from typing import Callable, Generic, Optional, Sequence, TypeVar

from yadr import operator as yo
from yadr.model import CompoundResult, Result, Token, TokenInfo, op_tokens


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

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}(kind={self.kind}, value={self.value})'

    def compute(self):
        if self.kind in [Token.NUMBER, Token.POOL, Token.QUALIFIER]:
            return self.value
        left = self.left.compute()
        right = self.right.compute()
        if self.kind in op_tokens:
            op = yo.ops_by_symbol[self.value]
        else:
            msg = f'Unknown token {self.kind}'
            raise TypeError(msg)
        return op(left, right)


class Unary(Tree):
    """A unary tree."""
    def __init__(self,
                 kind: Token,
                 value: int | str,
                 child: Optional['Tree'] = None) -> None:
        self.kind = kind
        self.value = value
        self.child = child

    def compute(self):
        if self.kind in [Token.NUMBER, Token.POOL, Token.QUALIFIER]:
            return self.value
        child = self.child.compute()
        if self.kind in op_tokens:
            op = yo.ops_by_symbol[self.value]
        return op(child)


def next_rule(next_rule: Callable) -> Callable:
    """A decorator for simplifying parsing rules."""
    def outer_wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner_wrapper(*args, **kwargs) -> Callable:
            left = next_rule(*args, **kwargs)
            return fn(next_rule, left, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper


def u_next_rule(next_rule: Callable) -> Callable:
    """A decorator for simplifying parsing rules."""
    def outer_wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner_wrapper(*args, **kwargs) -> Callable:
            return fn(next_rule, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper


# Parsing initiation.
def parse(tokens: Sequence[TokenInfo]) -> Result | CompoundResult:
    """Parse dice notation tokens."""
    if (Token.ROLL_DELIMITER, ';') not in tokens:
        return _parse_roll(tokens)              # type: ignore

    rolls = []
    while (Token.ROLL_DELIMITER, ';') in tokens:
        index = tokens.index((Token.ROLL_DELIMITER, ';'))
        rolls.append(tokens[0:index])
        tokens = tokens[index + 1:]
    else:
        rolls.append(tokens)
    results: Sequence[Result] = []
    for roll in rolls:
        results.append(parse(roll))             # type: ignore
    return CompoundResult(results)


def _parse_roll(tokens: Sequence[TokenInfo]) -> int | tuple[int, ...] | None:
    trees = [Tree(*token) for token in tokens]
    trees = trees[::-1]
    parsed = last_rule(trees)
    if parsed:
        return parsed.compute()
    return None


# Parsing rules.
def groups_and_numbers(trees: list[Tree]) -> Tree:
    """Final rule, covering numbers, groups, and unaries."""
    kind = trees[-1].kind
    if kind in [Token.NUMBER, Token.POOL, Token.QUALIFIER]:
        return trees.pop()
    elif kind == Token.GROUP_OPEN:
        _ = trees.pop()
    else:
        msg = f'Unrecognized token {kind}'
        raise TypeError(msg)
    expression = last_rule(trees)
    if trees[-1].kind == Token.GROUP_CLOSE:
        _ = trees.pop()
    return expression


@next_rule(groups_and_numbers)
def pool_gen_operators(next_rule: Callable,
                       left: Tree,
                       trees: list[Tree]):
    """Parse dice operations."""
    while (trees and trees[-1].kind == Token.POOL_GEN_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(pool_gen_operators)
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


@u_next_rule(pool_operators)
def u_pool_degen_operators(next_rule: Callable, trees: list[Tree]):
    """Parse dice operations."""
    if trees[-1].kind == Token.U_POOL_DEGEN_OPERATOR:
        tree = trees.pop()
        unary = Unary(tree.kind, tree.value)
        unary.child = next_rule(trees)
        return unary
    return next_rule(trees)


@next_rule(u_pool_degen_operators)
def pool_degen_operators(next_rule: Callable,
                         left: Tree,
                         trees: list[Tree]):
    """Parse dice operations."""
    while (trees and trees[-1].kind == Token.POOL_DEGEN_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(pool_degen_operators)
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


@next_rule(add_sub)
def comparison_op(next_rule: Callable,
                  left: Tree,
                  trees: list[Tree]):
    """Parse comparison operator."""
    while (trees
           and trees[-1].kind == Token.COMPARISON_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


@next_rule(comparison_op)
def options_op(next_rule: Callable,
               left: Tree,
               trees: list[Tree]):
    """Parse options operator."""
    while (trees
           and trees[-1].kind == Token.OPTIONS_OPERATOR):
        tree = trees.pop()
        tree.left = left
        tree.right = next_rule(trees)
        left = tree
    return left


# Set the last rule in order of operations to make it a little easier
# to update as new operations are added.
last_rule = options_op
