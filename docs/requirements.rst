#################
yadr Requirements
#################

The purpose of this document is to detail the requirements for the
`yadr` package. This is an initial take to help with planning. There
may be additional requirements or non-required features added in the
future. Changes may be made in the code that are not reflected here.


Purpose
-------
The purposes of `yadr` are:

*   Provide a random number generator that simulates the use of
    polyhedral dice as used in table top gaming.
*   Use a common syntax for die rolling that can be easily understood
    and used outside of the context of this package.


Functional Requirements
-----------------------
The following are the functional requirements for `yadr`:

1.  `yadr` can generate a random integer (called a "roll").
2.  `yadr` can generate that number within a range that represents the
    number of faces on a die, such as 1-6, 1-10, 1-20.
3.  `yadr` can represent dice of arbitrary integer size.
4.  `yadr` can add or subtract a modifier to or from the roll.
5.  `yadr` can roll multiple dice of the same type at once, returning
    the sum.
6.  `yadr` can roll multiple dice of the same type at once, returning
    the value of each die.
7.  `yadr` can roll multiple dice of the same type at once, concatenating
    the values.
8.  `yadr` can perform requirements 5-7 on dice of different types.
9.  `yadr` can perform basic arithmetic operations on the results of
    a roll.
10. `yadr` can perform basic arithmetic operations on the results of
    multiple rolls.
11. `yadr` rolls can explode (a roll above a certain number causes the
    die to be rerolled and its result added to the previous result,
    see the old West End d6 System's wild die).
12. `yadr` can accept a value required for success.
13. `yadr` can determine whether a roll was a success.
14. `yadr` can count the number of successes over multiple dice (see
    systems like White Wolf's Vampire: the Masquerade).
15. `yadr` can map die faces to symbols (see Games Workshop's 
    Hero Quest).
16. `yadr` can roll a number of dice and only use a given number of the
    highest rolls (see advantage in Wizard of the Coast's Dungeons &
    Dragons 5th Edition).
17. `yadr` can roll a number of dice and only use a given number of the
    lowest rolls (see advantage in Wizard of the Coast's Dungeons &
    Dragons 5th Edition).
18. `yadr` rolls can deflate (a roll below a certain number removes
    itself and other dice from the total).
19. `yadr` can remap the value of the faces of a die.
20. `yadr` can cap the value of a die.


Technical Requirements
----------------------
The following are the technical requirements for `yadr`:

1.  `yadr` can be seeded to allow predictable result for testing.
2.  `yadr` can use the `secrets` standard Python library for better
    random number generation.
