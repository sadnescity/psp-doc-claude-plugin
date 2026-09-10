---
name: exception-handler
description: "The exception handler itself, disassembled and annotated, and the debug exception vectors. Use when following what the firmware does after a trap."
---

The second half of chapter 9: the dispatch routine the vectors call, the
32-entry handler table, in which only interrupt, syscall and error are live and
every other slot points at a hang loop, the frame the error path saves
registers into, the interrupt path with its numbered interrupt list and the two
thread-manager routines it calls, the syscall path with its table header and
frame, and the debug exception vectors with their sub-handlers.

Worth opening when you need to know where a trapped register value ends up, or
what state the machine is left in after a fault; the table of hang entries is
why an unhandled exception looks like a freeze rather than a message.

All of it is annotated pseudocode from one firmware dump, at kernel addresses,
so it explains behaviour rather than offering addresses to patch. The same
interrupt list is in psptek-registers, there next to the flag and mask
registers that raise the interrupts; the two disagree on the names of the USB
entries, and PSPTEK's are the ones whose names match their descriptions.

---

## 9  Exception Processing

### 9.5  Exception Handler

- return from exception using eret

`exception_handler(u32 offset /* v0 */) /* 8801cd70` **`(exceptionman:0x0670)`** `*/`\
`{`\
`    if (COP0CTRL.25!=NULL) /*` **`Profiler HW Base`** `*/`\
`    {`\
`        `**`; profiler stuff`**\
`        *(PROFILER+0x0c)=offset; /*` **`save v0 to PROFILER+0x0c (stall total)`** `*/`\
`        v1=*(PROFILER+0x00);`\
`        v0=*(v1+0);`\
`        *(v1+0)=0;`\
`        sync();`\
`        if(*(PROFILER+0x08)==0)`\
`        `{ `            *(PROFILER+0x04)=v0;`\
`        `} `        `**`; count cpu ticks`**\
`        *(PROFILER+0x08)++; /* cpu ck */`\
`        offset=*(PROFILER+0x0c); /*` **`get v0 from PROFILER+0x0c (stall total)`** `*/`\
`    }`\
`    /*` **`jump to exception handler from table`** `*/`\
`    u8 *Exception_Vector_Table;`\
`    Exception_Vector_Table=COP0CTRL.8; /*` **`Exception Vector Table`** `*/`\
`    call((u32)Exception_Vector_Table[offset]);`\
`}` \
 \
`void *ExceptionVectorTable[32] /* 8801ea00` **`(exceptionman) Exception Vector Table (32 Entries)`** `*/`\
`{`\
`/*  0 */ 88020F74` **`(interruptman:0x2274)`** `/* IRQ (=default_irq_handler) */`\
`/*  1 */ 8801D130` **`(hang)while(1);`**\
`/*  2 */ 8801D130` **`(hang)while(1);`**\
`/*  3 */ 8801D130` **`(hang)while(1);`**\
`/*  4 */ 8801D130` **`(hang)while(1);`**\
`/*  5 */ 8801D130` **`(hang)while(1);`**\
`/*  6 */ 8801D130` **`(hang)while(1);`**\
`/*  7 */ 8801D130` **`(hang)while(1);`**\
`/*  8 */ 88021E74` **`(interruptman:0x3174)`** `/* syscall (=EXC_8_Syscall handler) */`\
`/*  9 */ 8801D130` **`(hang)while(1);`**\
`/* 10 */ 8801D130` **`(hang)while(1);`**\
`/* 11 */ 8801D130` **`(hang)while(1);`**\
`/* 12 */ 8801D130` **`(hang)while(1);`**\
`/* 13 */ 8801D130` **`(hang)while(1);`**\
`/* 14 */ 8801D130` **`(hang)while(1);`**\
`/* 15 */ 8801D130` **`(hang)while(1);`**\
`/* 16 */ 8801D130` **`(hang)while(1);`**\
`/* 17 */ 8801D130` **`(hang)while(1);`**\
`/* 18 */ 8801D130` **`(hang)while(1);`**\
`/* 19 */ 8801D130` **`(hang)while(1);`**\
`/* 20 */ 8801D130` **`(hang)while(1);`**\
`/* 21 */ 8801D130` **`(hang)while(1);`**\
`/* 22 */ 8801D130` **`(hang)while(1);`**\
`/* 23 */ 8801D130` **`(hang)while(1);`**\
`/* 24 */ 8801D130` **`(hang)while(1);`** `/* debug exception */`\
`/* 25 */ 8801D130` **`(hang)while(1);`**\
`/* 26 */ 8801D130` **`(hang)while(1);`**\
`/* 27 */ 8801D130` **`(hang)while(1);`**\
`/* 28 */ 8801D130` **`(hang)while(1);`**\
`/* 29 */ 8801D130` **`(hang)while(1);`**\
`/* 30 */ 8801D130` **`(hang)while(1);`**\
`/* 31 */ 8801D370` **`(exceptionman:0x0c70)`** `/* error, default (=default_error_handler) */` \
`}` \
note: the PSP Kernel provides a function called `sceKernelRegisterPriorityExceptionHandler` to register a handler in the above table.

#### 9.5.1  error

`typedef struct`\
`{`\
`    /* 0x00 */ unsigned long unk;`\
`    /* 0x04 */ unsigned long at;`\
`    /* 0x08 */ unsigned long a0;`\
`    /* 0x0c */ unsigned long a1;`\
`    /* 0x10 */ unsigned long a2;`\
`    /* 0x14 */ unsigned long a3;`\
`    /* 0x18 */ unsigned long t0;`\
`    /* 0x1c */ unsigned long t1;`\
`    /* 0x20 */ unsigned long t2;`\
`    /* 0x24 */ unsigned long t3;`\
`    /* 0x28 */ unsigned long t4;`\
`    /* 0x2c */ unsigned long t5;`\
`    /* 0x30 */ unsigned long t6;`\
`    /* 0x34 */ unsigned long t7;`\
`    /* 0x38 */ unsigned long s0;`\
`    /* 0x3c */ unsigned long s1;`\
`    /* 0x40 */ unsigned long s2;`\
`    /* 0x44 */ unsigned long s3;`\
`    /* 0x48 */ unsigned long s4;`\
`    /* 0x4c */ unsigned long s5;`\
`    /* 0x50 */ unsigned long s6;`\
`    /* 0x54 */ unsigned long s7;`\
`    /* 0x58 */ unsigned long t8;`\
`    /* 0x5c */ unsigned long t9;`\
`    /* 0x60 */ unsigned long k0;`\
`    /* 0x64 */ unsigned long k1;`\
`    /* 0x68 */ unsigned long gp;`\
`    /* 0x6c */ unsigned long sp;`\
`    /* 0x70 */ unsigned long fp;`\
`    /* 0x74 */ unsigned long ra;` \
`    /* 0x78 */ unsigned long hi;`\
`    /* 0x7c */ unsigned long lo;` \
`    /* 0x80 */ unsigned long f0;`\
`    /* 0x84 */ unsigned long f1;`\
`    /* 0x88 */ unsigned long f2;`\
`    /* 0x8c */ unsigned long f3;`\
`    /* 0x90 */ unsigned long f4;`\
`    /* 0x94 */ unsigned long f5;`\
`    /* 0x98 */ unsigned long f6;`\
`    /* 0x9c */ unsigned long f7;`\
`    /* 0xa0 */ unsigned long f8;`\
`    /* 0xa4 */ unsigned long f9;`\
`    /* 0xa8 */ unsigned long f10;`\
`    /* 0xac */ unsigned long f11;`\
`    /* 0xb0 */ unsigned long f12;`\
`    /* 0xb4 */ unsigned long f13;`\
`    /* 0xb8 */ unsigned long f14;`\
`    /* 0xbc */ unsigned long f15;`\
`    /* 0xc0 */ unsigned long f16;`\
`    /* 0xc4 */ unsigned long f17;`\
`    /* 0xc8 */ unsigned long f18;`\
`    /* 0xcc */ unsigned long f19;`\
`    /* 0xd0 */ unsigned long f20;`\
`    /* 0xd4 */ unsigned long f21;`\
`    /* 0xd8 */ unsigned long f22;`\
`    /* 0xdc */ unsigned long f23;`\
`    /* 0xe0 */ unsigned long f24;`\
`    /* 0xe4 */ unsigned long f25;`\
`    /* 0xe8 */ unsigned long f26;`\
`    /* 0xec */ unsigned long f27;`\
`    /* 0xf0 */ unsigned long f28;`\
`    /* 0xf4 */ unsigned long f29;`\
`    /* 0xf8 */ unsigned long f30;`\
`    /* 0xfc */ unsigned long f31;`\
`} ERRFRAME; /* 0x8801e8c0 */` \
 \
