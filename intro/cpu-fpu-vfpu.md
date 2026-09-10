Two coprocessors. COP1 is the ordinary MIPS floating point unit and gets thin
treatment: a bare list of FPR0-31 against the firmware modules that use each,
with the column headers lost in conversion, and a control register table in
which only FIR, FCCR, FEXR, FENR and FCSR are named. COP2 is the substance —
how 128 single precision registers are addressed as singles, pairs, triples,
quads and 2x2, 3x3 or 4x4 matrices, normal or transposed, the S/C/R/M/E naming
that follows from it, and the extra registers above 127: the prefix stacks,
the condition register and the random number generator state.

Coming from the PSX, note that COP2 means something else here. On the R3000A
it is the GTE, fixed point geometry; on the Allegrex it is a floating point
vector unit with an instruction set of its own, so a cop2 opcode in a PSP
disassembly has nothing to do with what a PSX hack did with the GTE. The PSX
has no COP1 at all.

For patching BOOT.BIN this is mostly recognition work. Text and menu hacks
rarely need the VFPU, but if the routine being hooked uses it, the prefix
stacks and the condition register are live state a hook must not disturb, and
the naming section is what makes S130 or M100 readable. The VFPU instructions
themselves are in cpu-instructions.
