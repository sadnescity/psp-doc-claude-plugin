GE commands 0x9B to 0xD0: where the GE reads and writes pixels. FBP/FBW and
ZBP/ZBW set the frame and depth buffers, TBP0-7, TBW0-7 and TSIZE0-7 the texture
of each mipmap level, CBP/CBPH the CLUT, TRXSBP/TRXDBP a buffer transfer; TMAP,
TMODE, TPSM, CMODE, TFLT, TWRAP, TFUNC and TEC how it is sampled, FDIST/FCOL fog.

This is the half of the chapter that answers where a font is: the texture address
is TBP0 plus the high bits in TBW0, the format is TPSM (modes 4 to 7 are indexed
and need a CLUT at CBP/CBPH, its format in CMODE), the size is TSIZE0, TMODE bit
0 says whether the texels are swizzled - graphic-formats explains that layout -
and TFUNC whether the texture replaces the vertex colour or is modulated by it.

The command format, the GE float and BASE are in ge-overview. Two gaps: CMODE
documents only its mask and pixel format, its other two fields being marked ???,
and FFAR (0xCD) is named in the command table but has no section.
