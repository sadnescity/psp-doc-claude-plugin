---
name: graphic-formats
description: "PSP pixel formats: the bit layout of the direct colour formats (1555, 4444, 565 and 8888), texture swizzling, and the PSP's DXT1/DXT3/DXT5 block layout. Use when decoding a texture or CLUT dumped from VRAM, or when a swizzled texture comes out shredded. Font formats (PGF) are in file-formats."
---

Chapter 27 is the pixel-level companion to the GE chapter: the bit layout of the
four direct formats (1555 ABGR, 4444 ABGR, 565 BGR, 8888 ABGR), a worked example
of swizzling, and the PSP's variant of DXT1, DXT3 and DXT5, whose block fields
are ordered differently from a .DDS file.

Read it after ge-textures has told you which format a texture is in: TPSM names
the mode, this chapter says what the bits mean, and the same four formats are the
CLUT entry formats. The swizzling section is the one that matters when a font or
a menu texture dumped out of VRAM comes back shredded - the GE works in blocks of
16 bytes by 8 rows, and a swizzled texture has been reordered into them.

There is nothing here about font formats: the PGF
file format is in file-formats. Nor is there anything on how the indexed formats
pack their pixels, and 27.6.2 DXT3 is an empty heading covered under DXT5.

---

## 27  Graphic Formats

### 27.1  1555 ABGR

+-----------------------------------------------------------------------+
|   -------- -------- -------- --------                                 |
|   `15`          `8` `7`           `0`                                 |
|   `abbb`     `bbgg` `gggr`     `rrrr`                                 |
|   -------- -------- -------- --------                                 |
+-----------------------------------------------------------------------+
|   ------------ --- -----------------                                  |
|    **bit(s)**      **description**                                    |
|                 a  alpha                                              |
|                 b  blue                                               |
|                 g  green                                              |
|                 r  red                                                |
|   ------------ --- -----------------                                  |
+-----------------------------------------------------------------------+

### 27.2  4444 ABGR

+-----------------------------------------------------------------------+
|   -------- -------- -------- --------                                 |
|   `15`          `8` `7`           `0`                                 |
|   `aaaa`     `bbbb` `gggg`     `rrrr`                                 |
|   -------- -------- -------- --------                                 |
+-----------------------------------------------------------------------+
|   ------------ --- -----------------                                  |
|    **bit(s)**      **description**                                    |
|                 a  alpha                                              |
|                 b  blue                                               |
|                 g  green                                              |
|                 r  red                                                |
|   ------------ --- -----------------                                  |
+-----------------------------------------------------------------------+

### 27.3  565 BGR

+-----------------------------------------------------------------------+
|   -------- -------- -------- --------                                 |
|   `15`          `8` `7`           `0`                                 |
|   `bbbb`     `bggg` `gggr`     `rrrr`                                 |
|   -------- -------- -------- --------                                 |
+-----------------------------------------------------------------------+
|   ------------ --- -----------------                                  |
|    **bit(s)**      **description**                                    |
|                 b  blue                                               |
|                 g  green                                              |
|                 r  red                                                |
|   ------------ --- -----------------                                  |
+-----------------------------------------------------------------------+

### 27.4  8888 ABGR

+---------------------------------------------------------------------------+
|   -------- -------- -------- -------- -------- -------- -------- -------- |
|   `31`         `24` `23`         `16` `15`          `8` `7`           `0` |
|   `aaaa`     `aaaa` `bbbb`     `bbbb` `gggg`     `gggg` `rrrr`     `rrrr` |
|   -------- -------- -------- -------- -------- -------- -------- -------- |
+---------------------------------------------------------------------------+
|   ------------ --- -----------------                                      |
|    **bit(s)**      **description**                                        |
|                 a  alpha                                                  |
|                 b  blue                                                   |
|                 g  green                                                  |
|                 r  red                                                    |
|   ------------ --- -----------------                                      |
+---------------------------------------------------------------------------+

### 27.5  swizzling

Internally, the GE processes textures as 16 bytes by 8 rows blocks (independent of actual pixelformat, so a 32\*32 32-bit texture is a 128\*32 texture from the swizzlings point of view). When you are not swizzling, this means it will have to do scattered reads from the texture as it moves the block into its texture-cache, which has a big impact on performance. To improve on this, you can re-order your textures into these blocks so that it can fetch one entire block by reading sequentially.\

