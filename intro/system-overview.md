YAPSPD's chapter 2, a spec sheet for the PSP-1000: the two Allegrex cores and
their clock range, the memory sizes, the screen, then model codes, the box-code
table that maps a letter on the retail carton to the firmware inside, and the
accessories with their 2005 prices.

For reverse engineering the useful content is three numbers, 32MB of main
memory, a 480x272 screen and a second CPU, plus the note that the development
unit had 64MB where the retail one has 32. Addresses belong to memory-map, the
framebuffer to video, the second CPU to media-engine.

It stops at the PSP-1000 and its regional variants, so there is nothing on the
later models. psptek-registers opens with the same spec sheet redone in 2012,
which does cover them, and the two do not agree on the embedded DRAM: this
chapter says 4MB, PSPTEK says 8MB of VRAM, while memory-map gives a 2MB VRAM
window at 0x04000000 and video documents the mirrors above it. Trust memory-map
for anything you intend to address.
