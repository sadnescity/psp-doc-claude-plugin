Jeremy Fitzhardinge's PSP Cache HOWTO, 2005, from the uofw/upspd collection.
It is the fuller copy of the text YAPSPD reproduces as chapter 4.10, which the
cpu-cache skill holds: this one keeps the opening on why a cache exists at all
and the note that the prototypes are in psputils.h. Prefer it.

The practical part is short and worth having exactly right. Cache lines are
managed whole, a dirty line reaches main memory only when it is evicted,
nothing on this machine snoops, and the 0x40000000 alias of a pointer bypasses
the cache completely — which is why mixing the cached and the uncached view of
one buffer fails quietly and only sometimes. The PSX has none of this, so a
PSX hack brings no habits for it and nothing in one prepares you to expect it.

The document covers the data cache only. The instruction cache is named, set
aside as a concern for dynamic code generation, and never returned to — no
invalidation function for it appears anywhere, which matters for a hack that
writes code into RAM at run time rather than into BOOT.BIN. It ends on a TODO
for diagrams that was never filled in.