`void *user_error_handler; /* 0x8801d368 */`\
`void *curr_nmi_handler; /* 0x8801d884 */`\
`int flag; /* 0x8801d880 */`\
`default_error_handler(void) /* 8801D370-8801d770` **`(exceptionman:0x0c70)`** `*/`\
`{`\
`    if(flag) goto l8801d76c; // break` \
`    flag++;`\
`    curr_nmi_handler=NULL; /* clear nmi handler addr */`\
`    v0=sp;`\
`    sp=0x8801e8c0;` \
`    /* save at-ra in frame (not shown */`\
`    (ERRFRAME*)sp->hi=mfhi();`\
`    (ERRFRAME*)sp->lo=mflo();`\
`    /* save f0-f31 (not shown) */` \
`    s0=*(0xbc100000);`\
`    if((s0&0x03ff03ff)==0) goto l8801d768; // break` \
`    v1=bitrev(s0); // reverse bit order`\
`    s1=clz(v1); // count left zeros` \
`    if((s0&0x000003ff)==0)`\
`    {`\
`        if((s0&0x03ff0000)==0) goto l8801d768; // break`\
`        a0=1;`\
`        s2=s0> >0x10; // nmi nr`\
`    }`\
`    else`\
`    {`\
`        a0=0;`\
`        s2=s1; // nmi nr`\
`    }` \
`    if(s2==0x00000008)`\
`    {`\
`        v0=0xbc100010;`\
`    }`\
`    else if(s2==0x00000009)`\
`    {`\
`        v0=0xbc100028;`\
`    }`\
`    else`\
`    {`\
`        v0=0xbc100034-(s2< <2);`\
`    }` \
`    v0=*(v0);` \
`    if((v0> >0x1f)!=0)`\
`    {`\
`        a1=1;`\
`    }`\
`    else`\
`    {`\
`        a1=0;`\
`    }` \
`    k0=v0&0x80000000;`\
`    a3=COP0CTRL.0;`\
`    t0=COP0CTRL.1;`\
`    v0=COP0CTRL.18; /* NMI vector table addr */`\
`    curr_nmi_handler=*(v0+(s2< <2)); /* get addr of handler */` \
`    if(curr_nmi_handler)`\
`    {`\
`        *(0xbc100004)=s0;`\
`        call(curr_nmi_handler); /* a0=0/1 a1=0/1 k0=0xbc100004; sp=0x8801e8c0; */`\
`    }` \
`    /* restore f0-f1 (not shown) */`\
`    mthi((ERRFRAME*)sp->hi);`\
`    mtlo((ERRFRAME*)sp->lo);`\
`    /* restore at-ra (not shown) */` \
`    flag=0;`\
`    COP0STAT.12=COP0CTRL.19&0xffbfffff; /* status */` \
`    if(curr_nmi_handler!=NULL)`\
`    {`\
`        /* restore remaining regs and return from exception */`\
`        COP0STAT.12=COP0STAT.12&0xffefffff; /* status */`\
`        COP0STAT.13=COP0CTRL.20; /* cause */`\
`        COP0STAT.30=COP0CTRL.1; /* Error EPC */`\
`        v0=COP0CTRL.6;`\
`        v1=COP0CTRL.7;`\
`        eret();`\
`    }`\
`    else`\
`    {`\
`        call(user_error_handler);`\
`    }`\
`l8801d768:`\
`    brk(0x20000);`\
`l8801d76c:`\
`    brk(0x20000);`\
`}`\

#### 9.5.2  interrupt

##### 9.5.2.1 [  Interrupt Cause]{#sec9.5.2.1}

