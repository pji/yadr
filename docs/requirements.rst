#################
yadr Requirements
#################

The purpose of this document is to detail the requirements for the
`yadr` package. This is an initial take to help with planning. There
may be additional requirements or non-required features added in the
future. Changes may be made in the code that are not reflected here.


Purpose
=======
The purposes of `yadr` are:

*   Provide a random number generator that simulates the use of
    polyhedral dice as used in table top gaming.
*   Use a common syntax for die rolling that can be easily understood
    and used outside of the context of this package.


Functional Requirements
=======================
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
15. `yadr` can roll a number of dice and only use a given number of the
    highest rolls (see advantage in Wizard of the Coast's Dungeons &
    Dragons 5th Edition).
16. `yadr` can roll a number of dice and only use a given number of the
    lowest rolls (see advantage in Wizard of the Coast's Dungeons &
    Dragons 5th Edition).
17. `yadr` rolls can deflate (a roll below a certain number removes
    itself and other dice from the total).
18. `yadr` can cap the value of a die.

The following are stretch requirements that would be nice to have:

#.  `yadr` can map die faces to symbols (see Games Workshop's 
    Hero Quest).
#.  `yadr` can remap the value of the faces of a die.


Technical Requirements
======================
The following are the technical requirements for `yadr`:

#.  `yadr` can be seeded to allow predictable result for testing.

The following are stretch requirements that would be nice to have:

#.  `yadr` can use the `secrets` standard Python library for better
    random number generation.


Design Discussion
=================
The purpose of this section is to think through design challenges
encountered in the course of developing `yadr`. As this is a living
process, information here is not guaranteed to describe the current
state of the package.


Lexing Lookups
--------------
Right now, lexing follows the following process:

*   Get character.
*   Send character to processing method for current state.
*   Check:
    *   If character should be buffered,
    *   If state changes,
    *   If character allowed.

The problem is that these checks are all bound to the processing method
for the current state. It works, but it means that the processing method
for each state must be updated each time a new token is created. This
is getting tedious and error prone as the list of tokens increased.
Maybe there is a better way to do this.

I was thinking that we could reverse the situation, have each token
define what can come before it. That doesn't solve the problem though.
Whether you are determining what comes before or what comes after, you
still have to detail the relationships between each token. With large
numbers of tokens, that's going to be a large number of relationships.

Still, maybe there is a way to set this up through configuration rather
than large `if` structures.

The ambiguity between the negative sign and subtraction operator is a
problem. If I ignore that, I could probably collapse all the Char.is_*
methods into one that returns a token. Maybe that's still the way to
go. I'd just need a special case to handle the ambiguity of the
hyphen character.