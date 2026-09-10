This is YAPSPD 4.10, and it is Jeremy Fitzhardinge's cache HOWTO reproduced:
same sections, same sentences, minus the opening that explains what a cache is
for and minus the note that the prototypes live in psputils.h, plus a few
transcription errors. The cache skill holds the same document from its own
source, fuller and cleaner. Read that one; this exists because it is part of
chapter 4.

In either copy the content has no PSX counterpart, since the R3000A has no
writeback data cache to flush, and the failure it describes is the silent
kind: data still sitting in a dirty cache line that another unit never sees.

Note the scope. All five functions listed are Dcache; the instruction cache is
named once, set aside as something only dynamic code generation need worry
about, and never given a function. Writing instructions into RAM at run time
is precisely that case.
