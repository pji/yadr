"""
operator
~~~~~~~~

Operators for handling the dice part of dice notation.
"""
import operator
import random
from collections.abc import Callable, Sequence


# Result types for annotation.
Options = tuple[str, str]
Pool = Sequence[int]


# Operation types for annotation.
CompOp = Callable[[int, int], bool]
OptionsOp = Callable[[str, str], Options]
ChoiceOp = Callable[[bool, Options], str]
PoolGenOp = Callable[[int, int], Pool]
DiceOp = Callable[[int, int], int]
MathOp = Callable[[int, int], int]
PoolOp = Callable[[Pool, int], Pool]
PoolDegenOp = Callable[[Pool, int], int]
UPoolDegenOp = Callable[[Pool], int]
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
def choice_options(a: str, b: str) -> Options:
    """Create the options for a choice.

    :ref:`YADN` reference: :ref:`choice_options`

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
def choice(boolean: bool, options: Options) -> str:
    """Make a choice.

    :ref:`YADN` reference: :ref:`choice`

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
    """Roll a number of dice and keep the highest.

    :ref:`YADN` reference: :ref:`keep_high`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The highest value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5dh6.
        >>> keep_high_die(5, 6)
        5

    """
    pool = dice_pool(num, size)
    return max(pool)


@operation('dl')
def keep_low_die(num: int, size: int) -> int:
    """Roll a number of dice and keep the lowest.

    :ref:`YADN` reference: :ref:`keep_low`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The lowest value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5dh6.
        >>> keep_low_die(5, 6)
        1

    """
    pool = dice_pool(num, size)
    return min(pool)


