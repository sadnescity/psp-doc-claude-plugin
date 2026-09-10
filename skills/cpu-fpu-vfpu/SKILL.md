---
name: cpu-fpu-vfpu
description: "The PSP floating point units: COP1 (FPU) status and control registers, and COP2 (VFPU) registers and matrices. Use when a routine does floating point or vector work."
---

Two coprocessors. COP1 is the ordinary MIPS floating point unit and gets thin
treatment: a bare list of FPR0-31 against the firmware modules that use each,
with the column headers lost in conversion, and a control register table in
which only FIR, FCCR, FEXR, FENR and FCSR are named. COP2 is the substance —
how 128 single precision registers are addressed as singles, pairs, triples,
quads and 2x2, 3x3 or 4x4 matrices, normal or transposed, the S/C/R/M/E naming
that follows from it, and the extra registers above 127: the prefix stacks,
the condition register and the random number generator state.

Coming from the PSX, note that COP2 means something else here. On the R3000A
it is the GTE, fixed point geometry; on the Allegrex it is a floating point
vector unit with an instruction set of its own, so a cop2 opcode in a PSP
disassembly has nothing to do with what a PSX hack did with the GTE. The PSX
has no COP1 at all.

For patching BOOT.BIN this is mostly recognition work. Text and menu hacks
rarely need the VFPU, but if the routine being hooked uses it, the prefix
stacks and the condition register are live state a hook must not disturb, and
the naming section is what makes S130 or M100 readable. The VFPU instructions
themselves are in cpu-instructions.

---

## 4  CPU Overview

### 4.4  COP1 (FPU)

32 32bit General Purpose Floatingpoint Registers (FPR0-FPR31)

#### 4.4.1  Status Registers (mfc/mtc)

+:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   ---- --- --- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    0           vshmain,video_plugin,update_plugin,sysreg,semawm,savedata_plugin,photo_plugin, paf,pafmini,osk_plugin,opening_plugin,netplay_client_plugin,music_plugin,msvideo_plugin,lcdc,impose_plugin,auth_plugin,common_gui,dialogmain,                                               |
|    1           vshmain,video_plugin,update_plugin,sysreg,sysclib,savedata_utility,savedata_plugin,power,photo_plugin, paf,pafmini,osk_plugin,opening_plugin,netplay_server_utility,netconf_plugin,music_plugin,msvideo_plugin,lcdc,impose_plugin,dialogmain,                              |
|    2           video_plugin,sysreg,photo_plugin, paf,pafmini,osk_plugin,music_plugin,msvideo_plugin,lcdc,                                                                                                                                                                                 |
|    3           video_plugin,sysreg,photo_plugin, paf,pafmini,music_plugin,                                                                                                                                                                                                                |
|    4           vshmain,video_plugin,paf,pafmini,dialogmain,                                                                                                                                                                                                                               |
|    5           video_plugin,sysreg,photo_plugin, paf,pafmini,                                                                                                                                                                                                                             |
|    6           paf,pafmini,                                                                                                                                                                                                                                                               |
|    7                                                                                                                                                                                                                                                                                      |
|    8           video_plugin,paf,pafmini,                                                                                                                                                                                                                                                  |
|    9           paf,pafmini,                                                                                                                                                                                                                                                               |
|    10                                                                                                                                                                                                                                                                                     |
|    11                                                                                                                                                                                                                                                                                     |
|    12          vshmain,video_plugin,update_plugin,sysconf_plugin,sysclib,savedata_utility,savedata_plugin,savedata_auto_dialog,photo_plugin, paf,pafmini,opening_plugin,netplay_client_plugin,netconf_plugin,music_plugin,msvideo_plugin,auth_plugin,common_gui,dialogmain,game_plugin,   |
|    13          vshmain,update_plugin,sysconf_plugin,savedata_utility,savedata_plugin,photo_plugin, paf,pafmini,osk_plugin,netplay_client_plugin,netconf_plugin,music_plugin,msvideo_plugin,game_plugin,common_gui,                                                                        |
|    14          vshmain,video_plugin,sysconf_plugin,savedata_utility,savedata_plugin,photo_plugin, paf,pafmini,music_plugin,msvideo_plugin,game_plugin,                                                                                                                                    |
|    15          syscon                                                                                                                                                                                                                                                                     |
|    16          paf,pafmini,                                                                                                                                                                                                                                                               |
|    17                                                                                                                                                                                                                                                                                     |
|    18                                                                                                                                                                                                                                                                                     |
|    19                                                                                                                                                                                                                                                                                     |
|    20          vshmain,video_plugin,sysconf_plugin,savedata_plugin,photo_plugin, paf,pafmini,osk_plugin,music_plugin,msvideo_plugin,impose_plugin,game_plugin,common_gui,dialogmain,                                                                                                      |
|    21          video_plugin,photo_plugin, paf,pafmini,osk_plugin,music_plugin,msvideo_plugin,game_plugin,common_gui,                                                                                                                                                                      |
|    22          sysconf_plugin,photo_plugin, paf,pafmini,music_plugin,msvideo_plugin,game_plugin,common_gui,                                                                                                                                                                               |
|    23          photo_plugin, paf,pafmini,                                                                                                                                                                                                                                                 |
|    24          paf,pafmini,                                                                                                                                                                                                                                                               |
|    25          paf,pafmini,                                                                                                                                                                                                                                                               |
|    26                                                                                                                                                                                                                                                                                     |
|    27                                                                                                                                                                                                                                                                                     |
|    28                                                                                                                                                                                                                                                                                     |
|    29                                                                                                                                                                                                                                                                                     |
|    30                                                                                                                                                                                                                                                                                     |
|    31                                                                                                                                                                                                                                                                                     |
|   ---- --- --- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

