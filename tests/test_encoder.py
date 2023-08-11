"""
test_encoder
~~~~~~~~~~~~

Unit tests for the yadr.encoder module.
"""
from yadr import encode as e
from yadr import model as m


# Test Encoder.encode().
def test_boolean():
    """An bool becomes a string containing the YADN boolean."""
    exp = 'T'
    data = True
    encode_test(exp, data)


def test_compound_result():
    """A CompoundResult becomes a string of roll delimited values."""
    exp = '[1, 1, 3, 8]; 3'
    data = m.CompoundResult((
        (1, 1, 3, 8),
        3
    ))
    encode_test(exp, data)


def test_number():
    """An int becomes a string containing the YADN number."""
    exp = '3'
    data = 3
    encode_test(exp, data)


def test_pool():
    """A tuple of integers becomes a string containing the
    YADN pool.
    """
    exp = '[1, 1, 3, 8]'
    data = (1, 1, 3, 8)
    encode_test(exp, data)


def test_qualifier():
    """A string becomes a double-quoted string."""
    exp = '"spam"'
    data = 'spam'
    encode_test(exp, data)


def encode_test(expected, data):
    """Run a test on :meth:`Encoder.encode`."""
    encoder = e.Encoder()
    assert encoder.encode(data) == expected
