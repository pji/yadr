#############################
yadr: Yet Another Dice Roller
#############################

Another common RPG die rolling syntax random number generator.


Why did you do this?
====================
That's a very good question. I guess the answer is that I started just
to see if I could, and it snowballed from there. In order to explore
Python, I had built a few packages in the past that would randomly
generate table top role playing game (TTRPG) characters. Each of them
had a version of a dice rolling module I had written, so I had this
code in a bunch of places.

"I'll make that a package!" I thought.

But, wait, what if I want to use dice from different game systems? I
had run across Backus Naur form (BNF) descriptions of languages in the
past when looking into algorithms, and it seemed like writing a
parser to handle different dice systems seemed a reasonable way to go.
As reasonable as any thought involving, "I'll use BNF here," can be,
I guess. And so was born Yet Another Dice Notation (YADN) and `yadr`.

For a description of YADN see: YADN_

.. _YADN: https://yadr.readthedocs.io/en/latest/dice_notation.html


Do we need another Python dice rolling package?
===============================================
No. Probably not. Unsurprisingly, there seems to be a lot of people who
play TTRPGs and write Python packages. This is yet another one.

Hence the name.


Does it support my game?
========================
Check through the YADN doc to see if the operations you need are described
there. If not, open an issue, and I'll see what I can do.


Why does it require Python 3.10?
================================
Another reason for this package is I wanted a project to explore the
new `match case` feature in Python 3.10. I'd read that parsing is
one of the cases where it's really useful.

So, I implemented it.

Then I removed it.

The problem isn't with `match case`. It worked well enough, and I
think the syntax was fairly clear. I'm not really sure it bought me
anything over using `if...elif...else`, but I think that is because
everything I'm lexing or parsing is fairly simple. More complex cases
my see greater benefit from `match...case`.

The problem is with `mypy`. It doesn't support `match case` yet.
So, my options were:

1.  Ditch `mypy`,
2.  Mark all the `match` blocks as `type: ignore`,
3.  Go back to `if`.

Option 2 was just a mess in the code.

My impression is that `mypy` is still here to stay, so I want to try
to make things work with it.

So, I went back to `if`, at least until `mypy` better supports `match
case`.

Since I removed the `match case`, I can probably lower the Python
requirement to 3.7 or so. If anyone ever uses this, I'll think about
it. For now, I'm only testing it under a 3.10 virtual environment, so
I'll keep it at 3.10.


How do I use this package?
==========================
If you want to execute the package from the command line, you can
install the package using `pip` or other Python package manager, and
run it as a module with the following::

    python -m yadr <YADN_string>

If you want to import it into your own code, install and import the
package as usual. You can then use the `roll()` function in the `yadr`
module to execute a string of YADN.::

    >>> import yadr
    >>>
    >>> yadn = '3d6'
    >>> result = yadr.roll(yadn)


How do I run the tests?
=======================
I'm using the `pytest` library for the unit tests. To just run those tests,
go to the root of your clone of the `yadr` repository and use the following
command::

    python3 -m pytest

The full suite of style checks, mypy, and such I use can be run using a
shortcut I have set up in the Makefile::

    make pre