#### 4.4.2  Control Registers (cfc/ctc)

+:--------------------------------------------------------------------------------------------------:+
|   ---- --------- -------------------------------------------- ------------------------------------ |
|    0   `FIR`     Floating Point Implementation Register       sysmem                               |
|    1   `FCR1`                                                                                      |
|    2   `FCR2`                                                                                      |
|    3   `FCR3`                                                                                      |
|    4   `FCR4`                                                                                      |
|    5   `FCR5`                                                                                      |
|    6   `FCR6`                                                 interrupt handler                    |
|    7   `FCR7`                                                                                      |
|    8   `FCR8`                                                                                      |
|    9   `FCR9`                                                                                      |
|    10  `FCR10`                                                                                     |
|    11  `FCR11`                                                                                     |
|    12  `FCR12`                                                                                     |
|    13  `FCR13`                                                                                     |
|    14  `FCR14`                                                                                     |
|    15  `FCR15`                                                                                     |
|    16  `FCR16`                                                                                     |
|    17  `FCR17`                                                                                     |
|    18  `FCR18`                                                                                     |
|    19  `FCR19`                                                                                     |
|    20  `FCR20`                                                                                     |
|    21  `FCR21`                                                                                     |
|    22  `FCR22`                                                                                     |
|    23  `FCR23`                                                                                     |
|    24  `FCR24`                                                                                     |
|    25  `FCCR`    Floating Point Condition Codes Register                                           |
|    26  `FEXR`    Floating Point Exceptions Register                                                |
|    27  `FCR27`                                                                                     |
|    28  `FENR`    Floating Point Enables Register                                                   |
|    29  `FCR29`                                                                                     |
|    30  `FCR30`                                                                                     |
|    31  `FCSR`    Floating Point Control and Status Register   sysmem, interruptman, paf, pafmini   |
|   ---- --------- -------------------------------------------- ------------------------------------ |
+----------------------------------------------------------------------------------------------------+

### 4.5  COP2 (VFPU)

The psp\'s VFPU (Vector Floating Point Unit) is a coprocessor that can perform quite a few useful operations. The main purpose of it is vector and matrix processing, but it also supports trigonemtric functions and other mathematical operations, conversions, and mathematical constants.

#### 4.5.1  Registers

The VFPU has 128 single precision floating point (IEEE 754) registers (VFR0-VFR127), but they are arranged and accessed in various ways that make it very flexible. Many of the instructions for the VFPU support operations on:

- a single register
- a pair of registers
- three registers
- four regiters
- 2x2 matrix
- 3x3 matrix
- 4x4 matrix

And if that weren\'t enough, it can work with matrices in normal or transposed orders. The registers are grouped into 8 blocks of 16 registers each. This gives you enough room to work with 8 4x4 matrices, 8 3x3 matrices, 32 2x2 matrices. Or you can store up to 32 quad vectors, 40 triple vectors, 64 paired vectors, or 128 single values. The register names you use on the VFPU depends highly on the instruction being performed, and can quickly become a nightmare when trying to figure out how to access or modify certain registers. Register names are numbered with 3 digits: Matrix, Column and Row. The tables below show how single, pair, triple, quad and matrix registers are mapped within a single 16 register block []{#tth_tAb1}

