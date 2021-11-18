"""
operator
~~~~~~~~

Operators for handling the dice part of dice notation.
"""
import random
from typing import Sequence


# Classes.
class Roll:
    """A dice roll."""
    # Magic methods.
    def __init__(self, pool: Sequence[int]) -> None:
        self.pool = tuple(pool)

    def __add__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return self.value + other.value
        if isinstance(other, int):
            return self.value + other
        return NotImplemented

    def __floordiv__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return self.value // other.value
        if isinstance(other, int):
            return self.value // other
        return NotImplemented

    def __mul__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return self.value * other.value
        if isinstance(other, int):
            return self.value * other
        return NotImplemented

    def __pow__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return self.value ** other.value
        if isinstance(other, int):
            return self.value ** other
        return NotImplemented

    def __sub__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            return self.value - other.value
        if isinstance(other, int):
            return self.value - other
        return NotImplemented

    # Properties.
    @property
    def value(self):
        return sum(self.pool)


# Dice operations.
def _seed(seed: int | str | bytes) -> None:
    """Seed the random number generator for testing purposes."""
    if isinstance(seed, str):
        seed = bytes(seed, encoding='utf_8')
    if isinstance(seed, bytes):
        seed = int.from_bytes(seed, 'little')
    random.seed(seed)


def die(num: int, size: int) -> int:
    """Roll a number of same-sized dice and return the result."""
    pool = dice_pool(num, size)
    return sum(pool)


def dice_pool(num: int, size: int) -> tuple[int, ...]:
    """Roll a die pool."""
    return tuple(random.randint(1, size) for _ in range(num))


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
