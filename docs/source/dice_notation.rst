.. _YADN:

####
YADN
####

:dfn:`Yet Another Dice Notation (YADN)` is a dice notation syntax.

The purpose of this document is to define the syntax of :ref:`YADN`
for the purposes of the :mod:`yadr` package. It has the following goals:

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
*   KSU: Grammars_
*   gnebehay: parser_

.. _Grammar: https://github.com/gtmanfred/dicetray
.. _d20: https://d20.readthedocs.io/en/latest/start.html
.. _Python_dice: https://github.com/markbrockettrobson/python_dice
.. _Grammars: https://people.cs.ksu.edu/~schmidt/505f10/bnfS.html
.. _parser: https://github.com/gnebehay/parser


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
using something like Backus-Naur Form (BNF) notation. (I'll probably
eventually update it to ABNF, but I think this is close enough to
understandable for now.)::

    DIGIT ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    NEGATIVE_SIGN ::= -
    NUMBER ::= DIGIT | DIGIT NUMBER | NEGATIVE_SIGN NUMBER
    GROUP_OPEN ::= (
    GROUP_CLOSE ::= )
    AS_OPERATOR ::= + | -
    MD_OPERATOR ::= * | / | %
    EX_OPERATOR ::= ^
    OPERATOR ::= AS_OPERATOR | MD_OPERATOR | EX_OPERATOR
    DICE_OPERATOR ::= d | d! | dc | dh | dl | dw
    GROUP ::= GROUP_OPEN EXPRESSION GROUP_CLOSE
    DICE_EXPRESSION ::= EXPRESSION DICE_OPERATOR EXPRESSION
    EXPRESSION ::= NUMBER 
                | GROUP
                | DICE_EXPRESSION
                | POOL_DEGEN_EXPRESSION
                | EXPRESSION OPERATOR EXPRESSION

    MEMBER_DELIMITER ::= ,
    MEMBER ::= NUMBER | NUMBER MEMBER_DELIMITER MEMBER
    POOL_OPEN ::= [
    POOL_CLOSE ::= ]
    POOL ::= POOL_OPEN MEMBER POOL_CLOSE
    
    POOL_GEN_OPERATOR ::= dp | g!
    POOL_GEN_EXPRESSION ::= EXPRESSION POOL_GEN_OPERATOR EXPRESSION
    
    POOL_OPERATOR ::= pa | pb | pc | pf | ph | pl | pr | p%
    POOL_GROUP ::= OPEN_GROUP POOL_EXPRESSION CLOSE_GROUP
    POOL_EXPRESSION ::= POOL POOL_OPERATOR EXPRESSION
                     | POOL_GEN_EXPRESSION POOL_OPERATOR EXPRESSION
                     | POOL_GROUP POOL_OPERATOR EXPRESSION

    U_POOL_DEGEN_OPERATOR ::= C | N | S
    POOL_DEGEN_OPERATOR ::= ns | nb
    POOL_DEGEN_EXPRESSION ::= U_POOL_DEGEN_OPERATOR POOL
                           | U_POOL_DEGEN_OPERATOR POOL_EXPRESSION
                           | POOL POOL_DEGEN_OPERATOR EXPRESSION
                           | POOL_EXPRESSION POOL_DEGEN_OPERATOR EXPRESSION

    QUALIFIER_DELIMITER ::= "
    LETTER ::= %x0020-%x0021 %x0022-%xffff
    SPACE = " "
    TEXT ::= LETTER
          | NUMBER
          | TEXT LETTER
          | TEXT NUMBER
          | TEXT SPACE
          | TEXT TEXT
    QUALIFIER ::= QUALIFIER_DELIMITER TEXT QUALIFIER_DELIMITER

    COMPARISON_OPERATOR ::= > | >= | == | != | <= | <
    BOOLEAN ::= T | F
    COMPARISON_EXPRESSION ::= EXPRESION COMPARISON_OPERATOR EXPRESION

    CHOICE_OPERATOR :: = ?
    OPTIONS_OPERATOR ::= :
    CHOICE_OPTIONS ::= QUALIFIER OPTIONS_OPERATOR QUALIFIER
    CHOICE_EXPRESSION ::= COMPARISON_EXPRESSION CHOICE_OPERATOR CHOICE_OPTIONS
                       | BOOLEAN CHOICE_OPERATOR CHOICE_OPTIONS

    MAP_OPEN ::= {
    MAP_CLOSE ::= }
    KEY ::= NUMBER | QUALIFIER
    VALUE ::= NUMBER | QUALIFIER
    KV_DELIMITER ::= :
    KV_PAIR ::= KEY KV_DELIMITER VALUE
    PAIR_DELIMETER ::= ,
    MAP_NAME ::= QUALIFIER
    NAME_DELIMITER ::= =
    MAP_CONTENT :: = KV_PAIR | KV_PAIR PAIR_DELIMITER KV_PAIR
    MAP ::= MAP_OPEN MAP_NAME NAME_DELIMITER MAP_CONTENT MAP_CLOSE
    MAPPING_OPERATOR ::= m=
    MAPPING_EXPRESSION ::= EXPRESSION MAPPING_OPERATOR MAP_NAME
                        | POOL_EXPRESSION MAPPING_OPERATOR MAP_NAME
                        | MAPPING_EXPRESSION MAPPING_OPERATOR MAP_NAME

    ROLL_DELIMITER ::= ;
    ROLL ::= EXPRESSION
          | POOL_EXPRESSION
          | CHOICE_EXPRESSION
          | MAP
          | ROLL ROLL_DELIMITER ROLL
    RESULT ::= NUMBER | POOL | RESULT ROLL_DELIMITER RESULT


