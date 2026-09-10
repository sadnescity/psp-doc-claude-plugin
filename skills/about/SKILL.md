---
name: about
description: "What this PSP documentation covers and how it was put together. Background only; the technical chapters are the other skills."
---

## 1  Introductional Rant

If you don\'t know what programming a machine down to the metal is all about, go away! no really, this document is not for you! if you are seeking for advice on using existing solutions, such as SDKs or libraries, you will find little to none information that is of any use for you and you might only become frustrated by figuring out how little you know. If you however aren\'t afraid of numbers and want to dare jumping into the snake-pit of semi-accurate information based on guesswork done by a bunch of freaks - feel invited. this was made to give you what you need in the most compressed and visually pleasing form possible. *Stuff that matters.*

### 1.1  Things that are in this document

just about everything explicitly and specifically related to the PSP hard- and software internals and its programming. everything inside the box is subject to be documented, may it be relevant for actual programming or not. its ment as a reference for everyone who wants to know in all possible detail what makes this thing tick.\
one more thing: please notice that this is a technical documentation which is presented for pure educational purposes and higher learning, and not a moral lesson. i have decided against leaving out any information since i believe that information by itself should not be crippled in any way. if you choose to abuse this information for any kind of illegal activities (**PLEASE DON\'T!**) so be it, but don\'t bother me with it.

### 1.2  Things that are *not* in this document

several things were decided to not being put into this document because they didn\'t fit into the \'technical documentation\' type of concept. They may be documented seperatly some time but not now and not here. These things are:

- Tips on Emulating the PSP on another Host system (this kind of information is only useful for a very limited number of people, and additionally might be highly confusing and/or misleading for those who are writing actual PSP programs)
- Instructions on using any tools that let you upload and execute code on the PSP, or any other development related tools **except** anything related to setting up and using gcc as a cross-compiler targeted to the PSP.
- anything related to gaming, cheat-codes and the like. (this is a tech-doc not a gaming FAQ!)
- detailed and/or complete sourcecode, except when a formal explanation would just over-complicate things. (this is a documentation, not a code library)
- anything related to playing/booting/copying pirated games (as you may have noticed, **we do not support piracy!**)

some of these may be arguable, so if you think they should be here - probably along the lines of the appendix - don\'t hesitate to write the chapter in question and send it to me. i might include it if you write it, but other than that i wont care (there is still enough other stuff to complete).

### 1.3  Conventions

- we count bits starting from 0, the most significant bit of a byte is bit 7. when visualising a byte the most significant bit comes first (left), and the least significant bit comes last (right).
- when dealing with 16- or 32 byte values all figures are in big endian byte order. this means that the most significant byte comes first (left), and the least significant byte comes last (right). notice that this is **not** the way values are actually handled by the allegrex cpu (since it is little endian).
- if known (from patents or other freely available sources) we use the same terminology as Sony does, in particular we try to use the same names and abbreviations for hardware registers, signals and the like as a weak attempt of providing consistency with other existing documentation.
- absolute memory addresses are shown as used in real world PSP Programs. For this matter we dont use physical adresses to avoid confusion for the majority of our readers.
- code snippets are in either real or pseudo C language. any logical or arithmetic expressions outside code snippets are loosely simelar to C notation according to the following table:
  +:---------------------------------------------------------------------:+
  |   ----------------------------------- ------------                    |
  |   **Description**                      **Symbol**                     |
  |   logical or bitwhise AND                 `&`                         |
  |   logical or bitwhise OR                  `|`                         |
  |   logical or bitwhise exclusive OR        `^`                         |
  |   logical or bitwhise NOT (inverse)       `!`                         |
  |   equality or assignment                  `=`                         |
  |   addition                                `+`                         |
  |   substraction                            `-`                         |
  |   multiplication                          `*`                         |
  |   division                                `/`                         |
  |   ----------------------------------- ------------                    |
  +-----------------------------------------------------------------------+

  \
  \
  please notice that -outside code- we do not make a difference between logical and bitwhise operations. if in doubt the operation is bitwhise, it should however be clearly visible from the context.
