#########################
Yet Another Dice Notation
#########################

The purpose of this document is to define the syntax of dice notation
for the purposes of the `yadr` package. It has the following goals:

*   Follow commonly seen features of other dice notations.
*   Avoid surprising users where possible.
*   Support common features used by systems that use dice.


What is dice notation?
======================
Dice notation is a common syntax for describing how dice are used in
games that use dice. The Wikipedia article provides a good overview of
it's origin and purpose: `Dice_notation`_

.. _Dice_notation: https://en.wikipedia.org/wiki/Dice_notation


Sources
=======
The following sources were used for inspiration and to look for common
practices when building this document:

*   Dicetray: Grammar_
*   d20: d20_
*   Python dice: Python_dice_
*   KSU: Grammars_trees_interpreters_

.. _Grammar: https://github.com/gtmanfred/dicetray
.. _d20: https://d20.readthedocs.io/en/latest/start.html
.. _Python_dice: https://github.com/markbrockettrobson/python_dice
.. _Grammars_trees_interpreters: https://people.cs.ksu.edu/~schmidt/505f10/bnfS.html


Common Terms
============
For the purpose of this document, the following terms are defined as
follows:

fair:
    (adj.) A random number generator that is equally likely to generate
    any number within the range of numbers it can generate. While not
    necessarily true, this document assumes common random number
    generators used by computer systems can be considered fair.

die (*pl.* dice):
    (noun) A fair random number generator that generates integers within
    a range from one to the size of the die. For example, a "die four"
    (alternatively "four-sided die" or "d4") would generate a random
    integer n within the range 1 ≤ n ≤ 4.

pool:
    (noun) The set of individual integers generated from each dice when
    one or more dice are rolled. For example, if 2d6 are rolled, and
    one die generates a two and the other generates a four, the pool
    contains a two and a four.

roll:
    (verb) The generation of one or more random numbers from one or more
    dice.
    
    (noun) The result of one or more rolled dice.


YADN Description
================
The following provides a description of Yet Another Dice Notation (YADN)
using Backus-Naur Form (BNF) notation (or something I hope is close to
accomplishing that goal, since this is the first time I'm trying to write
BNF)::

    DIGIT ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    NUMBER ::= DIGIT | DIGIT NUMBER
    MEMBER_DELIMITER ::= ,
    MEMBER ::= NUMBER | NUMBER MEMBER_DELIMITER MEMBER
    POOL_OPEN ::= {
    POOL_CLOSE ::= }
    POOL ::= POOL_OPEN MEMBER POOL_CLOSE
    OPERATOR ::= ^ | * | / | + | -
    DICE_OPERATOR ::= d | d! | dh | dl | dp
    ROLL_OPERATOR ::= c | f | h | l | s | !
    GROUP_OPEN ::= (
    GROUP_CLOSE ::= )
    GROUP ::= GROUP_OPEN EXPRESSION GROUP_CLOSE
    EXPRESSION ::= NUMBER | POOL | GROUP | DICE_EXPRESSION | 
                   ROLL_EXPRESSION | EXPRESSION OPERATOR EXPRESSION
    DICE_EXPRESSION ::= EXPRESSION DICE_OPERATOR EXPRESSION
    ROLL_EXPRESSION ::= DICE_EXPRESSION ROLL_OPERATOR EXPRESSION

The majority of the rules follow the rules of basic integer arithmetic,
with the addition of operators for rolling dice. Dice operators are
resolved first in the order of operations, which then follows the
standard PEMDAS order after.


Dice Operators
==============
The dice operators are defined in YADN as follows:

*x* d *y* (dice sum):
    Generate x random integers n within the range 1 ≤ n ≤ y. Unless
    modified by a roll operator, the result is treated as the sum
    of the integers. Roll operators are allowed to interact with the
    individual integers. This represents the case of rolling a number
    of the same dice. For example::
    
        n = 1d20
        n = {11}
        n = 11

*x* d! *y* (exploding dice sum):
    Like `dice sum` but if any n = y, it explodes (a new integer in the
    same range is generated and added to n). New integers generated
    from explosions also explode if they equal y. For example::
    
        n = 6d!4
        n = {1, 4, 3, 4, 4, 1}
        n = {1, 4+1, 3, 4+4, 4+2, 1}
        n = {1, 4+1, 3, 4+4+4, 4+2, 1}
        n = {1, 4+1, 3, 4+4+4+1, 4+2, 1}
        n = {1, 5, 3, 13, 6, 1}
        n = 29

*x* dh *y* (keep high die):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    the integer with the highest value. For example:
    
        n = 2dh20
        n = {1, 17}
        n = 17

*x* dl *y* (keep low die):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    the integer with the lowest value. For example:
    
        n = 2dl20
        n = {1, 17}
        n = 1

*x* dp *y* (dice pool):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    all integers as individual values. Arithmetic operators act on
    each value in the pool individually. For example::
    
        n = 5dp10 + 2
        n = {3, 4, 7, 10, 3} + 2
        n = {5, 6, 9, 12, 5}


Roll Operators
==============
*Describe roll operators here.*