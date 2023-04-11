.. lexing_:

######
Lexing
######

.. warning::
    If you are using this package to implement dice rolling, you
    should never have to directly interact with these classes. These
    are only documented to help with maintenance.

:dfn:`Lexing` is the act of transforming text, such as Python code or
a :ref:`YADN` string, into tokens for parsing.

:ref:`YADN` is a little complex. This implementation has three
different lexers to handle its subsyntaxes. All three lexers are
built on the :class:`yadr.base.BaseLexer` abstract base class.

.. autoclass:: yadr.base.BaseLexer
    :members:
.. autoclass:: yadr.lex.Lexer
    :members:
.. autoclass:: yadr.maps.Lexer
    :members:
.. autoclass:: yadr.pools.Lexer
    :members:
