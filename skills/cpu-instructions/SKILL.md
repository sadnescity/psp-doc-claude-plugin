---
name: cpu-instructions
description: "PSP instruction encoding: the instruction format, the MIPS instructions YAPSPD documents, the Allegrex-only ones (halt, mfic, mtic) and the VFPU instruction set. Use when decoding an opcode by hand. For what the Allegrex has and the PSX R3000A has not, read allegrex-vs-r3000a first: this chapter is thin on that."
---

The instruction formats come first — I-type, J-type and R-type with their bit
fields — and that is the part worth keeping, for decoding a word by hand. What
follows is uneven. Section 4.7, "MIPS Instructions", documents lw, sw and
addiu and stops; 4.8 adds the three Allegrex-only opcodes, halt, mfic and
mtic; 4.9 is the remaining four fifths of the chapter, thirty-seven VFPU
instructions with encodings and a page each.

So this is not an instruction set reference. There is not one branch or jump
in it, no beq, bne, j or jal, even though the J-type format is defined and
then never used by anything. When carrying a PSX hack over, read
allegrex-vs-r3000a first: the opcodes that quietly break a patch to BOOT.BIN
are the ones the Allegrex has and the R3000A has not, and none of them appear
here.

Section 4.8 does earn its place. mfic and mtic are how interrupts are masked
on this machine, with the save, disable and restore idiom spelled out, and
halt is what the kernel idle thread runs. The PSX has no equivalent of either.

---

## 4  CPU Overview

### 4.6  Instruction Format

Every CPU instruction consists of a single word (32 bits) aligned on a word boundary and the major instruction formats are shown here:

- I-Type (Immediate)
  +:---------------------------------------------------------------------:+
  |   ---------- --------- --------- --------------------                 |
  |   `op    `   `rs   `   `rt   `   `immediate       `                   |
  |   `oooooo`   `sssss`   `ttttt`   `iiiiiiiiiiiiiiii`                   |
  |   `31  26`   `25 21`   `20 16`   `15             0`                   |
  |   ---------- --------- --------- --------------------                 |
  +-----------------------------------------------------------------------+
- J-Type (Jump)
  +:---------------------------------------------------------------------:+
  |   ---------- ------------------------------                           |
  |   `op    `   `target                    `                             |
  |   `oooooo`   `tttttttttttttttttttttttttt`                             |
  |   `31  26`   `25                       0`                             |
  |   ---------- ------------------------------                           |
  +-----------------------------------------------------------------------+
- R-Type (Register)
  +:---------------------------------------------------------------------:+
  |   ---------- --------- --------- --------- --------- ----------       |
  |   `op    `   `rs   `   `rt   `   `rd   `   `shamt`   `func  `         |
  |   `oooooo`   `sssss`   `ttttt`   `ddddd`   `aaaaa`   `ffffff`         |
  |   `31  26`   `25 21`   `20 16`   `15 11`   `10  6`   `5    0`         |
  |   ---------- --------- --------- --------- --------- ----------       |
  +-----------------------------------------------------------------------+

where:

+:------------------------------------------------------------------------------:+
|   ----------- ---------------------------------------------------------------- |
|   op          6-bit operation code                                             |
|   rs          5-bit source register specifier                                  |
|   rt          5-bit target (source/destination) register or branch condition   |
|   immediate   16-bit immediate, branch displacement or address displacement    |
|   target      26-bit jump target address                                       |
|   rd          5-bit destination register specifier                             |
|   shamt       5-bit shift amount                                               |
|   func        6-bit function field                                             |
|   ----------- ---------------------------------------------------------------- |
+--------------------------------------------------------------------------------+

### 4.7  MIPS Instructions