[]{#tth_tAb1}

+-------------------------------------------------------------------------+
|   ------------ ---------- ---------------- ---------------------------- |
|     **Number**   **Subs** **Name**         **Description**              |
|              0            `UART_ALL`                                    |
|              1            `SPI_ALL`                                     |
|              2            `TIM_PERI_ALL`                                |
|              3            `USB_ALL`                                     |
|              4         32 `GPIO`           GPIO                         |
|              5            `ATA`            ATA/ATAPI                    |
|              6         16 `SPOCK`          UMD MAN                      |
|              7            `SMS1`           Memstick (MSCM0)             |
|              8            `SMS2`           WLAN                         |
|              9            `MG`                                          |
|             10            `AUDIO1`                                      |
|             11            `AUDIO2`                                      |
|             12            `IIC`            I2C                          |
|             13            `KEY`                                         |
|             14            `SIRCS`          IrDA                         |
|             15            `TIM0_SYS`       Systimer 0                   |
|             16            `TIM1_SYS`       Systimer 1                   |
|             17            `TIM2_SYS`       Systimer 2                   |
|             18            `TIM3_SYS`       Systimer 3                   |
|             19            `COUNT`          Thread0                      |
|             20            `EMC_SM`         NAND                         |
|             21         10 `DMAC128`        DMACPLUS                     |
|             22            `DMAC_SC1`       DMA0                         |
|             23            `DMAC_SC2`       DMA1                         |
|             24            `KIRK`           MEMLMD                       |
|             25         32 `AW`             GE                           |
|             26            `USB_MAIN`                                    |
|             27                                                          |
|             28                                                          |
|             29                                                          |
|             30         32 `VSYNC`          Display VBlank               |
|             31            `SYS_REG`        ME Codec                     |
|             32            `UART1`                                       |
|             33            `UART2`                                       |
|             34            `UART3`                                       |
|             35            `UART4`                                       |
|             36            `UART5`          HP Remote                    |
|             37            `UART6`                                       |
|             38                                                          |
|             39                                                          |
|             40            `SPI1`                                        |
|             41            `SPI2`                                        |
|             42            `SPI3`                                        |
|             43            `SPI4`                                        |
|             44            `SPI5`                                        |
|             45            `SPI6`                                        |
|             46                                                          |
|             47                                                          |
|             48            `TIM1_PERI`                                   |
|             49            `TIM2_PERI`                                   |
|             50            `TIM3_PERI`                                   |
|             51            `TIM4_PERI`                                   |
|             52                                                          |
|             53                                                          |
|             54                                                          |
|             55                                                          |
|             56            `USB_TS`         USB Resume                   |
|             57            `USBCON_TS`      USB Ready                    |
|             58            `USBDIS_TS`      USB Connect                  |
|             59            `USBREADY_TS`    USB Disconnect               |
|             60            `SMS1_CON`       Memstick Insertion (MSCM1)   |
|             61            `SMS1_DISCON`    Memstick Removal (MSCM2)     |
|             62            `SMS2_CON`       WLAN                         |
|             63            `SMS2_DISCON`    WLAN                         |
|             64            `SOFT1`                                       |
|             65            `SOFT2`          Thread1                      |
|             66            `CPUTIMER`       Interrupt                    |
|   ------------ ---------- ---------------- ---------------------------- |
+-------------------------------------------------------------------------+

##### 9.5.2.2 [  Interrupt Handler]{#sec9.5.2.2}

`typedef struct`\
`{`\
`    /* 0x00 */ unsigned long unk000; /* some kind of flag */`\
`    /* 0x04 */ unsigned long at;`\
`    /* 0x08 */ unsigned long gprv0;`\
`    /* 0x0c */ unsigned long gprv1;` \
`    /* 0x10 */ unsigned long a0;`\
`    /* 0x14 */ unsigned long a1;`\
`    /* 0x18 */ unsigned long a2;`\
`    /* 0x1c */ unsigned long a3;` \
`    /* 0x20 */ unsigned long t0;`\
`    /* 0x24 */ unsigned long t1;`\
`    /* 0x28 */ unsigned long t2;`\
`    /* 0x2c */ unsigned long t3;`\
`    /* 0x30 */ unsigned long t4;`\
`    /* 0x34 */ unsigned long t5;`\
`    /* 0x38 */ unsigned long t6;`\
`    /* 0x3c */ unsigned long t7;`\
`    /* 0x40 */ unsigned long s0;`\
`    /* 0x44 */ unsigned long s1;`\
`    /* 0x48 */ unsigned long s2;`\
`    /* 0x4c */ unsigned long s3;`\
`    /* 0x50 */ unsigned long s4;`\
`    /* 0x54 */ unsigned long s5;`\
`    /* 0x58 */ unsigned long s6;`\
`    /* 0x5c */ unsigned long s7;`\
`    /* 0x60 */ unsigned long t8;`\
`    /* 0x64 */ unsigned long t9;` \
`    /* 0x68 */ unsigned long k0;`\
`    /* 0x6c */ unsigned long k1;`\
`    /* 0x70 */ unsigned long gp;`\
`    /* 0x74 */ unsigned long sp;`\
`    /* 0x78 */ unsigned long fp;`\
`    /* 0x7c */ unsigned long ra;` \
`    /* 0x80 */ unsigned long f0;`\
`    /* 0x84 */ unsigned long f1;`\
`    /* 0x88 */ unsigned long f2;`\
`    /* 0x8c */ unsigned long f3;`\
`    /* 0x90 */ unsigned long f4;`\
`    /* 0x94 */ unsigned long f5;`\
`    /* 0x98 */ unsigned long f6;`\
`    /* 0x9c */ unsigned long f7;`\
`    /* 0xa0 */ unsigned long f8;`\
`    /* 0xa4 */ unsigned long f9;`\
`    /* 0xa8 */ unsigned long f10;`\
`    /* 0xac */ unsigned long f11;`\
`    /* 0xb0 */ unsigned long f12;`\
`    /* 0xb4 */ unsigned long f13;`\
`    /* 0xb8 */ unsigned long f14;`\
`    /* 0xbc */ unsigned long f15;`\
`    /* 0xc0 */ unsigned long f16;`\
`    /* 0xc4 */ unsigned long f17;`\
`    /* 0xc8 */ unsigned long f18;`\
`    /* 0xcc */ unsigned long f19;`\
`    /* 0xd0 */ unsigned long f20;`\
`    /* 0xd4 */ unsigned long f21;`\
`    /* 0xd8 */ unsigned long f22;`\
`    /* 0xdc */ unsigned long f23;`\
`    /* 0xe0 */ unsigned long f24;`\
`    /* 0xe4 */ unsigned long f25;`\
`    /* 0xe8 */ unsigned long f26;`\
`    /* 0xec */ unsigned long f27;`\
`    /* 0xf0 */ unsigned long f28;`\
`    /* 0xf4 */ unsigned long f29;`\
`    /* 0xf8 */ unsigned long f30;`\
`    /* 0xfc */ unsigned long f31;` \
`    /* 0x100 */ unsigned long unk100; /* COP1CTRL.6 */`\
`    /* 0x104 */ unsigned long hi;`\
`    /* 0x108 */ unsigned long lo;`\
`    /* 0x10c */ unsigned long cop0status;`\
`    /* 0x110 */ unsigned long cop0epc;`\
`    /* 0x114 */ unsigned long cop0cause;`\
`} IRQFRAME;` \
`void * /* [r] 0x88020f6c 'null' handler address */` \
`// these 3 structs are probably the same`\
`typedef struct `\
`{`\
`/* 0x00 */ u32 unk00;`\
`/* 0x04 */ u32 unk04;`\
`} struct88022610 [4]; /* [r/w] 0x88022610 ? (2628) */` \
`typedef struct `\
`{`\
`/* 0x00 */ u32 unk00;`\
`/* 0x04 */ u32 unk04;`\
`} struct88022630 [4]; /* [r/w] 0x88022630 ? */` \
`typedef struct `\
`{`\
`/* 0x00 */ u32 unk00;`\
`/* 0x04 */ u32 unk04;`\
} `struct88022650 [4]; /* [r/w] 0x88022650 ? */` \
`typedef struct `\
`{`\
`/* 0x00 */ void *entry;`\
`/* 0x04 */ void *gp;`\
`/* 0x08 */ u32`\
`/* 0x0c */ u32 calls;`\
`/* 0x10 */ u32 min_clock_lo;`\
`/* 0x14 */ u32 min_clock_hi;`\
`/* 0x18 */ u32 max_clock_lo;`\
`/* 0x1c */ u32 max_clock_hi;`\
`/* 0x20 */ u32 total_clock_lo;`\
`/* 0x24 */ u32 total_clock_hi;`\
`/* 0x28 */ void *`\
`/* 0x2c */ void *`\
`/* 0x30 */ u32`\
`/* 0x34 */ u32`\
`} IntrHandlerOptionParam *IntrHandlerOption[67]; /* [r/w] 88022770 */` \
`/* [r/w] 0x8802277c ? some flag */`\
`unsigned long long88022780[4]; /* [w] 0x88022780 stackpointer before calling handler */`\
`/* [w] 0x88022790 ? cop0stat.9 count */`\
`/* [w] 0x88022794 ? cop0stat.9 count */`\
`/* [w] 0x88022798 ? */`\
`/* [r/w] 0x8802279c ? */`\
`/* [r/w] 0x880227a0 ? counter */` \
`typedef struct `\
`{`\
`/* 0x00 */ u32 unk00;`\
`/* 0x04 */ u32 unk04;`\
`} struct880227a4; /* [r] 0x880227a4 ? */` \
`void * /* [r] 880227ac ? handler address (8803be58 threadman:?) */`\
`void * /* [r] 880227b0 ? handler address (8802d724 threadman:?) */`\
`/* [r] 880227b4 ? stack stuff */`\
`void * /* [r/w] 880227d0 ? handler address */` \
`default_irq_handler(void) /* 88020F74` **`(interruptman:0x2274)`** `*/`\
`{`\
`    /* `\
`        some preparations, set up the stack`\
`        (beware of gotos :])`\
`    */` \
`    v1=sp; // original stackpointer`\
`    if(*(0x8802277c)==0) goto l88020fa4;`\
`    if((COP0CTRL.2&0x18)!=0) goto l88020fb8; /* cop0.status */`\
`    goto l88020f94;`\
`l88020fa4:`\
`    *(0x88022790)=COP0STAT.9; /* count */`\
`l88020fb8:`\
`    if(COP0CTRL.14!=0) goto l88020fc4; /* GPR.sp.Kernel */`\
`l88020f94: `\
`    /* allocate and align stackframe */`\
`    sp=(sp+0xfffffee0)&0xffffffc0;`\
`l88020fc4:` \
`    /*`\
`        save environment on the stack`\
`    */` \
`    (IRQFRAME*)sp->at=at;`\
`    (IRQFRAME*)sp->sp=v1; // original stackpointer`\
`    (IRQFRAME*)sp->gprv0=COP0CTRL.4;`\
`    (IRQFRAME*)sp->gprv1=COP0CTRL.5;`\
`    (IRQFRAME*)sp->a0=a0;`\
`    (IRQFRAME*)sp->a1=a1;`\
`    (IRQFRAME*)sp->a2=a2;`\
`    (IRQFRAME*)sp->a3=a3;`\
`    (IRQFRAME*)sp->k0=k0;`\
`    (IRQFRAME*)sp->k1=k1;`\
`    (IRQFRAME*)sp->gp=gp;`\
`    (IRQFRAME*)sp->fp=fp;`\
`    (IRQFRAME*)sp->ra=ra;`\
`    (IRQFRAME*)sp->hi=mfhi();`\
`    (IRQFRAME*)sp->lo=mflo();`\
`    (IRQFRAME*)sp->cop0status=COP0CTRL.2;`\
`    (IRQFRAME*)sp->cop0cause=COP0CTRL.3;`\
`    (IRQFRAME*)sp->cop0epc=COP0CTRL.0;`\
`    (IRQFRAME*)sp->unk100=COP1CTRL.2;` \
`    COP1CTRL.6=0;`\
`    COP1CTRL.6=0x00000e00;` \
`    /*`\
`        alloc space on stack for local variables`\
`    */`\
`    (IRQFRAME*)sp->unk=0;` \
`    if(*(0x8802277c))`\
`    `{ `        a1=COP0CTRL.15; /* GPR.sp.User */`\
`        k0=sp;`\
`        if(COP0CTRL.2&0x18) sp=a1; /* cop0status */`\
`        a0=*(0x880227b4) + 0x0240;`\
`        at=(sp<a0);`\
`        if(at!=0)`\
`        {`\
`            COP0STAT.12=(IRQFRAME*)sp->cop0status & 0x2fffffe0; /* status */`\
`            while(1)`\
`            {`\
`                brk(0xfff);`\
`            }`\
`        }`\
`        sp+=0xffffffe0; /* alloc 0x20 bytes on stack */`\
`        *(sp+0x001c)=k0; // save pointer to IRQFRAME`\
`    }`\
`    else`\
`    {`\
`        k0=sp;`\
`        sp=0x880257a0;`\
`        *(sp+0x1c)=k0; // save pointer to IRQFRAME` \
`        for(i=0;i<4;i++)`\
`        {`\
`            struct88022630[i]=struct88022610[i];`\
`        }`\
`    `}\
`    k1=*(0x8802277c);`\
`    *(0x8802277c)++; `\
`    v0=88022208(); /* also returns v1 */`\
`    struct88022650[k1].unk00=v0;`\
`    struct88022650[k1].unk04=v1;`\
`    long88022780[k1]=sp;` \
`    /*`\
`        find number of irq (and put it in a0)`\
`    */`\
`    v0=(IRQFRAME*)k0->cop0status & 0x2fffffe0;`\
`    COP0STAT.12=v0; // status` \
`    if(( (v0 & (IRQFRAME*)k0->cop0cause) &0x8300)!=0)`\
`    `{ `        v1=((v1< <5)|v1)< <0x10;`\
`        v1=clz(v1); // count left zeros`\
`        k1=66-v1; /* 66=highest irq number */`\
`        v0=88022218(struct88022630[0].unk00,struct88022630[0].unk04);`\
`        a0=k1;`\
`    }`\
`    else`\
`    {`\
`        v0=880221d8(); /* also returns v1 */`\
`        for(k0=0;k0<3 /* ? */;k0++)`\
`        {`\
`            a0=struct88022630[k0+1].unk00; // 0x88022638`\
`            a1=struct88022630[k0+1].unk04; // 0x8802263c`\
`            a2=a0&v0;`\
`            a3=a1&v1;` \
`            if((a2|a3)!=0)`\
`            {`\
`                v0=88022218(struct88022630[k0].unk00,struct88022630[k0].unk04);` \
`                k0=a2;`\
`                k1=a3;`\
`                if(k0)`\
`                `{\
`                    a1=bitrev(k0); // reverse bit order`\
`                    a0=clz(a1); // count left zeros`\
`                }`\
`                else`\
`                {`\
`                    if(k1==0)`\
`                    {`\
`                        /* set handler address to 'null' handler and end irq handling */`\
`                        *(0x880227d0)=*(0x88020f6c); // 88021c98`\
`                        goto l880219d4; // call handler *(0x880227d0)`\
`                    `} `                    a1=bitrev(k1); // reverse bit order`\
`                    a0=clz(a1); // count left zeros`\
`                    a0+=0x0020;`\
`                }` \
`                goto l880211e4; // call registered handler in a0`\
`            }` \
`        }` \
`        /* set handler address to 'null' handler and end irq handling */`\
`        *(0x880227d0)=*(0x88020f6c); // 88021c98`\
`        goto l880219d4; // call handler *(0x880227d0)`\
`    `}\
`l880211e4:` \
`    /*`\
`        call registered handler for individual interrupt (in a0)`\
`    */`\
`    k0=IntrHandlerOption[a0]->entry;`\
`    k1=IntrHandlerOption[a0]->entry;` \
`    if((k1==3) - |(k1==0)) // no handler registered`\
`    `{\
`        /* set handler address to 'null' handler and end irq handling */`\
`        *(0x880227d0)=*(0x88020f6c); // 88021c98`\
`        goto l880219d4; // call handler *(0x880227d0)`\
`    `} `    *(sp+0x0014)=a0;`\
`    *(0x88022798)=a0;` \
`    if(a0!=0x88022798)`\
`    `{\
`        if((a0+0xffffffc0)<0)`\
`        `{\
`            v0=88022234(a0); /* also returns v1 */`\
`        }`\
`        else`\
`        {`\
`            v0=~((v0+1)< <8);`\
`            v1=COP0STAT.13 & v0; /* cause */`\
`            COP0STAT.13=v1; /* cause */`\
`        `} `    `}\
`    while(1)`\
`    {`\
`        *(sp+0x0018)=k0; /* k0: pointer to IntrHandlerOptionParam */`\
`        a1=*(k0+0x0008);` \
`        a2=*(sp+0x001c); // get pointer to IRQFRAME`\
`        a2=(IRQFRAME*)a2->cop0epc;` \
`        gp=*(k0+0x0004);`\
`        v0=k1&0x0003;`\
`        at=0x0003;` \
`        if(v0==at)`\
`        {`\
`            *(0x880227d0)=k1&0xfffffffc; /* handler address */`\
`            goto l880219d4; // call handler *(0x880227d0)`\
`        `} `        else if(v0!=0)`\
`        `{\
`            v0=*(sp+0x001c); // get pointer to IRQFRAME`\
`            if((IRQFRAME*)v0->unk000!=4)`\
`            `{\
`                /* save t0...t9 in *(v0+0x20...0x64)(not shown) */`\
`                /* save f0...t31 in *(v0+0x80...0xfc)(not shown) */`\
`                (IRQFRAME*)v0->unk000=4;`\
`            `} `        `}\
`        if((*(k0+0x0030) & 0x0100)==0)`\
`        `{\
`            ra=COP0STAT.9; /* count */`\
`            v1=struct880227a4.unk04+(ra<struct880227a4.unk00);`\
`            *(sp+0x000c)=ra;`\
`            *(sp+0x0010)=v1;`\
`        `}\
`        v0=k1&0xfffffffc;`\
`        ra=(a0<0x40);`\
`        mtic(ra);`\
`        k1=0;` \
`        call(v0); /* call handler (jal) */` \
`        mtic(0);`\
`        k0=*(sp+0x0018);`\
`        a0=*(k0+0x0030) & 0x0100;` \
`        if(a0==0)`\
`        `{\
`            *(sp)=v0;`\
`            a3=0x880227a4;`\
`            v1=struct880227a4.unk04;`\
`            a2=((COP0STAT.9)<(struct880227a4.unk00)); /* count */`\
`            v1+=a2;`\
`            a0=*(sp+0x000c);`\
`            a1=*(sp+0x0010);`\
`            v1-=a1;`\
`            a1=(v0<a0);`\
`            v0-=a0;`\
`            v1-=a1;`\
`            a0=*(k0+0x0010);`\
`            a1=*(k0+0x0014);` \
`            if((a1<v1)==0)`\
`            `{\
`                if((a1!=v1)|((a0<v0)==0))`\
`                `{\
`                    *(k0+0x0010)=v0;`\
`                    *(k0+0x0014)=v1;`\
`                `} `            `}\
`            a0=*(k0+0x0018);`\
`            a1=*(k0+0x001c);` \
`            if((v1<a1)==0)`\
`            `{\
`                if((v1!=a1)|((v0<a0)==0))`\
`                `{\
`                    *(k0+0x0018)=v0;`\
`                    *(k0+0x001c)=v1;`\
`                `} `            }` \
`            a0=*(k0+0x0020) + v0;`\
`            a1=*(k0+0x0024) + v1 + (a0<v0);`\
`            *(k0+0x0020)+=a0;`\
`            *(k0+0x0024)+=a1;`\
`            v0=*(sp);`\
`        `}\
`        *(0x8802279c)++;`\
`        *(k0+0x000c)++;`\
`        a0=*(k0+0x0030) & 0x1000;` \
`        if(a0!=0) break;`\
`        v0++;`\
`        if(v0==0) break;`\
`        ra=v0+1;`\
`        if(ra==0)`\
`        `{\
`            a0=*(sp+0x0014);`\
`            v1=66; // 66=number of highest irq`\
`            if(a0==v1) break;`\
`            v0=a0+0xffffffc0;` \
`            if(v0>=0)`\
`            `{\
`                COP0STAT.12=COP0STAT.12&(((v0+1)< <8)^0xffffffff); /* status */`\
`                break;` \
`            `}\
`            /* make bitmask */`\
`            v0=0;v1=0;`\
`            a1=a0+0xffffffe0;` \
`            if(a1<0)`\
`            `{\
`                v0=1< <a0;`\
`            `} `            else`\
`            `{\
`                v1=1< <a1;`\
`            `}\
`            v0^=0xffffffff; v1^=0xffffffff;` \
`            /* AND array with mask (0x60 bytes) */`\
`            a2=0x88022610; // start`\
`            a3=a2+0x0060; // end` \
`            do`\
`            {`\
`                *(a2+0)&=v0; `\
`                *(a2+4)&=v1; `\
`                a2+=8;`\
`            } while(a2<a3);` \
`            break;` \
`        `} `        v0=(v0-1)< <2;`\
`        ra=*(sp+0x0018);`\
`        ra=*(ra+0x0028);`\
`        a0=*(sp+0x0014);`\
`        k0=*(ra);`\
`        k1=*(k0);`\
`    } // while(1)` \
`    v0=*(0x8802277c) - 1;`\
`    *(0x8802277c)=v0;` \
`    if(v0==0)`\
`    `{\
`        ra=0x88022628;`\
`    `} `    else`\
`    `{\
`        k1=v0< <3;`\
`        ra=0x88022650+k1;`\
`    `}\
`    88022218(*(ra),*(ra+0x0004));` \
`    /* ********** ********** ********** ********** ********** **********`\
`        thread management`\
`    */` \
`    a0=*(sp+0x001c); // pointer to IRQFRAME` \
`    if(*(0x8802277c)==0)`\
`    `{\
`        v0=0x880227a0;`\
`        *(0x880227a0)++;`\
`        call(*(0x880227b0)); /* call handler (jal) (8802d724 threadman:?) (note: accesses memory at the second 4mb!) */`\
`        a0=*(sp+0x001c); // pointer to IRQFRAME` \
`        if(v0!=0)`\
`        `{\
`            if((IRQFRAME*)a0->unk000!=4)`\
`            `{\
`                /* save t0...t9 in *(a0+0x20...0x64)(not shown) */`\
`                /* save f0...t31 in *(a0+0x80...0xfc)(not shown) */`\
`                (IRQFRAME*)a0->unk000=4;`\
`            `}\
`            a0=call(*(0x880227ac)); /* call handler (jal) (8803be58 threadman:?) returns pointer to IRQFRAME */`\
`        `} `    `}\
`    /* ********** ********** ********** ********** ********** **********`\
`        restore environment and return from exception`\
`    */` \
`    sp=a0; // get pointer to IRQFRAME`\
`    a0=(IRQFRAME*)sp->unk000; // flag ?` \
`    if(a0==1)`\
`    `{\
`        /* restore f20...f31 from *(sp+0xd0...0xfc) (not shown) */ `\
`        COP1CTRL.6=0;`\
`        COP1CTRL.6=(IRQFRAME*)sp->unk100;`\
`        /* restore s0...s7,gp,fp from *(sp+0x40...0x5c,0x70,0x78) (not shown) */ `\
`        ra=(IRQFRAME*)sp->ra; /* handler address */`\
`        v0=0x0008ff00;`\
`        COP0STAT.12=((IRQFRAME*)sp->cop0status & (~v0)) - (COP0STAT.12 & v0); /* Status */`\
`        *(0x88022794)=COP0STAT.9; /* Count */`\
`        /* restore k0,k1,sp from *(sp+0x68,0x6c,0x74) (not shown) */ `\
`        v0=1;`\
`        call(ra); /* call handler (j) */`\
`        /* never reaches here ********** ********** ********** */`\
`    `}\
`    else if(a0!=0)`\
`    `{\
`        /* restore f0...f31 from *(sp+0x80...0xfc) (not shown) */ `\
`        mthi((IRQFRAME*)sp->hi);`\
`        mtlo((IRQFRAME*)sp->lo);`\
`        /* restore at...fp from *(sp+0x04...0x78) (not shown) */ `\
`    `} `    else`\
`    `{\
`        mthi((IRQFRAME*)sp->hi);`\
`        mtlo((IRQFRAME*)sp->lo);`\
`        /* restore at...a3,gp,fp from *(sp+0x04...0x1c,0x70,0x78) (not shown) */ `\
`    `}\
`    ra=0x0008ff00;`\
`    COP0STAT.12=(((IRQFRAME*)sp->cop0status) & (~ra)) - (COP0STAT.12 & ra); /* status */`\
`    COP0STAT.14=(IRQFRAME*)sp->cop0epc; /* epc */`\
`    COP1CTRL.6=0;`\
`    COP1CTRL.6=(IRQFRAME*)sp->unk100;`\
`    *(0x88022794)=COP0STAT.9; /* count */;` \
`    /*`\
`        Profiler Stuff`\
`    */` \
`    if(COP0CTRL.25!=0) /* PROFILER_BASE */`\
`    `{\
`        k0=*(PROFILER_BASE+0x0008);`\
`        if(k0!=0)`\
`        `{\
`            k0--;`\
`            *(PROFILER_BASE+0x0008)=k0;`\
`            if(k0==0)`\
`            `{\
`                k0=*(PROFILER_BASE+0x0004);`\
`                k1=*(PROFILER_BASE);`\
`                *(k1)=k0;`\
`                sync();`\
`            `} `        `} `    `}\
`    /* restore k0,k1,ra,sp from *(sp+0x68,0x6c,0x7c,0x74) (not shown) */ `\
`    eret();` \
`    /* ********** ********** ********** ********** ********** **********`\
`        restore environment and call handler *(0x880227d0)`\
`    `\*/\
`l880219d4: `\
`    v0=*(0x8802277c)-1;`\
`    *(0x8802277c)=v0;`\
`    88022218(struct88022650[v0].unk00,struct88022650[v0].unk04);`\
`    sp=*(sp+0x001c); /* get pointer to IRQFRAME */` \
`    if((IRQFRAME*)sp->unk000==4)`\
`    `{\
`        /* restore t0...t9 from *(sp+0x20...0x64) (not shown) */ `\
`        /* restore f0...f31 from *(sp+0x80...0xfc) (not shown) */ `\
`    `}\
`    mtic(0);`\
`    COP0CTRL.3=(IRQFRAME*)sp->cop0cause; /* cop0.cause */`\
`    COP0CTRL.0=(IRQFRAME*)sp->cop0epc; /* cop0.epc */`\
`    COP0CTRL.4=(IRQFRAME*)sp->gprv0; /* gpr.v0 */`\
`    COP0CTRL.5=(IRQFRAME*)sp->gprv1; /* gpr.v1 */`\
`    v0=0xfff700ff;`\
`    COP0CTRL.2=((IRQFRAME*)sp->cop0status & v0) |((~v0) & COP0STAT.12); /* cop0.status, Status */`\
`    /* restore at,a0...a3,k0..gp,fp,ra from *(sp+...) (not shown) */ `\
`    mthi((IRQFRAME*)sp->hi);`\
`    mtlo((IRQFRAME*)sp->lo);`\
`    COP0STAT.12=(IRQFRAME*)sp->cop0status; /* Status */`\
`    COP1CTRL.6=0;`\
`    COP1CTRL.6=(IRQFRAME*)sp->unk100;`\
`    COP0CTRL.4=(IRQFRAME*)sp->gprv0; /* gpr.v0 */`\
`    COP0CTRL.5=(IRQFRAME*)sp->gprv1; /* gpr.v1 */`\
`    sp=(IRQFRAME*)sp->sp;`\
`    call(*(0x880227d0)) /* call handler (j) */` \
`    /* will never reach here ********** ********** ********** */`\
`}` \
`/* 'null' handler */`\
`void 88021c98(void)`\
`    COP0STAT.14=COP0CTRL.0;`\
`    COP0STAT.12=COP0CTRL.2;`\
`    v0=COP0CTRL.4;`\
`    v1=COP0CTRL.5;`\
`    eret();`\
}\
`unsigned long 880221d8(void)`\
`    v0=*(0xbc300000) & 0xfffffff0;`\
`    v1=*(0xbc300010);`\
`    return v0; /* also v1 */`\
}\
`unsigned long 88022208(void)`\
`    v0=*(0xbc300008);`\
`    v1=*(0xbc300018);`\
`    return v0; /* also v1 */`\
}\
`unsigned long 88022218(unsigned long a0, unsigned long a1)`\
`    *(0xbc300008)=a0|0x0000000f;`\
`    *(0xbc300018)=a1;`\
`    sync();`\
`    return 0xbc300000;`\
}\
`unsigned long 88022234(unsigned long a0)`\
`    if((0x1f>=a0)&(a0>=0x1e))`\
`    `{ `        v1=1< <a0;`\
`        v0=0xbc300000;`\
`        *(0xbc300000)=v1;`\
`        sync();`\
`    `} `    return v0; /* also v1 */`\
}\

