.. _api:

##########
Public API
##########

The following are the functions that make up the public API of :mod:`yadr`.


Rolling Dice
============
:class:`yadr.roll` is the main interface to :mod:`yadr`, and in most
cases it's all you need.

.. autofunction:: yadr.roll


Managing Dice Maps
==================
If you're playing a game that uses symbol-based dice rather than ones
with numbers, you may need to use a dice map to translate the dice
rolls into those symbols. You can handle that in :ref:`YADN`, but the
following functions can be useful, too.

.. autofunction:: yadr.add_dice_map
.. autofunction:: yadr.list_dice_maps
