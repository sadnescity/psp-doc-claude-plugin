GE commands 0xD2 to 0xEE, the per-pixel end of the pipeline: PSM for the frame
buffer format, CLEAR, SCISSOR1/SCISSOR2, NEARZ/FARZ, the colour, alpha, stencil
and depth tests, ALPHA with SFIX/DFIX for blending, dithering, logic op, the
depth and pixel masks, and the TRXKICK block transfer. Two closing sections
measure the texture cache and the bandwidth of texture reads from RAM and VRAM.

Two of these decide whether translated text is visible at all. The scissor
rectangle bounds what a draw may touch, so it is the first thing to read out of a
list when a string that got longer than the English one loses its tail; ALPHA and
ATST are how a glyph with an alpha channel is composited over the box behind it.

The command format and the GE float are in ge-overview. SCISSOR1 and SCISSOR2 are
given as bit fields with no prose, and ALPHA lists the values of the destination
function and the blend operation but leaves the source function without a table.