##### 9.5.2.3 [  Thread Management]{#sec9.5.2.3}

// note: this is the first of two routines called by the interrupt handler `unsigned long 8802d724(void) /* 8802d724 - threadman: ? */`\
`    a1=0x88040000;`\
`    a0=0x88042a08;`\
`    a2=*(a0+0x0418); // 0x88042e20`\
`    v0=0;`\
`    if(a2==0)`\
`    `{ `        v1=*(a1+0x2a08); // 0x88042a08`\
`        a2=*(a0+0x0004); // 0x88042a0c`\
`        a1=a2^v1;`\
`        v0=(0<a1);`\
`        if(v0!=0)`\
`        `{ `            *(v1+0x00e4)=v1+0x00e8;`\
`        `} `    `} `    return v0;`\
}\
// note: this is the second of two routines called by the interrupt handler `8803be58( /* a0 */ ) /* 8803be58 - threadman:? */`\
`{`\
`    /*`\
`        create stackframe (0x10 bytes) and save s0,s1,s2,ra (not shown)`\
`    */` \
`    s2=0x88040000;`\
`    v1=s2+0x2a08;`\
`    a1=*(v1+0x418); // 0x88042e20`\
`    v0=a0;` \
`    if(a1==0)`\
`    {`\
`        s0=*(s2+0x2a08);`\
`        v0=*(s0+0x000c);` \
`        if(*(s0+0x0108)!=0)`\
`        {`\
`            a0=0xbc400000;` /\* `PROFILER+0x00` \*/ `            a2=v0+0x0010;`\
`            a3=0xbc400000;` /\* `PROFILER+0x00` \*/ `            t0=0xbc400050;` /\* `PROFILER+0x50` \*/ \
`            /* copy profiler regs to *(a2) (0x50 bytes) */`\
`            do`\
`            {`\
`                t3=*(a3+0x00);`\
`                t2=*(a3+0x04);`\
`                a1=*(a3+0x08);`\
`                t1=*(a3+0x0c);`\
`                *(a2)=t3;`\
`                a3+=0x10;`\
`                a2+=0x10;`\
`                *(a2+0xfffffff4)=t2;`\
`                *(a2+0xfffffff8)=a1;`\
`                *(a2+0xfffffffc)=t1;`\
`            } while(a3!=t0);`\
`            v0=*(a3);`\
`            *(a2)=v0;`\
`            v0=*(s0+0x000c);`\
`        }` \
`        a2=+0x0020;`\
`        s1=s2+0x2a08;`\
`        if(v0==a2) goto 0x8803bf48;`\
`        a2=*(s0+0x0070);`\
`        t0=*(s0+0x00f4);`\
`        a1=*(s0+0x0008);`\
`        a3=*(a2);`\
`        s1=*(t0+0x0074);` \
`        if(a3!=a1)`\
`        {`\
`            a3=*(s0+0x0074);`\
`            t8=0x88040000;`\
`            a0=0x88042634;`\
`            t0=s1;`\
`            880412b8(0x88042634,0x00000000,0x00000000,0x00000000)`\
`            t7=s2+0x2a08;`\
`            t6=*(t7+0x0640);`\
`            t5=*(u8*)(t6+0x15);`\
`            t4=t5< <2;`\
`            a0=s0-t4;`\
`            880405a0(0x00000000,0x00000000,0x00000000,0x00000000)`\
`        }` \
`l8803bf28:`\
`        t9=*(s0+0x00d0);`\
`        a2=*(s0+0x007c);`\
`        if(t9<0) goto l8803c150;`\
`        a2=*(s0+0x0070);`\
`l8803bf38:`\
`        t4=(s1<a2);`\
`        if(t4!=0) goto 0x8803c11c;`\
`        a3=*(s0+0x0074);`\
`        s1=s2+0x2a08;`\
`l8803bf48:`\
`        v0=*(s1+0x0004);` \
`        if(v0==0)`\
`        {`\
`            88040310(a0,a1,a2,a3)`; `            v0=*(s1+0x0004);`\
`        }` \
`        if(s0==v0)`\
`        `{ `            v1=t6+0x0001;`\
`            *(s1+0x0680)=v1;`\
`        }`\
`        else`\
`        {`\
`            t6=*(s1+0x0680);`\
`            88038090(0x00000000,0x00000000,0x00000000,0x00000000);`\
`            t7=s1+0x0428;`\
`            t9=*(t7+0x0004);`\
`            t1=*(s1+0x0428);`\
`            t6=s0+0x0064;`\
`            a1=*(s0+0x0064);`\
`            t2=*(t6+0x0004);`\
`            a0=0;`\
`            t5=t9< <0;`\
`            a3=0;`\
`            t9=a0+t1;`\
`            t8=0;`\
`            t3=(t9<t1);`\
`            t4=t2< <0;`\
`            a2=t5+a3;`\
`            t2=t8+a1;`\
`            t5=a2+t3;`\
`            a0=t4+a3;`\
`            t3=(t2<a1);`\
`            a1=a0+t3;`\
`            t8=(v0<t9);`\
`            t3=v1-t5;`\
`            a0=v0-t9;`\
`            t5=t2+a0;`\
`            t4=t3-t8;`\
`            t9=(t5<a0);`\
`            t8=a1+t4;`\
`            t0=t8+t9;`\
`            t3=v1> >0;`\
`            t2=t0> >0;`\
`            *(t7+0x0004)=t3;`\
`            *(s1+0x0428)=v0;`\
`            *(t6+0x0004)=t2;`\
`            *(s0+0x0064)=t5;`\
`            a0=*(s1+0x067c);`\
`            t9=*(s0+0x00e4);`\
`            a1=a0+0x0001;`\
`            *(s1+0x067c)=a1;`\
`            t1=*(t9);`\
`            v1=t1+0x0001;`\
`            *(t9)=v1;`\
`        }` \
`        s1=s2+0x2a08;`\
`        v1=*(s1+0x0738);`\
`        s2=*(s1+0x0004);` \
`        if(v1!=0)`\
`        `{ `            t0=*(s0+0x0010);`\
`            a3=*(s0+0x0008);`\
`            t2=*(s2+0x0010);`\
`            t1=*(s2+0x0008);`\
`            a0=+0x0001;`\
`            a1=0;`\
`            a2=0x00000004;`\
`            call(v1);`\
`            s0=*(s1+0x0004);`\
`        }`\
`        else`\
`        {`\
`            s0=*(s1+0x0004);`\
`        `}\
`        s1=0x88040000;`\
`        v1=*(s0+0x0108);`\
`        *(s1+0x2a08)=s0; //0x88042a08` \
`        if(v1==0)`\
`        {`\
`            COP0CTRL.25=0x00000000;` /\* `PROFILER_BASE` \*/ `            a0=*(s0+0x00f4);`\
`        }`\
`        else`\
`        {`\
`            t0=v1+0x0060;`\
`            a3=0xbc400000;` /\* `PROFILER+0x00` \*/ `            a2=v1+0x0010;` \
`            do`\
`            {`\
`                t8=*(a2);`\
`                a1=*(a2+0x0004);`\
`                t4=*(a2+0x0008);`\
`                t7=*(a2+0x000c);`\
`                *(a3)=t8;`\
`                a2+=0x10;`\
`                a3+=0x10;`\
`                *(a3-0x0c)=a1;`\
`                *(a3-0x08)=t4;`\
`                *(a3-0x04)=t7;`\
`            } while(a2!=0);` \
`            v0=*(a2);`\
`            *(a3)=v0;`\
`            sync();`\
`            t0=*(s0+0x0108);`\
`            COP0CTRL.25=t0; /* PROFILER_BASE */`\
`            a0=*(s0+0x00f4);`\
`        }` \
`        v0=0x40000000;`\
`        t2=*(a0+0x010c);`\
`        a3=t2&v0;` \
`        if(a3!=0)`\
`        {`\
`            a0=s0;`\
`            8803c1b4(0x00000000,0x00000000,0x00000000,0x00000000);`\
`            a0=*(s0+0x00f4);`\
`        }` \
`        COP0CTRL.14=a0; /* GPR.sp.KERNEL */`\
`        t3=*(s0+0x0104);`\
`        COP0CTRL.15=t3; /* GPR.sp.USER */`\
`        a2=s0+0x0100;`\
`        COP0CTRL.16=a2; /* CurrentTCB */`\
`        v0=*(s0+0x00f4);`\
`    }`\
`    /*`\
`        restore ra,s2,s1,s0 and destroy stackframe (0x10 bytes) (not shown)`\
`    */` \
`    return v0;`\
`l8803c11c:`\
`    a1=*(s0+0x0008);`\
`    t8=0x88040000;`\
`    a0=t8+0x2634;`\
`    t0=s1`; `    880412b8(0x88042634,0x00000000,0x00000000,0x00000000)`\
`    t7=s2+0x2a08;`\
`    t6=*(t7+0x0640);`\
`    t5=*(u8*)(t6+0x15);`\
`    s1=t5< <2;`\
`    a0=s0-s1;`\
`    880405a0(0x00000000,0x00000000,0x00000000,0x00000000)`\
`    s1=s2+0x2a08;`\
`    goto l8803bf48`; `l8803c150:`\
`    a1=*(s0+0x0008);`\
`    v1=*(a2);`\
`    t3=0x88040000;`\
`    if(v1==a1) goto 0x8803c188;`\
`    a3=*(s0+0x0080);`\
`    a0=t3+0x2634;`\
`    t0=s1;`\
`    880412b8(0x88042634,0x00000000,0x00000000,0x00000000)`; `    t2=s2+0x2a08;`\
`    a0=*(t2+0x0640);`\
`    a1=*(u8*)(a0+0x15);`\
`    t1=a1< <2;`\
`    a0=s0-t1;`\
`    880405a0(0x00000000,0x00000000,0x00000000,0x00000000)`\
`l8803c188:`\
`    v0=*(s0+0x00f4);`\
`    a3=*(v0+0x010c);`\
`    a2=*(s0+0x0070);`\
`    if((a3&0x0018)!=0) goto 0x8803bf38;`\
`    a2=*(s0+0x007c);`\
`    t0=(s1<a2);`\
`    s1=s2+0x2a08;`\
`    if(t0==0) goto 0x8803bf48;`\
`    a3=*(s0+0x0080);`\
`    goto l8803c11c;`\
}\
`// called by 8803be58`\
`88038090()`\
`{`\
`    ...`\
`}` \
`// called by 8803be58`\
`8803c1b4(/* a0 */) /* 8803c1b4 - threadman: ? */`\
`{`\
`    sp+=0xfffffff0;`\
`    *(sp+0x0008)=s2;`\
`    s2=0x88040000;`\
`    *(sp+0x0004)=s1;`\
`    s1=a0;`\
`    a0=s2+0x2a08;`\
`    *(sp+0x000c)=ra;`\
`    *(sp)=s0;`\
`    v0=*(0x88042e24);`\
`    a1=*(s1+0x00fc);`\
`    ra=*(sp+0x000c);`\
`    if(v0!=a1)`\
`    `{ `        v1=*(s1+0x00d0);`\
`        a1=*(a0+0x0420);`\
`        s0=v1> >0x1f;`\
`        s0_d=s0;`\
`        s0=s2+0x2a08;`\
`        if(a1!=s0_d)`\
`        `{ `            8802d984(0x00000000,0x00000000,0x00000000,0x00000000)`\
`            if(s0==0)`\
`            `{ `                a3=*(0xbc000044);`\
`                v0=a3|0x0020;`\
`            }`\
`            else`\
`            {`\
`                a0=*(0xbc000044);`\
`                a2=0xffffffdf;`\
`                v0=a0&a2;`\
`            `} `            at=0xbc000000;`\
`            *(0xbc000044)=v0;`\
`            sync();`\
`            t0=s2+0x2a08;`\
`            *(t0+0x0420)=s0;`\
`            s0=s2+0x2a08;`\
`        `} `        t1=*(s0+0x041c);`\
`        a0=t1;`\
`        if(t1!=0)`\
`        `{ `            8802d760(0x00000000,0x00000000,0x00000000,0x00000000)`; `            t4=*(s1+0x00fc);`\
`        }`\
`        else`\
`        {`\
`            t4=*(s1+0x00fc);`\
`        `} `        *(s0+0x041c)=t4;`\
`        8802d874(t4,0x00000000,0x00000000,0x00000000)`; `        t3=*(s0+0x0684);`\
`        t2=t3+0x0001;`\
`        *(s0+0x0684)=t2;`\
`        ra=*(sp+0x000c);`\
`    `} `    s2=*(sp+0x0008);`\
`    s1=*(sp+0x0004);`\
`    s0=*(sp);`\
`    sp+=0x0010;`\
`    return v0;`\
`}` \
`8802d760()`\
`    ...`\
}\
`8802d874()`\
`    ...`\
}\
`8802d984()`\
`    ...`\
}\
`/* following functions are located in the second 'protected' 4mb */` \
`88040310()`\
`{`\
`    ...`\
`}` \
`880405a0()`\
`{`\
`    ...`\
`}` \
`880412b8()`\
`{`\
`    ...`\
`}`\

#### 9.5.3  syscall

`typedef struct _SCTABHDR`\
`{`\
`    struct _SCTABHDR *next; /* pointer to next table */`\
`    unsigned long offset; /* offset to substract from syscall code */`\
`    unsigned long num; /* number of entries in list*/`\
`    unsigned long unk; /* ? */`\
`} SCTABHDR;` \
`typedef struct`\
`{`\
`    unsigned long status; /* COP0CTRL.2 */`\
`    unsigned long epc; /* COP0STAT.14 */`\
`    unsigned long sp; /* sp*/`\
`    unsigned long ra; /* ra*/`\
`    unsigned long k1; /* k1*/`\
`    unsigned long unk14; /* COP1CTRL.2*/`\
`    unsigned long unk18; /* COP0CTRL.4*/`\
`    unsigned long tcb; /* *(COP0CTRL.16) */`\
`} SCFRAME;`\
`EXC_8_Syscall_handler(/* v0, v1 */) /* 88021e74-88022018` **`(interruptman:0x3174) */`**\
`{`\
`    v0=COP0CTRL.0 /* COP0.EPC */`\
`    v1=COP0CTRL.3 /* COP0.Cause */`\
`    t6=COP0CTRL.13 /* max sc */`\
`    t7=COP0STAT.21 /* sc code */`\
`    v0+=4;`\
`    COP0STAT.14=v0; /* EPC */`\
`    t4=COP0CTRL.12; /* sc tab */`\
`    if(t7<=t6) /* if syscall is in range */`\
`    {`\
`        t4+=t7; /* sc tab + sc code */`\
`        t7=*(t4+0x10)`\
`        if(v1>=0)`\
`        {`\
`            call(t7); /* call regular individual syscall handler */`\
`        }`\
`        while(1)`\
`        {`\
`            break #ffe`\
`        }`\
`    }`\
`    /* further handling for syscall that is not in range */`\
`    if(v1> >=0x1f) v0=ra;`\
`    COP0STAT.14=v0; /* EPC */`\
`    do`\
`    {`\
`        t4=*(t4+0); /* 0x88026820 (8802379c 0) */`\
`        t5=*(t4+4); /* (0x00) 0x8000 (0 x) */`\
`        t6=*(t4+8); /* (0xfc) 0xbffc (0 x) */`\
`        if(t5==0)`\
`        `{ `            COP0STAT.14=COP0CTRL.0;`\
`            v0=*(0x88021e6c); /* ? reverse further */`\
`            call($v0);`\
`        `} `    } while((t7<t5)|(t6<t7)); /* sccode<t5 or scnum<sccode */`\
`    t7-=t5; /* sccode-=offset */`\
`    t4+=t7; /* sctab+=sccode */`\
`    t7=*(t4+0x10); /* get handler address */` \
 \
`    /* get stackframe address */`\
`    if(COP0CTRL.2&0x0018==0) t4=sp; /* COP0.Status */`\
`    else t4=COP0CTRL.15; /* GPR.sp.USER */`\
`    t4-=sizeof(SCFRAME);` \
 \
`    (SCFRAME*)t4->status=COP0CTRL.2; /* COP0.Status */`\
`    (SCFRAME*)t4->epc=COP0STAT.14; /* EPC */`\
`    (SCFRAME*)t4->sp=sp;`\
`    (SCFRAME*)t4->ra=ra;`\
`    (SCFRAME*)t4->k1=k1;`\
`    (SCFRAME*)t4->unk18=COP0CTRL.4; /* GPR.v0 */`\
`    (SCFRAME*)t4->unk14=COP1CTRL.2;` \
 \
`    COP1CTRL.6=0;`\
`    COP1CTRL.6=0x00000e00;` \
 \
`    /* set frame and call handler */`\
`    sp=t4;`\
`    t6=COP0CTRL.16; /* current.TCB */`\
`    if(t6!=0) `\
`    {`\
`        (SCFRAME*)t4->tcb=*(t6);`\
`        *(t6)=sp;`\
`    `} `    k1=(COP0CTRL.2&0x00ff)< <16; /* COP0.Status */`\
`    COP0STAT.12=COP0CTRL.2&0x0000ffe5; /* status */`\
`    call(t7);` \
 \
`    /* restore original frame and return */`\
`    mtic(0);`\
`    COP0STAT.12=((SCFRAME*)sp->status&0xfff700ff) - (COP0STAT.12&0x0008ff00); /* status */`\
`    t6=COP0CTRL.16; /* current.TCB */`\
`    if(t6!=0)`\
`    `{ `        *(t6)=(SCFRAME*)sp->tcb;`\
`    `} `    COP1CTRL.6=0;`\
`    COP1CTRL.6=(SCFRAME*)sp->unk14;`\
`    k1=(SCFRAME*)sp->k1;`\
`    ra=(SCFRAME*)sp->ra;`\
`    COP0STAT.14=(SCFRAME*)sp->epc; /* EPC */`\
`    sp=(SCFRAME*)sp->sp;`\
`    eret();`\
`}`\

### 9.6  Debug Exception Vectors

- return from exception using `dreg`\

`bfc01000(/* v0, v1 */) /*` **`(exceptionman, power)`** `*/`\
`{`\
`    COP0CTRL.26=v0 /*` **`save v0`** **`in cc0.26 (Ex.GPR.v0)`** `*/`\
`    call (COP0CTRL.10); /*` **`jump (indirect over vector in cc0.10)`** `*/`\
}\
following handlers look all like the one above\
`bfc01100(/* v0 */)` \
`bfc01200(/* v0 */)` \
`bfc01300(/* v0 */)` \
`bfc01400(/* v0 */)` \
`bfc01500(/* v0 */)` \
`bfc01600(/* v0 */)` \
`bfc01700(/* v0 */)` \
`bfc01800(/* v0 */) /*` **`(me_wrapper)`** `*/` \
`bfc01900(/* v0 */)` \
`bfc01a00(/* v0 */)` \
`bfc01b00(/* v0 */)` \
`bfc01c00(/* v0 */)` \
`bfc01d00(/* v0 */)` \
`bfc01e00(/* v0 */)` \
`bfc01f00(/* v0 */)` \

