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
