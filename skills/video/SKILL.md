---
name: video
description: "PSP VRAM basics: VRAM at 0x04000000, the 16- and 32-bit pixel formats, the 480x272 screen inside a 512-pixel virtual width, and the four VRAM mirrors, one of which hands back a linearised depth buffer. Use when turning a framebuffer or texture address into pixels or back, or reading the depth buffer out of VRAM. Display modes and the LCD controller are not here: see psptek-registers."
---

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

---

## 10  Video Processing

### 10.1  Overview

- vram is located at `0x04000000`\
- Pixel format is 16 bit BGR (ABBBBBGGGGGRRRRR.) or 32 bit
- visible Screen is 480\*272 pixel
- virtual Screensize is 512\*272 pixel

### 10.2  VRAM Mirrors

Writing to the VRAM Mirrors seem to have no effect; setting the drawbuffer pointer to one of these VRAM aliases just works as normal. So these Mirrors only have effects for reads, but work for all readers. (GE, Framebuffer scandout\...)

#### 10.2.1  VRAM

*[Figure: 512x272 colour buffer of the test scene: a shaded knot of interlocking tube rings in purple on a lavender background, with a debug timing bar along the bottom.]*

##### 10.2.1.1 [  Depth Buffer]{#sec10.2.1.1}

The raw depth buffer in the normal VRAM space is rearranged in a swizzled-like way. This is the raw dump of the depth buffer converted to an 8bpp greyscale: *[Figure: the depth buffer read from normal VRAM as 8bpp greyscale: no longer recognisable as the object, just fragments cut into vertical strips and scattered across the image.]*

#### 10.2.2  VRAM +2Mib

VRAM with \"swizzle\" *[Figure: the depth buffer read through the VRAM+2MiB mirror as 8bpp greyscale: the object is broken into regular vertical stripes, 16 pixels wide, that are out of order.]* This is clearly a fairly simple structure, with a simple column-wise rearrangement of each 16 pixel (32 byte) strip. When rearranged, it looks as expected: *[Figure: the VRAM+2MiB dump after reordering the columns: a clean greyscale depth image of the ring knot on black, the same shape as the colour buffer above.]*

#### 10.2.3  VRAM +4Mib

identical to normal VRAM

#### 10.2.4  VRAM +6Mib

VRAM with \"swizzle\" + 32-byte column interleave. Reading from VRAM+6Mib will give you a proper linearized version of the depth buffer with no effort. The GE sees the same view; a GE copy operation returns the same data (represented as RGB 565): *[Figure: 480x272 frame with the depth buffer, read via VRAM+6MiB, copied by the GE and shown as RGB565: the knot appears as green/blue banded tubes in a black rectangle drawn over the lavender scene.]*