#### 9.6.1  Debug Handler

`typedef struct`\
`{`\
`    unsigned long flags;`\
`    unsigned long unknown; /* probably DRCTRL */`\
`    unsigned long IBC;`\
`    unsigned long DBC;`\
`    unsigned long IBA;`\
`    unsigned long IBAM;`\
`    unsigned long DBA;`\
`    unsigned long DBAM;`\
`    unsigned long DBD;`\
`    unsigned long DBDM;`\
`} DBGENV;`\
`DBGENV dbgenv;`\
`debug_handler(/* v1 */) /* 8801ce30` **`(exceptionman:0x0730)`** `*/` \
`{`\
`DBGENV *env;`\
`    COP0CTRL.27=v1; /* save v1 */`\
`    env=COP0CTRL.28; /* v0=8801ec10 */`\
`    v1=env->flags;`\
`    if(v1&0x0004)`\
`    {`\
`        goto dbg_handler_0005( env /* v0 */ ); /* store debug environment */`\
`    }`\
`    else if(v1&0x0008) `\
`    {`\
`        goto dbg_handler_000a( env /* v0 */ ); /* restore debug environment */`\
`    }`\
`    else if(v1&0x0001) `\
`    {`\
`        goto dbg_handler_0005( env /* v0 */ ); /* store debug environment */`\
`    }`\
`    else if(v1&0x0002) `\
`    {`\
`        goto dbg_handler_000a( env /* v0 */ ); /* restore debug environment */`\
`    }`\
`    else if(v1&0x0010) /* single step in kernel mode one instuction then continue */`\
`    {`\
`        goto dbg_handler_0010( env /* v0 */ ); `\
`    }`\
`    else if(v1&0x0020) /* single step one instruction in user mode and continue */`\
`    {`\
`        goto dbg_handler_0020( env /* v0 */ ); `\
`    }`\
`    else if(v1&0x0040) /* single step in kernel mode one instuction then break into debugger */`\
`    {`\
`        goto dbg_handler_0040( env /* v0 */ ); `\
`    }`\
`    else if(v1&0x0080) /* single step one instruction in user mode then break into debugger */`\
`    {`\
`        goto dbg_handler_0080( env /* v0 */ ); `\
`    }`\
`    else if(v1&0x0100) /* clear step mode */`\
`    {`\
`        goto dbg_handler_0100( env /* v0 */ ); `\
`    }`\
`    `\
`    /* default */ `\
`    `\
`    DRCNTL&=0xffdf;`\
`    *(COP0CTRL.28+4)=DRCNTL;`\
`    COP0CTRL.4 =COP0CTRL.26; /* GPR.v0 = Ex.GPR.v0 */`\
`    COP0CTRL.5 =COP0CTRL.27; /* GPR.v1 = Ex.GPR.v1 */`\
`    COP0CTRL.0 = DEPC /* COP0.EPC=DEPC */`\
`    DEPC=&8801d10c; /* -> below */`\
`    COP0CTRL.3=COP0STAT.13; /* COP0.Cause = Cause */`\
`    COP0CTRL.1=COP0STAT.30; /* COP0.EPC.err = ErrorEPC */`\
`    v0=COP0STAT.12; /* Status */`\
`    COP0CTRL.2=v0; /* COP0.Status = v0 */`\
`    COP0STAT.12=v0|0x00000002;`\
`    dret();`\
`}` \
`8801d10c()`\
`{`\
`    exception_handler(24< <2);`\
`}` \
this code immediatly follows (?)\
`8801d118( /* v0 */ )`\
`{`\
`    COP0CTRL.26=v0; // save v0`\
`    v0=COP0CTRL.10; // debug handler address`\
`    call(v0) // call debug handler`\
`}`\

##### 9.6.1.1 [  Debug Sub Handler 0005]{#sec9.6.1.1}

`dbg_handler_0005( DBGENV *env /* v0 */ ) /* 0x8801cf30 */`\
`    DEPC+=4;`\
`    env->flags=0;`\
`    env->IBC=IBC;`\
`    env->DBC=DBC;`\
`    env->IBA=IBA;`\
`    env->IBAM=IBAM;`\
`    env->DBA=DBA;`\
`    env->DBAM=DBAM;`\
`    env->DBD=DBD;`\
`    env->DBDM=DBDM;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.2 [  Debug Sub Handler 000a]{#sec9.6.1.2}

`dbg_handler_000a(DBGENV *env /* v0 */ ) /* 0x8801cf90 */`\
`    DEPC+=4;`\
`    env->flags=0;`\
`    IBC=env->IBC;`\
`    DBC=env->DBC;`\
`    IBA=env->IBA;`\
`    IBAM=env->IBAM;`\
`    DBA=env->DBA;`\
`    DBAM=env->DBAM;`\
`    DBD=env->DBD;`\
`    DBDM=env->DBDM;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.3 [  Debug Sub Handler 0010]{#sec9.6.1.3}

`dbg_handler_0010(DBGENV *env /* v0 */ ) /* 0x8801cff0 */`\
`    env->flags=0x0100; /* clear step mode */`\
`    DEPC=COP0STAT.14; /* DEPC=COP0.EPC */`\
`    COP0STAT.12&=0xfff9; /* COP0.Status */`\
`    DRCNTL|=0x0020;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.4 [  Debug Sub Handler 0020]{#sec9.6.1.4}

`dbg_handler_0020(DBGENV *env /* v0 */ ) /* 0x8801d02c */`\
`    env->flags=0x0100; /* clear step mode */`\
`    DEPC=COP0STAT.14; /* DEPC=EPC */`\
`    COP0STAT.12=(COP0STAT.12&0xfff9)|0x0010; /* COP0.Status */`\
`    DRCNTL|=0x0020;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.5 [  Debug Sub Handler 0040]{#sec9.6.1.5}

`dbg_handler_0040(DBGENV *env /* v0 */ ) /* 0x8801d070 */`\
`    env->flags=0;`\
`    DEPC=COP0STAT.14; /* DEPC=EPC */`\
`    COP0STAT.12&=0xfff9; /* COP0.Status */`\
`    DRCNTL|=0x0020;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.6 [  Debug Sub Handler 0080]{#sec9.6.1.6}

`dbg_handler_0080(DBGENV *env /* v0 */ ) /* 0x8801d0a8 */`\
`    env->flags=0;`\
`    DEPC=COP0STAT.14; /* DEPC=EPC */`\
`    COP0STAT.12=(COP0STAT.12&0xfff9)|0x0010; /* COP0.Status */`\
`    DRCNTL|=0x0020;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\

##### 9.6.1.7 [  Debug Sub Handler 0100]{#sec9.6.1.7}

`dbg_handler_0100(DBGENV *env /* v0 */ ) /* 0x8801d0e8 */`\
`{`\
`    env->flags=0;`\
`    DRCNTL&=0xffdf;`\
`    v0=COP0CTRL.26; /* restore v0 */`\
`    v1=COP0CTRL.27; /* restore v1 */`\
`    dret();`\
`}`\
