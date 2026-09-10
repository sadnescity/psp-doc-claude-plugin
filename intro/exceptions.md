The first half of YAPSPD's chapter 9: the table of exception cause codes, then
the reset vector at 0xBFC00000, the EBASE entry that interrupts and syscalls
arrive through, and the error handler, those three as annotated pseudocode
rather than register documentation.

The cause table is what a crash is read against: it separates a misaligned load
or store from a fetch of an address that is not memory and from a word that is
not an instruction, the three ordinary outcomes of a patch that writes a bad
pointer or lands mid-instruction. The reset path is also where the split
between the two cores shows: the vector reads a COP0 register to tell which CPU
it is on and sends the Media Engine elsewhere.

The cause list is generic MIPS, with the three TLB entries marked (n/a). The
pseudocode is retail firmware at fixed kernel addresses, not anything inside a
game's own executable. What the handler does once it has the cause is in
exception-handler.
