"""
operator
~~~~~~~~

Operators for handling the dice part of dice notation.
"""
import random


def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes."""
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)


def die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result."""
    pool = die_pool(num, size)
    return sum(pool)


def exploding_die(num: int, size: int) -> int:
    """Roll a number of exploding same-sized dice."""
    def explode(value: int) -> int:
        if value == size:
            explode_value = random.randint(1, size)
            value += explode(explode_value)
        return value
    
    pool = die_pool(num, size)
    pool = [explode(n) for n in pool]
    return sum(pool)


def die_pool(num: int, size: int) -> tuple[int, ...]:
    """Roll a die pool."""
    return tuple(random.randint(1, size) for _ in range(num))