Chapter 27 is the pixel-level companion to the GE chapter: the bit layout of the
four direct formats (1555 ABGR, 4444 ABGR, 565 BGR, 8888 ABGR), a worked example
of swizzling, and the PSP's variant of DXT1, DXT3 and DXT5, whose block fields
are ordered differently from a .DDS file.

Read it after ge-textures has told you which format a texture is in: TPSM names
the mode, this chapter says what the bits mean, and the same four formats are the
CLUT entry formats. The swizzling section is the one that matters when a font or
a menu texture dumped out of VRAM comes back shredded - the GE works in blocks of
16 bytes by 8 rows, and a swizzled texture has been reordered into them.

Despite the skill description, there is nothing here about font formats: the PGF
file format is in file-formats. Nor is there anything on how the indexed formats
pack their pixels, and 27.6.2 DXT3 is an empty heading covered under DXT5.
