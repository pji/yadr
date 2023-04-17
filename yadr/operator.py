"""
operator
~~~~~~~~

Operators for handling the dice part of dice notation.
"""
from collections.abc import Callable, Sequence
import random
import operator


# Types for annotation.
OptionsOp = Callable[[str, str], tuple[str, str]]
ChoiceOp = Callable[[bool, tuple[str, str]], str]
PoolGenOp = Callable[[int, int], tuple[int, ...]]
DiceOp = Callable[[int, int], int]
MathOp = Callable[[int, int], int]
PoolOp = Callable[[Sequence[int], int], tuple[int, ...]]
PoolDegenOp = Callable[[Sequence[int], int], int]
UPoolDegenOp = Callable[[Sequence[int]], int]
Operation = Callable


# Registration.
ops: dict[str, Operation] = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.floordiv,
    '%': operator.mod,
    '+': operator.add,
    '-': operator.sub,
    '>': operator.gt,
    '<': operator.le,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
}


class operation:
    """A registration decorator for operations.

    :param symbol: The string used to refer to the operation.
    :return: None.
    :rtype: NoneType
    """
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def __call__(self, fn: Operation) -> Operation:
        """Register the operation.

        :param fn: The decorated function. It's sent automatically
            when :class:`operator.operation` is used as a decorator.
        :return: The decorated :class:`collections.abc.Callable`.
        :rtype: Callable
        """
        ops[self.symbol] = fn
        return fn


# Choice operators.
@operation(':')
def choice_options(a: str, b: str) -> tuple[str, str]:
    """Create the options for a choice.

    :ref:`YADN` reference: :ref:`qualifiers`

    :param a: The qualifier for the true condition of a choice.
    :param b: The qualifier for the false condition of a choice.
    :return: The qualifiers as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> choice_options('success', 'failure')
        ('success', 'failure')
    """
    return (a, b)


@operation('?')
def choice(boolean: bool, options: tuple[str, str]) -> str:
    """Make a choice.

    :ref:`YADN` reference: :ref:`qualifiers`

    :param boolean: The decision as a :class:`bool`.
    :param options: The two options to pick from.
    :return: The chosen option as a :class:`str`.
    :rtype: str

    Usage::

        >>> choice(False, ('spam', 'eggs'))
        'eggs'
    """
    result = options[0]
    if not boolean:
        result = options[1]
    return result


# Dice operators.
@operation('dc')
def concat(num: int, size: int) -> int:
    """Concatenate the least significant digits.

    :ref:`YADN` reference: :ref:`concat`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The concatenated least significant digits as an
        :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 2d10 as percentile dice. It's not quite right,
        >>> # since 00 should be 100, but the physical dice have
        >>> # that problem, too.
        >>> concat(2, 10)
        21
    """
    base = 10
    pool = dice_pool(num, size)
    pool = pool_modulo(pool, base)
    return pool_concatenate(pool)


@operation('d')
def die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result.

    :ref:`YADN` reference: :ref:`die`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The sum of the result of each die as an :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 3d6.
        >>> die(3, 6)
        5

    """
    pool = dice_pool(num, size)
    return sum(pool)


@operation('d!')
def exploding_die(num: int, size: int) -> int:
    """Roll a number of exploding same-sized dice.

    :ref:`YADN` reference: :ref:`explode`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The sum of the result of each die as an :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5d!6.
        >>> exploding_die(5, 6)
        15

    """
    return sum(exploding_pool(num, size))


@operation('dh')
def keep_high_die(num: int, size: int) -> int:
    """Roll a number of dice and keep the highest."""
    pool = dice_pool(num, size)
    return max(pool)


@operation('dl')
def keep_low_die(num: int, size: int) -> int:
    """Roll a number of dice and keep the lowest."""
    pool = dice_pool(num, size)
    return min(pool)


@operation('dw')
def wild_die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result."""
    wild = exploding_pool(1, size)
    regular = dice_pool(num - 1, size)
    if wild[0] == 1:
        return 0
    return sum((sum(wild), sum(regular)))


# Pool operators.
@operation('pc')
def pool_cap(pool: Sequence[int], cap: int) -> tuple[int, ...]:
    """Cap the maximum value in a pool."""
    result = []
    for value in pool:
        if value > cap:
            value = cap
        result.append(value)
    return tuple(result)


@operation('pf')
def pool_floor(pool: Sequence[int], floor: int) -> tuple[int, ...]:
    """Floor the minimum value in a pool."""
    result = []
    for value in pool:
        if value < floor:
            value = floor
        result.append(value)
    return tuple(result)


@operation('pa')
def pool_keep_above(pool: Sequence[int], floor: int) -> tuple[int, ...]:
    return tuple(n for n in pool if n >= floor)


@operation('pb')
def pool_keep_below(pool: Sequence[int], ceiling: int) -> tuple[int, ...]:
    return tuple(n for n in pool if n <= ceiling)


@operation('ph')
def pool_keep_high(pool: Sequence[int], keep: int) -> tuple[int, ...]:
    """Keep a number of the highest dice."""
    pool = list(pool)
    remove = len(pool) - keep
    for _ in range(remove):
        low_value = max(pool)
        low_index = 0
        for i, n in enumerate(pool):
            if n < low_value:
                low_value = n
                low_index = i
        pool.pop(low_index)
    return tuple(pool)


@operation('pl')
def pool_keep_low(pool: Sequence[int], keep: int) -> tuple[int, ...]:
    """Keep a number of the lowest dice."""
    pool = list(pool)
    remove = len(pool) - keep
    for _ in range(remove):
        high_value = min(pool)
        high_index = 0
        for i, n in enumerate(pool):
            if n > high_value:
                high_value = n
                high_index = i
        pool.pop(high_index)
    return tuple(pool)


@operation('p%')
def pool_modulo(pool: Sequence[int], divisor: int) -> tuple[int, ...]:
    """Perform a modulo operation of each member."""
    return tuple(n % divisor for n in pool)


@operation('pr')
def pool_remove(pool: Sequence[int], cut: int) -> tuple[int, ...]:
    """Remove members of a pool of the given value."""
    return tuple(n for n in pool if n != cut)


# Pool degeneration operators.
@operation('C')
def pool_concatenate(pool: Sequence[int]) -> int:
    """Count the dice in the pool."""
    str_value = ''.join((str(m) for m in pool))
    return int(str_value)


@operation('N')
def pool_count(pool: Sequence[int]) -> int:
    """Count the dice in the pool."""
    return len(pool)


@operation('S')
def pool_sum(pool: Sequence[int]) -> int:
    """Sum the dice in the pool."""
    return sum(pool)


@operation('ns')
def count_successes(pool: Sequence[int], target: int) -> int:
    """Count the number of successes in the pool."""
    pool = pool_keep_above(pool, target)
    return len(pool)


@operation('nb')
def count_successes_with_botch(pool: Sequence[int], target: int) -> int:
    """Count the number of successes in the pool. Then remove a success
    for each botch.
    """
    botches = len([n for n in pool if n == 1])
    pool = pool_keep_above(pool, target)
    return len(pool) - botches


# Pool generation operator.
@operation('g')
def dice_pool(num: int, size: int) -> tuple[int, ...]:
    """Roll a die pool."""
    return tuple(random.randint(1, size) for _ in range(num))


@operation('g!')
def exploding_pool(num: int, size: int) -> tuple[int, ...]:
    """Roll a die pool."""
    pool: Sequence[int] = dice_pool(num, size)
    pool = [_explode(n, size) for n in pool]
    return tuple(pool)


# Utility functions.
def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes."""
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)


def _explode(value: int, size: int) -> int:
    if value == size:
        explode_value = random.randint(1, size)
        value += _explode(explode_value, size)
    return value
