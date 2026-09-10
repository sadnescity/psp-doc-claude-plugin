---
name: cpu
description: "PSP CPU registers: the 32 general purpose registers and their calling convention, the debug registers, and COP0 system control. Use when reading MIPS assembly for the PSP or when code touches a coprocessor 0 register."
---

Chapter 4 as far as the caches: the 32 general purpose registers under their
o32 names, the debug registers, and coprocessor 0 in two banks — the status
registers reached with mfc0/mtc0 and a second set of control registers reached
with cfc0/ctc0, every row tagged with the firmware modules that touch it.

The calling convention is the one a PSX hook already assumes — arguments in
a0-a3, result in v0, s0-s7 preserved across a call, return address in ra — and
it carries over to BOOT.BIN unchanged, since that is MIPS like a PSX
executable. What does not carry over is the address a patch lands at: BOOT.BIN
is a relocatable PRX, and file-formats is where the relocations are written
down.

Two COP0 entries have no R3000A counterpart: register 22 is CPUId, reading 0
on the main CPU and 1 on the Media Engine, and register 25 is EBase, which
puts the exception vector in a register instead of at a fixed address. The
whole cfc0/ctc0 bank is Allegrex, not standard MIPS. Note also what is
missing: no HI, LO or PC, and no instructions at all — for those read
cpu-instructions and allegrex-vs-r3000a. The 4.3.1 table lost its column
headers in conversion and reads as a flat run of cells: number, access, name,
meaning, modules.

---

## 4  CPU Overview

### 4.1  Registers

32 32bit General Purpose Integer Registers (R0-R31)

+:---------------------------------------------------------------------:+
|   ---- --------- ---------------------------------------------        |
|    0    `zero`   wired zero                                           |
|    1     `at`    assembler temp                                       |
|    2     `v0`    return value                                         |
|    3     `v1`                                                         |
|    4     `a0`    argument registers                                   |
|    5     `a1`                                                         |
|    6     `a2`                                                         |
|    7     `a3`                                                         |
|    8     `t0`    caller saved (o32 old style names: default)          |
|    9     `t1`                                                         |
|    10    `t2`                                                         |
|    11    `t3`                                                         |
|    12    `t4`    caller saved                                         |
|    13    `t5`                                                         |
|    14    `t6`                                                         |
|    15    `t7`                                                         |
|    16    `s0`    callee saved                                         |
|    17    `s1`                                                         |
|    18    `s2`                                                         |
|    19    `s3`                                                         |
|    20    `s4`                                                         |
|    21    `s5`                                                         |
|    22    `s6`                                                         |
|    23    `s7`                                                         |
|    24    `t8`    caller saved                                         |
|    25    `t9`                                                         |
|    26    `k0`    kernel temporary                                     |
|    27    `k1`                                                         |
|    28    `gp`    global pointer                                       |
|    29    `sp`    stack pointer                                        |
|    30   `fp/s8`  frame pointer                                        |
|    31    `ra`    return address                                       |
|   ---- --------- ---------------------------------------------        |
+-----------------------------------------------------------------------+

### 4.2  Debug Registers

