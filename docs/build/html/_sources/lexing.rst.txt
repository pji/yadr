.. lexing_:

######
Lexing
######

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
