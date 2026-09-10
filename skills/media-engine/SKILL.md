---
name: media-engine
description: "The Media Engine, the second Allegrex core: its memory, how it is started and how the two CPUs talk. Use when code runs on the ME rather than the main CPU."
---

YAPSPD's chapter 5, and one of the thinnest in the book: four observations
hedged with "appears to", the Media Engine's physical and virtual memory maps
(2MB of RAM of its own, main memory shared at the address the main CPU uses),
and its COP0 register list. The COP0 control-register and COP1 sections are
headings with nothing under them.

What it settles directly is the question of which core code is running on: one
COP0 register reads 0 on the main CPU and 1 on the ME, and the reset vector in
exceptions branches on exactly that. Whether a routine could run on the ME at
all is better answered from psptek-registers, whose spec sheet is where it says
the ME has an FPU but no VFPU.

Starting the ME and handing work to it is not documented here. The registers
involved, the cross-CPU interrupt, the shared semaphore and the reset and
bus-clock enables, are in hardware-registers under system config, and exceptions
walks the ME reset handler step by step. Note also that the block YAPSPD labels
ME Control at 0xBCC00000 is what psptek-registers calls the VirtualMobileEngine
controller; both describe the same four offsets and both are nearly empty.

---

## 5  Media Engine

### 5.1  Overview

- Video RAM appears to be inaccessable, at least at the usual address. (there is something mapped at 0x04000000 ?, appears to be mmio and not ram)
- I/O seems to be accessable (unconfirmed)
- looks like the exception handler location is set by loading cop0 register 25 (usually perfcnt) with the address of your handler
- INT 31 catches the ME irq on the main core

### 5.2  Memory Map

#### 5.2.1  physical Memory

+:-----------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ---------------------------------- |
|     **start**       **end**      **size**  **description**                    |
|    `0x00000000`   `0x001fffff`     2mb     ME internal RAM                    |
|    `0x08000000`   `0x09ffffff`     32mb    Main Memory                        |
|    `0x1fc00000`   `0x1fcfffff`     1mb     Hardware Exception Vectors (RAM)   |
|   -------------- -------------- ---------- ---------------------------------- |
+-------------------------------------------------------------------------------+

#### 5.2.2  Ram Usage

+:-----------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ---------------------------------- |
|     **start**       **end**      **size**  **description**                    |
|    `0x80000000`   `0x801fffff`     2mb     ME internal RAM                    |
|    `0x88000000`   `0x89ffffff`     32mb    Main Memory                        |
|    `0xbfc00000`   `0xbfcfffff`     1mb     Hardware Exception Vectors (RAM)   |
|   -------------- -------------- ---------- ---------------------------------- |
+-------------------------------------------------------------------------------+

### 5.3  COP0

#### 5.3.1  Status registers (mfc/mtc)

0

 

 

 

1

 

 

 

2

 

 

 

3

 

 

 

4

 

 

 

5

 

 

 

6

 

 

 

7

 

 

 

8

r

badvaddr

virtual address of last error/exception

9

r/w

count

system counter

10

 

 

 

11

r/w

compare

counter comparison value

12

r/w

status

system status

13

r/w

cause

exception cause

14

r/w

EPC

exception program counter

15

r

prid

processor revision id

16

r

config

configuration

17

 

 

 

18

 

 

 

19

 

 

 

20

 

 

 

21

 

SC-code

SC-code \< \< 2

22

 

 

CPU ID (0=Main, 1=ME)

23

 

 

 

24

?

?

?

25

r/w

Ebase

virtual address of exception vector

26

 

 

 

27

 

 

 

28

r/w

TagLo

cache instruction register

29

r/w

TagHi

cache instruction register

30

r/w

ErrorEPC

error exception program counter

31

 

 

 

#### 5.3.2  Control Registers (cfc/ctc)

### 5.4  COP1 (FPU)

#### 5.4.1  Status Registers (mfc/mtc)

#### 5.4.2  Control Registers (cfc/ctc)
