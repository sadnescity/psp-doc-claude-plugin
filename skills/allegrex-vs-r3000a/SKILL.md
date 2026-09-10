---
name: allegrex-vs-r3000a
description: "What the PSP's Allegrex CPU has that the PSX's R3000A does not: branch-likely (beql, bnel, blezl, bgtzl), ext, ins, seb, seh, wsbh, rotr, movz, movn, clz, mul, madd — with their encodings and the delay-slot rule that differs. Use when porting PSX assembly work to PSP, when a disassembler prints .word in the middle of code, or before patching an instruction whose meaning is not obvious."
---

# Allegrex against R3000A

The instruction chapters of both sources stop short: YAPSPD documents three MIPS
instructions and three Allegrex ones and leaves the rest to the MIPS manuals,
and the module tutorial's assembly section is a primer. This fills the gap for
the case that matters when carrying work over from the PlayStation: the PSP core
is a **MIPS32 (R4000-based) Allegrex**, the PSX one an **R3000A**, and the extra
instructions are exactly where a PSX-trained eye, or a PSX-era disassembler,
goes wrong.

## The trap

A disassembler written for the R3000A prints `.word` for anything it does not
know. Those words are **not data**: patching over one, or reading past it as if
the function ended there, breaks a jump with nothing to warn you.

Measured on a real PSP game (Breath of Fire III, 783360 words of code): an
R3000A-only decoder failed on **3.6%** of them, and the two most frequent were
`bnel` (3178) and `beql` (2758).

## Branch-likely — the ones that bite

| mnemonic | opcode | encoding |
|---|---|---|
| `beql rs,rt,off` | `0x50000000` | `010100 sssss ttttt oooooooooooooooo` |
| `bnel rs,rt,off` | `0x54000000` | `010101 sssss ttttt oooooooooooooooo` |
| `blezl rs,off` | `0x58000000` | `010110 sssss 00000 oooooooooooooooo` |
| `bgtzl rs,off` | `0x5C000000` | `010111 sssss 00000 oooooooooooooooo` |
| `bltzl rs,off` | `0x04020000` | REGIMM, rt = `00010` |
| `bgezl rs,off` | `0x04030000` | REGIMM, rt = `00011` |

**The delay slot rule is different.** On a plain `beq`/`bne` the delay-slot
instruction always runs. On the *likely* forms it runs **only if the branch is
taken**; if it is not, the slot is nullified. Compilers use them to hoist the
first instruction of a loop body, so the slot usually carries real work — which
is why treating one as `nop` filler, the way a PSX habit suggests, changes what
the code does.

## MIPS32 instructions the R3000A has not

| mnemonic | opcode | notes |
|---|---|---|
| `ext rt,rs,pos,size` | `0x7C000000` fn `000000` | bitfield extract; rd holds size-1 |
| `ins rt,rs,pos,size` | `0x7C000004` fn `000100` | bitfield insert; rd holds pos+size-1 |
| `seb rd,rt` | `0x7C000420` | sign-extend byte (SPECIAL3/BSHFL, sa = `10000`) |
| `seh rd,rt` | `0x7C000620` | sign-extend halfword (sa = `11000`) |
| `wsbh rd,rt` | `0x7C000020` | swap bytes within halfwords (sa = `00010`) |
| `rotr rd,rt,sa` | SPECIAL fn `000010`, bit 21 set | rotate right — shares the `srl` encoding |
| `rotrv rd,rt,rs` | SPECIAL fn `000110`, bit 6 set | shares `srlv` |
| `movz rd,rs,rt` | SPECIAL fn `001010` | move if rt is zero |
| `movn rd,rs,rt` | SPECIAL fn `001011` | move if rt is not zero |
| `mul rd,rs,rt` | SPECIAL2 fn `000010` | result straight into rd, HI/LO untouched |
| `madd/maddu/msub/msubu` | SPECIAL2 fn `000000/000001/000100/000101` | multiply-accumulate into HI/LO |
| `clz/clo rd,rs` | SPECIAL2 fn `100000/100001` | count leading zeroes/ones |

`rotr` hiding inside the `srl` encoding is worth remembering: an R3000A decoder
reads `rotr t0,t1,4` as `srl t0,t1,4` and says nothing.

## Allegrex-only

| mnemonic | opcode | notes |
|---|---|---|
| `halt` | `0x70000000` | wait for an interrupt |
| `mfic rt,rd` | `0x70000024` | read the interrupt controller state |
| `mtic rt,rd` | `0x70000026` | write it |
| `bitrev rd,rt` | SPECIAL3, BSHFL sa = `10100` | reverse the bits of a word |

Also present: the VFPU as COP2 (`op = 010010`). On the R3000A COP2 is the GTE,
so a `cop2` opcode carried over from PSX habits means nothing familiar here —
see cpu-fpu-vfpu.

## What the PSP has *not*, despite being newer

- 64-bit instructions
- `ll`, `sc`, `ldc1`, `sdc1`, `ldc2`, `sdc2`, `lwc2`, `swc2` — some replaced by
  VFPU equivalents under other names
- trap and TLB instructions
- `bltzal`, `bgezal`, `bltzall`, `bgezall`
- COP2 branch instructions

## Checking your own tools

The quick test on any disassembler you rely on: feed it `0x54000000` and
`0x7C000420`. If they come back as `bnel` and `seb` it understands the Allegrex;
if they come back as `.word`, it is an R3000A decoder and every branch-likely in
the binary is invisible to it.
