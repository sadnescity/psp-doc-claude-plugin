---
name: psptek-registers
description: "PSP hardware components and registers, device by device, with addresses and bit fields. Fuller than the hardware-registers chapter of YAPSPD; use it when that one comes up short."
---

PSPTEK, a register document written in 2012 by Alex Marshall, separate from
YAPSPD and covering the same ground as its chapter 8 and more: a spec sheet, a
memory map, a flat I/O map of every register address it knows, then device
sections for memory protection, the system controller, the interrupt
controller, the profiler, the VME controller, NAND, the Graphics Engine, KIRK,
the LCD controller, GPIO and the UARTs.

Open this one first when chasing a register access. The I/O map is the only
single-page index of register addresses in either source, and the device
sections name each register and its bits where YAPSPD often leaves them blank.
It is fuller than hardware-registers on memory protection, on the system
controller's NMI registers, and above all on the interrupt controller, where
YAPSPD has four addresses marked "mask ?" and this has flags, masks and the
numbered interrupt list. It alone documents the LCD controller and the GE
control registers; YAPSPD's video chapter carries no registers at all. Go back
to YAPSPD for the NAND transfer sequences, the KIRK key blobs and the per-bit
UART detail.

Addresses here are physical, 1C000000h and up; code uses the uncached kernel
window 0xA0000000 higher, which is the form YAPSPD prints. The contents list
ends in "Other: TODO", and audio, DMA, UMD, USB and Memory Stick are indeed
absent.

---

