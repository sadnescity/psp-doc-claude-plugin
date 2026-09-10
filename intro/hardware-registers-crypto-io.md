The rest of YAPSPD's chapter 8: the KIRK crypto engine at 0xBDE00000, GPIO, and
two of the eight UART blocks, the one it calls UART4 and the one it calls UART3,
the headphone/remote SIO. Game code reaches none of this directly; it matters
when following how an EBOOT, a save or a UMD is decrypted, since every such path
ends in a KIRK command.

Against psptek-registers, which covers the same four devices, the two are
complementary rather than one being fuller. PSPTEK names the whole command set,
documents the phase and status registers, and states that KIRK's source and
destination pointers must be physical addresses; this chapter gives the buffer
sizes each command expects and which firmware module issues it, and prints two
key blobs PSPTEK does not have, with no word on what they unlock. On the UARTs
this chapter is the more detailed, with per-bit status and control, while PSPTEK
lists all eight blocks and only the bits they share. Mind the numbering there:
the block called UART3 here sits at the address PSPTEK numbers UART5, and
PSPTEK's interrupt list is the one that ties UART5 to the remote. On GPIO
neither source knows what the pins are wired to, and both leave the tables blank.
