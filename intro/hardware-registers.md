The first half of YAPSPD's chapter 8: memory protection at 0xBC000000, system
config at 0xBC100000 (NMI, RAM size, the SC/ME RPC interrupt and semaphore, the
reset, bus-clock and I/O enables), the interrupt controller, the profiler, the
block it calls ME Control, and the NAND controller. Addresses are written as
code uses them, in the uncached kernel window, so use it when a routine stores
somewhere in the 0xBC-0xBF range and you need the device behind it.

psptek-registers covers the same devices from a second document and is fuller on
most of them: it names every register, has twelve memory-protection registers
where this has four, and turns the interrupt controller, four addresses labelled
"mask ?" here, into named flag and mask registers with the interrupt list beside
them. Come back here for the profiler procedure and the NAND command set and
transfer sequences. The register that is 1C000000h there is 0xBC000000 here:
physical against kernel-uncached, a difference of 0xA0000000.

Neither half of chapter 8 covers audio, UMD, Memory Stick, USB, WLAN or the DMA
controllers; those YAPSPD chapters are stubs and ship as no skill at all.
Several bit tables here are printed empty.
