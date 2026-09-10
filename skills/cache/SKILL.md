---
name: cache
description: "The PSP data and instruction caches: how they work, the uncached 0x40000000 mirror, writeback and invalidation, and when code has to force them. Use when memory reads stale values, when writing code at run time, or when a patch that works on the emulator does not on hardware -- the PSX has no such cache, so none of this has a PSX counterpart."
---

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

---

::: doc-title
# PSP Cache HOWTO

[Jeremy Fitzhardinge \<<jeremy@goop.org>\>]{.author} [11 Oct 2005]{.date}

## Introduction

The PSP\'s MIPS CPU incorporates a data cache to speed up access to memory. The cache can be mostly ignored, but it cannot be forgotten. This HOWTO describes what the cache is, how it works, why and when you need to care about it, and what to do.

If this isn\'t clear, looks wrong, or anything else, please [mail me](mailto:jeremy@goop.org?subject=PSP%20Cache%20HOWTO).

## What is a cache?

The PSP\'s main CPU, where all your code runs, is a 32-bit MIPS RISC design. It normally runs at about 222-333MHz. This is much faster than the memory it is attached to. If it had to wait for memory every time it needs to read or write a value, then its effective speed would be much slower.

The MIPS solves this like all other modern CPUs: by having caches. A cache is a small piece of memory which is local to the CPU (typically on the same chip), which is much faster to access than main memory. The downside is that it\'s also much smaller than main memory (32kB vs 32MB on the PSP), so the CPU still needs to use main memory.

There are actually two caches: the data cache and the instruction cache. The data cache is used when your program does a load or store to memory, and the instruction cache is used to actually execute all the instructions of your program. In general you can ignore the instruction cache unless you\'re using dynamic code generation (but you probably know everything in this document if you\'re doing that), though the discussion of cache locality also applies to the instruction cache.

