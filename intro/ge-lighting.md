GE commands 0x50 to 0x9A: the shade model, the material colours (emissive,
ambient, diffuse, specular, specular power, ambient alpha), the light model, and
then the type, position, direction, attenuation and colours of each of the four
lights.

Little of this bears on interface work. With lighting disabled through LTE none
of these registers reach the result, and the colour of a glyph or a box comes
from the vertex colour and from the texture function in ge-textures instead. Keep
the chapter for the opposite case: a display list thick with light commands is
describing the scene, which tells you the drawing you are looking for is not there.

The command format and the GE float are in ge-overview. The chapter is thin at
the end: the eight spot light registers at 0x87-0x8E are listed by argument only,
with no name, and 0x51 RNORM and 0x52 get no section at all.
