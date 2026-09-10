PSPTEK, a register document written in 2012 by Alex Marshall, separate from
YAPSPD and covering the same ground as its chapter 8 and more: a spec sheet, a
memory map, a flat I/O map of every register address it knows, then device
sections for memory protection, the system controller, the interrupt
controller, the profiler, the VME controller, NAND, the Graphics Engine, KIRK,
the LCD controller, GPIO and the UARTs.

Open this one first when chasing a register access. The I/O map is the only
single-page index of register addresses in either source, and the device
sections name each register and its bits where YAPSPD often leaves them blank.
It is fuller than hardware-registers on memory protection, on the system
controller's NMI registers, and above all on the interrupt controller, where
YAPSPD has four addresses marked "mask ?" and this has flags, masks and the
numbered interrupt list. It alone documents the LCD controller and the GE
control registers; YAPSPD's video chapter carries no registers at all. Go back
to YAPSPD for the NAND transfer sequences, the KIRK key blobs and the per-bit
UART detail.

Addresses here are physical, 1C000000h and up; code uses the uncached kernel
window 0xA0000000 higher, which is the form YAPSPD prints. The contents list
ends in "Other: TODO", and audio, DMA, UMD, USB and Memory Stick are indeed
absent.
