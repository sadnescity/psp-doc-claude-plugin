The instruction formats come first — I-type, J-type and R-type with their bit
fields — and that is the part worth keeping, for decoding a word by hand. What
follows is uneven. Section 4.7, "MIPS Instructions", documents lw, sw and
addiu and stops; 4.8 adds the three Allegrex-only opcodes, halt, mfic and
mtic; 4.9 is the remaining four fifths of the chapter, thirty-seven VFPU
instructions with encodings and a page each.

So this is not an instruction set reference. There is not one branch or jump
in it, no beq, bne, j or jal, even though the J-type format is defined and
then never used by anything. When carrying a PSX hack over, read
allegrex-vs-r3000a first: the opcodes that quietly break a patch to BOOT.BIN
are the ones the Allegrex has and the R3000A has not, and none of them appear
here.

Section 4.8 does earn its place. mfic and mtic are how interrupts are masked
on this machine, with the save, disable and restore idiom spelled out, and
halt is what the kernel idle thread runs. The PSX has no equivalent of either.