(The PSP\'s cache structure is pretty simple compared to other CPUs. There\'s only a 32k L1 cache; there\'s no L2 cache to worry about.)

## Cache structure and operation

OK, so the cache is a small piece of fast memory which keeps copies of pieces of main memory. How does it do this?

The 32k of cache is divided up into 64-byte chunks, called cache lines. The cache is managed in terms of cache lines, so even if you only use 1 byte of a line, all 64 bytes are allocated.

When the CPU goes to read a piece of memory, it first looks to see if there\'s a copy of the memory in cache. If there is, this is called a cache hit, and it can fetch the data in a few cycles. If not, this is a cache miss, and it will take a long time (possibly dozens of cycles) to fetch from main memory. However, on a cache miss, it will find a new cache line for the data, and read from main memory into the cache line; the next time you touch this 64-byte area of memory, it will probably get a cache hit.

Writes are similar. When your program writes to memory, it will just write into the cache, allocating a cache line if necessary. Subsequent writes and reads to that cache line will be cache hits.

A cache line can be in one of three states: invalid, clean or dirty. Invalid means that the cache line has no useful data, and no memory operation will hit it. Clean means that the cache line contains an up-to-date copy of a piece of main memory. Dirty means that the cache line has been written to, and main memory is out of date.

So, what does \"allocate a cache line\" mean? Because the cache is small relative to main memory, whenever you need a new cache line, you probably need to throw something else out. If the cache line you\'re replacing is invalid, then you can just start using it. If the line is clean, you can also just drop the old line and start using it. If it is dirty, however, you need to write the old contents back to memory before reusing the line; if you don\'t then previously written data will effectively disappear.

Note that this means that there\'s an indefinite, non-deterministic amount of time before a write actually hits main memory. The only thing which normally pushes a dirty cache line into memory is being replaced. If it is never replaced, then it will never be written.

(I could talk about the associativity of the cache and the replacement policy, but it isn\'t really relevant.)

## Cache Coherency

All this happens transparently from a software perspective. Apart from the performance effects of all this going on, there\'s really no way to know it\'s happening, and you can safely ignore it. Or can you?

The tricky part about all this is that the CPU ends up with its own copy of pieces of main memory. If the CPU were the only user of memory in the system, then this would be fine, but the PSP has several other functional units which all use memory, and communicate with the main CPU via memory. In order for this to work, you need to make sure that every user of memory has a consistent and coherent view of memory.

In the Intel world, the CPU performs something called \"cache snooping\". This means that a dedicated piece of hardware looks at all memory operations to main memory, and checks to see if the CPU\'s cache has a more up-to-date version of the memory. It also looks at memory writes, and makes sure that the CPU\'s cache has the most up-to-date version of the data.

The PSP\'s MIPS isn\'t like that. It has no snooping or hardware coherency support, which leads to a problem: if you simply write out a set of commands for the GE into memory, and then tell the GE to run them, there\'s no guarantee that your commands have actually been written to memory by the time GE tries to run them; they could just be still sitting there in dirty cache lines. You\'ll see some vertices looking fine, but others are way off in space. You\'ll see most of your texture, but chunks of it are missing or junk.

## The Uncached Address Space

The MIPS offers one solution to this problem: the uncached address space. If you bit-wise OR your pointer with 0x40000000 you end up with a corresponding pointer in the uncached address space, which is generally known as an uncached pointer. These two pointers are aliases: they\'re two different pointers which refer to the same piece of physical memory.

When you use the uncached pointer, the memory access completely bypasses all the machinery described above: reads will come straight from memory, and writes will go straight to memory.

This leads to a potential problem. If you use memory through the cached pointer, and then start using the uncached pointer, then you will be in a world of pain. It won\'t explode, crash or do anything obvious. It may seem to work perfectly well 99% of the time. But then you\'ll get bitten by strange, non-deterministic, elusive bugs which will move around and disappear every time you try to debug the problem.

When you use uncached memory, it completely ignores the cache, and the cache completely ignores the uncached access. If you write to cached memory, then read via uncached, you won\'t necessarily see the previously written value because it\'s still in cache. If you write via the uncached pointer, your write may get undone at some later arbitrary point when the dirty cache line eventually gets written.

The solution? You need to:

1.  **Always** use cache-line aligned allocations; this means `memalign` rather than `malloc` (and always make sure your allocation is a cache-line size multiple too).
2.  [Write-invalidate](#write-invalidate) memory before using an uncached pointer alias to the memory.

Note that even if you freshly allocate memory and never touch it with a cached pointer, you still need to write-invalidate the memory range, because it may still be partially cached from when it was previously allocated (this is quite likely, because efficient allocators will try to return still-cached memory for good cache use).

## Cache Management Functions

The PSP SDK also provides a set of functions for manipulating the cache. Their prototypes are in `<psputils.h>`. These are:

`void sceKernelDcacheWritebackAll(void)`
: Writes back all dirty cache-lines in memory. All cache lines which were previously valid will remain valid, but all dirty cache lines will become clean. This is useful for when you write some data to be read by another memory-using device.

`void sceKernelDcacheWritebackInvalidateAll(void)`
: This writes back all dirty cache-lines, and invalidates the whole cache. This is useful when you want to read some data written by another device. If another device writes memory, but the CPU has clean valid cache lines for that memory, it will read stale data unless you invalidate the cache first. This function is safe because it also writes dirty cache lines, so there\'s no risk of data loss.

`void sceKernelDcacheWritebackRange(const void *p, unsigned int size)`
: This writes back a range of memory, making the cache lines in that range clean. `p` and `size` should be aligned to the cache-line size. This will probably be more efficient than writing back the whole cache if size is relatively small, but if size is more than around 16k, it\'s probably better to just writeback the whole thing.

`void sceKernelDcacheWritebackInvalidateRange(const void *p, unsigned int size)`
: This writes back a range of memory and invalidates the cache for that range. `p` and `size` should be aligned to the cache-line size. This is like `sceKernelDcacheWritebackInvalidateAll`, but it only affects the specified memory range. This is likely to be more efficient, because it doesn\'t completely destroy the cache\'s working-set. You should **always** use this on a range of memory before accessing it via an uncached pointer.

`sceKernelDcacheInvalidateRange(const void *p, unsigned int size)`
: This function should be used with **extreme** caution. It will invalidate a range of cache lines; if they were previously dirty, then the dirty data will be discarded. This should be used when you want to force data to be fetched from main memory, and you\'re certain that there are no dirty cache lines in that range of memory. It is *very* important that `p` and `size` are cache-aligned. Because this function affects whole cache lines, if you pass an unaligned pointer or size, then you may end up affecting unintended data.

#### TODO

- Diagrams