Order of Operations
===================
The order of operations in YADN is as follows:

#.  Grouping and identity
#.  Pool generation operations
#.  Pool operations
#.  Pool degeneration operations
#.  Dice operations
#.  Exponentiation
#.  Multiplication and division
#.  Addition and subtraction
#.  Options and choices

Operations involving pools are placed high in the order to allow them
to be generated, acted on, and collapsed before they would acted on
by operations and dice operators that can't handle pools. However,
this leads to potential errors where a pool is generated but not
collapsed before it is passed to an operator. The trade-off seems
worthwhile here, but this may be reviewed in the future.


Pool Generation Operators
=========================
Pool generation operators generate a pool. These serve as the foundation
for most dice interactions described by YADN. The pool generation
operators are defined as follows:

x dp y (dice pool):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    all integers as the member of a pool. For example::
    
        n = 5dp10
        n = [3, 4, 7, 10, 3]

x g! y (exploding pool):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    all integers as the member of a pool. Each pool member can explode
    (see "exploding dice" above). For example.::
    
        n = 6g!6
        n = [2, 6, 1, 1, 6, 3]
        n = [2, 6+3, 1, 1, 6+6, 3]
        n = [2, 6+3, 1, 1, 6+6+1, 3]
        n = [2, 9, 1, 1, 13, 3]


Pool Operators
==============
Pool operators interact with or change a pool or its members. They
are defined as follows:

P pa y (pool keep above):
    For a given pool P, remove all members with a value below y. For
    example::
    
        n = 5dp10 pa 7
        n = [3, 1, 9, 7, 10] pa 7
        n = [ 9, 7, 10]

P pb y (pool keep below):
    For a given pool P, remove all members with a value above y. For
    example::
    
        n = 5dp10 pb 7
        n = [3, 1, 9, 7, 10] pa 7
        n = [3, 1]

P pc y (pool cap):
    For a given pool P, limit the maximum value of each member in P
    to y. Values greater than y become y. For example::
    
        n = 5dp10 pc 7
        n = [3, 1, 9, 7, 10] pc 7
        n = [3, 1, 7, 7, 7]

P pc y (pool floor):
    For a given pool P, limit the minimum value of each member in P
    to y. Values greater than y become y. For example::
    
        n = 5dp10 pf 7
        n = [3, 1, 9, 7, 10] pf 7
        n = [7, 7, 9, 7, 10]

P ph y (pool keep high):
    For a given pool P, select the top y members with the highest
    values. Return those members as a pool. For example::
    
        n = 5dp10 ph 3
        n = [3, 1, 9, 7, 10] ph 3
        n = [9, 7, 10]

P pl y (pool keep low):
    For a given pool P, select the top y members with the lowest
    values. Return those members as a pool.
    For example::
    
        n = 5dp10 pl 3
        n = [3, 1, 9, 7, 10] pl 3
        n = [3, 1, 7]

P pr y (pool remove):
    For a given pool P, remove all members with value y.
    For example::
    
        n = 5dp10 pr 7
        n = [3, 1, 9, 7, 10] pr 7
        n = [3, 1, 9, 10]

P p% y (pool modulo):
    For a given pool P, perform a modulo y operation on each member
    (M % y). For example::
    
        n = 5dp10 pr 7
        n = [3, 1, 9, 7, 10] pz 10
        n = [3, 1, 9, 0]


Pool Degeneration Operators
===========================
Pool degeneration operators act on the members of a pool, collapsing it
into a number. They are defined as follows:

P ns y (count successes):
    For a given pool P, count the number of members with a value greater
    than or equal to y. Return that count. For example::
    
        n = 5dp10 ps 7
        n = [3, 1, 9, 7, 10] ps 7
        n = 3

P nb y (count successes and botches):
    For a given pool P, let a be the number of members with a value
    greater than or equal to y. Let b be the number of members with
    a value of one. Return the difference between a and b. For example::
    
        n = 5dp10 pb 7
        n = [3, 1, 9, 7, 10] pb 7
        n = N [3, 1, 9, 7, 10] pa 7 - N [3, 1, 9, 7, 10] pb 1
        n = N [9, 7, 10] - N [1]
        n = 3 - 1
        n = 2

C P (pool concatenate):
    For a given pool P, concatenate the digits of each member. For example::
    
        n = C 5dp10
        n = C [3, 1, 9, 7, 10]
        n = 319710

N P (pool count):
    For a given pool P, return the number of members in P. For example::
    
        n = N 5dp10
        n = N [3, 1, 9, 7, 10]
        n = 5

S P (pool sum):
    For a given pool P, add together the values of all members. Return
    that sum. For example::
    
        n = S 5dp10
        n = S [3, 1, 9, 7, 10]
        n = 30


Dice Operators
==============
Dice operators generate a pool, act on the members, and then collapse
that pool into a number. They are defined as follows:

x d y (dice sum):
    Generate x random integers n within the range 1 ≤ n ≤ y. Unless
    modified by a roll operator, the result is treated as the sum
    of the integers. Roll operators are allowed to interact with the
    individual integers. This represents the case of rolling a number
    of the same dice. For example::
    
        n = 1d20
        n = S[11]
        n = 11

x dc y (concat):
    Generate x random integers n within the range 1 ≤ n ≤ y. Concatenate
    the least significant digit of each value into a single integer. For
    example::
    
        n = 2dc20
        n = C [3, 17] p% 10
        n = C [3, 7]
        n = 37

x d! y (exploding dice):
    Like `dice sum` but if any n = y, it explodes (a new integer in the
    same range is generated and added to n). New integers generated
    from explosions also explode if they equal y. For example::
    
        n = 6d!4
        n = S[1, 4, 3, 4, 4, 1]
        n = S[1, 4+1, 3, 4+4, 4+2, 1]
        n = S[1, 4+1, 3, 4+4+4, 4+2, 1]
        n = S[1, 4+1, 3, 4+4+4+1, 4+2, 1]
        n = S[1, 5, 3, 13, 6, 1]
        n = 29

x dh y (keep high die):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    the integer with the highest value. For example::
    
        n = 2dh20
        n = S([1, 17] ph 1)
        n = S[17]
        n = 17

x dl y (keep low die):
    Generate x random integers n within the range 1 ≤ n ≤ y. Return
    the integer with the lowest value. For example::
    
        n = 2dl20
        n = S([1, 17] pl 1)
        n = S[1]
        n = 1

