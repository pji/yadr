.. execution:

#########
Execution
#########

.. warning::
    If you are using this package to implement dice rolling, you
    should never have to directly interact with these classes. These
    are only documented to help with maintenance.

For :mod:`yadr`, :dfn:`execution` is the act of executing a tree of
tokens to produce a result.

There are two types of trees.

.. autoclass:: yadr.parser.Tree
    :members:
.. autoclass:: yadr.parser.Unary
    :members:
