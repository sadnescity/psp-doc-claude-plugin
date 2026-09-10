---
name: exceptions
description: "PSP exception processing: the cause register and its codes, the reset vector, the EBASE vector for interrupts and syscalls, and the error handler. Use when the machine traps and you need to read why."
---

The first half of YAPSPD's chapter 9: the table of exception cause codes, then
the reset vector at 0xBFC00000, the EBASE entry that interrupts and syscalls
arrive through, and the error handler, those three as annotated pseudocode
rather than register documentation.

The cause table is what a crash is read against: it separates a misaligned load
or store from a fetch of an address that is not memory and from a word that is
not an instruction, the three ordinary outcomes of a patch that writes a bad
pointer or lands mid-instruction. The reset path is also where the split
between the two cores shows: the vector reads a COP0 register to tell which CPU
it is on and sends the Media Engine elsewhere.

The cause list is generic MIPS, with the three TLB entries marked (n/a). The
pseudocode is retail firmware at fixed kernel addresses, not anything inside a
game's own executable. What the handler does once it has the cause is in
exception-handler.

---

## 9  Exception Processing

### 9.1  Exception Cause

The cause of the exception that was raised can be determined by the value of the cause register (causereg \> \> 2 to b\
specific) which has the following meaning:\

+:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   ---- ------- ------------------------------------------------ ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    0     INT   Interrupt                                        Hardware or Software Interrupt.                                                                                                                                                                                                           |
|    1     MOD   (n/a) TLB modification                           The memory address translation mapped to a TLB entry, but that entrys dirty-bit was set.                                                                                                                                                  |
|    2    TLBL   (n/a) TLB load/inst fetch                        TLB exception caused by a data load (i.e., a load word or similar instruction) or instruction fetch. The memory address translation did not match any valid TLB entry.                                                                    |
|    3    TLBS   (n/a) TLB store                                  TLB exception caused by a data store (i.e., a store word or similar instruction). The memory address translation did not match any valid TLB entry.                                                                                       |
|    4    ADEL   Address load/inst fetch                          The PC was not word-aligned, or the address the load instruction wanted to load from was not aligned to the width of the load instruction. (For example, load halfword instructions must be 2-byte aligned.)                              |
|    5    ADES   Address store                                    The address the store instruction wanted to store to was not aligned to the width of the store instruction. (For example, store halfword instructions must be 2-byte aligned.)                                                            |
|    6     IBE   Bus error (instr)                                The PC does not correspond to any real area of memory                                                                                                                                                                                     |
|    7     DBE   Bus error (data)                                 The target address of the load or store instruction does not correspond to any real area of memory.                                                                                                                                       |
|    8     SYS   Syscall                                          Some code was trying to call the operating system, using a SYSCALL instruction. This exception is the processors way of transferring control to the operating system.                                                                     |
|    9     BP    Breakpoint                                       Some process executed a BREAK instruction. This is the processors way of allowing the operating system to stop the process and do whatever is appropriate (alert the user using the debugger, for example).                               |
|    10    RI    Reserved instruction                             Some code executed something which wasn\'t a valid MIPS-1 instruction.                                                                                                                                                                    |
|    11    CPU   Coprocessor unusable                             Some code executed an instruction which tried to reference a coprocessor that isn\'t valid                                                                                                                                                |
|    12    OV    Arithmetic overflow                              Some code executed an instruction whose arithmetic answer was too big to fit in a register using twos-complement arithmetic. The processor issues this exception so that the operating system can stop or otherwise signal the process.   |
|    13    TR    Trap                                                                                                                                                                                                                                                                                       |
|    14   VCEI   Virtual Coherency Exception (instruction).                                                                                                                                                                                                                                                 |
|    15    FPE   FPU Exception                                                                                                                                                                                                                                                                              |
|    16          (reserved)                                                                                                                                                                                                                                                                                 |
|    17          (reserved)                                                                                                                                                                                                                                                                                 |
|    18          (reserved)                                                                                                                                                                                                                                                                                 |
|    19          (reserved)                                                                                                                                                                                                                                                                                 |
|    20          (reserved)                                                                                                                                                                                                                                                                                 |
|    21          (reserved)                                                                                                                                                                                                                                                                                 |
|    22          (reserved)                                                                                                                                                                                                                                                                                 |
|    23   WATCH  Reference to WatchHi/WatchLo address detected.                                                                                                                                                                                                                                             |
|    24   DEBUG  Debug Exception                                                                                                                                                                                                                                                                            |
|    25          (reserved)                                                                                                                                                                                                                                                                                 |
|    26          (reserved)                                                                                                                                                                                                                                                                                 |
|    27          (reserved)                                                                                                                                                                                                                                                                                 |
|    28          (reserved)                                                                                                                                                                                                                                                                                 |
|    29          (reserved)                                                                                                                                                                                                                                                                                 |
|    30          (reserved)                                                                                                                                                                                                                                                                                 |
|    31   VCED   Virtual Coherency Exception (data)               called \'Error\' on the PSP                                                                                                                                                                                                               |
|   ---- ------- ------------------------------------------------ ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