@operation('dw')
def wild_die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result, with
    one of the dice being the wild die.

    :ref:`YADN` reference: :ref:`wild_die`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The sum of the values as an :class:`int`.
    :rtype: int

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5dw6.
        >>> wild_die(5, 6)
        0

    """
    wild = exploding_pool(1, size)
    regular = dice_pool(num - 1, size)
    if wild[0] == 1:
        return 0
    return sum((sum(wild), sum(regular)))


# Pool operators.
@operation('pc')
def pool_cap(pool: Pool, cap: int) -> Pool:
    """Cap the maximum value in a pool.

    :ref:`YADN` reference: :ref:`pool_cap`

    :param pool: A sequence of die values.
    :param cap: The maximum value of a die roll.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pc6.
        >>> pool_cap([4, 10, 3, 5, 1, 9], 6)
        (4, 6, 3, 5, 1, 6)

    """
    result = []
    for value in pool:
        if value > cap:
            value = cap
        result.append(value)
    return tuple(result)


@operation('pf')
def pool_floor(pool: Pool, floor: int) -> Pool:
    """Floor the minimum value in a pool.

    :ref:`YADN` reference: :ref:`pool_floor`

    :param pool: A sequence of die values.
    :param floor: The minimum value of a die roll.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pf6.
        >>> pool_floor([4, 10, 3, 5, 1, 9], 6)
        (6, 10, 6, 6, 6, 9)

    """
    result = []
    for value in pool:
        if value < floor:
            value = floor
        result.append(value)
    return tuple(result)


@operation('pa')
def pool_keep_above(pool: Pool, floor: int) -> Pool:
    """Discard all values in a pool below a given value.

    :ref:`YADN` reference: :ref:`pool_keep_above`

    :param pool: A sequence of die values.
    :param floor: The minimum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pa6.
        >>> pool_keep_above([4, 10, 3, 5, 1, 9], 6)
        (10, 9)

    """
    return tuple(n for n in pool if n >= floor)


@operation('pb')
def pool_keep_below(pool: Pool, ceiling: int) -> Pool:
    """Discard all values in a pool above a given value.

    :ref:`YADN` reference: :ref:`pool_keep_below`

    :param pool: A sequence of die values.
    :param ceiling: The maximum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pb6.
        >>> pool_keep_below([4, 10, 3, 5, 1, 9], 6)
        (4, 3, 5, 1)

    """
    return tuple(n for n in pool if n <= ceiling)


@operation('ph')
def pool_keep_high(pool: Pool, keep: int) -> Pool:
    """Keep a number of the highest dice.

    :ref:`YADN` reference: :ref:`pool_keep_high`

    :param pool: A sequence of die values.
    :param keep: The maximum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]ph3.
        >>> pool_keep_high([4, 10, 3, 5, 1, 9], 3)
        (10, 5, 9)

    """
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
def pool_keep_low(pool: Pool, keep: int) -> Pool:
    """Keep a number of the lowest dice.

    :ref:`YADN` reference: :ref:`pool_keep_low`

    :param pool: A sequence of die values.
    :param keep: The maximum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pl3.
        >>> pool_keep_low([4, 10, 3, 5, 1, 9], 3)
        (4, 3, 1)

    """
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
def pool_modulo(pool: Pool, divisor: int) -> Pool:
    """Perform a modulo operation of each member.

    :ref:`YADN` reference: :ref:`pool_mod`

    :param pool: A sequence of die values.
    :param divisor: The maximum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]p%3.
        >>> pool_modulo([4, 10, 3, 5, 1, 9], 3)
        (1, 1, 0, 2, 1, 0)

    """
    return tuple(n % divisor for n in pool)


@operation('pr')
def pool_remove(pool: Pool, cut: int) -> Pool:
    """Remove members of a pool of the given value.

    :ref:`YADN` reference: :ref:`pool_remove`

    :param pool: A sequence of die values.
    :param cut: The maximum value to keep.
    :return: The resulting values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]pr5.
        >>> pool_remove([4, 10, 3, 5, 1, 9], 5)
        (4, 10, 3, 1, 9)

    """
    return tuple(n for n in pool if n != cut)


# Pool degeneration operators.
@operation('C')
def pool_concatenate(pool: Pool) -> int:
    """Concatenate the dice in the pool.

    :ref:`YADN` reference: :ref:`pool_concat`

    :param pool: A sequence of die values.
    :return: The resulting value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # Roll C[4, 10, 3, 5, 1, 9].
        >>> pool_concatenate([4, 10, 3, 5, 1, 9])
        4103519

    """
    str_value = ''.join((str(m) for m in pool))
    return int(str_value)


@operation('N')
def pool_count(pool: Pool) -> int:
    """Count the dice in the pool.

    :ref:`YADN` reference: :ref:`pool_count`

    :param pool: A sequence of die values.
    :return: The resulting value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # Roll N[4, 10, 3, 5, 1, 9].
        >>> pool_count([4, 10, 3, 5, 1, 9])
        6

    """
    return len(pool)


@operation('S')
def pool_sum(pool: Pool) -> int:
    """Sum the dice in the pool.

    :ref:`YADN` reference: :ref:`pool_sum`

    :param pool: A sequence of die values.
    :return: The resulting value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # Roll S[4, 10, 3, 5, 1, 9].
        >>> pool_sum([4, 10, 3, 5, 1, 9])
        32

    """
    return sum(pool)


@operation('ns')
def count_successes(pool: Pool, target: int) -> int:
    """Count the number of successes in the pool.

    :ref:`YADN` reference: :ref:`count_successes`

    :param pool: A sequence of die values.
    :param target: The target number for success.
    :return: The resulting value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]ns6.
        >>> count_successes([4, 10, 3, 5, 1, 9], 6)
        2

    """
    pool = pool_keep_above(pool, target)
    return len(pool)


@operation('nb')
def count_successes_with_botch(pool: Pool, target: int) -> int:
    """Count the number of successes in the pool. Then remove a success
    for each botch.

    :ref:`YADN` reference: :ref:`count_botch`

    :param pool: A sequence of die values.
    :param target: The target number for success.
    :return: The resulting value as an :class:`int`.
    :rtype: int

    Usage::

        >>> # Roll [4, 10, 3, 5, 1, 9]nb6.
        >>> count_successes_with_botch([4, 10, 3, 5, 1, 9], 6)
        1

    """
    botches = len([n for n in pool if n == 1])
    pool = pool_keep_above(pool, target)
    return len(pool) - botches


# Pool generation operator.
@operation('g')
def dice_pool(num: int, size: int) -> Pool:
    """Roll a dice pool.

    :ref:`YADN` reference: :ref:`dice_pool`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The the values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5g6.
        >>> dice_pool(5, 6)
        (1, 1, 3, 5, 5)

    """
    return tuple(random.randint(1, size) for _ in range(num))


@operation('g!')
def exploding_pool(num: int, size: int) -> Pool:
    """Roll an exploding dice pool.

    :ref:`YADN` reference: :ref:`exploding_pool`

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The the values as a :class:`tuple`.
    :rtype: tuple

    Usage::

        >>> # This line is to ensure predictability for testing.
        >>> # Do not use outside of test cases.
        >>> _seed('spam')
        >>>
        >>> # Roll 5g!6.
        >>> exploding_pool(5, 6)
        (1, 1, 3, 5, 5)

    """
    pool: Pool = dice_pool(num, size)
    pool = [_explode(n, size) for n in pool]
    return tuple(pool)


# Utility functions.
def _explode(value: int, size: int) -> int:
    """Explode the value of a die.

    :param num: The number of dice to roll.
    :param size: The highest number that can be rolled on a die.
    :return: The the values as an :class:`int`.
    :rtype: int
    """
    if value == size:
        explode_value = random.randint(1, size)
        value += _explode(explode_value, size)
    return value


def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes.

    :param seed: A seed value for the random number generator.
    :return: None.
    :rtype: NoneType
    """
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)