+:---------------------------------------------------------------------:+
|   ---- ---------- ------------------------------------------------    |
|    0   `DRCNTL`   Debug Register Control register                     |
|    1   `DEPC`     Debug Exception PC register                         |
|    2   `DDATA0`   Debug Data Monitor 0 and Monitor Data register      |
|    3   `DDATA1`   Debug Data Monitor 1 register                       |
|    4   `IBC`      Instruction Breakpoint Control/Status register      |
|    5   `DBC`      Data Breakpoint Control/Status register             |
|    6   `DR6`      Reserved                                            |
|    7   `DR7`      Reserved                                            |
|    8   `IBA`      Instruction Breakpoint Address register             |
|    9   `IBAM`     Instruction Breakpoint Address Mask register        |
|    10  `DR10`     Reserved                                            |
|    11  `DR11`     Reserved                                            |
|    12  `DBA`      Data Breakpoint Address register                    |
|    13  `DBAM`     Data Breakpoint Address Mask register               |
|    14  `DBD`      Data Breakpoint Data register                       |
|    15  `DBDM`     Data Breakpoint Data Mask register                  |
|    16  `DR16`     Undefined                                           |
|    17  `DR17`     Undefined                                           |
|    18  `DR18`     Undefined                                           |
|    19  `DR19`     Undefined                                           |
|    20  `DR20`     Undefined                                           |
|    21  `DR21`     Undefined                                           |
|    22  `DR22`     Undefined                                           |
|    23  `DR23`     Undefined                                           |
|    24  `DR24`     Undefined                                           |
|    25  `DR25`     Undefined                                           |
|    26  `DR26`     Undefined                                           |
|    27  `DR27`     Undefined                                           |
|    28  `DR28`     Undefined                                           |
|    29  `DR29`     Undefined                                           |
|    30  `DR30`     Undefined                                           |
|    31  `DR31`     Undefined                                           |
|   ---- ---------- ------------------------------------------------    |
+-----------------------------------------------------------------------+

### 4.3  COP0 (System Control)

#### 4.3.1  Status Registers (mfc/mtc)

0

\-

 

not available (TLB)

 

1

\-

 

not available (TLB)

 

2

\-

 

not available (TLB)

 

3

\-

 

not available (TLB)

 

4

\-

 

not available (TLB context)

 

5

\-

 

not available (TLB)

 

6

\-

 

not available (TLB)

 

7

 

 

?

 

8

r

`BadVaddr`

virtual address of last error/exception

sysmem

9

r/w

`Count`

system counter

interruptman,sysmem

10

\-

 

not available (TLB)

 

11

r/w

`Compare`

counter comparison value

interruptman,sysmem

12

r/w

`Status`

system status

threadman, reboot, mewrapper,mebooterumdvideo,mebooter,loadcore,interruptman, loadexec, exceptionman,sysmem

13

r/w

`Cause`

exception cause

threadman, mewrapper,mebooterumdvideo,mebooter,interruptman,exceptionman,sysmem

14

r/w

`EPC`

exception program counter

loadcore,interruptman,exceptionman,sysmem

15

r

`PRId`

processor revision id

interruptman,sysmem

16

r/w

`Config`

configuration

utils,reboot,mewrapper,mebooterumdvideo,mebooter,loadcore,sysmem

17

 

 

?

 

18

 

 

? Watch LO

 

19

 

 

? Watch HI

 

20

\-

 

not available (TLB XContext)

 

21

r

`SCCode`

Ssyscall-code\< \<2

interruptman

22

r

`CPUId`

CPU ID (0=Main, 1=ME)

threadman, sysreg, reboot,loadcore,interruptman,exceptionman,sysmem

23

 

 

?

 

24

 

 

?

 

25

r/w

`EBase`

virtual address of exception vector

threadman, exceptionman,sysmem

26

 

 

? Cache ECC

 

27

 

 

? Cache Error

 

28

r/w

`TagLo`

cache instruction register

utils,reboot,mewrapper,mebooterumdvideo,mebooter,sysmem

29

r/w

`TagHi`

cache instruction register

utils,reboot,mewrapper,mebooterumdvideo,mebooter,sysmem

30

r/w

`ErrorEPC`

error exception program counter

exceptionman,sysmem

31

 

 

?

 

#### 4.3.2  Control Registers (cfc/ctc)

+:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   --------- ------------------- ------------ -------------- ----------------------------- ------------------------------------------------------------------------- ---------------------------------------------- |
|    **num**                                                                                **used by**                                                                                                              |
|       0     `COP0.EPC`                       context                                      EBase Handler, general exception handler, error handler,syscall handler   sysmem,interruptman, exceptionman              |
|       1     `COP0.EPC.err`      0xbfc00000   context                                      error (HW,SW,NMI) exception handler, error handler                        sysmem,exceptionman                            |
|       2     `COP0.Status `                   context                                      EBase Handler, general exception handler,syscall handler                  sysmem,interruptman, exceptionman              |
|       3     `COP0.Cause`                     context                                      EBase Handler, general exception handler,syscall handler                  sysmem,interruptman, exceptionman              |
|       4     `GPR.v0`                         context        saved v0                      general exception handler ,syscall handler                                sysmem,interruptman, exceptionman              |
|       5     `GPR.v1`                         context        saved v1                      general exception handler                                                 sysmem,interruptman, exceptionman              |
|       6     `GPR.v0.err`        0xbfc00000   context        saved v0                      error (HW,SW,NMI) exception handler, EBase Handler                        sysmem,exceptionman                            |
|       7     `GPR.v1.err`        0xbfc00000   context        saved v1                      error (HW,SW,NMI) exception handler, EBase Handler                        sysmem,exceptionman                            |
|       8     `EXC_TABLE`                      vector table   Exception vector table addr   general exception handler                                                 sysmem,exceptionman(init)                      |
|       9     `EXC_31_ERROR`      0xbfc00000   vector         Error handler addr            error (HW,SW,NMI) exception handler                                       sysmem,exceptionman(init)                      |
|      10     `EXC_27_DEBUG`      0xbfc01000   vector         Debug handler addr            debug exception handler                                                   sysmem,exceptionman                            |
|      11     `EXC_8_SYSCALL`                  vector         Syscall handler addr          EBase Handler, register/release exception handler functions               sysmem,exceptionman                            |
|      12     `SC_TABLE`                       vector table   (1st) syscalls table addr     syscall handler                                                           sysmem,interruptman(init),                     |
|      13     `SC_MAX`                         int            (1st) max syscall code        syscall handler                                                           sysmem,interruptman(init),                     |
|      14     `GPR.sp.Kernel`                  context        Stackpointer Kernel                                                                                     sysmem,threadman (init), interruptman,         |
|      15     `GPR.sp.User`                    context                                      syscall handler                                                           sysmem,threadman (init), interruptman,         |
|      16     `CurrentTCB`                     context                                      syscall handler                                                           sysmem,threadman (init), interruptman,         |
|      17     ?                                                                             ?                                                                         sysmem                                         |
|      18     `NMI_TABLE`         0xbfc00000   vector table   NMI vector table addr         error handler                                                             sysmem,exceptionman(init)                      |
|      19     `COP0.Status.err`   0xbfc00000   context                                      EBase Handler, error (HW,SW,NMI) exception handler                        sysmem,exceptionman                            |
|      20     `COP0.Cause.err`    0xbfc00000   context                                      error (HW,SW,NMI) exception handler                                       sysmem,exceptionman                            |
|      21     ?                                                                             ?                                                                         sysmem                                         |
|      22     ?                                                                             ?                                                                         sysmem                                         |
|      23     ? GPR.v0                         ? context                                    ?                                                                         sysmem                                         |
|      24     ? GPR.v1                         ? context                                    ?                                                                         sysmem                                         |
|      25     `PROFILER_BASE`                  vector         profiler hw base addr         general exception handler                                                 sysmem,threadman, interruptman, exceptionman   |
|      26     `GPR.v0.dbg`        0xbfc01000   context                                      debug exception handler                                                   sysmem,exceptionman                            |
|      27     `GPR.v1.dbg`        0xbfc01000   context                                      debug exception handler                                                   sysmem,exceptionman                            |
|      28     `DBGENV`            0xbfc01000   vector         debug handler env addr        debug exception handler                                                   sysmem,exceptionman                            |
|      29     ?                                                                             ?                                                                         sysmem                                         |
|      30     ?                                                                             ?                                                                         sysmem                                         |
|      31     ?                                                                             ?                                                                         sysmem                                         |
|   --------- ------------------- ------------ -------------- ----------------------------- ------------------------------------------------------------------------- ---------------------------------------------- |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