### 9.2  Reset Vector (HW,SW,NMI)

`bfc00000(/* v0 */) /*` **`(exceptionman, mebooter, mebooter_umdvideo, me_wrapper, power, sysreg)`** `*/`\
`{`\
`    COP0CTRL.6=v0 /*` **`save v0`** **`in cc0.6 (GPR.v0)`** `*/`\
`    if(COP0STAT.22!=0) /*` **`get c0.22 (CPU ID?) (if!=0 then ME)`** `*/`\
`    {`\
`        goto ME_Reset_Handler; /*` **`jump`** **`directly to ME Reset Handler`** `*/`\
`    `} `else {`\
`        call (COP0CTRL.9); /*` **`jump (indirect over vector in cc0.9) to Error Handler (EXC_31_ERROR handler)`** `*/`\
`    `}\

#### 9.2.1  ME Reset Handler

`ME_Reset_Handler() /* bfc00040` **`(mebooter, mebooter_umdvideo, me_wrapper)`** `*/`\
`{`\
`    *(0xbc100050)=0x00000007; /* bus clock enable AW?/AW?/ME */`\
`    *(0xbc100004)=0xffffffff; /* acknowledge/clear all interrupts */`\
`    *(0xbc100040)=0x00000001; /* set ram size (32mb) */` \
`    k0=COP0STAT.16; /*` **`get c0.16 (Config)`** `*/`\
`    COP0STAT.28=0; /*` **`set c0.28 (TagLo) = 0`** `*/`\
`    COP0STAT.29=0; /*` **`set c0.29 (TagHi) = 0`** `*/` \
`    /* invalidate caches */` \
`    k1=0x0800< <((k0> >6)&0x00000007);`\
`    do()`\
`    {`\
`        k1-=0x40;`\
`        asm('cache 0x01, 0($k1)'); /*` **`Index Invalidate (primary Data Cache)`** `*/`\
`    } while(k1!=0);`\
`    k1=0x0800< <((k0> >(3))&0x00000007);`\
`    do()`\
`    {`\
`        k1-=0x40;`\
`        asm('cache 0x11, 0($k1)'); /*` **`Hit Invalidate (primary Data Cache)`** `*/`\
`    } while(k1!=0);` \
`    COP0STAT.13=0; /*` **`set c0.13 (Cause) = 0`** `*/`\
`    COP0STAT.12=0x20000000; /*` **`set set c0.12 (Status) = 0x20000000`** `*/` \
`    *(0xbcc00010)=0x0001;`\
`    while(*(0xbcc00010)==1){/*` **`wait`** `*/};`\
`    *(0xbcc00070)=0x00000001;`\
`    *(0xbcc00030)=0x00000008;`\
`    *(0xbcc00040)=0x00000002;`\
`    sync();` \
`    /* k0=0x88380000 t0=0xbfc00000 sp=0x80200000 */`\
`    88380000(0,0x88300000,0x00080000); /* call handler at 0x88380000 */`\
`}` \
`88380000()`\
`{`\
`...`\
`}`\

### 9.3  EBASE Vector (IRQ,Syscall)

`EBase( /* v0, v1 */) /* 8801cd38 */`\
`{`\
`    COP0CTRL.6=v0; /* save v1 in cc0.6 (GPR.v0) */`\
`    COP0CTRL.7=v1; /* save v1 in cc0.7 (GPR.v1) */`\
`    COP0CTRL.0=COP0STAT.30; /*` **`save (EPC) in cc0.0 Exception Program Counter`** `*/`\
`    COP0CTRL.2=COP0STAT.12; /*` **`save v1 (Status) in cc0.2 Status register`** `*/`\
`    u32 cause=COP0STAT.13;`\
`    COP0CTRL.3=cause; /*` **`save (Cause) in cc0.3`** `*/;`\
`    cause&=0x7c;`\
`    if(cause!=(8< <2)) /* not syscall? */`\
`    {`\
`        exception_handler(cause); /* v0=offset in table */`\
`    } else {`\
`        call (COP0CTRL.11); /*` **`jump (indirect over vector in cc0.11) to Syscall Handler (EXC_8_Syscall handler)`** `*/`\
`    }`\

### 9.4  Error Handler

`EXC_31_ERROR_handler(/* v1 */) /*` **`(exceptionman:0x06c8)`** `*/`\
`{`\
`    COP0CTRL.7=v1; /*` **`save v1 in cc0.7 (GPR.v1) */`**\
`    COP0CTRL.20=COP0STAT.13; /*` **`save (Cause) in cc0.20`** `*/;`\
`    COP0CTRL.1=COP0STAT.30; /*` **`save (ErrorEPC) in cc0.1`** **`Error Exception Program Counter`** `*/`\
`    COP0CTRL.19=COP0STAT.12; /*` **`save v1 (Status) in cc0.19 Status register`** `*/`\
`    exception_handler(31< <2); /*` **`v0=0x007c default offset in table`** `*/`\
`}`\
