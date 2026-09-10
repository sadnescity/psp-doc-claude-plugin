Not YAPSPD but a 2007 tutorial by Anissian, kept whole: a client, server and
supervisor example built with the PSPSDK, module entry points and module_start,
export libraries and import stubs, how a NID is computed and resolved, how the
kernel holds a loaded module as a SceModule with its entry and stub tables, and
three ways to change one already in memory — its export table, the exported
function itself, or the caller's import stub.

It is the only text here that shows those tables as live structures and says
what patching one actually rewrites, which is the picture to have in mind when
reading a stub in a disassembler.

Be clear about what it is not. Section 5.2, "What is a PRX", reads in full: "A
PRX (Relocatable eXecutable) is similar to ELF. (to be completed)". The document
is aimed at homebrew on firmware 1.5 and 3.03OE and patches at run time; the
relocation format and the on-disc layout of an executable are not in it, and are
in file-formats instead. Section 7 is a short MIPS primer, a register table and
an explanation of jal and ra, not an instruction reference; cpu and
cpu-instructions cover that. The figures came out of the PDF as scrambled
columns of text, though the prose around them survived.