[]{#tth_tAb1}

+--------------------------------------------------------------------------------------------------------------------------------------------+
|   --------------------- -------------- --------------------------------------- ----------------------------------------------------------- |
|   **Mnemonic**          **Opcode**     `op     rs    rt    offset          `   **Description**                                             |
|   `lw rt, offset(rs)`   `0x8c000000`   `100011 sssss ttttt oooooooooooooooo`   LoadWord Relative to Address in General Purpose Register    |
|   `sw rt, offset(rs)`   `0xac000000`   `101011 sssss ttttt oooooooooooooooo`   StoreWord Relative to Address in General Purpose Register   |
|   --------------------- -------------- --------------------------------------- ----------------------------------------------------------- |
+--------------------------------------------------------------------------------------------------------------------------------------------+

[]{#tth_tAb1}

+------------------------------------------------------------------------------------------------------------------+
|   ------------------------- -------------- --------------------------------------- ----------------------------- |
|   **Mnemonic**              **Opcode**     `op     rs    rt    immediate       `   **Description**               |
|   `addiu rt,rs,immediate`   `0x24000000`   `001001 sssss ttttt iiiiiiiiiiiiiiii`   Add Immediate Unsigned Word   |
|   ------------------------- -------------- --------------------------------------- ----------------------------- |
+------------------------------------------------------------------------------------------------------------------+

#### 4.7.1  lw

+---------------------------------------------------------------------------+
|   -------- -------------------------------------------------------------- |
|   **lw**   **LoadWord Relative to Address in General Purpose Register**   |
|            `%rt <- word_at_address (offset + %base)`                      |
|   -------- -------------------------------------------------------------- |
+---------------------------------------------------------------------------+
|   -------------------------- ---                                          |
|    `lw %rt, offset(%base) `                                               |
|   -------------------------- ---                                          |
+---------------------------------------------------------------------------+
|   ---------- --------------------------------------------                 |
|   `%rt`      GPR Target Register (0\...31)                                |
|   `%base`    GPR, specifies Source Address Base                           |
|   `offset`   signed Offset added to Source Address Base                   |
|   ---------- --------------------------------------------                 |
+---------------------------------------------------------------------------+

#### 4.7.2  sw

+----------------------------------------------------------------------------+
|   -------- --------------------------------------------------------------- |
|   **sw**   **StoreWord Relative to Address in General Purpose Register**   |
|            `word_at_address (offset + %base) <- %rt`                       |
|   -------- --------------------------------------------------------------- |
+----------------------------------------------------------------------------+
|   -------------------------- ---                                           |
|    `sw %rt, offset(%base) `                                                |
|   -------------------------- ---                                           |
+----------------------------------------------------------------------------+
|   ---------- --------------------------------------------                  |
|   `%rt`      GPR Target Register (0\...31)                                 |
|   `%base`    GPR, specifies Source Address Base                            |
|   `offset`   signed Offset added to Source Address Base                    |
|   ---------- --------------------------------------------                  |
+----------------------------------------------------------------------------+

#### 4.7.3  addiu

+-----------------------------------------------------------------------+
|   ----------- -----------------------------------------               |
|   **addiu**   **Add Immediate Unsigned Word**                         |
|               `%rt <- %rs + sign_extended(immediate)`                 |
|   ----------- -----------------------------------------               |
+-----------------------------------------------------------------------+
|   ------------------------------ ---                                  |
|    `addiu %rt, %rs, immediate `                                       |
|   ------------------------------ ---                                  |
+-----------------------------------------------------------------------+
|   ------------- --------------------------------                      |
|   `%rt`         GPR Target Register (0\...31)                         |
|   `%rs`         GPR Source Register (0\...31)                         |
|   `immediate`   value added to Source Register                        |
|   ------------- --------------------------------                      |
+-----------------------------------------------------------------------+

### 4.8  Allegrex Instructions

[]{#tth_tAb1}

+-----------------------------------------------------------------------------------------------------------------+
|   -------------- -------------- ----------------------------------------- ------------------------------------- |
|   **Mnemonic**   **Opcode**     `op     rs    rt    rd    shamt func`     **Description**                       |
|   `halt`         `0x70000000`   `011100 00000 00000 00000 00000 000000`   halt execution until next interrupt   |
|   `mfic rt,rd`   `0x70000024`   `011100 00000 ttttt ddddd 00000 100100`   move from IC (Interrupt) register     |
|   `mtic rt,rd`   `0x70000026`   `011100 00000 ttttt ddddd 00000 100110`   move to IC (Interrupt) register       |
|   -------------- -------------- ----------------------------------------- ------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------+

#### 4.8.1  halt

+-----------------------------------------------------------------------+
|   ---------- -----------------------------------------                |
|   **halt**   **halt execution until next interrupt**                  |
|                                                                       |
|   ---------- -----------------------------------------                |
+-----------------------------------------------------------------------+
|   -------- ---                                                        |
|    `halt`                                                             |
|   -------- ---                                                        |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

- this instruction is used in the idle-thread of the kernel, probably to initiate power saving

#### 4.8.2  mfic / mtic

+-----------------------------------------------------------------------+
|   ---------- ---------------------------------------                  |
|   **mfic**   **move from IC (Interrupt) register**                    |
|                                                                       |
|   ---------- ---------------------------------------                  |
+-----------------------------------------------------------------------+
|   -------------- ---                                                  |
|    `mfic rt,rd`                                                       |
|   -------------- ---                                                  |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

\

+-----------------------------------------------------------------------+
|   ---------- -------------------------------------                    |
|   **mtic**   **move to IC (Interrupt) register**                      |
|                                                                       |
|   ---------- -------------------------------------                    |
+-----------------------------------------------------------------------+
|   -------------- ---                                                  |
|    `mtic rt,rd`                                                       |
|   -------------- ---                                                  |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

- `mfic $v0, zero`\
  to save the interrupt state in v0
- `mtic zero, zero`\
  to disable them
- `mtic $a0, zero`\
  to renable based on the original mask in a0

### 4.9  VFPU Instructions

[]{#tth_tAb1}

+------------------------------------------------------------------------------------------------------------------------------------------+
|   --------------------------- -------------- ----------------------------------------- ------------------------------------------------- |
|   **Mnemonic**                **Opcode**     `op     rs    rt    offset         c  `   **Description**                                   |
|   `lv.q rt, offset(rs)`       `0xd8000000`   `110110 sssss ttttt oooooooooooooo 0 t`   LoadVector.Quadword Relative to Address in GPR    |
|   `sv.q rt, offset(rs), wb`   `0xf8000000`   `111110 sssss ttttt oooooooooooooo w t`   StoreVector.Quadword Relative to Address in GPR   |
|   --------------------------- -------------- ----------------------------------------- ------------------------------------------------- |
+------------------------------------------------------------------------------------------------------------------------------------------+

[]{#tth_tAb1}

+-------------------------------------------------------------------------------------------------------------------+
|   ----------------------- --------------- ------------------------------------------ ---------------------------- |
|   **Mnemonic**            **Opcode**      `op         rt        rs        rd     `   **Description**              |
|   `vadd.s rd,rs,rt`       `0x60000000`    `011000 000 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vadd.p rd,rs,rt`       `0x60000080`    `011000 000 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vadd.t rd,rs,rt`       `0x60008000`    `011000 000 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vadd.q rd,rs,rt`       `0x60008080`    `011000 000 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vsub.s rd,rs,rt`       `0x60800000`    `011010 000 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vsub.p rd,rs,rt`       `0x60800080`    `011010 000 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vsub.t rd,rs,rt`       `0x60808000`    `011010 000 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vsub.q rd,rs,rt`       `0x60808080`    `011010 000 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vdiv.s rd,rs,rt`       `0x63800000`    `011000 111 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vdiv.p rd,rs,rt`       `0x63800080`    `011000 111 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vdiv.t rd,rs,rt`       `0x63808000`    `011000 111 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vdiv.q rd,rs,rt`       `0x63808080`    `011000 111 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vmul.s rd,rs,rt`       `0x64000000`    `011001 000 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vmul.p rd,rs,rt`       `0x64000080`    `011001 000 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vmul.t rd,rs,rt`       `0x64008000 `   `011001 000 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vmul.q rd,rs,rt`       `0x64008080`    `011001 000 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vdot.p rd,rs,rt`       `0x64800080`    `011001 001 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vdot.t rd,rs,rt`       `0x64808000`    `011001 001 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vdot.q rd,rs,rt`       `0x64808080`    `011001 001 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vhdp.p rd,rs,rt`       `0x66000080`    `011001 100 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vhdp.t rd,rs,rt`       `0x66008000`    `011001 100 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vhdp.q rd,rs,rt`       `0x66008080`    `011001 100 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vmin.s rd,rs,rt`       `0x6D000000`    `011011 010 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vmin.p rd,rs,rt`       `0x6D000080`    `011011 010 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vmin.t rd,rs,rt`       `0x6D008000`    `011011 010 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vmin.q rd,rs,rt`       `0x6D008080`    `011011 010 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vmax.s rd,rs,rt`       `0x6D800000`    `011011 011 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vmax.p rd,rs,rt`       `0x6D800080`    `011011 011 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vmax.t rd,rs,rt`       `0x6D808000`    `011011 011 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vmax.q rd,rs,rt`       `0x6D808080`    `011011 011 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vabs.s rd,rs`          `0xd0010000`    `110100 000 0000001 0 sssssss 0 ddddddd`                                |
|   `vabs.p rd,rs`          `0xd0010080`    `110100 000 0000001 0 sssssss 1 ddddddd`                                |
|   `vabs.t rd,rs`          `0xd0018000`    `110100 000 0000001 1 sssssss 0 ddddddd`                                |
|   `vabs.q rd,rs`          `0xd0018080`    `110100 000 0000001 1 sssssss 1 ddddddd`                                |
|   `vneg.s rd,rs`          `0xd0020000`    `110100 000 0000010 0 sssssss 0 ddddddd`                                |
|   `vneg.p rd,rs`          `0xd0020080`    `110100 000 0000010 0 sssssss 1 ddddddd`                                |
|   `vneg.t rd,rs`          `0xd0028000`    `110100 000 0000010 1 sssssss 0 ddddddd`                                |
|   `vneg.q rd,rs`          `0xd0028080`    `110100 000 0000010 1 sssssss 1 ddddddd`                                |
|   `vidt.p rd`             `0xd0030080`    `110100 000 0000011 0 0000000 1 ddddddd`                                |
|   `vidt.t rd`             `0xd0038000`    `110100 000 0000011 1 0000000 0 ddddddd`                                |
|   `vidt.q rd`             `0xd0038080`    `110100 000 0000011 1 0000000 1 ddddddd`                                |
|   `vzero.s rd`            `0xd0060000`    `110100 000 0000110 0 0000000 0 ddddddd`   SetVectorZero.Single         |
|   `vzero.p rd`            `0xd0060080`    `110100 000 0000110 0 0000000 1 ddddddd`   SetVectorZero.Pair           |
|   `vzero.t rd`            `0xd0068000`    `110100 000 0000110 1 0000000 0 ddddddd`   SetVectorZero.Triple         |
|   `vzero.q rd`            `0xd0068080`    `110100 000 0000110 1 0000000 1 ddddddd`   SetVectorZero.Quad           |
|   `vone.s rd`             `0xd0070000`    `110100 000 0000111 0 0000000 0 ddddddd`   SetVectorOne.Single          |
|   `vone.p rd`             `0xd0070080`    `110100 000 0000111 0 0000000 1 ddddddd`   SetVectorOne.Pair            |
|   `vone.t rd`             `0xd0078000`    `110100 000 0000111 1 0000000 0 ddddddd`   SetVectorOne.Triple          |
|   `vone.q rd`             `0xd0078080`    `110100 000 0000111 1 0000000 1 ddddddd`   SetVectorOne.Quad            |
|   `vrcp.s rs,rd`          `0xd0100000`    `110100 000 0010000 0 sssssss 0 ddddddd`                                |
|   `vrcp.p rs,rd`          `0xd0100080`    `110100 000 0010000 0 sssssss 1 ddddddd`                                |
|   `vrcp.t rs,rd`          `0xd0108000`    `110100 000 0010000 1 sssssss 0 ddddddd`                                |
|   `vrcp.q rs,rd`          `0xd0108080`    `110100 000 0010000 1 sssssss 1 ddddddd`                                |
|   `vrsq.s rs,rd`          `0xd0110000`    `110100 000 0010001 0 sssssss 0 ddddddd`                                |
|   `vrsq.p rs,rd`          `0xd0110080`    `110100 000 0010001 0 sssssss 1 ddddddd`                                |
|   `vrsq.t rs,rd`          `0xd0118000`    `110100 000 0010001 1 sssssss 0 ddddddd`                                |
|   `vrsq.q rs,rd`          `0xd0118080`    `110100 000 0010001 1 sssssss 1 ddddddd`                                |
|   `vsin.s rs,rd`          `0xd0120000`    `110100 000 0010010 0 sssssss 0 ddddddd`                                |
|   `vsin.p rs,rd`          `0xd0120080`    `110100 000 0010010 0 sssssss 1 ddddddd`                                |
|   `vsin.t rs,rd`          `0xd0128000`    `110100 000 0010010 1 sssssss 0 ddddddd`                                |
|   `vsin.q rs,rd`          `0xd0128080`    `110100 000 0010010 1 sssssss 1 ddddddd`                                |
|   `vcos.s rs,rd`          `0xd0130000`    `110100 000 0010011 0 sssssss 0 ddddddd`                                |
|   `vcos.p rs,rd`          `0xd0130080`    `110100 000 0010011 0 sssssss 1 ddddddd`                                |
|   `vcos.t rs,rd`          `0xd0138000`    `110100 000 0010011 1 sssssss 0 ddddddd`                                |
|   `vcos.q rs,rd`          `0xd0138080`    `110100 000 0010011 1 sssssss 1 ddddddd`                                |
|   `vexp2.s rs,rd`         `0xd0140000`    `110100 000 0010100 0 sssssss 0 ddddddd`                                |
|   `vexp2.p rs,rd`         `0xd0140080`    `110100 000 0010100 0 sssssss 1 ddddddd`                                |
|   `vexp2.t rs,rd`         `0xd0148000`    `110100 000 0010100 1 sssssss 0 ddddddd`                                |
|   `vexp2.q rs,rd`         `0xd0148080`    `110100 000 0010100 1 sssssss 1 ddddddd`                                |
|   `vlog2.s rs,rd`         `0xd0150000`    `110100 000 0010101 0 sssssss 0 ddddddd`                                |
|   `vlog2.p rs,rd`         `0xd0150080`    `110100 000 0010101 0 sssssss 1 ddddddd`                                |
|   `vlog2.t rs,rd`         `0xd0158000`    `110100 000 0010101 1 sssssss 0 ddddddd`                                |
|   `vlog2.q rs,rd`         `0xd0158080`    `110100 000 0010101 1 sssssss 1 ddddddd`                                |
|   `vsqrt.s rs,rd`         `0xd0160000`    `110100 000 0010110 0 sssssss 0 ddddddd`                                |
|   `vsqrt.p rs,rd`         `0xd0160080`    `110100 000 0010110 0 sssssss 1 ddddddd`                                |
|   `vsqrt.t rs,rd`         `0xd0168000`    `110100 000 0010110 1 sssssss 0 ddddddd`                                |
|   `vsqrt.q rs,rd`         `0xd0168080`    `110100 000 0010110 1 sssssss 1 ddddddd`                                |
|   `vasin.s rs,rd`         `0xd0170000`    `110100 000 0010111 0 sssssss 0 ddddddd`                                |
|   `vasin.p rs,rd`         `0xd0170080`    `110100 000 0010111 0 sssssss 1 ddddddd`                                |
|   `vasin.t rs,rd`         `0xd0178000`    `110100 000 0010111 1 sssssss 0 ddddddd`                                |
|   `vasin.q rs,rd`         `0xd0178080`    `110100 000 0010111 1 sssssss 1 ddddddd`                                |
|   `vnrcp.s rs,rd`         `0xd0180000`    `110100 000 0011000 0 sssssss 0 ddddddd`                                |
|   `vnrcp.p rs,rd`         `0xd0180080`    `110100 000 0011000 0 sssssss 1 ddddddd`                                |
|   `vnrcp.t rs,rd`         `0xd0188000`    `110100 000 0011000 1 sssssss 0 ddddddd`                                |
|   `vnrcp.q rs,rd`         `0xd0188080`    `110100 000 0011000 1 sssssss 1 ddddddd`                                |
|   `vnsin.s rs,rd`         `0xd01a0000`    `110100 000 0011010 0 sssssss 0 ddddddd`                                |
|   `vnsin.p rs,rd`         `0xd01a0080`    `110100 000 0011010 0 sssssss 1 ddddddd`                                |
|   `vnsin.t rs,rd`         `0xd01a8000`    `110100 000 0011010 1 sssssss 0 ddddddd`                                |
|   `vnsin.q rs,rd`         `0xd01a8080`    `110100 000 0011010 1 sssssss 1 ddddddd`                                |
|   `vrexp2.s rs,rd`        `0xd01c0000`    `110100 000 0011100 0 sssssss 0 ddddddd`                                |
|   `vrexp2.p rs,rd`        `0xd01c0080`    `110100 000 0011100 0 sssssss 1 ddddddd`                                |
|   `vrexp2.t rs,rd`        `0xd01c8000`    `110100 000 0011100 1 sssssss 0 ddddddd`                                |
|   `vrexp2.q rs,rd`        `0xd01c8080`    `110100 000 0011100 1 sssssss 1 ddddddd`                                |
|   `vi2uc.q rd,rs`         `0xd03c8080`    `110100 000 0111100 1 sssssss 1 ddddddd`   int to unsigned char         |
|   `vi2s.p rd,rs`          `0xd03f0080`    `110100 000 0111111 0 sssssss 1 ddddddd`   int to short                 |
|   `vi2s.q rd,rs`          `0xd03f8080`    `110100 000 0111111 1 sssssss 1 ddddddd`   int to short                 |
|   `vsgn.s rd,rs`          `0xd04a0000`    `110100 000 1001010 0 sssssss 0 ddddddd`                                |
|   `vsgn.p rd,rs`          `0xd04a0080`    `110100 000 1001010 0 sssssss 1 ddddddd`                                |
|   `vsgn.t rd,rs`          `0xd04a8000`    `110100 000 1001010 1 sssssss 0 ddddddd`                                |
|   `vsgn.q rd,rs`          `0xd04a8080`    `110100 000 1001010 1 sssssss 1 ddddddd`                                |
|   `vcst.s rd, a`          `0xd0600000`    `110100 000 11aaaaa 0 0000000 0 ddddddd`                                |
|   `vcst.p rd, a`          `0xd0600080`    `110100 000 11aaaaa 0 0000000 1 ddddddd`                                |
|   `vcst.t rd, a`          `0xd0608000`    `110100 000 11aaaaa 1 0000000 0 ddddddd`                                |
|   `vcst.q rd, a`          `0xd0608080`    `110100 000 11aaaaa 1 0000000 1 ddddddd`                                |
|   `vf2in.s rd,rs,scale`   `0xd2000000`    `110100 100 SSSSSSS 0 sssssss 0 ddddddd`   float to int round to near   |
|   `vf2in.p rd,rs,scale`   `0xd2000080`    `110100 100 SSSSSSS 0 sssssss 1 ddddddd`                                |
|   `vf2in.t rd,rs,scale`   `0xd2008000`    `110100 100 SSSSSSS 1 sssssss 0 ddddddd`                                |
|   `vf2in.q rd,rs,scale`   `0xd2008080`    `110100 100 SSSSSSS 1 sssssss 1 ddddddd`                                |
|   `vi2f.s rd,rs,scale`    `0xd2800000`    `110100 101 SSSSSSS 0 sssssss 0 ddddddd`   int to float                 |
|   `vi2f.p rd,rs,scale`    `0xd2800080`    `110100 101 SSSSSSS 0 sssssss 1 ddddddd`                                |
|   `vi2f.t rd,rs,scale`    `0xd2808000`    `110100 101 SSSSSSS 1 sssssss 0 ddddddd`                                |
|   `vi2f.q rd,rs,scale`    `0xd2808080`    `110100 101 SSSSSSS 1 sssssss 1 ddddddd`                                |
|   `vmmul.p rd,rs,rt`      `0xf0000080`    `111100 000 ttttttt 0 sSsssss 1 ddddddd`   (\*1)                        |
|   `vmmul.t rd,rs,rt`      `0xf0008000`    `111100 000 ttttttt 1 sSsssss 0 ddddddd`   (\*1)                        |
|   `vmmul.q rd,rs,rt`      `0xf0008080`    `111100 000 ttttttt 1 sSsssss 1 ddddddd`   (\*1)                        |
|   `vhtfm2.p rd,rs,rt`     `0xf0800000`    `111100 001 ttttttt 0 sssssss 0 ddddddd`                                |
|   `vtfm2.p rd,rs,rt`      `0xf0800080`    `111100 001 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vhtfm3.t rd,rs,rt`     `0xf1000080`    `111100 010 ttttttt 0 sssssss 1 ddddddd`                                |
|   `vtfm3.t rd,rs,rt`      `0xf1008000`    `111100 010 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vhtfm4.q rd,rs,rt`     `0xf1808000`    `111100 011 ttttttt 1 sssssss 0 ddddddd`                                |
|   `vtfm4.q rd,rs,rt`      `0xf1808080`    `111100 011 ttttttt 1 sssssss 1 ddddddd`                                |
|   `vmidt.p rd`            `0xf3830080`    `111100 111 0000011 0 0000000 1 ddddddd`   SetMatrixIdentity.Pair       |
|   `vmidt.t rd`            `0xf3838000`    `111100 111 0000011 1 0000000 0 ddddddd`   SetMatrixIdentity.Triple     |
|   `vmidt.q rd`            `0xf3838080`    `111100 111 0000011 1 0000000 1 ddddddd`   SetMatrixIdentity.Quad       |
|   `vmzero.p rd`           `0xf3860080`    `111100 111 0000110 0 0000000 1 ddddddd`   SetMatrixZero.Pair           |
|   `vmzero.t rd`           `0xf3868000`    `111100 111 0000110 1 0000000 0 ddddddd`   SetMatrixZero.Triple         |
|   `vmzero.q rd`           `0xf3868080`    `111100 111 0000110 1 0000000 1 ddddddd`   SetMatrixZero.Quad           |
|   ----------------------- --------------- ------------------------------------------ ---------------------------- |
+-------------------------------------------------------------------------------------------------------------------+

\*1) bit 5 of rs is inverted\
VFPU load/store instructions seem to support only 16-byte-aligned accesses (similiar to Altivec and SSE).\

#### 4.9.1  lv

+--------------------------------------------------------------------------------------+
|   -------- ------------------------------------------------------------------------- |
|   **lv**   **LoadVector Quadword Relative to Address in General Purpose Register**   |
|            `fpu_vtr <- vector_at_address (offset + %gpr)`                            |
|   -------- ------------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------+
|   -------------------------------- ---                                               |
|    `lv.q %vfpu_rt, offset(%base)`                                                    |
|   -------------------------------- ---                                               |
+--------------------------------------------------------------------------------------+
|   ----------- ---------------------------------------------------                    |
|   `%fpu_rt`   VFPU Vector Target Register (column0-31/row32-63)                      |
|   `%base`     GPR, specifies Source Address Base                                     |
|   `offset`    signed Offset added to Source Address Base                             |
|   ----------- ---------------------------------------------------                    |
+--------------------------------------------------------------------------------------+

Final Address needs to be 64-byte aligned.

#### 4.9.2  sv

+---------------------------------------------------------------------------------------+
|   -------- -------------------------------------------------------------------------- |
|   **sv**   **StoreVector Quadword Relative to Address in General Purpose Register**   |
|            `vector_at_address (offset + %gpr) <- fpu_vtr`                             |
|   -------- -------------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------+
|   ----------------------------------------------- ---                                 |
|    `sv.q %vfpu_rt, offset(%base), cache_policy `                                      |
|   ----------------------------------------------- ---                                 |
+---------------------------------------------------------------------------------------+
|   ---------------- ---------------------------------------------------                |
|   `%fpu_rt`        VFPU Vector Target Register (column0-31/row32-63)                  |
|   `%base`          specifies Source Address Base                                      |
|   `offset`         signed Offset added to Source Address Base                         |
|   `cache_policy`   0 = write-through, 1 = write-back                                  |
|   ---------------- ---------------------------------------------------                |
+---------------------------------------------------------------------------------------+

Final Address needs to be 64-byte aligned.

#### 4.9.3  vzero

+----------------------------------------------------------------------------+
|   ----------- ---------------------------------------------                |
|   **vzero**   **SetVectorZero (Single/Pair/Triple/Quad)**                  |
|               `vfpu_regs[%vfpu_rt] <- 0.0f`                                |
|   ----------- ---------------------------------------------                |
+----------------------------------------------------------------------------+
|   -------------------- ---------------------------------                   |
|    `vzero.s %vfpu_rt`  Set 1 Vector Component to 0.0f                      |
|    `vzero.p %vfpu_rt`  Set 2 Vector Components to 0.0f                     |
|    `vzero.t %vfpu_rt`  Set 3 Vector Components to 0.0f                     |
|    `vzero.q %vfpu_rt`  Set 4 Vector Components to 0.0f                     |
|   -------------------- ---------------------------------                   |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rt`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.4  vone

+----------------------------------------------------------------------------+
|   ---------- --------------------------------------------                  |
|   **vone**   **SetVectorOne (Single/Pair/Triple/Quad)**                    |
|              `vfpu_regs[%vfpu_rt] <- 0.0f`                                 |
|   ---------- --------------------------------------------                  |
+----------------------------------------------------------------------------+
|   ------------------- ---------------------------------                    |
|    `vone.s %vfpu_rt`  Set 1 Vector Component to 1.0f                       |
|    `vone.p %vfpu_rt`  Set 2 Vector Components to 1.0f                      |
|    `vone.t %vfpu_rt`  Set 3 Vector Components to 1.0f                      |
|    `vone.q %vfpu_rt`  Set 4 Vector Components to 1.0f                      |
|   ------------------- ---------------------------------                    |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rt`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.5  vmzero

+----------------------------------------------------------------------------+
|   ------------ --------------------------------------                      |
|   **vmzero**   **SetMatrixZero (Pair/Triple/Quad)**                        |
|                `vfpu_mtx[%vfpu_rt] <- 0.0f`                                |
|   ------------ --------------------------------------                      |
+----------------------------------------------------------------------------+
|   --------------------- ---------------------------                        |
|    `vmzero.p %vfpu_rt`  Set 2x2 Submatrix to 0.0f                          |
|    `vmzero.t %vfpu_rt`  Set 3x3 Submatrix to 0.0f                          |
|    `vmzero.q %vfpu_rt`  Set 4x4 Matrix to 0.0f                             |
|   --------------------- ---------------------------                        |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rt`   VFPU Matrix Target Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.6  vmidt

+----------------------------------------------------------------------------+
|   ----------- ------------------------------------------                   |
|   **vmidt**   **SetMatrixIdentity (Pair/Triple/Quad)**                     |
|               `vfpu_mtx[%vfpu_rt] <- identity matrix`                      |
|   ----------- ------------------------------------------                   |
+----------------------------------------------------------------------------+
|   -------------------- -------------------------------                     |
|    `vmidt.p %vfpu_rt`  Set 2x2 Submatrix to Identity                       |
|    `vmidt.t %vfpu_rt`  Set 3x3 Submatrix to Identity                       |
|    `vmidt.q %vfpu_rt`  Set 4x4 Matrix to Identity                          |
|   -------------------- -------------------------------                     |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rt`   VFPU Matrix Target Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.7  vmmul

+-------------------------------------------------------------------------+
|   ----------- ---                                                       |
|   **vmmul**                                                             |
|                                                                         |
|   ----------- ---                                                       |
+-------------------------------------------------------------------------+
|   ---------------------------------------- ---------------------------- |
|    `vmmul.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  multiply 2 2x2 Submatrices   |
|    `vmmul.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  multiply 2 3x3 Submatrices   |
|    `vmmul.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  multiply 2 4x4 Matrices      |
|   ---------------------------------------- ---------------------------- |
+-------------------------------------------------------------------------+
|   --- ---                                                               |
|                                                                         |
|                                                                         |
|                                                                         |
|   --- ---                                                               |
+-------------------------------------------------------------------------+

#### 4.9.8  vrcp

+----------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------          |
|   **vrcp**   **Reciprocal (Single/Pair/Triple/Quad)**                      |
|              `vfpu_regs[%vfpu_rd] <- 1.0 / vfpu_regs[%vfpu_rs]`            |
|   ---------- ----------------------------------------------------          |
+----------------------------------------------------------------------------+
|   ----------------------------- --------------------------------------     |
|    `vrcp.s %vfpu_rd, %vfpu_rs`  calculate reciprocal (1/z) on single       |
|    `vrcp.p %vfpu_rd, %vfpu_rs`  calculate reciprocal (1/z) on pair         |
|    `vrcp.t %vfpu_rd, %vfpu_rs`  calculate reciprocal (1/z) on triple       |
|    `vrcp.q %vfpu_rd, %vfpu_rs`  calculate reciprocal (1/z) on quad         |
|   ----------------------------- --------------------------------------     |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.9  vexp2

+------------------------------------------------------------------------------------------------------+
|   ----------- -------------------------------------------------------------------------------------- |
|   **vexp2**   **Exp2 (Single/Pair/Triple/Quad) (calculate 2 raised to the specified real number)**   |
|               `vfpu_regs[%vfpu_rd] <- 2^(vfpu_regs[%vfpu_rs])`                                       |
|   ----------- -------------------------------------------------------------------------------------- |
+------------------------------------------------------------------------------------------------------+
|   ------------------------------ --------------------                                                |
|    `vexp2.s %vfpu_rd, %vfpu_rs`  calculate 2 \*\* y                                                  |
|    `vexp2.p %vfpu_rd, %vfpu_rs`  calculate 2 \*\* y                                                  |
|    `vexp2.t %vfpu_rd, %vfpu_rs`  calculate 2 \*\* y                                                  |
|    `vexp2.q %vfpu_rd, %vfpu_rs`  calculate 2 \*\* y                                                  |
|   ------------------------------ --------------------                                                |
+------------------------------------------------------------------------------------------------------+
|   ------------ -----------------------------------------------------------                           |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)                             |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                             |
|                                                                                                      |
|   ------------ -----------------------------------------------------------                           |
+------------------------------------------------------------------------------------------------------+

#### 4.9.10  vlog2

+--------------------------------------------------------------------------------------------------------------+
|   ----------- ---------------------------------------------------------------------------------------------- |
|   **vlog2**   **Log2 (Single/Pair/Triple/Quad) (calculate logarithm base 2 of the specified real number)**   |
|               `vfpu_regs[%vfpu_rd] <- log2(vfpu_regs[%vfpu_rs])`                                             |
|   ----------- ---------------------------------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------------------------------+
|   ------------------------------ ---                                                                         |
|    `vlog2.s %vfpu_rd, %vfpu_rs`                                                                              |
|    `vlog2.p %vfpu_rd, %vfpu_rs`                                                                              |
|    `vlog2.t %vfpu_rd, %vfpu_rs`                                                                              |
|    `vlog2.q %vfpu_rd, %vfpu_rs`                                                                              |
|   ------------------------------ ---                                                                         |
+--------------------------------------------------------------------------------------------------------------+
|   ------------ -----------------------------------------------------------                                   |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)                                     |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                                     |
|                                                                                                              |
|   ------------ -----------------------------------------------------------                                   |
+--------------------------------------------------------------------------------------------------------------+

#### 4.9.11  vsqrt

+----------------------------------------------------------------------------+
|   ----------- ----------------------------------------------------         |
|   **vsqrt**   **SquareRoot (Single/Pair/Triple/Quad)**                     |
|               `vfpu_regs[%vfpu_rd] <- sqrt(vfpu_regs[%vfpu_rs])`           |
|   ----------- ----------------------------------------------------         |
+----------------------------------------------------------------------------+
|   ------------------------------ -----------------------                   |
|    `vsqrt.s %vfpu_rd, %vfpu_rs`  calculate square root                     |
|    `vsqrt.p %vfpu_rd, %vfpu_rs`  calculate square root                     |
|    `vsqrt.t %vfpu_rd, %vfpu_rs`  calculate square root                     |
|    `vsqrt.q %vfpu_rd, %vfpu_rs`  calculate square root                     |
|   ------------------------------ -----------------------                   |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.12  vrsq

+-----------------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------------           |
|   **vrsq**   **ReciprocalSquareRoot (Single/Pair/Triple/Quad)**                   |
|              `vfpu_regs[%vfpu_rd] <- 1.0 / sqrt(vfpu_regs[%vfpu_rs])`             |
|   ---------- ----------------------------------------------------------           |
+-----------------------------------------------------------------------------------+
|   ----------------------------- ------------------------------------------------- |
|    `vrsq.s %vfpu_rd, %vfpu_rs`  calculate reciprocal sqrt (1/sqrt(x)) on single   |
|    `vrsq.p %vfpu_rd, %vfpu_rs`  calculate reciprocal sqrt (1/sqrt(x)) on pair     |
|    `vrsq.t %vfpu_rd, %vfpu_rs`  calculate reciprocal sqrt (1/sqrt(x)) on triple   |
|    `vrsq.q %vfpu_rd, %vfpu_rs`  calculate reciprocal sqrt (1/sqrt(x)) on quad     |
|   ----------------------------- ------------------------------------------------- |
+-----------------------------------------------------------------------------------+
|   ------------ -----------------------------------------------------------        |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)          |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|                                                                                   |
|   ------------ -----------------------------------------------------------        |
+-----------------------------------------------------------------------------------+

#### 4.9.13  vsin

+----------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------          |
|   **vsin**   **Sinus (Single/Pair/Triple/Quad)**                           |
|              `vfpu_regs[%vfpu_rd] <- sin(vfpu_regs[%vfpu_rs]) `            |
|   ---------- ----------------------------------------------------          |
+----------------------------------------------------------------------------+
|   ----------------------------- -------------------------                  |
|    `vsin.s %vfpu_rd, %vfpu_rs`  calculate sin on single                    |
|    `vsin.p %vfpu_rd, %vfpu_rs`  calculate sin on pair                      |
|    `vsin.t %vfpu_rd, %vfpu_rs`  calculate sin on triple                    |
|    `vsin.q %vfpu_rd, %vfpu_rs`  calculate sin on quad                      |
|   ----------------------------- -------------------------                  |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

note: trig functions on the vfpu expect input values like vsin(degrees/90) or vsin(2/PI \* radians)

#### 4.9.14  vcos

+----------------------------------------------------------------------------+
|   ---------- ---------------------------------------------------           |
|   **vcos**   **Cosine (Single/Pair/Triple/Quad)**                          |
|              `vfpu_regs[%vfpu_rd] <- cos(vfpu_regs[%vfpu_rs])`             |
|   ---------- ---------------------------------------------------           |
+----------------------------------------------------------------------------+
|   ----------------------------- -------------------------                  |
|    `vcos.s %vfpu_rd, %vfpu_rs`  calculate cos on single                    |
|    `vcos.p %vfpu_rd, %vfpu_rs`  calculate cos on pair                      |
|    `vcos.t %vfpu_rd, %vfpu_rs`  calculate cos on triple                    |
|    `vcos.q %vfpu_rd, %vfpu_rs`  calculate cos on quad                      |
|   ----------------------------- -------------------------                  |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

Note by John Kelley: trig functions on the vfpu expect input values like vsin(degrees/90) or vsin(2/PI \* radians)

#### 4.9.15  vasin

+----------------------------------------------------------------------------+
|   ----------- ------------------------------------------------------       |
|   **vasin**   **ArcSin (Single/Pair/Triple/Quad)**                         |
|               `vfpu_regs[%vfpu_rd] <- arcsin(vfpu_regs[%vfpu_rs])`         |
|   ----------- ------------------------------------------------------       |
+----------------------------------------------------------------------------+
|   ------------------------------ ------------------                        |
|    `vasin.s %vfpu_rd, %vfpu_rs`  calculate arcsin                          |
|    `vasin.p %vfpu_rd, %vfpu_rs`  calculate arcsin                          |
|    `vasin.t %vfpu_rd, %vfpu_rs`  calculate arcsin                          |
|    `vasin.q %vfpu_rd, %vfpu_rs`  calculate arcsin                          |
|   ------------------------------ ------------------                        |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.16  vnrcp

+----------------------------------------------------------------------------+
|   ----------- --------------------------------------------------           |
|   **vnrcp**   **NegativeReciprocal (Single/Pair/Triple/Quad)**             |
|               `vfpu_regs[%vfpu_rd] <- -1/vfpu_regs[%vfpu_rs]`              |
|   ----------- --------------------------------------------------           |
+----------------------------------------------------------------------------+
|   ------------------------------ -------------------------------           |
|    `vnrcp.s %vfpu_rd, %vfpu_rs`  calculate negative reciprocal             |
|    `vnrcp.p %vfpu_rd, %vfpu_rs`  calculate negative reciprocal             |
|    `vnrcp.t %vfpu_rd, %vfpu_rs`  calculate negative reciprocal             |
|    `vnrcp.q %vfpu_rd, %vfpu_rs`  calculate negative reciprocal             |
|   ------------------------------ -------------------------------           |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|   `%vfpu_rs`   VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|                                                                            |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.17  vnsin

+----------------------------------------------------------------------------+
|   ----------- ----------------------------------------------------         |
|   **vnsin**   **NegativeSin (Single/Pair/Triple/Quad)**                    |
|               `vfpu_regs[%vfpu_rd] <- -sin(vfpu_regs[%vfpu_rs])`           |
|   ----------- ----------------------------------------------------         |
+----------------------------------------------------------------------------+
|   ------------------------------ ------------------------                  |
|    `vnsin.s %vfpu_rd, %vfpu_rs`  calculate negative sin                    |
|    `vnsin.p %vfpu_rd, %vfpu_rs`  calculate negative sin                    |
|    `vnsin.t %vfpu_rd, %vfpu_rs`  calculate negative sin                    |
|    `vnsin.q %vfpu_rd, %vfpu_rs`  calculate negative sin                    |
|   ------------------------------ ------------------------                  |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.18  vrexp2

+----------------------------------------------------------------------------+
|   ------------ ------------------------------------------------------      |
|    **vrexp2**  **ReciprocalExp2 (Single/Pair/Triple/Quad)**                |
|                `vfpu_regs[%vfpu_rd] <- 1/exp2(vfpu_regs[%vfpu_rs])`        |
|   ------------ ------------------------------------------------------      |
+----------------------------------------------------------------------------+
|   ------------------------------- --------------------                     |
|    `vrexp2.s %vfpu_rd, %vfpu_rs`  calculate 1/(2\^y)                       |
|    `vrexp2.p %vfpu_rd, %vfpu_rs`  calculate 1/(2\^y)                       |
|    `vrexp2.t %vfpu_rd, %vfpu_rs`  calculate 1/(2\^y)                       |
|    `vrexp2.q %vfpu_rd, %vfpu_rs`  calculate 1/(2\^y)                       |
|   ------------------------------- --------------------                     |
+----------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Target Register (\[s - p - t - q\]reg 0..127)   |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)   |
|   ------------ ----------------------------------------------------------- |
+----------------------------------------------------------------------------+

#### 4.9.19  vi2uc

+-----------------------------------------------------------------------+
|   ----------- --------------------------                              |
|   **vi2uc**   **int to unsigned char**                                |
|                                                                       |
|   ----------- --------------------------                              |
+-----------------------------------------------------------------------+
|   ------------------------------ ---                                  |
|    `vi2uc.q %vfpu_rd, %vfpu_rs`                                       |
|   ------------------------------ ---                                  |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

#### 4.9.20  vi2s

+-----------------------------------------------------------------------+
|   ---------- ------------------                                       |
|   **vi2s**   **int to short**                                         |
|                                                                       |
|   ---------- ------------------                                       |
+-----------------------------------------------------------------------+
|   ----------------------------- ---                                   |
|    `vi2s.p %vfpu_rd, %vfpu_rs`                                        |
|    `vi2s.q %vfpu_rd, %vfpu_rs`                                        |
|   ----------------------------- ---                                   |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

#### 4.9.21  vcst

+---------------------------------------------------------------------------------+
|   ---------- ---------------------------------------------                      |
|    **vcst**  **StoreConstant (Single/Pair/Triple/Quad)**                        |
|              `vfpu_regs[%vfpu_rd] <- constants[%a]`                             |
|   ---------- ---------------------------------------------                      |
+---------------------------------------------------------------------------------+
|   ----------------------- ----------------------------                          |
|    `vcst.s %vfpu_rd, %a`  store constant into single                            |
|    `vcst.p %vfpu_rd, %a`  store constant into pair                              |
|    `vcst.t %vfpu_rd, %a`  store constant into triple                            |
|    `vcst.q %vfpu_rd, %a`  store constant into quad                              |
|   ----------------------- ----------------------------                          |
+---------------------------------------------------------------------------------+
|   ------------ ---------------------------------------------------------------- |
|   `%vfpu_rd`   VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)   |
|                                                                                 |
|   `%a`         VFPU Constant                                                    |
|   ------------ ---------------------------------------------------------------- |
+---------------------------------------------------------------------------------+

+:---------------------------------------------------------------------:+
|   -------- -------------- ------------------------------------------- |
|     **ID** **Constant**                                     **Value** |
|          0 n/a                                                      0 |
|          1 HUGE             340282346638528859811704183484516925440.0 |
|          2 SQRT(2)                                            1.41421 |
|          3 1/SQRT(2)                                          0.70711 |
|          4 2/SQRT(PI)                                         1.12838 |
|          5 2/PI                                               0.63662 |
|          6 1/PI                                               0.31831 |
|          7 PI/4                                               0.78540 |
|          8 PI/2                                               1.57080 |
|          9 PI                                                 3.14159 |
|         10 E                                                  2,71828 |
|         11 LOG2E                                              1.44270 |
|         12 LOG10E                                             0.43429 |
|         13 LN2                                                0.69315 |
|         14 LN10                                               2.30259 |
|         15 2\*PI                                              6.28319 |
|         16 PI/6                                               0.52360 |
|         17 LOG10TWO                                           0.30103 |
|         18 LOG2TEN                                            3.32193 |
|         19 SQRT(3)/2                                          0.86603 |
|      20-31 n/a                                                      0 |
|   -------- -------------- ------------------------------------------- |
+-----------------------------------------------------------------------+

#### 4.9.22  vf2in

+-----------------------------------------------------------------------+
|   ----------- --------------------------------                        |
|   **vf2in**   **float to int round to near**                          |
|                                                                       |
|   ----------- --------------------------------                        |
+-----------------------------------------------------------------------+
|   ------------------------------------- ---                           |
|    `vf2in.s %vfpu_rd, %vfpu_rs, scale`                                |
|    `vf2in.p %vfpu_rd, %vfpu_rs, scale`                                |
|    `vf2in.t %vfpu_rd, %vfpu_rs, scale`                                |
|    `vf2in.q %vfpu_rd, %vfpu_rs, scale`                                |
|   ------------------------------------- ---                           |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

#### 4.9.23  vi2f

+-----------------------------------------------------------------------+
|   ---------- ------------------                                       |
|   **vi2f**   **int to float**                                         |
|                                                                       |
|   ---------- ------------------                                       |
+-----------------------------------------------------------------------+
|   ------------------------------------ ---                            |
|    `vi2f.s %vfpu_rd, %vfpu_rs, scale`                                 |
|    `vi2f.p %vfpu_rd, %vfpu_rs, scale`                                 |
|    `vi2f.t %vfpu_rd, %vfpu_rs, scale`                                 |
|    `vi2f.q %vfpu_rd, %vfpu_rs, scale`                                 |
|   ------------------------------------ ---                            |
+-----------------------------------------------------------------------+
|   --- ---                                                             |
|                                                                       |
|                                                                       |
|                                                                       |
|   --- ---                                                             |
+-----------------------------------------------------------------------+

#### 4.9.24  vadd

+-----------------------------------------------------------------------------------+
|   ---------- -------------------------------------------------------------------- |
|   **vadd**   **VectorAdd (Single/Pair/Triple/Quad)**                              |
|              `vfpu_regs[%vfpu_rd] <- vfpu_regs[%vfpu_rs] + vfpu_regs[%vfpu_rt]`   |
|   ---------- -------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------+
|   --------------------------------------- ------------                            |
|    `vadd.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  Add Single                              |
|    `vadd.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Add Pair                                |
|    `vadd.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Add Triple                              |
|    `vadd.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Add Quad                                |
|   --------------------------------------- ------------                            |
+-----------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------   |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)     |
|   ------------ ----------------------------------------------------------------   |
+-----------------------------------------------------------------------------------+

#### 4.9.25  vsub

+-----------------------------------------------------------------------------------+
|   ---------- -------------------------------------------------------------------- |
|    **vsub**  **VectorSub (Single/Pair/Triple/Quad)**                              |
|              `vfpu_regs[%vfpu_rd] <- vfpu_regs[%vfpu_rs] - vfpu_regs[%vfpu_rt]`   |
|   ---------- -------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------+
|   --------------------------------------- ------------                            |
|    `vsub.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  Sub Single                              |
|    `vsub.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Sub Pair                                |
|    `vsub.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Sub Triple                              |
|    `vsub.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Sub Quad                                |
|   --------------------------------------- ------------                            |
+-----------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------   |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)     |
|   ------------ ----------------------------------------------------------------   |
+-----------------------------------------------------------------------------------+

#### 4.9.26  vdiv

+-----------------------------------------------------------------------------------+
|   ---------- -------------------------------------------------------------------- |
|   **vdiv**   **VectorDiv (Single/Pair/Triple/Quad)**                              |
|              `vfpu_regs[%vfpu_rd] <- vfpu_regs[%vfpu_rs] / vfpu_regs[%vfpu_rt]`   |
|   ---------- -------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------+
|   --------------------------------------- ------------                            |
|    `vdiv.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  div Single                              |
|    `vdiv.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  div Pair                                |
|    `vdiv.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  div Triple                              |
|    `vdiv.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  div Quad                                |
|   --------------------------------------- ------------                            |
+-----------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------   |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)     |
|   ------------ ----------------------------------------------------------------   |
+-----------------------------------------------------------------------------------+

#### 4.9.27  vmul

+-----------------------------------------------------------------------------------+
|   ---------- -------------------------------------------------------------------- |
|    **vmul**  **VectorMul (Single/Pair/Triple/Quad)**                              |
|              `vfpu_regs[%vfpu_rd] <- vfpu_regs[%vfpu_rs] * vfpu_regs[%vfpu_rt]`   |
|   ---------- -------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------+
|   --------------------------------------- ------------                            |
|    `vmul.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  mul Single                              |
|    `vmul.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  mul Pair                                |
|    `vmul.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  mul Triple                              |
|    `vmul.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  mul Quad                                |
|   --------------------------------------- ------------                            |
+-----------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------   |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)          |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)     |
|   ------------ ----------------------------------------------------------------   |
+-----------------------------------------------------------------------------------+

#### 4.9.28  vdot

+----------------------------------------------------------------------------------------------+
|   ---------- ------------------------------------------------------------------------------- |
|    **vdot**  **VectorDotProduct (Pair/Triple/Quad)**                                         |
|              `vfpu_regs[%vfpu_rd] <- dotproduct(vfpu_regs[%vfpu_rs], vfpu_regs[%vfpu_rt])`   |
|   ---------- ------------------------------------------------------------------------------- |
+----------------------------------------------------------------------------------------------+
|   --------------------------------------- --------------------                               |
|    `vdot.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Pair                                   |
|    `vdot.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Triple                                 |
|    `vdot.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Quad                                   |
|   --------------------------------------- --------------------                               |
+----------------------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------              |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                     |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                     |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)                |
|   ------------ ----------------------------------------------------------------              |
+----------------------------------------------------------------------------------------------+

#### 4.9.29  vhdp

+--------------------------------------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------------------------------------------- |
|   **vhdp**   **VectorHomogenousDotProduct (Pair/Triple/Quad)**                                         |
|              `vfpu_regs[%vfpu_rd] <- homogenousdotproduct(vfpu_regs[%vfpu_rs], vfpu_regs[%vfpu_rt])`   |
|   ---------- ----------------------------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------------------------+
|   --------------------------------------- --------------------                                         |
|    `vhdp.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Pair                                             |
|    `vhdp.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Triple                                           |
|    `vhdp.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Dot Product Quad                                             |
|   --------------------------------------- --------------------                                         |
+--------------------------------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------                        |
|    `%vfpu_rt`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                               |
|    `%vfpu_rs`  VFPU Vector Source Register (\[s - p - t - q\]reg 0..127)                               |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)                          |
|   ------------ ----------------------------------------------------------------                        |
+--------------------------------------------------------------------------------------------------------+

#### 4.9.30  vidt

+---------------------------------------------------------------------------------+
|   ---------- -------------------------------------------                        |
|    **vidt**  **VectorLoadIdentity (Pair/Triple/Quad)**                          |
|              `vfpu_regs[%vfpu_rd] <- identity vector`                           |
|   ---------- -------------------------------------------                        |
+---------------------------------------------------------------------------------+
|   ------------------- ----------------------------                              |
|    `vidt.p %vfpu_rd`  Set 2x1 Vector to Identity                                |
|    `vidt.t %vfpu_rd`  Set 3x1 Vector to Identity                                |
|    `vidt.q %vfpu_rd`  Set 4x1 Vector to Identity                                |
|   ------------------- ----------------------------                              |
+---------------------------------------------------------------------------------+
|   ------------ ---------------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)   |
|   ------------ ---------------------------------------------------------------- |
+---------------------------------------------------------------------------------+

#### 4.9.31  vabs

+------------------------------------------------------------------------------+
|   ---------- ---------------------------------------------------             |
|    **vabs**  **AbsoluteValue (Single/Pair/Triple/Quad)**                     |
|              `vfpu_regs[%vfpu_rd] <- abs(vfpu_regs[%vfpu_rs])`               |
|   ---------- ---------------------------------------------------             |
+------------------------------------------------------------------------------+
|   ----------------------------- -----------------------                      |
|    `vabs.s %vfpu_rd, %vfpu_rs`  Absolute Value Single                        |
|    `vabs.p %vfpu_rd, %vfpu_rs`  Absolute Value Pair                          |
|    `vabs.t %vfpu_rd, %vfpu_rs`  Absolute Value Triple                        |
|    `vabs.q %vfpu_rd, %vfpu_rs`  Absolute Value Quad                          |
|   ----------------------------- -----------------------                      |
+------------------------------------------------------------------------------+
|   ------------ ------------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Destination Register (m\[p - t - q\]reg 0..127)   |
|    `%vfpu_rs`  VFPU Vector Source Register (m\[p - t - q\]reg 0..127)        |
|   ------------ ------------------------------------------------------------- |
+------------------------------------------------------------------------------+

#### 4.9.32  vneg

+------------------------------------------------------------------------------+
|   ---------- -----------------------------------------------                 |
|    **vneg**  **Negate (Single/Pair/Triple/Quad)**                            |
|              `vfpu_regs[%vfpu_rd] <- -vfpu_regs[%vfpu_rs]`                   |
|   ---------- -----------------------------------------------                 |
+------------------------------------------------------------------------------+
|   ----------------------------- ---------------                              |
|    `vneg.s %vfpu_rd, %vfpu_rs`  Negate Single                                |
|    `vneg.p %vfpu_rd, %vfpu_rs`  Negate Pair                                  |
|    `vneg.t %vfpu_rd, %vfpu_rs`  Negate Triple                                |
|    `vneg.q %vfpu_rd, %vfpu_rs`  Negate Quad                                  |
|   ----------------------------- ---------------                              |
+------------------------------------------------------------------------------+
|   ------------ ------------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Destination Register (m\[p - t - q\]reg 0..127)   |
|    `%vfpu_rs`  VFPU Vector Source Register (m\[p - t - q\]reg 0..127)        |
|   ------------ ------------------------------------------------------------- |
+------------------------------------------------------------------------------+

#### 4.9.33  vsgn

+------------------------------------------------------------------------------+
|   ---------- -----------------------------------------------------           |
|    **vsgn**  **Sign.(Single/Pair/Triple/Quad )**                             |
|              `vfpu_regs[%vfpu_rd] <- sign(vfpu_regs[%vfpu_rs]) `             |
|   ---------- -----------------------------------------------------           |
+------------------------------------------------------------------------------+
|   ----------------------------- -----------------                            |
|    `vsgn.s %vfpu_rd, %vfpu_rs`  Get Sign Single                              |
|    `vsgn.p %vfpu_rd, %vfpu_rs`  Get Sign Pair                                |
|    `vsgn.t %vfpu_rd, %vfpu_rs`  Get Sign Triple                              |
|    `vsgn.q %vfpu_rd, %vfpu_rs`  Get Sign Quad                                |
|   ----------------------------- -----------------                            |
+------------------------------------------------------------------------------+
|   ------------ ------------------------------------------------------------- |
|    `%vfpu_rd`  VFPU Vector Destination Register (m\[p - t - q\]reg 0..127)   |
|    `%vfpu_rs`  VFPU Vector Source Register (m\[p - t - q\]reg 0..127)        |
|   ------------ ------------------------------------------------------------- |
+------------------------------------------------------------------------------+

Sets rd values to 1 or -1, depending on sign of input values

#### 4.9.34  vmin

+--------------------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------------------------- |
|    **vmin**  **VectorMin (Single/Pair/Triple/Quad)**                                 |
|              `vfpu_regs[%vfpu_rd] <- min(vfpu_regs[%vfpu_rs], vfpu_reg[%vfpu_rt])`   |
|   ---------- ----------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------+
|   --------------------------------------- --------------------------                 |
|    `vmin.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Minimum Value Single                   |
|    `vmin.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Minimum Value Pair                     |
|    `vmin.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Minimum Value Triple                   |
|    `vmin.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Minimum Value Quad                     |
|   --------------------------------------- --------------------------                 |
+--------------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------      |
|    `%vfpu_rt`  VFPU Vector Source Register (sreg 0..127)                             |
|    `%vfpu_rs`  VFPU Vector Source Register (\[p - t - q\]reg 0..127)                 |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)        |
|   ------------ ----------------------------------------------------------------      |
+--------------------------------------------------------------------------------------+

#### 4.9.35  vmax

+--------------------------------------------------------------------------------------+
|   ---------- ----------------------------------------------------------------------- |
|    **vmax**  **VectorMax (Single/Pair/Triple/Quad)**                                 |
|              `vfpu_regs[%vfpu_rd] <- max(vfpu_regs[%vfpu_rs], vfpu_reg[%vfpu_rt])`   |
|   ---------- ----------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------+
|   --------------------------------------- --------------------------                 |
|    `vmax.s %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Maximum Value Single                   |
|    `vmax.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Maximum Value Pair                     |
|    `vmax.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Maximum Value Triple                   |
|    `vmax.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Get Maximum Value Quad                     |
|   --------------------------------------- --------------------------                 |
+--------------------------------------------------------------------------------------+
|   ------------ ----------------------------------------------------------------      |
|    `%vfpu_rt`  VFPU Vector Source Register (sreg 0..127)                             |
|    `%vfpu_rs`  VFPU Vector Source Register (\[p - t - q\]reg 0..127)                 |
|    `%vfpu_rd`  VFPU Vector Destination Register (\[s - p - t - q\]reg 0..127)        |
|   ------------ ----------------------------------------------------------------      |
+--------------------------------------------------------------------------------------+

#### 4.9.36  vtfm

+-------------------------------------------------------------------------------------------------+
|   ---------- ---------------------------------------------------------------------------------- |
|    **vtfm**  **VectorTransform (Pair/Triple/Quad)**                                             |
|              `vfpu_regs[%vfpu_rd] <- transform(vfpu_matrix[%vfpu_rs], vfpu_vector[%vfpu_rt])`   |
|   ---------- ---------------------------------------------------------------------------------- |
+-------------------------------------------------------------------------------------------------+
|   ---------------------------------------- ------------------------------------------           |
|    `vtfm2.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Transform pair vector by pair matrix                 |
|    `vtfm3.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Transform triple vector by triple matrix             |
|    `vtfm4.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Transform quad vector by quad matrix                 |
|   ---------------------------------------- ------------------------------------------           |
+-------------------------------------------------------------------------------------------------+
|   ------------ ------------------------------------------------                                 |
|    `%vfpu_rt`  VFPU Vector Source Register (qreg 0..127)                                        |
|    `%vfpu_rs`  VFPU Matrix Source Register (qmatrix 0..127)                                     |
|    `%vfpu_rd`  VFPU Vector Destination Register (qreg 0..127)                                   |
|   ------------ ------------------------------------------------                                 |
+-------------------------------------------------------------------------------------------------+

#### 4.9.37  vhtfm

+-------------------------------------------------------------------------------------------------------------+
|   ----------- --------------------------------------------------------------------------------------------- |
|    **vhtfm**  **VectorHomogeneousTransform (Pair/Triple/Quad)**                                             |
|               `vfpu_regs[%vfpu_rd] <- homeogenoustransform(vfpu_matrix[%vfpu_rs], vfpu_vector[%vfpu_rt])`   |
|   ----------- --------------------------------------------------------------------------------------------- |
+-------------------------------------------------------------------------------------------------------------+
|   ----------------------------------------- ----------------------------------------------------            |
|    `vhtfm2.p %vfpu_rd, %vfpu_rs, %vfpu_rt`  Homogeneous transform quad vector by pair matrix                |
|    `vhtfm3.t %vfpu_rd, %vfpu_rs, %vfpu_rt`  Homogeneous transform quad vector by triple matrix              |
|    `vhtfm4.q %vfpu_rd, %vfpu_rs, %vfpu_rt`  Homogeneous transform quad vector by quad matrix                |
|   ----------------------------------------- ----------------------------------------------------            |
+-------------------------------------------------------------------------------------------------------------+
|   ------------ ------------------------------------------------                                             |
|    `%vfpu_rt`  VFPU Vector Source Register (qreg 0..127)                                                    |
|    `%vfpu_rs`  VFPU Matrix Source Register (qmatrix 0..127)                                                 |
|    `%vfpu_rd`  VFPU Vector Destination Register (qreg 0..127)                                               |
|   ------------ ------------------------------------------------                                             |
+-------------------------------------------------------------------------------------------------------------+