+:-----------------------------------------------------------------------------------------------------------:+
|   ---------------------------------------------------- ---------------------------------------------------- |
|   `00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F`\   `0G 0H 0I 0J 0K 0L 0M 0N 0O 0P 0Q 0R 0S 0T 0U 0V`\   |
|   `10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F`\   `1G 1H 1I 1J 1K 1L 1M 1N 1O 1P 1Q 1R 1S 1T 1U 1V`\   |
|   `20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F`\   `2G 2H 2I 2J 2K 2L 2M 2N 2O 2P 2Q 2R 2S 2T 2U 2V`\   |
|   `30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F`\   `3G 3H 3I 3J 3K 3L 3M 3N 3O 3P 3Q 3R 3S 3T 3U 3V`\   |
|   `40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F`\   `4G 4H 4I 4J 4K 4L 4M 4N 4O 4P 4Q 4R 4S 4T 4U 4V`\   |
|   `50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F`\   `5G 5H 5I 5J 5K 5L 5M 5N 5O 5P 5Q 5R 5S 5T 5U 5V`\   |
|   `60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F`\   `6G 6H 6I 6J 6K 6L 6M 6N 6O 6P 6Q 6R 6S 6T 6U 6V`\   |
|   `70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F`    `7G 7H 7I 7J 7K 7L 7M 7N 7O 7P 7Q 7R 7S 7T 7U 7V`    |
|                                                                                                             |
|   ---------------------------------------------------- ---------------------------------------------------- |
+-------------------------------------------------------------------------------------------------------------+

\
The block above is a 32 bytes by 8 lines texture block (so it could be a 8\*8 32-bit block, or a 16\*8 16-bit block). Each pixel is represented here by a vertical index (first value) of 0-7. The second index is the horizontal index, ranging from 0-U. When reorganizing this for swizzling, we will order the data so that when the GE needs to read something in the first 16×8 block, if can just fetch that entire block, instead of offsetting into the texture for each line it has to read. The resulting swizzled portion looks like this:\

+:--------------------------------------------------------------------------------------------------------------:+
|   ------------------------------------------------------------------------------------------------------------ |
|   `00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F`**` `**`10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F`\   |
|   `20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F`**` `**`30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F`\   |
|   `40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F`**` `**`50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F`\   |
|   `60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F`**` `**`70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F`    |
|                                                                                                                |
|   `0G 0H 0I 0J 0K 0L 0M 0N 0O 0P 0Q 0R 0S 0T 0U 0V 1G 1H 1I 1J 1K 1L 1M 1N 1O 1P 1Q 1R 1S 1T 1U 1V`\           |
|   `2G 2H 2I 2J 2K 2L 2M 2N 2O 2P 2Q 2R 2S 2T 2U 2V 3G 3H 3I 3J 3K 3L 3M 3N 3O 3P 3Q 3R 3S 3T 3U 3V`\           |
|   `4G 4H 4I 4J 4K 4L 4M 4N 4O 4P 4Q 4R 4S 4T 4U 4V 5G 5H 5I 5J 5K 5L 5M 5N 5O 5P 5Q 5R 5S 5T 5U 5V`\           |
|   `6G 6H 6I 6J 6K 6L 6M 6N 6O 6P 6Q 6R 6S 6T 6U 6V 7G 7H 7I 7J 7K 7L 7M 7N 7O 7P 7Q 7R 7S 7T 7U 7V `           |
|   ------------------------------------------------------------------------------------------------------------ |
+----------------------------------------------------------------------------------------------------------------+

\
Notice how the rectangular 16\*8 blocks have ended up as sequential data, ready for direct reading by the GE.

### 27.6  S3TC Compression

Texture formats 8, 9 and 10 are DXT1, DXT3 and DXT5. The hardwares format is a little different from the standard (as you\'d find in a .DDS file, for example).

#### 27.6.1  DXT1

For DXT1, each 4x4 texel block has 2 16-bit 565 colours, and 16 2-bit per-texel fields (8 bytes/block). The PSP hardware expects the per-texel bits to come first, followed by the two colours. Colours are in RGB 565 format.

#### 27.6.2  DXT3

#### 27.6.3  DXT5

For DXT3 and DXT5, each 4x4 block has 8 bytes of alpha data followed by 8 bytes of pixel data. The PSP reverses this, so it wants the pixel data followed by alpha data. Also, the pixel data is normally encoded in the same way as the DXT1 blocks, which is also true for the PSP. The encoding is the same as for DXT1 textures, the colours are in RGB 565 format.
