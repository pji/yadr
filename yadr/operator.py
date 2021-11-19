"""
operator
~~~~~~~~

Operators for handling the dice part of dice notation.
"""
import random
from typing import Sequence


# Pool generation operator.
def dice_pool(num: int, size: int) -> tuple[int, ...]:
    """Roll a die pool."""
    return tuple(random.randint(1, size) for _ in range(num))


# Dice operators.
def concat(num: int, size: int) -> int:
    """Concatenate the least significant digits."""
    base = 10
    pool: Sequence[int] = dice_pool(num, size)
    pool = [n % base for n in pool]
    pool = [n * base ** i for i, n in enumerate(pool[::-1])]
    return sum(pool)


def die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result."""
    pool = dice_pool(num, size)
    return sum(pool)


def exploding_die(num: int, size: int) -> int:
    """Roll a number of exploding same-sized dice."""
    def explode(value: int) -> int:
        if value == size:
            explode_value = random.randint(1, size)
            value += explode(explode_value)
        return value

    pool: Sequence[int] = dice_pool(num, size)
    pool = [explode(n) for n in pool]
    return sum(pool)


def keep_high_die(num: int, size: int) -> int:
    """Roll a number of dice and keep the highest."""
    pool = dice_pool(num, size)
    return max(pool)


def keep_low_die(num: int, size: int) -> int:
    """Roll a number of dice and keep the lowest."""
    pool = dice_pool(num, size)
    return min(pool)


# Pool operators.
def pool_cap(pool: Sequence[int], cap: int) -> tuple[int, ...]:
    """Cap the maximum value in a pool."""
    result = []
    for value in pool:
        if value > cap:
            value = cap
        result.append(value)
    return tuple(result)


def pool_floor(pool: Sequence[int], floor: int) -> tuple[int, ...]:
    """Floor the minimum value in a pool."""
    result = []
    for value in pool:
        if value < floor:
            value = floor
        result.append(value)
    return tuple(result)


def pool_keep_above(pool: Sequence[int], floor: int) -> tuple[int, ...]:
    return tuple(n for n in pool if n >= floor)


def pool_keep_below(pool: Sequence[int], ceiling: int) -> tuple[int, ...]:
    return tuple(n for n in pool if n <= ceiling)


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


def pool_remove(pool: Sequence[int], cut: int) -> tuple[int, ...]:
    return tuple(n for n in pool if n != cut)


# Pool degeneration operators.
def pool_count(pool: Sequence[int]) -> int:
    """Count the dice in the pool."""
    return len(pool)


def pool_sum(pool: Sequence[int]) -> int:
    """Sum the dice in the pool."""
    return sum(pool)


def count_successes(pool: Sequence[int], target: int) -> int:
    """Count the number of successes in the pool."""
    pool = pool_keep_above(pool, target)
    return len(pool)


def count_successes_with_botch(pool: Sequence[int], target: int) -> int:
    botches = len([n for n in pool if n == 1])
    pool = pool_keep_above(pool, target)
    return len(pool) - botches


# Utility functions.
def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes."""
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)
