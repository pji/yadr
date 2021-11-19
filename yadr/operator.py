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


def pool_keep_high(pool: Sequence[int], keep: int) -> tuple[int, ...]:
    """Keep a number of the highest dice."""
    sorted_pool = sorted(n for n in pool)
    sorted_pool = sorted_pool[::-1]
    return tuple(sorted_pool)[:keep]


def pool_keep_low(pool: Sequence[int], keep: int) -> tuple[int, ...]:
    """Keep a number of the lowest dice."""
    sorted_pool = sorted(n for n in pool)
    return tuple(sorted_pool)[:keep]


# Utility functions.
def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes."""
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)
