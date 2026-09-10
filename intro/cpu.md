Chapter 4 as far as the caches: the 32 general purpose registers under their
o32 names, the debug registers, and coprocessor 0 in two banks — the status
registers reached with mfc0/mtc0 and a second set of control registers reached
with cfc0/ctc0, every row tagged with the firmware modules that touch it.

The calling convention is the one a PSX hook already assumes — arguments in
a0-a3, result in v0, s0-s7 preserved across a call, return address in ra — and
it carries over to BOOT.BIN unchanged, since that is MIPS like a PSX
executable. What does not carry over is the address a patch lands at: BOOT.BIN
is a relocatable PRX, and file-formats is where the relocations are written
down.

Two COP0 entries have no R3000A counterpart: register 22 is CPUId, reading 0
on the main CPU and 1 on the Media Engine, and register 25 is EBase, which
puts the exception vector in a register instead of at a fixed address. The
whole cfc0/ctc0 bank is Allegrex, not standard MIPS. Note also what is
missing: no HI, LO or PC, and no instructions at all — for those read
cpu-instructions and allegrex-vs-r3000a. The 4.3.1 table lost its column
headers in conversion and reads as a flat run of cells: number, access, name,
meaning, modules.
