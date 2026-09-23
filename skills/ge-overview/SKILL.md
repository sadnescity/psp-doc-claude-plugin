---
name: ge-overview
description: "Graphics Engine basics: command format, the GE float encoding, pointers, and the registers that switch features on. Read this before any of the ge-* command skills."
---

Chapter 11 of YAPSPD, split into five skills; this one holds what they share:
the command word (8-bit command, 24-bit argument), the 24-bit GE float, the BASE
register that supplies the high bits of a pointer, the Enable convention, and
the complete 0x00-0xFF command table.

Start here when disassembling a display list. A menu box or a line of text comes
down to a few commands - a texture pointer, a vertex list, a PRIM kick - and the
table is the only place that names every opcode, including ones with no section
of their own later (0x13 and 0x14, the matrix selects, RNORM, FFAR). The other
four skills take a range each: ge-flow-and-vertices for list flow and geometry,
ge-lighting, ge-textures for buffers and sampling, ge-raster for the pixel stage.

The chapter covers the command stream only: a list is handed to the hardware
through the GE registers at 0x1D400000 (GEEXEC, GEDLISTADDR), in psptek-registers.

---

## 11  3D Graphics Processing

*[Figure: block diagram of the Graphics Engine.]*

- HOSTIF (host interface): an AHB slave port to the outside, raises the Interrupt line, and feeds both the Surface Engine and, directly, the SETUP stage of the Rendering Engine.
- Surface Engine: BLEND -> SUBDIV -> TANDL -> VSORT -> CLIP; CLIP's output goes to SETUP.
- Rendering Engine: SETUP -> DDA -> TXM -> PIXOP -> DRAMIF; DRAMIF <-> eDRAM (2MB).
- BUS MATRIX1: the AHB master port to the outside; connects to HOSTIF, TXM, PIXOP and BUS MATRIX2.
- BUS MATRIX2: connects DRAMIF, BUS MATRIX1 and a second external AHB slave port.

### 11.1  GE Command Format

Each command word is divided into two parts, a 8-bit command and a 24-bit argument. The command is in the upper part of the word, and the argument in the lower. The argument can be either integer of a special kind of float that the GE supports (described below).

### 11.2  GE Floats

Floats processed in the command-stream are 24 bits instead of 32 that are used by the CPU. Conversion from 32 to 24 bits is done by shifting the value down 8 bits, losing the least significant bits of the mantissa.

### 11.3  Pointers

Some pointers use a shared register when loading addresses called BASE. This register must be written BEFORE you write to the designated register. All these registers are marked with (BASE) after the summary. Other pointers only use 28 bits of information, and their top bits are referred to as the \'4 most significant bits\' in pointer, which reflects bits 24-27, not 28-31 which could perhaps be believed from common terminology.

### 11.4  Enabling Registers

Any command or bit that has \'Enable\' in the name implies that setting the first bit (or the bit itself) enables the feature, and no ON/OFF-states are documented.

### 11.5  GE Command List

