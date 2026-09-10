Chapter 26, a catalogue of formats whose centre of gravity is the PRX section:
program headers, the .lib.ent and .lib.stub tables, .rodata.sceModuleInfo and
.rodata.sceResident, the ~PSP header an encrypted executable carries, and the
custom relocation format — section type 0x700000A0, entries of two words, with
the offset base and the address base packed into r_info beside the MIPS
relocation type. PBP, PARAM.SFO, PSAR, the PGF bitmap font format and a long
tail of registry and media formats follow it.

This is where the relocation entries are actually written down, which is what
decides whether an instruction added or moved inside BOOT.BIN still resolves
once the loader has relocated the module: r_offset is measured from one program
header, and the value already stored there is relocated from another.

The chapter is uneven. ELF gets three lines and a pointer to the standard ELF
documentation. .rodata.sceNid is a heading with nothing under it. Gamesave, AT3
and DIC are empty, and ISO, DAX and CSO get one line each, so there is nothing
here on ISO9660 or on the sector layout of a UMD. What the export and stub
tables are for once the module is running is in modules-and-patching; where
BOOT.BIN sits on the disc is in umd-game-structure.
