.. parsing:

#######
Parsing
#######

.. warning::
    If you are using this package to implement dice rolling, you
    should never have to directly interact with these classes. These
    are only documented to help with maintenance.

:dfn:`Parsing` is the act of matching tokens, in this case produced 
by a lexer, to a set of rules for execution.

:ref:`YADN` is maybe a bit over complex. This implementation has three
different parsers to handle its subsyntaxes.

.. autoclass:: yadr.parser.Parser
    :members:
.. autoclass:: yadr.maps.Parser
    :members:
.. autoclass:: yadr.pools.Parser
    :members:
