Chapter 10 is short: VRAM at 0x04000000, 16-bit BGR or 32-bit pixels, a 480x272
visible screen inside a 512x272 virtual one, and then the four views of VRAM the
hardware exposes. The normal one holds the depth buffer in a swizzled-like order;
+2MiB is swizzled, +4MiB is identical to normal, and +6MiB adds a 32-byte column
interleave that hands back a linearised depth buffer with no work.

Use it when turning an address into a pixel or back: a frame buffer or texture
pointer taken out of a GE list (FBP and TBP0 give 24 bits, the top four come from
their width register) is in VRAM only if it falls in the range given here, and
the 480 visible columns sit inside a 512-pixel virtual width.

The chapter stops there, well short of what its title suggests: no display modes,
no framebuffer setup, nothing on the LCD controller. Those registers are in
psptek-registers, under LCDC at 0x1E140000, and memory-map has the VRAM range.
