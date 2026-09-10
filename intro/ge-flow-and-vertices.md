GE commands 0x01 to 0x4D: what moves a display list along and what describes
geometry. VADDR and IADDR point at the vertex and index arrays, PRIM kicks them,
JUMP/BJUMP/CALL/RET/END/SIGNAL/FINISH structure the list, VTYPE says how one
vertex is laid out, and the rest set the matrices, the draw region, bones and
morph weights, and the viewport scale and offset.

This is usually where the hunt for whoever draws a menu box or a string ends. 2D
drawing is a PRIM with primitive type 110, sprites, over vertices whose VTYPE has
bit 23 set - what the chapter calls Bypass Transform Pipeline, raw coordinates
instead of transformed ones. VTYPE is also what lets you read the array VADDR
points at, since it gives the presence and the width of every field in a vertex.

In ge-overview: the command format, the GE float, BASE, and the four commands of
this range that get no section here (0x13, 0x14, and the matrix selects).