x dw y (wild die):
    Generate two pools of random integers within the range 1 ≤ n ≤ y.
    The first pool, called the "wild" pool, has only one member. The
    standard pool has x minus one (x - 1) members. If the value of
    the wild die is neither y nor 1, return the sum of the sums of
    the two pools. For example::
    
        n = 4dw6
        n = S[3] + S[5, 1, 6]
        n = 3 + 12
        n = 15
    
    The member in the wild pool (the "wild die") explodes (see "exploding
    dice" above).::
    
        n = 4dw6
        n = S[6] + S[5, 1, 6]
        n = S[6+3] + S[5, 1, 6]
        n = 9 + 12
        n = 21
    
    If the value of the wild die is one, return zero (technically, this
    should be "the roll fails", but that requires more complex roll
    results than YADN can currently handle).::
    
        n = 4dw6
        n = S[1] + S[5, 1, 6]
        n = 0


Qualifiers
==========
It is common for dice systems to turn a quantitative result generated
by the dice into a qualitative result. A common example of this is the
"critical hit" system in later editions of *Dungeons and Dragons:* in
most cases the `1d20` roll used for an attack just returns the rolled
number, but if the roll is a twenty it's a "critical hit," which
has additional effects beyond the twenty.

In YADN,  this addition information is returned as "qualifiers." A
simple example of this can be seen with the "sum success" pool
degeneration operator::

    n = 6g6 ss 20
    n = S 6g6 >= 20 ? "success" : "failure"
    n = S [3, 2, 6, 6, 1, 3] >= 20 ? "success" : "failure"
    n = 21 >= 20 ? "success" : "failure"
    n = true ? "success" : "failure"
    n = "success"


.. _dice_maps:

Dice Maps
=========
Maps are key-value pairs that can be used to substitute a mapped
value onto a roll result. For example, a mapping of the "ability die"
from *Star Wars: Edge of the Empire* would look like::

    {"ability" = 1: "blank",
                 2: "success",
                 3: "success",
                 4: "success success",
                 5: "advantage",
                 6: "advantage",
                 7: "success advantage",
                 8: "advantage advantage"}

A dice map cannot be part of an expression. Instead it is passed in a
separate roll before the role where it will be used. The map is then
stored in memory by its name, so that it can be referenced in a later
roll through a "mapping operator".

.. note:
    Manually entering a dice map for every roll expression is
    a tedious way to roll dice. Interpretors implementing YADN
    may include pre-built maps for common dice systems for users
    to reference. The implementation details are left to the
    developer. However, in multiuser systems be careful about
    allowing user generated dice maps to persist after a roll as
    it could allow users to overwrite dice maps used by other users.


Mapping Operators
=================
Mapping operators map roll results onto result maps. They are defined
as:

x m M or P m M:
    For a given number x, return the value for key x from result
    map M. For example::
    
        n = {"fudge" = 1:-1,2:0,3:1}; S(2g3 m "fudge")
        n = {"fudge" = 1:-1,2:0,3:1}; S([2, 1] m "fudge")
        n = S[0, -1]
        n = -1

    It can also work with pools. For a given pool P, return the value
    for each member m as a key m from the result map M. For example::
    
        n = {"fudge" = 1:-1,2:0,3:1}; 2g3 m "fudge"
        n = {"fudge" = 1:-1,2:0,3:1}; [2, 1] m "fudge"
        n = [0, -1]


Example Usage
=============
The following examples illustrate how YADN can be used to describe
dice rolls in various game systems.

*Dungeons and Dragons:* An attack roll with a plus three modifier::

    n = 1d20+3
    n = S[4]+3
    n = 4+3
    n = 7

*Dungeons and Dragons:* A roll to generate an ability score, using four
dice and dropping the lowest::

    n = 4dl6
    n = S[5, 1, 6, 6]
    n = S[5, 6, 6]
    n = 17

*Dungeons and Dragons:* A damage roll with a long sword, an extra
six-sided die of damage, and a plus five modifier::

    n = 1d8 + 1d6 + 5
    n = S[3] + S[1] + 5
    n = 3 + 1 + 5
    n = 9

*Dungeons and Dragons:* A 1-100 "percentile" roll before the availability
of ten-sided dice::

    n = 2dc20
    n = C [13, 9] p% 10
    n = C [3, 9]
    n = 39

*West End's Star Wars: the Roleplaying Game, Second Edition:* An attack
roll with a *Blaster* skill of "5D+2"::

    n = 5dw6 + 2
    n = S[1] + S[2, 5, 1, 6] + 2
    n = 0

*Mage: the Ascension:* A five dot roll with a success value of six::

    n = 5g10 nb 6
    n = [10, 2, 6, 1, 8] nb 6
    n = N [10, 1, 1, 1, 8] pa 6 - N [10, 1, 1, 1, 8] pb 1
    n = N [10, 8] - N [1, 1, 1]
    n = 2 - 3
    n = -1

*Vampire: the Masquerade, Fifth Edition:* A seven dot roll with two
hunger dice::

    n = 2g10; 5g10
    n = [6, 10]; [3, 10, 1, 7, 7]

.. note:
    YADN cannot handle counting values across multiple pools. This
    means it can't currently handle V:tM5's critical systems. Until it
    is able to handle more complex results, it will have to fall back to
    generating the pools and letting the humans figure things out from
    there.

*Fate:* The ladder used to determine dice outcomes::

    {"fateladder"=
        8: "Legendary",
        7: "Epic",
        6: "Fantastic",
        5: "Superb",
        4: "Great",
        3: "Good",
        2: "Fair",
        1: "Average",
        0: "Mediocre",
        -1: "Poor",
        -2: "Terrible"
    }

*Fate:* A roll with a skill rated as "Good" with the Fate system's Ladder
already stored as a dice map::

    n = (2d3 - 4) + 3 m "fateladder"
    n = (S[1, 3] - 4) + 3 m "fateladder"
    n = (4 - 4) + 3 m "fateladder"
    n = 0 + 3 m "fateladder"
    n = 3 m "fateladder"
    n = "Good"

*Star Wars: Edge of the Empire:* Slicing with a Computers of three and
Intellect of two while under heavy fire and having a broken wrist but
having a fragment of the terminal's passcode algorithms::

    n = 1p8m"ability"; 2g12m"proficiency"; 2g6m"setback"; 1g6m"boost"
    n = [4]m"ability"; [3, 9]m"proficiency"; [6, 6]m"setback"; [2]m"boost"
    n = ["success"];
        ["success", "success advantage"];
        ["threat", "threat"];
        ["blank"]
