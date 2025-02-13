.. _operators:

#########
Operators
#########

Operators are functions that implement the various operators found
in :ref:`YADN`. :mod:`yadr` is designed to avoid the need for
someone using it to ever need to call these functions directly. They
are intended to be invoked through the parsing of :ref:`YADN`. Their
documentation here is just intended for maintenance purposes.


:ref:`qualifiers`
=================

.. autofunction:: yadr.operator.choice
.. autofunction:: yadr.operator.choice_options


:ref:`dice_ops`
===============

.. autofunction:: yadr.operator.concat
.. autofunction:: yadr.operator.die
.. autofunction:: yadr.operator.exploding_die
.. autofunction:: yadr.operator.keep_high_die
.. autofunction:: yadr.operator.keep_low_die
.. autofunction:: yadr.operator.wild_die


:ref:`pool_gen_ops`
=====================

.. autofunction:: yadr.operator.dice_pool
.. autofunction:: yadr.operator.exploding_pool


:ref:`pool_ops`
===============

.. autofunction:: yadr.operator.pool_cap
.. autofunction:: yadr.operator.pool_floor
.. autofunction:: yadr.operator.pool_keep_above
.. autofunction:: yadr.operator.pool_keep_below
.. autofunction:: yadr.operator.pool_keep_high
.. autofunction:: yadr.operator.pool_keep_low
.. autofunction:: yadr.operator.pool_modulo
.. autofunction:: yadr.operator.pool_remove


:ref:`pool_degen_ops`
=====================
.. autofunction:: yadr.operator.pool_concatenate
.. autofunction:: yadr.operator.pool_count
.. autofunction:: yadr.operator.pool_sum
.. autofunction:: yadr.operator.count_successes
.. autofunction:: yadr.operator.count_successes_with_botch


The Random Number Generator
===========================
The random number generator (RNG) used to generate the die rolls is
set by the current value of :func:`yadr.operator.roll`. The value of
:func:`yadr.operator.roll` is a function that uses an RNG to perform
the die roll and return the result. There are currently two options
available for use as this rolling function:

*   :func:`yadr.operations._roll_random` (uses :func:`random.randint`)
*   :func:`yadr.operations._roll_secrets` (uses :func:`secrets.randbelow`)

The default rolling function is :func:`yadr.operations._roll_random`.

.. warning::
    While you can change the value of :func:`yadr.operations.roll` to
    change the RNG, doing so may not be thread safe. This probably
    doesn't matter in most situations but caution is still recommended.
