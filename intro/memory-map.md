Chapter 7: the six segment prefixes with their cached or uncached character
and the privilege each needs, the physical layout of scratchpad, video memory
and main memory, what sits where in kernel and user RAM, and a long list of
hardware register blocks given as address ranges tagged with the modules that
use them.

For patching, this is the chapter that says which window an address belongs
to. BOOT.BIN's loaded image lives in the user segment that starts at
0x08800000, so that is what an address read out of a PSP debugger normally is;
where in that window it lands is settled at load time, which is what the PRX
relocations are for (file-formats). Adding 0x40000000 to a pointer gives the
uncached alias of the same memory rather than a second buffer, and cache
explains why code does that.

Three things read oddly from the PSX. Video memory is plain CPU-addressable
RAM here, not something reachable only through GPU ports. The scratchpad is 16
kB, not a kilobyte. And every segment maps onto the same physical address, so
decoding an address means masking off the top three bits and nothing else.

Two limits. The hardware section gives blocks and their users, not bit fields;
psptek-registers has those. And the map is the 32 MB machine throughout — the
only 64 MB in YAPSPD is the DEM-100 dev kit, over in system-overview.
