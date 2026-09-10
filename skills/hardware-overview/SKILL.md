---
name: hardware-overview
description: "Mainboard, chips and WiFi hardware. Use when identifying a component or tracing a signal on the board."
---

## 3  Hardware Overview

### 3.1  Mainboard

#### 3.1.1  Revisions

**3.1.1.1 [  TA-079]{#sec3.1.1.1}  ** Flash/SDRAM: K5E5658HCM-D060 (3.0V/2.5V) ![images/TA-079-3a.jpg](TA-079-3a.jpg)**3.1.1.2 [  TA-080]{#sec3.1.1.2}  ** **3.1.1.3 [  TA-081]{#sec3.1.1.3}  ** **3.1.1.4 [  TA-082]{#sec3.1.1.4}  ** CPU Core : CXD2967GG Media Engine : CXD5026-203GG Flash/SDRAM: K5E5658ACM-D060 (1.8V/1.8V) ![images/PSP-ta082.jpg](PSP-ta082.jpg) You can identify this Motherboard by opening the UMD door and looking for the IC1003 label: ![images/TA-082-3b.jpg](TA-082-3b.jpg)**3.1.1.5 [  TA-086]{#sec3.1.1.5}  ** CPU Core : CXD2967GG Media Engine : CXD5026-203GG MCP : K5E5658ACM-D060 1.8V/1.8V ![images/TA-086small.png](TA-086small.png)

#### 3.1.2  Semiconductors

- ?
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |     SONY                                                              |
  |    A2707GL                                                            |
  |    504C28H                                                            |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Sony Part Number: A2703GL
- ?
  +:---------------------------------------------------------------------:+
  |   -------------------------                                           |
  |    National Semiconductors                                            |
  |            JM49SW                                                     |
  |            L00053B                                                    |
  |   -------------------------                                           |
  +-----------------------------------------------------------------------+

  \
  \
- ?
  +:---------------------------------------------------------------------:+
  |   --------                                                            |
  |     SN10                                                              |
  |     5257                                                              |
  |    TI 52W                                                             |
  |     Z422                                                              |
  |   --------                                                            |
  +-----------------------------------------------------------------------+

  \
  \
- ?
  +:---------------------------------------------------------------------:+
  |   --------------------------                                          |
  |    Fairchild Semiconductors                                           |
  |            MB44C001                                                   |
  |            0507 M20                                                   |
  |               E1                                                      |
  |   --------------------------                                          |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Fujitsu\
  Part Number: MB44C001
- ?
  +:---------------------------------------------------------------------:+
  |   --------------------------                                          |
  |    Freescale semiconductors                                           |
  |           SC901583EP                                                  |
  |            MXAJ0450                                                   |
  |   --------------------------                                          |
  +-----------------------------------------------------------------------+

  or
  +:---------------------------------------------------------------------:+
  |   --------------------------                                          |
  |    Freescale semiconductors                                           |
  |           SC901583EP                                                  |
  |            MXAA0445                                                   |
  |   --------------------------                                          |
  +-----------------------------------------------------------------------+

  \
  Manufacturer: Motorola Part Number: SC901583EP
- Graphics Processor Chip (MIPS CPU, 2MB embedded RAM)
  +:---------------------------------------------------------------------:+
  |   --------------------                                                |
  |      Sony Computer                                                    |
  |    Entertainment Inc.                                                 |
  |        CXD2962GG                                                      |
  |       (C)2004SCEI                                                     |
  |         509E90E                                                       |
  |          644031                                                       |
  |   --------------------                                                |
  +-----------------------------------------------------------------------+

  or
  +:---------------------------------------------------------------------:+
  |   --------------------                                                |
  |      Sony Computer                                                    |
  |    Entertainment Inc.                                                 |
  |        CXD2962GG                                                      |
  |       (C)2004SCEI                                                     |
  |         445801E                                                       |
  |          629571                                                       |
  |   --------------------                                                |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Sony Part Number: CXD2962GG
- 32MB NAND Flash + 32MB 333MHz DDR SDRAM
  +:---------------------------------------------------------------------:+
  |   -----------------                                                   |
  |      Samsung 501                                                      |
  |    K5E5658HCM-0060                                                    |
  |       BPL227AEE                                                       |
  |   -----------------                                                   |
  +-----------------------------------------------------------------------+

  or
  +:---------------------------------------------------------------------:+
  |   -----------------                                                   |
  |      Samsung 437                                                      |
  |    K5E5658HCM-D060                                                    |
  |       BPG036P2                                                        |
  |   -----------------                                                   |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Samsung Part Number: K5E5658HCM-D060000 Package: FBGA(FL), 137 balls Size: 10.5 x 13 x 1.4 mm Description: Samsung 1st generation MCP 3.0V/2.5V 32MB 8 bit Uniform Block NAND Flash + 32MB 32 bit 6ns CL3 DDR SDRAM in a 137 ball FBGA(LF) package.\
  \
  This is the pad layout on the PCB, in the PSP\'s natural orientation, with the main processor off to the left:\
  \
  ![images/pinout.png](pinout.png)\
  \
  +:--------------------------------------------------------------------------------------------------------------------:+
  |   ---------------- ------ ------------------------------------------------------------------------------------------ |
  |       **PIN**             **description**                                                                            |
  |       CK, /CK       DDR   Differential System Clock                                                                  |
  |         CKE               Clock enable                                                                               |
  |         /CS               Chip Select (active low)                                                                   |
  |         /RAS              Row Address Strobe (active low)                                                            |
  |         /CAS              Clolumn Address Strobe (active low)                                                        |
  |         /WEd              Write enable (active low)                                                                  |
  |     A0 \... A12           Address Input                                                                              |
  |     BA0 \... BA1          Bank Address Input                                                                         |
  |     DM0 \... DM3          Input Data Mask                                                                            |
  |    DQS0 \... DQS3         Data Strobe                                                                                |
  |    DQ0 \... DQ31          Data Input/Output                                                                          |
  |         Vdd               Power Supply                                                                               |
  |         Vddq              Data out Power                                                                             |
  |         Vss               Ground                                                                                     |
  |         Vssq              DQ Ground                                                                                  |
  |         /CE         NAND  Chip enable (active low)                                                                   |
  |         /RE               Read enable (active low)                                                                   |
  |         /WP               Write protection (active low)                                                              |
  |         /WEn              Write enable (active low)                                                                  |
  |         ALE               Address Latch enable                                                                       |
  |         CLE               Command Latch enable (command provided via IO0\...IO7 and latched on rising edge of /WE)   |
  |         R /B              Ready/Busy output (chip busy writing when low, can be read when high)                      |
  |     IO0 \... IO7          Data input/output                                                                          |
  |         Vcc               +3.3V Power Supply                                                                         |
  |         Vss               Ground                                                                                     |
  |          NC          \-   not connected                                                                              |
  |         DNU               do not use                                                                                 |
  |   ---------------- ------ ------------------------------------------------------------------------------------------ |
  +----------------------------------------------------------------------------------------------------------------------+

   \
   \
  Access protocol for flash chip is basically same as SAMSUNG\'s ordinal chip like K9F5608U0C but there exist difference. Block address should be specified as 3byte length. After writing 1byte command with CLE=H, you must write 4byte address with ALE=H, 3byte block number with 1byte offset within the block. Also you should better to do this sequence not so slowly, or ignored\
- Media Engine (MIPS CPU, 2MB embedded RAM)
  +:---------------------------------------------------------------------:+
  |   --------------------                                                |
  |      Sony Computer                                                    |
  |    Entertainment Inc.                                                 |
  |         CXD1876                                                       |
  |       (C)2004SCEI                                                     |
  |          -102GG                                                       |
  |         508C10E                                                       |
  |          280221                                                       |
  |   --------------------                                                |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Sony Part Number: CXD1876
- RTC, \...
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |    (C)2004                                                            |
  |     BAR14                                                             |
  |     07KF                                                              |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+
- ?
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |    (C)2004                                                            |
  |     BAR12                                                             |
  |     46KC                                                              |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+
- clock stuff
  +:---------------------------------------------------------------------:+
  |   -------                                                             |
  |    0450                                                               |
  |    27043                                                              |
  |    62592                                                              |
  |   -------                                                             |
  +-----------------------------------------------------------------------+

  or
  +:---------------------------------------------------------------------:+
  |   -------                                                             |
  |    0440                                                               |
  |    27043                                                              |
  |    62587                                                              |
  |   -------                                                             |
  +-----------------------------------------------------------------------+

  \
  converts 27 MHz into:
  - 36.83 MHz ?
  - 22.58 MHz ?
  - 27.00 MHz ?
  - 48.00 MHz USB
  - ? MHz ?
- Audio CODEC
  +:---------------------------------------------------------------------:+
  |   --------------------------                                          |
  |    Wolfson Microelectronics                                           |
  |            WM8973G                                                    |
  |            HAAGCRY                                                    |
  |   --------------------------                                          |
  +-----------------------------------------------------------------------+

  \
  \
  Manufacturer: Wolfson Microelectronics Part Number: WM8973G

#### 3.1.3  other

- UMD laser flatcable 18 of 22 used. other 4 have pins allocated on the chip (unknown function)
- Crystal oscillator 27 MHz
  +:---------------------------------------------------------------------:+
  |   -------                                                             |
  |    2700L                                                              |
  |    E52QA                                                              |
  |   -------                                                             |
  +-----------------------------------------------------------------------+
- Crystal 4 MHz
  +:---------------------------------------------------------------------:+
  |   -------------                                                       |
  |    \[M\] 4.00B                                                        |
  |   -------------                                                       |
  +-----------------------------------------------------------------------+
- Crystal 32.768 KHz
  +:---------------------------------------------------------------------:+
  |   -------                                                             |
  |    A507Y                                                              |
  |   -------                                                             |
  +-----------------------------------------------------------------------+

### 3.2  WIFI Daughterboard

The WIFI module is mounted on the underside of the SIRCS / Memory Stick daughterboard. It appears to be a complete self-contained module built on its own PC board. It is completely covered by an aluminum shield which is embossed with the MAC address and several other numerical codes, including the apparent part number: SWU-BXJ154N. It also says \"Sony Corporation, Made In China.\"

#### 3.2.1  Semiconductors

- RF Transceiver
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |    88W8010                                                            |
  |     NNB1                                                              |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+

  \
  Manufacturer: Marvell Libertas Part Number: 88W8010
- WEP and AES (802.11i ) hardware security engine. (ARM9 Processor, 802.11b(g), QoS (802.11e) )
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |    88W8380                                                            |
  |     BDK1                                                              |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+

  \
  Manufacturer: Marvell Libertas Part Number: 88W8380

### 3.3  Headphones/Remote Control

The headphone jack is a standard 3.5mm stereo, but there is also a small 6 pin connector next to it for the \"remote control\" that is included in the Value Pack. If we assume the following pin numbering (socket in the PSP as viewed from the outside): ![images/remocon.png](remocon.png)\
Then the pinout is as follows (tip/ring/sleeve refers to the three parts of the stereo jack)\

+:---------------------------------------------------------------------------------------------------------------------:+
|   --------- ---------------- ---------------------------------------------------------------------------------------- |
|    **Pin**   **Wire color**  **Function**                                                                             |
|       1          Brown       ? Shield ? (GND) - (unused by standard Remote/Headphones)                                |
|       2           Blue       Digital ground (GND)                                                                     |
|       3          Orange      TXD                                                                                      |
|       4          Green       Sense? (+2.5V, seems to be controlled by PSP) - (unused by standard Remote/Headphones)   |
|       5          Yellow      +2.5V (0V when Plug isnt inserted) \*1                                                   |
|       6           Grey       RXD                                                                                      |
|      Tip          Pink       Left audio (plus 600mv DC BIAS)                                                          |
|     Ring          Red        Right audio                                                                              |
|    Sleeve        Black       Audio ground (GND)                                                                       |
|   --------- ---------------- ---------------------------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------------+

 \
 \
\*1) If a jack is plugged in and the PSP is on standby, the 2.5V output is always active, regardless of whether the external device replies to potential PSP queries or not (see below). In other words, when the PSP is on standby, external power is applied indefinitely to any remote device. This is done so the PSP may be woken up using a PLAY command(`0x0001`) over the serial bus.\
If a jack is plugged in and the PSP is turned on, things become interesting:

- As soon as the PSP is turned on, voltage on pin 5 drops from +2.5V to 0V for about 0.5 seconds =\> this provides any external device plugged onto the remote port with a cold reset, as was previously identified
- After this reset phase, +2.5V is turned back on but it is only maintained if the remote device replies to a specific query within 5 secs.
- If no proper reply came from the external device within 5 secs, external voltage is turned off, until the PSP itself is powered off in

### 3.4  Memory Stick

![images/mstick_10p.png](mstick_10p.png)\

+:---------------------------------------------------------------------:+
|   --------- ------------ --------------------------------------       |
|    **Pin**   **Signal**  **Description**                              |
|       1         VSS                                                   |
|       2          BS      IN, Serial protocol bus state signal         |
|       3         VCC      IN                                           |
|       4         DIO      IN/OUT, Serial protocol data signal          |
|       5                  unused/reserved                              |
|       6         INS      Stick insertion/extraction detect            |
|       7                  unused/reserved                              |
|       8         SCLK     IN, Serial protocol clock signal             |
|       9         VCC                                                   |
|      10         VSS                                                   |
|   --------- ------------ --------------------------------------       |
+-----------------------------------------------------------------------+

### 3.5  Talkman Microphone

The circuit board contains three ICs and several smaller 4 or 6-terminal devices:

- A/D Converter
  +:---------------------------------------------------------------------:+
  |   ---------                                                           |
  |    WM8950G                                                            |
  |    58AD8TE                                                            |
  |   ---------                                                           |
  +-----------------------------------------------------------------------+
- USB Controller?
  +:---------------------------------------------------------------------:+
  |   --------                                                            |
  |    A01023                                                             |
  |    534104                                                             |
  |     A01                                                               |
  |   --------                                                            |
  +-----------------------------------------------------------------------+
- ?
  +:---------------------------------------------------------------------:+
  |   -----                                                               |
  |    564                                                                |
  |    5H4                                                                |
  |   -----                                                               |
  +-----------------------------------------------------------------------+
- It appears that the extra pins are power supply lines for the microphone circuit board.
- All five pins on the USB conector are used. Only four of these are defined for standard USB; the fifth should be NC.
