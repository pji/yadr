.. yadr documentation master file, created by
   sphinx-quickstart on Sun Apr  9 20:53:35 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. welome:

Welcome to yadr's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   /api.rst
   /dice_notation.rst
   /internals.rst
   /requirements.rst


.. _intro:

Introduction to :mod:`yadr`
===========================
The :mod:`yadr` package is a Yet Another Dice Notation (YADN) parser
that can be used to generate random numbers in a way that simulates
rolling dice for a game.

The name :dfn:`yadr` stands for "Yet Another Dice Roller," a reference
to the fact there is no shortage of dice rollers in PyPI.


.. _using:

Using :mod:`yadr`
=================
If you want to execute the package from the command line, you can
install the package using :mod:`pip` or other Python package manager, and
run it as a module with the following::

    python -m yadr <YADN_string>

If you want to import it into your own code, install and import the
package as usual. You can then use the :func:`yadr.roll()` function
to execute a string of YADN.::

    >>> import yadr
    >>>
    >>> yadn = '3d6'
    >>> result = yadr.roll(yadn)



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
