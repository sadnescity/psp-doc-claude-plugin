Chapter 11 of YAPSPD, split into five skills; this one holds what they share:
the command word (8-bit command, 24-bit argument), the 24-bit GE float, the BASE
register that supplies the high bits of a pointer, the Enable convention, and
the complete 0x00-0xFF command table.

Start here when disassembling a display list. A menu box or a line of text comes
down to a few commands - a texture pointer, a vertex list, a PRIM kick - and the
table is the only place that names every opcode, including ones with no section
of their own later (0x13 and 0x14, the matrix selects, RNORM, FFAR). The other
four skills take a range each: ge-flow-and-vertices for list flow and geometry,
ge-lighting, ge-textures for buffers and sampling, ge-raster for the pixel stage.

The chapter covers the command stream only: a list is handed to the hardware
through the GE registers at 0x1D400000 (GEEXEC, GEDLISTADDR), in psptek-registers.
