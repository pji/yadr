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
    return sum(random.randint(1, size) for _ in range(num))