\
[]{#tth_tAb1}

+---------------------------------------------------------------------------+
|   --------- ------------ ------------------------------------------------ |
|   **num**   **name**     **description**                                  |
|   `0x00`    `NOP`        No Operation                                     |
|   `0x01`    `VADDR`      Vertex List (BASE)                               |
|   `0x02`    `IADDR`      Index List (BASE)                                |
|   `0x03`                                                                  |
|   `0x04`    `PRIM `      Primitive Kick                                   |
|   `0x05`    `BEZIER`     Bezier Patch Kick                                |
|   `0x06`    `SPLINE`     Spline Surface Kick                              |
|   `0x07`    `BBOX`       Bounding Box                                     |
|   `0x08`    `JUMP`       Jump To New Address (BASE)                       |
|   `0x09 `   `BJUMP`      Conditional Jump (BASE)                          |
|   `0x0A`    `CALL`       Call Address (BASE)                              |
|   `0x0B`    `RET`        Return From Call                                 |
|   `0x0C`    `END`        Stop Execution                                   |
|   `0x0D`                                                                  |
|   `0x0E`    `SIGNAL`     Raise Signal Interrupt                           |
|   `0x0F `   `FINISH`     Complete Rendering                               |
|   `0x10 `   `BASE`       Base Address Register                            |
|   `0x11`                                                                  |
|   `0x12`    `VTYPE`      Vertex Type                                      |
|   `0x13`    `???`        Offset Address (BASE)                            |
|   `0x14`    `???`        Origin Address (BASE)                            |
|   `0x15 `   `REGION1`    Draw Region Start                                |
|   `0x16 `   `REGION2`    Draw Region End                                  |
|   `0x17`    `LTE`        Lighting Enable                                  |
|   `0x18 `   `LTE0`       Light 0 Enable                                   |
|   `0x19 `   `LTE1 `      Light 1 Enable                                   |
|   `0x1A`    `LTE2`       Light 2 Enable                                   |
|   `0x1B `   `LTE3`       Light 3 Enable                                   |
|   `0x1C `   `CPE`        Clip Plane Enable                                |
|   `0x1D`    `BCE`        Backface Culling Enable                          |
|   `0x1E `   `TME`        Texture Mapping Enable                           |
|   `0x1F `   `FGE`        Fog Enable                                       |
|   `0x20`    `DTE`        Dither Enable                                    |
|   `0x21`    `ABE`        Alpha Blend Enable                               |
|   `0x22`    `ATE`        Alpha Test Enable                                |
|   `0x23 `   `ZTE`        Depth Test Enable                                |
|   `0x24`    `STE`        Stencil Test Enable                              |
|   `0x25`    `AAE`        Anitaliasing Enable                              |
|   `0x26`    `PCE`        Patch Cull Enable                                |
|   `0x27`    `CTE`        Color Test Enable                                |
|   `0x28 `   `LOE`        Logical Operation Enable                         |
|   `0x29`                                                                  |
|   `0x2A`    `BOFS`       Bone Matrix Offset                               |
|   `0x2B `   `BONE`       Bone Matrix Upload                               |
|   `0x2C`    `MW0`        Morph Weight 0                                   |
|   `0x2D`    `MW1`        Morph Weight 1                                   |
|   `0x2E `   `MW2`        Morph Weight 2                                   |
|   `0x2F`    `MW3`        Morph Weight 3                                   |
|   `0x30 `   `MW4`        Morph Weight 4                                   |
|   `0x31 `   `MW5`        Morph Weight 5                                   |
|   `0x32`    `MW6`        Morph Weight 6                                   |
|   `0x33 `   `MW7`        Morph Weight 7                                   |
|   `0x34`                                                                  |
|   `0x35`                                                                  |
|   `0x36 `   `PSUB`       Patch Subdivision                                |
|   `0x37`    `PPRIM`      Patch Primitive                                  |
|   `0x38`    `PFACE`      Patch Front Face                                 |
|   `0x39`                                                                  |
|   `0x3A`    `WMS`        World Matrix Select                              |
|   `0x3B`    `WORLD`      World Matrix Upload                              |
|   `0x3C`    `VMS`        View Matrix Select                               |
|   `0x3D `   `VIEW`       View Matrix upload                               |
|   `0x3E `   `PMS`        Projection matrix Select                         |
|   `0x3F `   `PROJ`       Projection Matrix upload                         |
|   `0x40`    `TMS`        Texture Matrix Select                            |
|   `0x41 `   `TMATRIX`    Texture Matrix Upload                            |
|   `0x42`    `XSCALE`     Viewport Width Scale                             |
|   `0x43`    `YSCALE`     Viewport Height Scale                            |
|   `0x44 `   `ZSCALE`     Depth Scale                                      |
|   `0x45`    `XPOS`       Viewport X Position                              |
|   `0x46 `   `YPOS`       Viewport Y Position                              |
|   `0x47`    `ZPOS`       Depth Position                                   |
|   `0x48`    `USCALE`     Texture Scale U                                  |
|   `0x49`    `VSCALE`     Texture Scale V                                  |
|   `0x4A `   `UOFFSET`    Texture Offset U                                 |
|   `0x4B`    `VOFFSET`    Texture Offset V                                 |
|   `0x4C`    `OFFSETX`    Viewport offset (X)                              |
|   `0x4D `   `OFFSETY`    Viewport offset (Y)                              |
|   `0x4E`                                                                  |
|   `0x4F`                                                                  |
|   `0x50`    `SHADE`      Shade Model                                      |
|   `0x51`    `RNORM`      Reverse Face Normals Enable                      |
|   `0x52`                                                                  |
|   `0x53 `   `CMAT`       Color Material                                   |
|   `0x54 `   `EMC`        Emissive Model Color                             |
|   `0x55 `   `AMC`        Ambient Model Color                              |
|   `0x56`    `DMC`        Diffuse Model Color                              |
|   `0x57 `   `SMC`        Specular Model Color                             |
|   `0x58`    `AMA`        Ambient Model Alpha                              |
|   `0x59`                                                                  |
|   `0x5A`                                                                  |
|   `0x5B `   `SPOW`       Specular Power                                   |
|   `0x5C `   `ALC`        Ambient Light Color                              |
|   `0x5D`    `ALA`        Ambient Light Alpha                              |
|   `0x5E`    `LMODE`      Light Model                                      |
|   `0x5F`    `LT0`        Light Type 0                                     |
|   `0x60 `   `LT1`        Light Type 1                                     |
|   `0x61 `   `LT2`        Light Type 2                                     |
|   `0x62 `   `LT3`        Light Type 3                                     |
|   `0x63`    `LXP0`       Light X Position 0                               |
|   `0x64`    `LYP0`       Light Y Position 0                               |
|   `0x65`    `LZP0`       Light Z Position 0                               |
|   `0x66`    `LXP1`       Light X Position 1                               |
|   `0x67`    `LYP1`       Light Y Position 1                               |
|   `0x68`    `LZP1`       Light Z Position 1                               |
|   `0x69`    `LXP2`       Light X Position 2                               |
|   `0x6A`    `LYP2`       Light Y Position 2                               |
|   `0x6B`    `LZP2`       Light Z Position 2                               |
|   `0x6C`    `LXP3`       Light X Position 3                               |
|   `0x6D`    `LYP3`       Light Y Position 3                               |
|   `0x6E `   `LZP3`       Light Z Position 3                               |
|   `0x6F`    `LXD0`       Light X Direction 0                              |
|   `0x70 `   `LYD0`       Light Y Direction 0                              |
|   `0x71`    `LZD0`       Light Z Direction 0                              |
|   `0x72 `   `LXD1`       Light X Direction 1                              |
|   `0x73`    `LYD1`       Light Y Direction 1                              |
|   `0x74`    `LZD1`       Light Z Direction 1                              |
|   `0x75`    `LXD2`       Light X Direction 2                              |
|   `0x76 `   `LYD2`       Light Y Direction 2                              |
|   `0x77`    `LZD2`       Light Z Direction 2                              |
|   `0x78 `   `LXD3`       Light X Direction 3                              |
|   `0x79`    `LYD3`       Light Y Direction 3                              |
|   `0x7A `   `LZD3`       Light Z Direction 3                              |
|   `0x7B`    `LCA0`       Light Constant Attenuation 0                     |
|   `0x7C`    `LLA0`       Light Linear Attenuation 0                       |
|   `0x7D`    `LQA0`       Light Quadratic Attenuation 0                    |
|   `0x7E `   `LCA1`       Light Constant Attenuation 1                     |
|   `0x7F`    `LLA1`       Light Linear Attenuation 1                       |
|   `0x80 `   `LQA1`       Light Quadratic Attenuation 1                    |
|   `0x81`    `LCA2`       Light Constant Attenuation 2                     |
|   `0x82`    `LLA2`       Light Linear Attenuation 2                       |
|   `0x83 `   `LQA2`       Light Quadratic Attenuation 2                    |
|   `0x84`    `LCA3`       Light Constant Attenuation 3                     |
|   `0x85`    `LLA3`       Light Linear Attenuation 3                       |
|   `0x86`    `LQA3`       Light Quadratic Attenuation 3                    |
|   `0x87`    `???`        Spot light 0 exponent                            |
|   `0x88`    `???`        Spot light 1 exponent                            |
|   `0x89`    `???`        Spot light 2 exponent                            |
|   `0x8A`    `???`        Spot light 3 exponent                            |
|   `0x8B`    `???`        Spot light 0 cutoff                              |
|   `0x8C`    `???`        Spot light 1 cutoff                              |
|   `0x8D`    `???`        Spot light 2 cutoff                              |
|   `0x8E`    `???`        Spot light 3 cutoff                              |
|   `0x8F`    `ALC0`       Ambient Light Color 0                            |
|   `0x90 `   `DLC0`       Diffuse Light Color 0                            |
|   `0x91`    `SLC0`       Specular Light Color 0                           |
|   `0x92`    `ALC1`       Ambient Light Color 1                            |
|   `0x93 `   `DLC1`       Diffuse Light Color 1                            |
|   `0x94 `   `SLC1`       Specular Light Color 1                           |
|   `0x95`    `ALC2`       Ambient Light Color 2                            |
|   `0x96 `   `DLC2`       Diffuse Light Color 2                            |
|   `0x97`    `SLC2`       Specular Light Color 2                           |
|   `0x98`    `ALC3`       Ambient Light Color 3                            |
|   `0x99 `   `DLC3`       Diffuse Light Color 3                            |
|   `0x9A `   `SLC3`       Specular Light Color 3                           |
|   `0x9B `   `FFACE`      Front Face Culling Order                         |
|   `0x9C`    `FBP`        Frame Buffer Pointer                             |
|   `0x9D`    `FBW`        Frame Buffer Width                               |
|   `0x9E `   `ZBP`        Depth Buffer Pointer                             |
|   `0x9F`    `ZBW`        Depth Buffer Width                               |
|   `0xA0`    `TBP0`       Texture Buffer Pointer 0                         |
|   `0xA1`    `TBP1`       Texture Buffer Pointer 1                         |
|   `0xA2 `   `TBP2`       Texture Buffer Pointer 2                         |
|   `0xA3`    `TBP3`       Texture Buffer Pointer 3                         |
|   `0xA4 `   `TBP4`       Texture Buffer Pointer 4                         |
|   `0xA5 `   `TBP5`       Texture Buffer Pointer 5                         |
|   `0xA6`    `TBP6`       Texture Buffer Pointer 6                         |
|   `0xA7`    `TBP7`       Texture Buffer Pointer 7                         |
|   `0xA8`    `TBW0`       Texture Buffer Width 0                           |
|   `0xA9`    `TBW1`       Texture Buffer Width 1                           |
|   `0xAA`    `TBW2`       Texture Buffer Width 2                           |
|   `0xAB`    `TBW3`       Texture Buffer Width 3                           |
|   `0xAC`    `TBW4`       Texture Buffer Width 4                           |
|   `0xAD`    `TBW5`       Texture Buffer Width 5                           |
|   `0xAE`    `TBW6`       Texture Buffer Width 6                           |
|   `0xAF`    `TBW7`       Texture Buffer Width 7                           |
|   `0xB0`    `CBP`        CLUT Buffer Pointer                              |
|   `0xB1`    `CBPH`       CLUT Buffer Pointer H                            |
|   `0xB2 `   `TRXSBP`     Transmission Source Buffer Pointer               |
|   `0xB3`    `TRXSBW`     Transmission Source Buffer Width                 |
|   `0xB4 `   `TRXDBP`     Transmission Destination Buffer Pointer          |
|   `0xB5`    `TRXDBW`     Transmission Destination Buffer Width            |
|   `0xB6`                                                                  |
|   `0xB7`                                                                  |
|   `0xB8`    `TSIZE0`     Texture Size Level 0                             |
|   `0xB9`    `TSIZE1`     Texture Size Level 1                             |
|   `0xBA `   `TSIZE2`     Texture Size Level 2                             |
|   `0xBB `   `TSIZE3`     Texture Size Level 3                             |
|   `0xBC`    `TSIZE4`     Texture Size Level 4                             |
|   `0xBD`    `TSIZE5`     Texture Size Level 5                             |
|   `0xBE `   `TSIZE6`     Texture Size Level 6                             |
|   `0xBF`    `TSIZE7`     Texture Size Level 7                             |
|   `0xC0`    `TMAP`       Texture Projection Map Mode + Texture Map Mode   |
|   `0xC1`                 Texture Environment Map Matrix                   |
|   `0xC2`    `TMODE`      Texture Mode                                     |
|   `0xC3`    `TPSM`       Texture Pixel Storage Mode                       |
|   `0xC4`    `CLOAD`      CLUT Load                                        |
|   `0xC5 `   `CMODE`      CLUT Mode                                        |
|   `0xC6`    `TFLT`       Texture Filter                                   |
|   `0xC7 `   `TWRAP`      Texture Wrapping                                 |
|   `0xC8 `   `TBIAS`      Texture Level Bias (???)                         |
|   `0xC9`    `TFUNC`      Texture Function                                 |
|   `0xCA `   `TEC`        Texture Environment Color                        |
|   `0xCB`    `TFLUSH`     Texture Flush                                    |
|   `0xCC `   `TSYNC`      Texture Sync                                     |
|   `0xCD`    `FFAR`       Fog Far (???)                                    |
|   `0xCE `   `FDIST`      Fog Range                                        |
|   `0xCF`    `FCOL`       Fog Color                                        |
|   `0xD0`    `TSLOPE`     Texture Slope                                    |
|   `0xD1`                                                                  |
|   `0xD2`    `PSM`        Frame Buffer Pixel Storage Mode                  |
|   `0xD3`    `CLEAR`      Clear Flags                                      |
|   `0xD4`    `SCISSOR1`   Scissor Region Start                             |
|   `0xD5`    `SCISSOR2`   Scissor Region End                               |
|   `0xD6`    `NEARZ`      Near Depth Range                                 |
|   `0xD7`    `FARZ`       Far Depth Range                                  |
|   `0xD8 `   `CTST`       Color Test Function                              |
|   `0xD9`    `CREF`       Color Reference                                  |
|   `0xDA`    `CMSK`       Color Mask                                       |
|   `0xDB `   `ATST`       Alpha Test                                       |
|   `0xDC`    `STST`       Stencil Test                                     |
|   `0xDD`    `SOP`        Stencil Operations                               |
|   `0xDE`    `ZTST`       Depth Test Function                              |
|   `0xDF `   `ALPHA`      Alpha Blend                                      |
|   `0xE0`    `SFIX`       Source Fix Color                                 |
|   `0xE1`    `DFIX`       Destination Fix Color                            |
|   `0xE2`    `DTH0`       Dither Matrix Row 0                              |
|   `0xE3`    `DTH1`       Dither Matrix Row 1                              |
|   `0xE4 `   `DTH2`       Dither Matrix Row 2                              |
|   `0xE5`    `DTH3`       Dither Matrix Row 3                              |
|   `0xE6`    `LOP`        Logical Operation                                |
|   `0xE7 `   `ZMSK`       Depth Mask                                       |
|   `0xE8`    `PMSKC`      Pixel Mask Color                                 |
|   `0xE9`    `PMSKA`      Pixel Mask Alpha                                 |
|   `0xEA`    `TRXKICK`    Transmission Kick                                |
|   `0xEB`    `TRXSPOS`    Transfer Source Position                         |
|   `0xEC `   `TRXDPOS`    Transfer Destination Position                    |
|   `0xED`                                                                  |
|   `0xEE`    `TRXSIZE`    Transfer Size                                    |
|   `0xEF`                                                                  |
|   `0xF0`                                                                  |
|   `0xF1`                                                                  |
|   `0xF2`                                                                  |
|   `0xF3`                                                                  |
|   `0xF4`                                                                  |
|   `0xF5`                                                                  |
|   `0xF6`                                                                  |
|   `0xF7`                                                                  |
|   `0xF8`                                                                  |
|   `0xF9`                                                                  |
|   `0xFA`                                                                  |
|   `0xFB`                                                                  |
|   `0xFC`                                                                  |
|   `0xFD`                                                                  |
|   `0xFE`                                                                  |
|   `0xFF`                                                                  |
|   --------- ------------ ------------------------------------------------ |
+---------------------------------------------------------------------------+