**single Register**

 

  -------- -------- -------- --------
  `S000`   `S010`   `S020`   `S030`
  `S001`   `S011`   `S021`   `S031`
  `S002`   `S012`   `S022`   `S032`
  `S003`   `S013`   `S023`   `S033`
  -------- -------- -------- --------

 

**Quad Columns**

**Quad Rows**

  -------- -------- -------- --------
   `C000`   `C010`   `C020`   `C030`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

  -------- -------- -------- --------
   `R000`   `....`   `....`   `....`
   `R001`   `....`   `....`   `....`
   `R002`   `....`   `....`   `....`
   `R003`   `....`   `....`   `....`
  -------- -------- -------- --------

**4\*4 Matrix**

**4\*4 Transpose Matrix**

  -------- -------- -------- --------
   `M000`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

  -------- -------- -------- --------
   `E000`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

**Triple Columns (1)**

**Triple Columns (2)**

  -------- -------- -------- --------
   `C000`   `C010`   `C020`   `C030`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
   `    `   `    `   `    `   `    `
  -------- -------- -------- --------

  -------- -------- -------- --------
   `    `   `    `   `    `   `    `
   `C001`   `C011`   `C021`   `C031`
   `....`   `....`   `....`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

**Triple Rows (1)**

**Triple Rows (2)**

`R000`

`....`

`....`

`    `

`R001`

`....`

`....`

`    `

`R002`

`....`

`....`

`    `

`R003`

`....`

`....`

`    `

`    `

`R010`

`....`

`....`

`    `

`R011`

`....`

`....`

`    `

`R012`

`....`

`....`

`    `

`R013`

`....`

`....`

**3\*3 Matrix (1)**

**3\*3 Matrix (2)**

`M000`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`M001`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

**3\*3 Matrix (3)**

**3\*3 Matrix (4)**

`    `

`M10`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`M011`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

**3\*3 Transpose Matrix (1)**

**3\*3 Transpose Matrix (2)**

`E000`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`E001`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

**3\*3 Transpose Matrix (3)**

**3\*3 Transpose Matrix (4)**

`    `

`E10`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`    `

`E011`

`....`

`....`

`    `

`....`

`....`

`....`

`    `

`....`

`....`

`....`

**Pair Columns**

**Pair Rows**

  -------- -------- -------- --------
   `C000`   `C010`   `C020`   `C030`
   `....`   `....`   `....`   `....`
   `C002`   `C012`   `C022`   `C032`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

  -------- -------- -------- --------
   `R000`   `....`   `R020`   `....`
   `R001`   `....`   `R021`   `....`
   `R002`   `....`   `R022`   `....`
   `R003`   `....`   `R023`   `....`
  -------- -------- -------- --------

**2\*2 Matrix**

**2\*2 Transpose Matrix**

  -------- -------- -------- --------
   `M000`   `....`   `M020`   `....`
   `....`   `....`   `....`   `....`
   `M002`   `....`   `M022`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

  -------- -------- -------- --------
   `E000`   `....`   `E020`   `....`
   `....`   `....`   `....`   `....`
   `E002`   `....`   `E022`   `....`
   `....`   `....`   `....`   `....`
  -------- -------- -------- --------

Repeat all of the above with the other 7 blocks of registers. Just change the first digit of the register names to work on a different set

#### 4.5.2  Extra Registers

+:---------------------------------------------------------------------:+
|   ----- ------------- ---------------------------------------------   |
|    128  `VFPU_PFXS`   Source prefix stack                             |
|    129  `VFPU_PFXT`   Target prefix stack                             |
|    130  `VFPU_PFXD`   Destination prefix stack                        |
|    131  `VFPU_CC`     Condition information                           |
|    132  `VFPU_INF4`   VFPU internal information 4                     |
|    133  `VFPU_RSV5`   Not used (reserved)                             |
|    134  `VFPU_RSV6`   Not used (reserved)                             |
|    135  `VFPU_REV`    VFPU revision information                       |
|    136  `VFPU_RCX0`   Pseudorandom number generator information 0     |
|    137  `VFPU_RCX1`   Pseudorandom number generator information 1     |
|    138  `VFPU_RCX2`   Pseudorandom number generator information 2     |
|    139  `VFPU_RCX3`   Pseudorandom number generator information 3     |
|    140  `VFPU_RCX4`   Pseudorandom number generator information 4     |
|    141  `VFPU_RCX5`   Pseudorandom number generator information 5     |
|    142  `VFPU_RCX6`   Pseudorandom number generator information 6     |
|    143  `VFPU_RCX7`   Pseudorandom number generator information 7     |
|   ----- ------------- ---------------------------------------------   |
+-----------------------------------------------------------------------+