::: {style="text-align: center;"}
[PSPTEK]{#psptek .title}\
Sony PlayStation Portable - Technical Info\
Last Updated: February 07 2015 05:39:14 UTC\

+-------------------------------------------------+-----------------------------------------+
|   -------------------------------------         |   ------------------------------------- |
|   [  PSP Reference]{#pspref .section}           |   [  CPU Reference]{#cpuref .section}   |
|   -------------------------------------         |   ------------------------------------- |
|                                                 |                                         |
| \                                               | \                                       |
| **Overview**\                                   | **General Information**\                |
| [PSP Technical Data](#techdata)\                | CPU Overview\                           |
| [PSP Memory Map](#memmap)\                      | CPU Register Set\                       |
| [PSP I/O Map](#iomap)\                          | CPU Exceptions\                         |
| \                                               | CPU Memory Alignments\                  |
| **Hardware Programming**\                       | \                                       |
| [PSP Memory Management Controller](#memman)\    | **Instruction Set**\                    |
| [PSP System Controller](#syscon)\               | CPU Memory Access\                      |
| [PSP Interrupt Management Controller](#intman)\ | Pseudo-operations\                      |
| [PSP Profiler](#prof)\                          | \                                       |
| [PSP VirtualMobileEngine Controller](#vmectrl)\ | **Further Information**\                |
| [PSP NAND Flash Controller](#nandctrl)\         | CPU Datasheet\                          |
| [PSP GraphicsEngine 3D Video](#ge)\             | \                                       |
| [PSP KIRK Crypto Controller](#kirk)\            | **About PSPTEK**\                       |
| [PSP LCD Controller](#lcdc)\                    | [About this Document](#about)\          |
| [PSP GPIO Controller](#gpio)\                   |                                         |
| [PSP UART Ports](#uart)\                        |                                         |
| \                                               |                                         |
| **Other**\                                      |                                         |
| TODO\                                           |                                         |
+-------------------------------------------------+-----------------------------------------+

\

  --------------------------------------------
  [  PSP Technical Data]{#techdata .section}
  --------------------------------------------

**Processors**\
[  Main CPU    Allegrex 32-bit Little-endian RISC CPU with FPU and VFPU, 1 \~ 333MHz, MIPS III-based \
              Also known as SC                                                                     \
  ME CPU      Allegrex 32-bit Little-endian RISC CPU with FPU, 1 \~ 333MHz, MIPS III-based          \
  VME         Unknown DSP, 128-bit Bus, 166MHz                                                     \
]{.table}**Internal Memory**\
[  32MB        Main RAM (64MB PSP-2xxx, PSP-3xxx)                                                   \
  32MB        Firmware NAND Flash (64MB PSP-2xxx, PSP-3xxx)                                        \
  8MB         VRAM (EDRAM)                                                                         \
  16KB        SC CPU Scratchpad                                                                    \
  2MB         ME CPU Scratchpad                                                                    \
  32KB        SC CPU Cache (Data: 16KB, Code: 16KB)                                                \
  32KB        ME CPU Cache (Data: 16KB, Code: 16KB)                                                \
  2MB         Shared RAM                                                                           \
  4KB         Boot ROM                                                                             \
]{.table}**Video**\
[  Display     480x272 pixels (4.3 inch widescreen 16:9 TFT color LCD)                              \
  3D Engine                                                                                        \
  Framebuffer                                                                                      \
]{.table}**Sound**\
[  Effects     3D sound, synthesizer, effector, equalizer                                           \
  Codecs      ATRAC3, ATRAC3+, AAC, WMA, MP3                                                       \
  Output      Built-in-speaker (stereo), or headphones socket (stereo)                             \
]{.table}**Controls**\
[  Directional 4 buttons, analog stick                                                              \
  Buttons     4 face buttons, 2 shoulder buttons                                                   \
  Other       Home, Start, Select, Volume+, Volume-, Brightness, Mute                              \
]{.table}**Communication**\
[  Ports       USB, Infrared, Wireless LAN 802.11b, (AV-Out PSP-2xxx, PSP-3xxx)                     \
]{.table}**External Memory**\
[  Memstick    Memory Stick PRO Duo (up to 32GB)                                                    \
  UMD         1.8GB, Dual-Layer                                                                    \
]{.table}**Case Dimensions**\
[  Size (mm)   PSP-1xxx: 170x74x23                                                                  \
]{.table}**Power Supply**\
[  Battery     3.7V Li-Ion Removable Battery                                                        \
  Amperage    1800mAh PSP-1xxx                                                                     \
              1200mAh PSP-200x, PSP-300x                                                           \
              2200mAh Endurancy Battery                                                            \
  External    5V DC, 2000mA                                                                        \
  Life-time   Approx. 6 hours                                                                      \
]{.table}

   \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\
             IrDA           USB       UMD Open\
     \_\_\_\_\_\_\_\_,,,,\_\_\_\_\_\_\_\_\_\_\_,,\_\_\_\_\_\_\_\_\_\_,,,\_\_\_\_\_\_\_\_\_\
    /\_\_\_/    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_    \\\_\_\_\\ \
   / L      \|                               \|     R  \\\
  \|   \_\_    \|                               \|   (/\\)  \|\
  \| \_\|  \|\_  \|        4.3\" TFT SCREEN        \|         \|\
  \|\|  \\/  \| \|           480x272px           \| (\[\])( O)\|\
  \|\|\_ /\\ \_\| \|          100x56.25mm          \|         \|\
  \|  \|\_\_\|   \|                               \|   ( X)  \|\
  #WLAN     \|                               \|     LEDSo\
  #  \[AN\]   \|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\|    AC   o\
   \\\_\_\_\_\_ SPK HOME V- V+  BRI MUTE SEL STRT SPK \_==\_\_/\
         \\\_=\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_=\_/     \
   \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\
  

  --------------------------------------
  [  PSP Memory Map]{#memmap .section}
  --------------------------------------

**SC CPU Physical Memory**\
[  00010000    Scratchpad (16KB)                                                                    \
  04000000    VRAM (8MB)                                                                           \
  08000000    Main RAM (32MB, 64MB)                                                                \
  1C000000    I/O Ports                                                                            \
  1FC00000    Shared RAM (2MB) \[Contains exception vectors\]                                        \
  1FE00000    I/O Ports                                                                            \
]{.table}**ME CPU Physical Memory**\
[  00000000    Scratchpad (2MB)                                                                     \
  08000000    Main RAM (32MB, 64MB)                                                                \
  1C000000    I/O Ports                                                                            \
  1FC00000    Shared RAM (2MB) \[Contains exception vectors\]                                        \
  1FE00000    I/O Ports                                                                            \
]{.table}**Virtual Memory**\
[  00000000    KU0    Cached    User/Supervisor/Kernel                                                               \
  40000000    KU1    Uncached  User/Supervisor/Kernel                                                               \
  80000000    K0     Cached    Kernel                                                                               \
  A0000000    K1     Uncached  Kernel                                                                               \
  C0000000    K2/KS  Cached    Supervisor/Kernel                                                                    \
  E0000000    K3     Cached    Kernel                                                                               \
]{.table}\
**Data Format**\
The PSP\'s Allegrexs are wired to use little-endian memory format. Thus, when accessing 16-bit or 32-bit data in memory, the least significant byte is the first byte, and the most significant the last. This is the same as x86, Z80, and others.\
[]{.table}\

  ----------------------------------
  [  PSP I/O Map]{#iomap .section}
  ----------------------------------

**Memory Manager I/O Registers**\
[  1C000000  4    R/W  MEMPROT0       Memory protection 08000000-081FFFFF                                                  \
  1C000004  4    R/W  MEMPROT1       Memory protection 08200000-083FFFFF                                                  \
  1C000008  4    R/W  MEMPROT2       Memory protection 08400000-085FFFFF                                                  \
  1C00000C  4    R/W  MEMPROT3       Memory protection 08600000-087FFFFF                                                  \
  1C000010  4    R/W  MEMPROT4       Memory protection 08800000-089FFFFF?                                                 \
  1C000014  4    R/W  MEMPROT5       Memory protection 08A00000-08BFFFFF?                                                 \
  1C000018  4    R/W  MEMPROT6       Memory protection 08C00000-08DFFFFF?                                                 \
  1C00001C  4    R/W  MEMPROT7       Memory protection 08E00000-08FFFFFF?                                                 \
  1C000020  4    R/W  MEMPROT8       Memory protection 09000000-091FFFFF?                                                 \
  1C000024  4    R/W  MEMPROT9       Memory protection 09200000-093FFFFF?                                                 \
  1C000028  4    R/W  MEMPROT10      Memory protection 09400000-095FFFFF?                                                 \
  1C00002C  4    R/W  MEMPROT11      Memory protection 09600000-097FFFFF?                                                 \
  1C000030  4    R/W  -              Profiler control?                                                                    \
  1C000044  4    R/W  -              Unknown?                                                                             \
]{.table}**System Controller I/O Registers**\
[  1C100000  4    R/W  NMIEN          NMI enable mask                                                                      \
  1C100004  4    R/W  NMIFLAG        NMI flags                                                                            \
  1C10000C  4    R/W  NMI12          NMI12 control register?                                                              \
  1C100010  4    R/W  NMI8           NMI8 control register?                                                               \
  1C100014  4    R/W  NMI9           NMI9 control register?                                                               \
  1C100018  4    R/W  NMI7           NMI7 control register?                                                               \
  1C10001C  4    R/W  NMI6           NMI6 control register?                                                               \
  1C100020  4    R/W  NMI5           NMI5 control register?                                                               \
  1C100024  4    R/W  NMI4           NMI4 control register?                                                               \
  1C100028  4    R/W  NMI3           NMI3 control register?                                                               \
  1C10002C  4    R/W  NMI2           NMI2 control register?                                                               \
  1C100030  4    R/W  NMI1           NMI1 control register?                                                               \
  1C100034  4    R/W  NMI0           NMI0 control register?                                                               \
  1C100040  4    R/W  RAMSIZE        RAM size                                                                             \
  1C100044  4    R/W  RPCINT         SC/ME RPC interrupt                                                                  \
  1C100048  4    R/W  CPUSEMA        SC/ME semaphore                                                                      \
  1C10004C  4    R/W  RESETEN        Reset enable                                                                         \
  1C100050  4    R/W  BUSCLKEN       Bus clock enable                                                                     \
  1C100078  4    R/W  IOEN           I/O enable                                                                           \
  1C10007C  4    R/W  GPIOEN         GPIO enable                                                                          \
  1C100080  4    R/W  -              MemMan exception control?                                                            \
  1C100088  4    R/W  NMI13          NMI13 control register?                                                              \
  1C1000A0  4    R/W  NMI10          NMI10 control register?                                                              \
  1C1000A4  4    R/W  NMI11          NMI11 control register?                                                              \
  1C1000E0  4    R/W  NMI14          NMI14 control register?                                                              \
  1C1000E4  4    R/W  NMI15          NMI15 control register?                                                              \
]{.table}**Interrupt Manager I/O Registers**\
[  1C300000  4    R/W  -              Unknown?                                                                             \
  1C300004  4    R/W  INTFLG0        Interrupt Flag 0-31                                                                  \
  1C300008  4    R/W  INTMSK0        Interrupt Mask 0-31                                                                  \
  1C300010  4    R/W  -              Unknown?                                                                             \
  1C300014  4    R/W  INTFLG1        Interrupt Flag 32-63                                                                 \
  1C300018  4    R/W  INTMSK1        Interrupt Mask 32-63                                                                 \
  1C300020  4    R/W  -              Unknown?                                                                             \
  1C300024  4    R/W  INTFLG2        Interrupt Flag ?-?                                                                   \
  1C300028  4    R/W  INTMSK2        Interrupt Mask ?-?                                                                   \
]{.table}**Profiler I/O Registers**\
[  1C400000  4    R/W  PROFEN         Profiler enable                                                                      \
  1C400004  4    R/W  CNTSYSCLK      System clock cycles                                                                  \
  1C400008  4    R/W  CNTCPUCLK      CPU clock cycles                                                                     \
  1C40000C  4    R/W  CNTSTALL       Total stalled cycles                                                                 \
  1C400010  4    R/W  CNTSTALLINT    Internal stalled cycles                                                              \
  1C400014  4    R/W  CNTSTALLMEM    Memory stalled cycles                                                                \
  1C400018  4    R/W  CNTSTALLCOP    Coprocessor stalled cycles                                                           \
  1C40001C  4    R/W  CNTSTALLVFPU   VFPU stalled cycles                                                                  \
  1C400020  4    R/W  CNTSLEEP       Sleep cycles                                                                         \
  1C400024  4    R/W  CNTBUSACCESS   Bus access cycles                                                                    \
  1C400028  4    R/W  CNTUCACHELD    Uncached load count                                                                  \
  1C40002C  4    R/W  CNTUCACHEST    Uncached store count                                                                 \
  1C400030  4    R/W  CNTCACHELD     Cached load count                                                                    \
  1C400034  4    R/W  CNTCACHEST     Cached store count                                                                   \
  1C400038  4    R/W  CNTICACHEMISS  I-cache miss count                                                                   \
  1C40003C  4    R/W  CNTDCACHEMISS  D-cache miss count                                                                   \
  1C400040  4    R/W  CNTDCACHEWB    D-cache writeback count                                                              \
  1C400044  4    R/W  CNTCOP0INSN    Coprocessor 0 instruction count                                                      \
  1C400048  4    R/W  CNTFPUINSN     FPU instruction count                                                                \
  1C40004C  4    R/W  CNTVFPUINSN    VFPU instruction count                                                               \
  1C400050  4    R/W  CNTLOCALBUS    Local bus access cycles                                                              \
]{.table}**VME Control I/O Registers**\
[  1CC00010  4    R/W  VMERESET       VME reset                                                                            \
  1CC00030  4    R/W  -              Unknown?                                                                             \
  1CC00040  4    R/W  -              Unknown?                                                                             \
  1CC00070  4    R/W  -              Unknown?                                                                             \
]{.table}**NAND Flash I/O Registers**\
[  1D101000  4    R    NANDCTRL       NAND control                                                                         \
  1D101004  4    R    NANDSTATUS     NAND status                                                                          \
  1D101008  4    W    NANDCMD        NAND command                                                                         \
  1D10100C  4    W    NANDADDR       NAND address                                                                         \
  1D101014  4    W    NANDRESET      NAND reset?                                                                          \
  1D101020  4    W    NANDDMAADDR    NAND DMA address                                                                     \
  1D101024  4    R/W  NANDDMACTRL    NAND DMA control                                                                     \
  1D101028  4    R    NANDDMASTATUS  NAND DMA status                                                                      \
  1D101038  4    R/W  NANDDMAINTR    NAND DMA intr?                                                                       \
  1D101200  4    R/W  NANDRESUME     NAND resume?                                                                         \
  1D101300  4    R/W  NANDSERIAL     NAND serial data                                                                     \
  1FF00000  512  R/W  NANDDMABUF     NAND DMA data buffer                                                                 \
  1FF00800  4    R/W  NANDDMAECC     NAND DMA data ECC                                                                    \
  1FF00900  16   R/W  NANDDMASPARE   NAND DMA spare buffer                                                                \
]{.table}**GraphicsEngine I/O Registers**\
[  07F00000  4    R/W  GECTRLFIFO     GE control FIFO?                                                                     \
  07F80000  ?    R/W  GEEDRAM        GE EDRAM?                                                                            \
  1D400000  4    R/W  GERESET        GE reset                                                                             \
  1D400008  4    R    GEEDRAMSIZE    GE EDRAM size                                                                        \
  1D400100  4    R/W  GEEXEC         Execute GE display list                                                              \
  1D400108  4    R/W  GEDLISTADDR    GE display list address                                                              \
  1D500010  4    R/W  GEEDRAMRESET   GE EDRAM reset                                                                       \
]{.table}**KIRK I/O Registers**\
[  1DE00000  4    R    KIRKSIG        KIRK signature                                                                       \
  1DE00004  4    R    KIRKVER        KIRK version                                                                         \
  1DE00008  4    R/W  KIRKERR        KIRK error                                                                           \
  1DE0000C  4    R/W  KIRKPHASE      KIRK processing phase                                                                \
  1DE00010  4    R/W  KIRKCMD        KIRK command                                                                         \
  1DE00014  4    R/W  KIRKRESULT     KIRK result                                                                          \
  1DE00018  4    R/W  -              Unknown?                                                                             \
  1DE0001C  4    R/W  KIRKSTATUS     KIRK status                                                                          \
  1DE00020  4    R/W  -              Unknown?                                                                             \
  1DE00024  4    R/W  -              Unknown?                                                                             \
  1DE00028  4    R/W  KIRKPRVSTS     Previous Status                                                                      \
  1DE0002C  4    R/W  KIRKSRC        KIRK source buffer                                                                   \
  1DE00030  4    R/W  KIRKDST        KIRK destination buffer                                                              \
  1DE0004C  4    R/W  -              Unknown?                                                                             \
  1DE00050  4    R/W  -              Unknown?                                                                             \
]{.table}**LCDC I/O Registers**\
[  1E140000  4    R/W  LCDCEN         LCDC enable?                                                                         \
  1E140004  4    R/W  LCDCSYNCDIFF   LCDC sync difference                                                                 \
  1E140008  4    R/W  -              Unknown?                                                                             \
  1E140010  4    R/W  LCDCXBP        LCDC X back porch                                                                    \
  1E140014  4    R/W  LCDCXSYNC      LCDC X sync width                                                                    \
  1E140018  4    R/W  LCDCXFP        LCDC X front porch                                                                   \
  1E14001C  4    R/W  LCDCXRES       LCDC X resolution                                                                    \
  1E140020  4    R/W  LCDCYBP        LCDC Y back porch                                                                    \
  1E140024  4    R/W  LCDCYSYNC      LCDC Y sync width                                                                    \
  1E140028  4    R/W  LCDCYFP        LCDC Y front porch                                                                   \
  1E14002C  4    R/W  LCDCYRES       LCDC Y resolution                                                                    \
  1E140030  4    R    LCDCXPOS       LCDC X raster position                                                               \
  1E140034  4    R    LCDCYPOS       LCDC Y raster position                                                               \
  1E140040  4    R/W  LCDCYSHIFT     LCDC Y shift                                                                         \
  1E140044  4    R/W  LCDCXSHIFT     LCDC X shift                                                                         \
  1E140048  4    R/W  LCDCSCLXRES    LCDC scaled X resolution                                                             \
  1E14004C  4    R/W  LCDCSCLYRES    LCDC scaled Y resolution                                                             \
  1E140050  4    R/W  -              Unknown?                                                                             \
  1E140070  4    R/W  -              Unknown?                                                                             \
]{.table}**GPIO I/O Registers**\
[  1E240000  4    R/W  -              Unknown?                                                                             \
  1E240004  4    R    GPIOREAD       GPIO read                                                                            \
  1E240008  4    W    GPIOSET        GPIO set                                                                             \
  1E24000C  4    W    GPIOCLEAR      GPIO clear                                                                           \
]{.table}**UART I/O Registers**\
[  1E4x0000  4    R/W  UARTxFIFO      UART (1-4) FIFO                                                                      \
  1E4x0018  4    R/W  UARTxSTATUS    UART (1-4) status                                                                    \
  1E4x0024  4    R/W  UARTxBAUD1     UART (1-4) baudrate divisor 1                                                        \
  1E4x0028  4    R/W  UARTxBAUD2     UART (1-4) baudrate divisor 2                                                        \
  1E4x002C  4    R/W  UARTxCTRL      UART (1-4) control                                                                   \
  1E5x0000  4    R/W  UARTxFIFO      UART (5-8) FIFO                                                                      \
  1E5x0018  4    R/W  UARTxSTATUS    UART (5-8) status                                                                    \
  1E5x0024  4    R/W  UARTxBAUD1     UART (5-8) baudrate divisor 1                                                        \
  1E5x0028  4    R/W  UARTxBAUD2     UART (5-8) baudrate divisor 2                                                        \
  1E5x002C  4    R/W  UARTxCTRL      UART (5-8) control                                                                   \
]{.table}\

  --------------------------------------------------------
  [  PSP Memory Management Controller]{#memman .section}
  --------------------------------------------------------

**1C000000h - MEMPROT0 - Memory Protection 08000000h-081FFFFFh (R/W)**\
**1C000004h - MEMPROT1 - Memory Protection 08200000h-083FFFFFh (R/W)**\
**1C000008h - MEMPROT2 - Memory Protection 08400000h-085FFFFFh (R/W)**\
**1C00000Ch - MEMPROT3 - Memory Protection 08600000h-087FFFFFh (R/W)**\
**1C000010h - MEMPROT4 - Memory Protection 08800000h-089FFFFFh? (R/W)**\
**1C000014h - MEMPROT5 - Memory Protection 08A00000h-08BFFFFFh? (R/W)**\
**1C000018h - MEMPROT6 - Memory Protection 08C00000h-08DFFFFFh? (R/W)**\
**1C00001Ch - MEMPROT7 - Memory Protection 08E00000h-08FFFFFFh? (R/W)**\
**1C000020h - MEMPROT8 - Memory Protection 09000000h-091FFFFFh? (R/W)**\
**1C000024h - MEMPROT9 - Memory Protection 09200000h-093FFFFFh? (R/W)**\
**1C000028h - MEMPROT10 - Memory Protection 09400000h-095FFFFFh? (R/W)**\
**1C00002Ch - MEMPROT11 - Memory Protection 09600000h-097FFFFFh? (R/W)**\
[   Bit   Expl.\
  0     +00000000 -\> +0003FFFF User Read Enable                                         \
  1     +00000000 -\> +0003FFFF User Write Enable                                        \
  2     +00000000 -\> +0003FFFF Kernel Read Enable                                       \
  3     +00000000 -\> +0003FFFF Kernel Write Enable                                      \
  4     +00040000 -\> +0007FFFF User Read Enable                                         \
  5     +00040000 -\> +0007FFFF User Write Enable                                        \
  6     +00040000 -\> +0007FFFF Kernel Read Enable                                       \
  7     +00040000 -\> +0007FFFF Kernel Write Enable                                      \
  8     +00080000 -\> +000BFFFF User Read Enable                                         \
  9     +00080000 -\> +000BFFFF User Write Enable                                        \
  10    +00080000 -\> +000BFFFF Kernel Read Enable                                       \
  11    +00080000 -\> +000BFFFF Kernel Write Enable                                      \
  12    +000C0000 -\> +000FFFFF User Read Enable                                         \
  13    +000C0000 -\> +000FFFFF User Write Enable                                        \
  14    +000C0000 -\> +000FFFFF Kernel Read Enable                                       \
  15    +000C0000 -\> +000FFFFF Kernel Write Enable                                      \
  16    +00100000 -\> +0013FFFF User Read Enable                                         \
  17    +00100000 -\> +0013FFFF User Write Enable                                        \
  18    +00100000 -\> +0013FFFF Kernel Read Enable                                       \
  19    +00100000 -\> +0013FFFF Kernel Write Enable                                      \
  20    +00140000 -\> +0017FFFF User Read Enable                                         \
  21    +00140000 -\> +0017FFFF User Write Enable                                        \
  22    +00140000 -\> +0017FFFF Kernel Read Enable                                       \
  23    +00140000 -\> +0017FFFF Kernel Write Enable                                      \
  24    +00180000 -\> +001BFFFF User Read Enable                                         \
  25    +00180000 -\> +001BFFFF User Write Enable                                        \
  26    +00180000 -\> +001BFFFF Kernel Read Enable                                       \
  27    +00180000 -\> +001BFFFF Kernel Write Enable                                      \
  28    +001C0000 -\> +001FFFFF User Read Enable                                         \
  29    +001C0000 -\> +001FFFFF User Write Enable                                        \
  30    +001C0000 -\> +001FFFFF Kernel Read Enable                                       \
  31    +001C0000 -\> +001FFFFF Kernel Write Enable                                      \
]{.table}\
**1C000030h - Profiler control? (R/W)**\
[   Bit   Expl.\
  8     Thread profile enable?                                                          \
  9     Make profiler accessible in user mode                                           \
]{.table}\
**1C000044h - Unknown? (R/W)**\
[   Bit   Expl.\
  9     ?                                                                               \
]{.table}\
\

  ---------------------------------------------
  [  PSP System Controller]{#syscon .section}
  ---------------------------------------------

Which NMIs correspond to which events are currently unknown.\
**1C100000h - NMIEN - NMI enable mask (R/W)**\
[   Bit   Expl.\
  0-15  User NMI enable mask?                                                           \
  16-31 Kernel NMI enable mask?                                                         \
]{.table}\
**1C100004h - NMIFLAG - NMI flags (R/W)**\
[   Bit   Expl.\
  0     NMI0 flag                                                                       \
  1     NMI1 flag                                                                       \
  2     NMI2 flag                                                                       \
  3     NMI3 flag                                                                       \
  4     NMI4 flag                                                                       \
  5     NMI5 flag                                                                       \
  6     NMI6 flag                                                                       \
  7     NMI7 flag                                                                       \
  8     NMI8 flag                                                                       \
  9     NMI9 flag                                                                       \
  10    NMI10 flag                                                                      \
  11    NMI11 flag                                                                      \
  12    NMI12 flag                                                                      \
  13    NMI13 flag                                                                      \
  14    NMI14 flag                                                                      \
  15    NMI15 flag                                                                      \
]{.table}Writing 1 to any bit will acknowledge that interrupt.\
**1C10000Ch - NMI12 - NMI12 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100010h - NMI8 - NMI8 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100014h - NMI9 - NMI9 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100018h - NMI7 - NMI7 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C10001Ch - NMI6 - NMI6 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100020h - NMI5 - NMI5 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100024h - NMI4 - NMI4 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100028h - NMI3 - NMI3 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C10002Ch - NMI2 - NMI2 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100030h - NMI1 - NMI1 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100034h - NMI0 - NMI0 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C100040h - RAMSIZE - RAM size (R/W)**\
[   Bit   Expl.\
  0-1   RAM size (0=16MB, 1=32MB, 2=64MB, 3=128MB)                                      \
  11    ? (Read-only)                                                                   \
  24-31 Some hardware version? (Read-only) (0x40 on my PSP1001)                         \
]{.table}\
**1C100044h - RPCINT - SC/ME RPC interrupt (R/W)**\
[   Bit   Expl.\
  0     Post interrupt                                                                  \
]{.table}Writing 1 to bit0 posts an interrupt to the opposite CPU.\
**1C100048h - CPUSEMA - SC/ME semaphore (R/W)**\
[   Bit   Expl.\
  0-31  Semaphore                                                                       \
]{.table}Appears to be a shared lock for both CPUs. Can be used as a spinlock.\
**1C10004Ch - RESETEN - Reset enable (R/W)**\
[   Bit   Expl.\
  0     Top                                                                             \
  1     SC                                                                              \
  2     ME                                                                              \
  3     AW                                                                              \
  4     VME                                                                             \
  5     AVC                                                                             \
  6     USB                                                                             \
  7     ATA                                                                             \
  8-9   Memstick Interface                                                              \
  10    KIRK                                                                            \
  12    ATA HDD                                                                         \
  13    USB Host                                                                        \
  14-15 ? Memstick related?                                                             \
  16    ? Read only?                                                                    \
]{.table}Set a bit to assert RESET, clear to clear RESET.\
**1C100050h - BUSCLKEN - Bus clock enable (R/W)**\
[   Bit   Expl.\
  0     ME                                                                              \
  1     AW RegA Bus                                                                     \
  2     AW RegB Bus                                                                     \
  3     AW Edram Bus                                                                    \
  4     DMACPlus                                                                        \
  5-6   DMAC                                                                            \
  7     KIRK                                                                            \
  8     ATA                                                                             \
  9     USB                                                                             \
  10-11 Memstick Interface                                                              \
  12    ?                                                                               \
  13    NAND                                                                            \
  14    ?                                                                               \
  15-16 Audio                                                                           \
]{.table}Set a bit to enable clocking to the device, clear it to disable clocking.\
**1C100078h - IOEN - I/O enable (R/W)**\
[   Bit   Expl.\
  0     NAND                                                                            \
  1     USB                                                                             \
  2     ATA                                                                             \
  3-4   Memstick Interface                                                              \
  5     LCDC                                                                            \
  6-7   Audio                                                                           \
  8     IIC                                                                             \
  9     SIRCS                                                                           \
  10    Audio?                                                                          \
  11    KEY                                                                             \
  12    PWM                                                                             \
  13-18 UART                                                                            \
  19-24 SPI                                                                             \
]{.table}Unknown?\
**1C10007Ch - GPIOEN - GPIO enable (R/W)**\
[   Bit   Expl.\
  0-31  GPIO pin enables?                                                               \
]{.table}Either GPIO pin enable, or GPIO pin direction.\
**1C100080h - MemMan exception control? (R/W)**\
[   Bit   Expl.\
  0-2   Control? (7=No exception)                                                       \
]{.table}Writing 7 makes MemMan access violations not raise exceptions?\
**1C100088h - NMI13 - NMI13 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C1000A0h - NMI10 - NMI10 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C1000A4h - NMI11 - NMI11 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C1000E0h - NMI14 - NMI14 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1C1000E4h - NMI15 - NMI15 control register? (R/W?)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
\

  -----------------------------------------------------------
  [  PSP Interrupt Management Controller]{#intman .section}
  -----------------------------------------------------------

**1C300000h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}Very unknown.\
**1C300004h - INTFLG0 - Interrupt Flag 0-31 (R/W)**\
[   Bit   Expl.\
  0-31  Flags                                                                           \
]{.table}Flags for the first 32 interrupts. See below for which interrupt is which.\
**1C300008h - INTMSK0 - Interrupt Mask 0-31 (R/W)**\
[   Bit   Expl.\
  0-31  Mask                                                                            \
]{.table}Mask for the first 32 interrupts. See below for which interrupt is which.\
**1C300010h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}Very unknown.\
**1C300014h - INTFLG1 - Interrupt Flag 32-63 (R/W)**\
[   Bit   Expl.\
  0-31  Flags                                                                           \
]{.table}Flags for 32 interrupts starting with 32. See below for which interrupt is which.\
**1C300018h - INTMSK1 - Interrupt Mask 32-63 (R/W)**\
[   Bit   Expl.\
  0-31  Mask?                                                                           \
]{.table}Mask for 32 interrupts starting with 32. See below for which interrupt is which.\
**1C300020h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}Very unknown.\
**1C300024h - INTFLG2 - Interrupt Flag ?-? (R/W)**\
[   Bit   Expl.\
  0-3   Flags                                                                           \
]{.table}Flags for interrupts 38-39, and 46-47 ?\
**1C300028h - INTMSK2 - Interrupt Mask ?-? (R/W)**\
[   Bit   Expl.\
  0-3   Mask                                                                            \
]{.table}Mask for interrupts 38-39, and 46-47 ?\
**Interrupt List**\
[  0   UART_ALL       All UARTs           \
  1   SPI_ALL        All SPIs            \
  2   TIM_PERI_ALL   All timer expirations\
  3   USB_ALL        All USBs            \
  4   GPIO           GPIO                \
  5   ATA            ATA/ATAPI           \
  6   SPOCK          UMD Manager         \
  7   SMS1           Memstick (MSCM0)    \
  8   SMS2           WLAN                \
  9   MG                                 \
  10  AUDIO1                             \
  11  AUDIO2                             \
  12  IIC            I2C                 \
  13  KEY                                \
  14  SIRCS          IrDA                \
  15  TIM0_SYS       Systimer 0          \
  16  TIM1_SYS       Systimer 1          \
  17  TIM2_SYS       Systimer 2          \
  18  TIM3_SYS       Systimer 3          \
  19  COUNT          Thread0?            \
  20  EMC_SM         NAND                \
  21  DMAC128        DMAC+               \
  22  DMAC_SC1       DMA0                \
  23  DMAC_SC2       DMA1                \
  24  KIRK           MEMLMD?             \
  25  AW             GE                  \
  26  USB_MAIN                           \
  30  VSYNC          Display VSync       \
  31  SYS_REG        MediaEngine         \
  32  UART1                              \
  33  UART2                              \
  34  UART3                              \
  35  UART4                              \
  36  UART5          HP Remote           \
  37  UART6                              \
  40  SPI1                               \
  41  SPI2                               \
  42  SPI3                               \
  43  SPI4                               \
  44  SPI5                               \
  45  SPI6                               \
  48  TIM1_PERI                          \
  49  TIM2_PERI                          \
  50  TIM3_PERI                          \
  51  TIM4_PERI                          \
  56  USB_TS         USB Resume          \
  57  USBREADY_TS    USB Ready           \
  58  USBCON_TS      USB Connect         \
  59  USBDIS_TS      USB Disconnect      \
  60  SMS1_CON       Memstick Insert (MSCM1)\
  61  SMS1_DISCON    Memstick Insert (MSCM1)\
  62  SMS2_CON       WLAN                \
  63  SMS2_DISCON    WLAN                \
  64  SOFT1                              \
  65  SOFT2                              \
  66  CPUTIMER                           \
]{.table}\

  ----------------------------------
  [  PSP Profiler]{#prof .section}
  ----------------------------------

**1C400000h - PROFEN - Profiler enable (R/W)**\
[   Bit   Expl.\
  0     Enable                                                                          \
]{.table}\
**1C400004h - CNTSYSCLK - System clock cycles (R/W)**\
**1C400008h - CNTCPUCLK - CPU clock cycles (R/W)**\
**1C40000Ch - CNTSTALL - Total stalled cycles (R/W)**\
**1C400010h - CNTSTALLINT - Internal stalled cycles (R/W)**\
**1C400014h - CNTSTALLMEM - Memory stalled cycles (R/W)**\
**1C400018h - CNTSTALLCOP - Coprocessor stalled cycles (R/W)**\
**1C40001Ch - CNTSTALLVFPU - VFPU stalled cycles (R/W)**\
**1C400020h - CNTSLEEP - Sleep cycles (R/W)**\
**1C400024h - CNTBUSACCESS - Bus access cycles (R/W)**\
**1C400028h - CNTUCACHELD - Uncached load count (R/W)**\
**1C40002Ch - CNTUCACHEST - Uncached store count (R/W)**\
**1C400030h - CNTCACHELD - Cached load count (R/W)**\
**1C400034h - CNTCACHEST - Cached store count (R/W)**\
**1C400038h - CNTICACHEMISS - I-cache miss count (R/W)**\
**1C40003Ch - CNTDCACHEMISS - D-cache miss count (R/W)**\
**1C400040h - CNTDCACHEWB - D-cache writeback count (R/W)**\
**1C400044h - CNTCOP0INSN - Coprocessor 0 instruction count (R/W)**\
**1C400048h - CNTFPUINSN - FPU instruction count (R/W)**\
**1C40004Ch - CNTVFPUINSN - VFPU instruction count (R/W)**\
**1C400050h - CNTLOCALBUS - Local bus access cycles (R/W)**\
[   Bit   Expl.\
  0-31  Counter                                                                         \
]{.table}These register contain counters. They can be freely read from and written to.\
**Typical Usage**\
When you want to start profiling, you should disable the profiler, reset the counter registers by writing 0 to them, then enable the profiler.\
[]{.table}\

  -----------------------------------------------------------
  [  PSP VirtualMobileEngine Controller]{#vmectrl .section}
  -----------------------------------------------------------

Can **only** be accessed from the ME CPU.\
**1CC00010h - VMERESET - VME reset (R/W)**\
[   Bit   Expl.\
  0-31  Reset strobe                                                                    \
]{.table}Writing anything here causes the VME to reset. Reads return 0xFFFFFFFF while resetting, and 0 when reset is complete.\
**1C300030h - Unknown? (R/W)**\
[   Bit   Expl.\
  3     Unknown?                                                                        \
]{.table}\
**1C300040h - Unknown? (R/W)**\
[   Bit   Expl.\
  1     Unknown?                                                                        \
]{.table}\
**1C300070h - Unknown? (R/W)**\
[   Bit   Expl.\
  0     Unknown?                                                                        \
]{.table}\
\

  ---------------------------------------------------
  [  PSP NAND Flash Controller]{#nandctrl .section}
  ---------------------------------------------------

NAND stuff explanation.\
**1D101000h - NANDCTRL - NAND control (R)**\
[   Bit   Expl.\
  16    Read ECC  (0=don\'t calculate, 1=calculate)                                      \
  17    Write ECC (0=don\'t calculate, 1=calculate)                                      \
]{.table}\
**1D101004h - NANDSTATUS - NAND status (R)**\
[   Bit   Expl.\
  0     Status           (0=busy, 1=ready)                                              \
  7     Write protection (0=unprotected, 1=write protected)                             \
]{.table}\
**1D101008h - NANDCMD - NAND command (W)**\
[   Bit   Expl.\
  0-7   Command                                                                         \
]{.table}See below for command list.\
**1D10100Ch - NANDADDR - NAND address (W)**\
[   Bit   Expl.\
  10-26 Page to access                                                                  \
]{.table}Possibly just LBA \>\> 1?\
**1D101014h - NANDRESET - NAND reset? (W)**\
[   Bit   Expl.\
  0     Reset?                                                                          \
]{.table}\
**1D101020h - NANDDMAADDR - NAND DMA address (W)**\
[   Bit   Expl.\
  10-26 Page to access during DMA                                                       \
]{.table}Possibly just LBA \>\> 1?\
**1D101024h - NANDDMACTRL - NAND DMA control (R/W)**\
[   Bit   Expl.\
  0     DMA transfer progress (0=stopped, 1=running)                                    \
  1     Transfer direction    (0=NAND-\>MEM, 1=MEM-\>NAND)                                \
  8     Page data transfer    (0=no, 1=yes)                                             \
  9     Spare data transfer   (0=no, 1=yes)                                             \
]{.table}\
**1D101028h - NANDDMASTATUS - NAND DMA status (R)**\
[   Bit   Expl.\
  0-31  Error code (see below)                                                          \
]{.table}\
**1D101038h - NANDDMAINTR - NAND DMA intr? (R/W)**\
[   Bit   Expl.\
  0-31  Intr?                                                                           \
]{.table}\
**1D101200h - NANDRESUME - NAND resume? (R/W)**\
[   Bit   Expl.\
  0-31  ? (0B040205h to resume?)                                                        \
]{.table}\
**1D101300h - NANDSERIAL - NAND serial data (R/W)**\
[   Bit   Expl.\
  0-7   Byte 0                                                                          \
  8-15  Byte 1                                                                          \
  16-23 Byte 2                                                                          \
  24-31 Byte 3                                                                          \
]{.table}\
**1FF00000h - NANDDMABUF - NAND DMA data buffer (R/W)**\
These 512 bytes contain the page data to be transferred to/from the NAND during DMA. This does not include spare nor ECC information.\
**1FF00800h - NANDDMAECC - NAND DMA data ECC (R/W)**\
[   Bit   Expl.\
  0-31  Calculated ECC for DMA data                                                     \
]{.table}\
**1FF00900h - NANDDMASPARE - NAND DMA spare buffer (R/W)**\
These 16 bytes contain the spare data to be transferred to/from the NAND during DMA. This does not include spare nor ECC information.\
**Commands**\
[  **1st Cycle**  **2nd Cycle**  **Function**            **Output**                                            \
  0x00/0x01  -          Read (1?)           ?                                                 \
  0x50       -          Read (2?)           ?                                                 \
  0x90       -          Read ID             Manufacture code, device code                     \
  0xFF       -          Reset               ?                                                 \
  0x80       0x10       Page Program        ?                                                 \
  0x00       0x8A       Copy-back Program   ?                                                 \
  0x60       0xD0       Block Erase         ?                                                 \
  0x70       -          Read Status         Status                                            \
]{.table}\
**Reading from NAND**\
A simple (albeit inefficient) way to read from the NAND is to write the page you wish to read to NANDDMAADDR, write the appropriate bits to NANDDMACTRL, then wait for NANDDMACTRL\'s bit0 to go clear. Once that is complete, you can get your data from NANDDMABUF and/or NANDDMASPARE.\
[]{.table}\
**Writing to NAND**\
A simple (albeit inefficient) way to write to the NAND is to write the page you wish to write to NANDDMAADDR, write your data to NANDDMABUF and/or NANDDMASPARE, write the appropriate bits to NANDDMACTRL, then wait for NANDDMACTRL\'s bit0 to go clear.\
[]{.table}\
\

  -----------------------------------------------
  [  PSP GraphicsEngine 3D Video]{#ge .section}
  -----------------------------------------------

**07F00000h - GECTRLFIFO - GE control FIFO? (R/W)**\
[   Bit   Expl.\
  0-5   Subcommand?                                                                     \
  6-27  Parameters                                                                      \
  28-31 Command?                                                                        \
]{.table}Writes here push a command to the FIFO. FIFO length is unknown (possibly 64 items).\
Reads here start execution of the FIFO commands?\
**07F80000h - GEEDRAM - GE EDRAM? (R/W)**\
This seems to just be RAM? Possibly faster to access from the GE? Who knows\...\
It\'s at least 8224 bytes, quite possibly 16384 bytes.\
Cannot be accessed from SC when status register \$24 bit0 is clear.(!?)\
**1D400000h - GERESET - GE reset (R/W)**\
[   Bit   Expl.\
  0-31  Reset strobe                                                                    \
]{.table}Writing anything here causes the GraphicsEngine to reset. Reads return 0xFFFFFFFF while resetting, and 0 when reset is complete.\
**1D400008h - GEEDRAMSIZE - GE EDRAM size (R/W)**\
[   Bit   Expl.\
  0-31  EDRAM size (in KB?)                                                             \
]{.table}\
**1D400100h - GEEXEC - Execute GE display list (R/W)**\
[   Bit   Expl.\
  0-31  Execute strobe                                                                  \
]{.table}Writing anything here causes the GraphicsEngine to start processing the display list. Reads return 0xFFFFFFFF while executing, and 0 when execution is complete.\
**1D400108h - GEDLISTADDR - GE display list address (R/W)**\
[   Bit   Expl.\
  0-31  Physical display list address                                                   \
]{.table}The supplied address *must* be a physical address.\
**1D500010h - GEEDRAMRESET - GE EDRAM reset (R/W)**\
[   Bit   Expl.\
  0-31  Reset strobe                                                                    \
]{.table}Writing anything here causes the GraphicsEngine\'s EDRAM controller to reset. Reads return 0xFFFFFFFF while resetting, and 0 when reset is complete.\
**Control FIFO Commands**\
[  **Command**  **Subcommand** **Function**                        **Parameters**                                        \
  0x16     0x3F       ? Takes                         ?                                                 \
]{.table}\
TODO: Split this up into separate little sections with more info.\
\

  ------------------------------------------------
  [  PSP KIRK Crypto Controller]{#kirk .section}
  ------------------------------------------------

**1DE00000h - KIRKSIG - KIRK signature (R)**\
[   Bit   Expl.\
  0-31  \'KIRK\'                                                                          \
]{.table}Is this right? My PSP1001 returns 00000001h.\
**1DE00004h - KIRKVER - KIRK version (R)**\
[   Bit   Expl.\
  0-31  \'0010\'                                                                          \
]{.table}Is this right? My PSP1001 returns 00000001h.\
**1DE00008h - KIRKERR - KIRK error (R/W)**\
[   Bit   Expl.\
  0-31  Error                                                                           \
]{.table}Set to 1 on error by the command subroutine.\
**1DE0000Ch - KIRKPHASE - KIRK processing phase (R/W)**\
[   Bit   Expl.\
  0-1   Phase                                                                           \
]{.table}Setting this register sets the KIRK\'s processing phase. This is used to start processing.\
This will clear all of the bits in KIRKSTATUS and KIRKERR(?).\
**1DE00010h - KIRKCMD - KIRK command (R/W)**\
[   Bit   Expl.\
  0-4   Command                                                                         \
]{.table}See below for command list.\
**1DE00014h - KIRKRESULT - KIRK result (R/W)**\
[   Bit   Expl.\
  0-31  Result                                                                          \
]{.table}Holds the result of the command. Used for signature checks and such?\
**1DE00018h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1DE0001Ch - KIRKSTATUS - KIRK status (R/W)**\
[   Bit   Expl.\
  0     Phase Finish                                                                    \
  1     Phase Error?                                                                    \
  4     Phase 2 Needed                                                                  \
  5     ? (Phase 1 Error maybe?)                                                        \
]{.table}This should be used for checking processing status, and will notify when the processing has finished.\
All bits are 0 while execution is still in progress.\
If the command has two phases, Phase 2 Needed will be set when Phase Finish gets set.\
Bit1 and bit5 are not well known, but it seems that bit1 is Error for Phase 1, and Success for Phase 2? Bit5 is only checked for Phase 1, and leads to the same error codepath as bit1.\
**1DE00020h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1DE00024h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1DE00028h - KIRKPRVSTS - Previous Status (R/W)**\
[   Bit   Expl.\
  0-31  Previous Status                                                                 \
]{.table}This register is set to the previous KIRKSTATUS value at the end of the command subroutine.\
**1DE0002Ch - KIRKSRC - KIRK source buffer (R/W)**\
[   Bit   Expl.\
  0-31  Physical source address                                                         \
]{.table}The supplied address *must* be a physical address.\
**1DE00030h - KIRKDST - KIRK destination buffer (R/W)**\
[   Bit   Expl.\
  0-31  Physical destination address                                                    \
]{.table}The supplied address *must* be a physical address.\
**1DE0004Ch - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1DE00050h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**Commands**\
[  **Command**  **Function**                        **Header**                                            \
  0x01     Private decrypt                 ?                                                 \
  0x02     Encrypt (type2)                 ?                                                 \
  0x03     Decrypt (type2)                 ?                                                 \
  0x04     Encrypt (type3) (IV=0)          ?                                                 \
  0x05     Encrypt (type3) (IV=Fuse)       ?                                                 \
  0x06     Encrypt (type3) (IV=User)       ?                                                 \
  0x07     Decrypt (type3) (IV=0)          ?                                                 \
  0x08     Decrypt (type3) (IV=Fuse)       ?                                                 \
  0x09     Decrypt (type3) (IV=User)       ?                                                 \
  0x0A     Private Signature Check         ?                                                 \
  0x0B     SHA-1 Hash                      ?                                                 \
  0x0C     ECDSA Key Generate              ?                                                 \
  0x0D     ECDSA Point Multiply            ?                                                 \
  0x0E     Pseudo-random Number Generator  ?                                                 \
  0x0F     PRNG Seed? Init?                ?                                                 \
  0x10     ECDSA Sign                      ?                                                 \
  0x11     ECDSA Signature Check           ?                                                 \
]{.table}\
TODO: Split this up into separate little sections with more info.\
\

  ----------------------------------------
  [  PSP LCD Controller]{#lcdc .section}
  ----------------------------------------

**1E140000h - LCDCEN - LCDC enable? (R/W)**\
[   Bit   Expl.\
  0-1   Enable?                                                                         \
]{.table}The value written here does matter\...\
**1E140004h - LCDCSYNCDIFF - LCDC sync difference (R/W)**\
[   Bit   Expl.\
  0-31  Sync difference                                                                 \
]{.table}Sync difference is calculated with this formula: (xsync / zoom) - ysync\
**1E140008h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  Unknown?                                                                        \
]{.table}4th argument to sceLcdcCheckMode/SetMode.\
**1E140010h - LCDCXBP - LCDC X back porch (R/W)**\
[   Bit   Expl.\
  0-31  Back porch                                                                      \
]{.table}Horizontal back porch for LCD timing.\
**1E140014h - LCDCXSYNC - LCDC X sync width (R/W)**\
[   Bit   Expl.\
  0-31  H-sync width                                                                    \
]{.table}H-sync width for LCD timing.\
**1E140018h - LCDCXFP - LCDC X front porch (R/W)**\
[   Bit   Expl.\
  0-31  Front porch                                                                     \
]{.table}Horizontal front porch for LCD timing.\
**1E14001Ch - LCDCXRES - LCDC X resolution (R/W)**\
[   Bit   Expl.\
  0-31  Resolution                                                                      \
]{.table}Full horizontal resolution for LCD timing.\
**1E140020h - LCDCYBP - LCDC Y back porch (R/W)**\
[   Bit   Expl.\
  0-31  Back porch                                                                      \
]{.table}Vertical back porch for LCD timing.\
**1E140024h - LCDCYSYNC - LCDC Y sync width (R/W)**\
[   Bit   Expl.\
  0-31  V-sync width                                                                    \
]{.table}V-sync width for LCD timing.\
**1E140028h - LCDCYFP - LCDC Y front porch (R/W)**\
[   Bit   Expl.\
  0-31  Front porch                                                                     \
]{.table}Vertical front porch for LCD timing.\
**1E14002Ch - LCDCYRES - LCDC Y resolution (R/W)**\
[   Bit   Expl.\
  0-31  Resolution                                                                      \
]{.table}Full vertical resolution for LCD timing.\
**1E140030h - LCDCXPOS - LCDC X raster position (R)**\
[   Bit   Expl.\
  0-31  X raster position                                                               \
]{.table}Current horizontal raster position.\
**1E140034h - LCDCYPOS - LCDC Y raster position (R)**\
[   Bit   Expl.\
  0-31  Y raster position                                                               \
]{.table}Current vertical raster position.\
**1E140040h - LCDCYSHIFT - LCDC Y shift (R/W)**\
[   Bit   Expl.\
  0-31  Y shift                                                                         \
]{.table}The shift between hardware and software coordinates.\
**1E140044h - LCDCXSHIFT - LCDC X shift (R/W)**\
[   Bit   Expl.\
  0-31  X shift                                                                         \
]{.table}The shift between hardware and software coordinates.\
**1E140048h - LCDCSCLXRES - LCDC scaled X resolution (R/W)**\
[   Bit   Expl.\
  0-31  Scaled resolution                                                               \
]{.table}\
**1E14004Ch - LCDCSCLYRES - LCDC scaled Y resolution (R/W)**\
[   Bit   Expl.\
  0-31  Scaled resolution                                                               \
]{.table}Same as physical Y resolution.\
**1E140050h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  Unknown?                                                                        \
]{.table}\
**1E140070h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  Unknown?                                                                        \
]{.table}Set to 1 on sceLcdcResume and sceLcdcInit on Tachyon \>= 0x5000000\
**Timing diagram**

   \_\_\_ \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ \_\_\_ \_\_\_\
  \|   \|              A                 \|   \|   \|\
  \|\_\_\_\|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\|\_\_\_\|\_\_\_\|\
  \|   \|                                \|   \|   \|\
  \|   \|                                \|   \|   \|\
  \|   \|                                \|   \|   \|\
  \| A \|              B                 \| C \| D \|\
  \|   \|                                \|   \|   \|\
  \|   \|                                \|   \|   \|\
  \|\_\_\_\|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\|\_\_\_\|\_\_\_\|\
  \|   \|              C                 \|   \|   \|\
  \|\_\_\_\|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\|\_\_\_\|\_\_\_\|\
  \|   \|              D                 \|   \|   \|\
  \|\_\_\_\|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\|\_\_\_\|\_\_\_\|\
  A   Back porch\
  B   Display\
  C   Front porch\
  D   Sync\
  

\

  -----------------------------------------
  [  PSP GPIO Controller]{#gpio .section}
  -----------------------------------------

Which GPIO bits are what are currently unknown.\
**1E240000h - Unknown? (R/W)**\
[   Bit   Expl.\
  0-31  ?                                                                               \
]{.table}\
**1E240004h - GPIOREAD - GPIO read (R)**\
[   Bit   Expl.\
  0-31  GPIO pin data                                                                   \
]{.table}\
**1E240008h - GPIOSET - GPIO set (W)**\
[   Bit   Expl.\
  0-31  GPIO pin data                                                                   \
]{.table}Setting a bit in this register asserts the appropriate pin. Clear bits perform no action.\
**1E24000Ch - GPIOCLEAR - GPIO clear (W)**\
[   Bit   Expl.\
  0-31  GPIO pin data                                                                   \
]{.table}Setting a bit in this register clears the appropriate pin. Clear bits perform no action.\
\

  ------------------------------------
  [  PSP UART Ports]{#uart .section}
  ------------------------------------

**1E400000h - UART1FIFO - UART 1 FIFO (R/W)**\
**1E440000h - UART2FIFO - UART 2 FIFO (R/W)**\
**1E480000h - UART3FIFO - UART 3 FIFO (R/W)**\
**1E4C0000h - UART4FIFO - UART 4 FIFO (R/W)**\
**1E500000h - UART5FIFO - UART 5 FIFO (R/W)**\
**1E540000h - UART6FIFO - UART 6 FIFO (R/W)**\
**1E580000h - UART7FIFO - UART 7 FIFO (R/W)**\
**1E5C0000h - UART8FIFO - UART 8 FIFO (R/W)**\
[   Bit   Expl.\
  0-7   Data                                                                            \
]{.table}Writing writes a byte to the Tx buffer and advances the write position.\
Reading reads a byte from the Rx buffer and advances the read position.\
The FIFO is 32(?) bytes long.\
**1E400018h - UART1STATUS - UART 1 status (R/W)**\
**1E440018h - UART2STATUS - UART 2 status (R/W)**\
**1E480018h - UART3STATUS - UART 3 status (R/W)**\
**1E4C0018h - UART4STATUS - UART 4 status (R/W)**\
**1E500018h - UART5STATUS - UART 5 status (R/W)**\
**1E540018h - UART6STATUS - UART 6 status (R/W)**\
**1E580018h - UART7STATUS - UART 7 status (R/W)**\
**1E5C0018h - UART8STATUS - UART 8 status (R/W)**\
[   Bit   Expl.\
  4     Rx buffer status (1=empty)                                                      \
  5     Tx buffer status (1=full)                                                       \
]{.table}\
**1E400024h - UART1BAUD1 - UART 1 baudrate divisor 1 (W)**\
**1E440024h - UART2BAUD1 - UART 2 baudrate divisor 1 (W)**\
**1E480024h - UART3BAUD1 - UART 3 baudrate divisor 1 (W)**\
**1E4C0024h - UART4BAUD1 - UART 4 baudrate divisor 1 (W)**\
**1E500024h - UART5BAUD1 - UART 5 baudrate divisor 1 (W)**\
**1E540024h - UART6BAUD1 - UART 6 baudrate divisor 1 (W)**\
**1E580024h - UART7BAUD1 - UART 7 baudrate divisor 1 (W)**\
**1E5C0024h - UART8BAUD1 - UART 8 baudrate divisor 1 (W)**\
[   Bit   Expl.\
  0-?   Upper bits of baudrate divisor                                                  \
]{.table}See below for more details.\
**1E400028h - UART1BAUD2 - UART 1 baudrate divisor 2 (W)**\
**1E440028h - UART2BAUD2 - UART 2 baudrate divisor 2 (W)**\
**1E480028h - UART3BAUD2 - UART 3 baudrate divisor 2 (W)**\
**1E4C0028h - UART4BAUD2 - UART 4 baudrate divisor 2 (W)**\
**1E500028h - UART5BAUD2 - UART 5 baudrate divisor 2 (W)**\
**1E540028h - UART6BAUD2 - UART 6 baudrate divisor 2 (W)**\
**1E580028h - UART7BAUD2 - UART 7 baudrate divisor 2 (W)**\
**1E5C0028h - UART8BAUD2 - UART 8 baudrate divisor 2 (W)**\
[   Bit   Expl.\
  0-5   Lower bits of baudrate divisor                                                  \
]{.table}See below for more details.\
**1E40002Ch - UART1CTRL - UART 1 control (W)**\
**1E44002Ch - UART2CTRL - UART 2 control (W)**\
**1E48002Ch - UART3CTRL - UART 3 control (W)**\
**1E4C002Ch - UART4CTRL - UART 4 control (W)**\
**1E50002Ch - UART5CTRL - UART 5 control (W)**\
**1E54002Ch - UART6CTRL - UART 6 control (W)**\
**1E58002Ch - UART7CTRL - UART 7 control (W)**\
**1E5C002Ch - UART8CTRL - UART 8 control (W)**\
[   Bit   Expl.\
  5-6   Baudrate set?                                                                   \
]{.table}Set bits 5 and 6 to set the baudrate?\
\

  ------------------------------------------
  [  About this Document]{#about .section}
  ------------------------------------------

**About**\
PSPTEK written 2012 by Alex Marshall. Programming and register information for Sony PlayStation Portable.\
**Updates**\
This document will receive updates whenever I learn something new or am given information. This could take any amount of time, so don\'t expect regular updates.\
**Homepage**\
<http://daifukkat.su/> - My homepage\
<http://dodonpachi.daifukkat.su/psptek/> - psptek\
**Feedback**\
If you find any information contained in this document to be incorrect, incomplete, and/or misleading, *please* send me an email at trap15#raidenii.net.\
**Credits**\
Huge thanks to Martin Korth for the formatting and general inspiration for this document.\
Thanks for information and fixes,\
- YAPSPD (by groepaz)\
- kirk-engine\
- artart78\
- uOFW Project\
- UPSPD\
- TheLemonMan\
General thanks to,\
- Charles MacDonald\
- #pspcommunity\
- #raidenii\
- #HACKERCHANNEL\
