---
name: system-overview
description: "PSP-1000 specification sheet: CPU and bus clocks, memory sizes, screen, model and box codes, and accessories. Use for the shape of the machine. Later models are covered in psptek-registers."
---

YAPSPD's chapter 2, a spec sheet for the PSP-1000: the two Allegrex cores and
their clock range, the memory sizes, the screen, then model codes, the box-code
table that maps a letter on the retail carton to the firmware inside, and the
accessories with their 2005 prices.

For reverse engineering the useful content is three numbers, 32MB of main
memory, a 480x272 screen and a second CPU, plus the note that the development
unit had 64MB where the retail one has 32. Addresses belong to memory-map, the
framebuffer to video, the second CPU to media-engine.

It stops at the PSP-1000 and its regional variants, so there is nothing on the
later models. psptek-registers opens with the same spec sheet redone in 2012,
which does cover them, and the two do not agree on the embedded DRAM: this
chapter says 4MB, PSPTEK says 8MB of VRAM, while memory-map gives a 2MB VRAM
window at 0x04000000 and video documents the mirrors above it. Trust memory-map
for anything you intend to address.

---

## 2  System Overview

![images/kaigai_3a.png](kaigai_3a.png)

### 2.1  Playstation Portable Main Unit

- Main CPU (System clock frequency 1\~333MHz), MIPS32R2 \'Allegrex\' core (little endian)
- Media Engine CPU (System clock frequency 1\~333MHz), MIPS32R2 core (little endian)
- Main Memory 32MB (DDR SDRAM)
- Flash Memory 32MB
- Embedded DRAM 4MB
- 4.3 inch wide 16:9 high resolution TFT LCD screen, 480 x 272 pixel, 16.77 million colors, backlight, Maximum luminance 180 / 130 / 80cd/m2 (when using battery pack), 200 / 180 / 80cd/m2 (when using AC adaptor)
- custom \'Universal Media Disc\' (UMD), 60mm optical secured ROM disc with cartridge (1.8GB)
- Stereo Sound, two builtin Speakers
- Wireless LAN (IEEE802.11b, WiFi), a maximum of 16 PSP systems can be connected wirelessly through the ad-hoc mode, Typical indoor range of approx. 30m at 11Mbps and approx. 91m at 1Mbps. Typical outdoor range of approx. 120m at 11Mbps and approx. 460m at 1Mbps.
- USB 2.0 (mini-B)
- Memory Stick PRO Duo
- IrDA
- IR Remote (SIRCS)
- Main Connectors: Memory Stick Duo Slot, DC IN 5V connector, DC OUT connector, Headset connector, USB connector
- Keys/Switches: Directional buttons (Up/Down/Right/Left) , Analog Stick, Enter keys (Triangle, Circle, Cross, Square), Left, Right buttons, START button, SELECT button, HOME button, POWER/HOLD switch x, Display button, Sound button, Volume +/- buttons, Wireless LAN switch (ON/OFF), OPEN latch (UMD)
- Power Lithium-ion Battery
- AC Adaptor
- Recommended Retail Price 19,800 yen (20,790 yen tax inclusive), 249euro
- Dimensions Approximately 170mm (W) x 23mm (H) x 74mm (D)
- Weight Approximately 280g (including battery)

#### 2.1.1  Modells/Revisions

- PSP1000 - Japan - Released December 12, 2004
- PSP1000K - Japan - Value Pack - Released December 12, 2004
- PSP1001 - US - Released March 24, 2005
- PSP1001K - US Value Pack
- PSP1002 - Australia/New Zealand - released September 1, 2005
- PSP1002K - EU Value Pack
- PSP1003 - UK - released September 1, 2005
- PSP1004 - Europe, Middle East & Africa - released September 1, 2005
- PSP1005 - Korea - Released May 10, 2005
- PSP1006 - Hong Kong/Singapore
- PSP1007 - Taiwan
- PSP1008 - Russia
- PSP1009 - China

##### 2.1.1.1 [  Box Code]{#sec2.1.1.1}

on the Box is a label looking like this:

+:---------------------------------------------------------------------:+
|   ------------                                                        |
|     PSP-1001 K                                                        |
|           120V                                                        |
|              A                                                        |
|   ------------                                                        |
+-----------------------------------------------------------------------+

the Letter in the 3rd Line indicates the Firmware that is preinstalled:

+:---------------------------------------------------------------------:+
|   ------------- -------------- -----------                            |
|   **Boxcode**   **Firmware**   **Board**                              |
|   A             1.50                                                  |
|   B             1.51                                                  |
|   C,D,E         1.52                                                  |
|   F             2.00                                                  |
|   G             2.01                                                  |
|   H             2.50                                                  |
|   I             2.60                                                  |
|   J                                                                   |
|   K                                                                   |
|   L             2.81           TA-086                                 |
|   ------------- -------------- -----------                            |
+-----------------------------------------------------------------------+

### 2.2  Game Specifications

- UMD Audio (profile name TBD), UMD Video (profile name TBD)
- Video Codec: H.264 / AVC MP Level3
- Audio Codec: ATRAC3plus, MP3
- Security (Encryption) 128bit AES
- Access control Region, Parental Control

### 2.3  Supplied accessories

- AC adaptor (PSP-100)
- Battery pack (PSP-110)

### 2.4  Separately Sold Accessories

#### 2.4.1  Memory Stick Duo (PSP-M32)

- Copyright protection technology : MagicGateTM
- Capacity: 32MB to 32GB supported
- Recommended Retail Price 2,800 yen (2,940 yen tax inclusive)
- Dimensions: Approximately 20mm (W) x 1.6mm (H) x 31mm (D)
- Weight: Approximately 2g

#### 2.4.2  AC adaptor (PSP-100)

- Specifications Rated input voltage : 100V - 240V 50/60Hz
- Rated voltage/electrical current output : 5V / 2.0A
- Recommended Retail Price 3,500 yen (3,675 yen tax inclusive)
- Dimensions: Approximately 76mm (W) x 22mm (H) x 46mm (D)
- Weight: Approximately 44g

#### 2.4.3  Battery pack (PSP-110)

- Specifications Voltage/Capacity : 3.6V/1800mAh
- Recommended Retail Price 4,800 yen (5,040 yen tax inclusive)
- Dimensions: Approximately 52mm (W) x 12.5mm (H) x 36mm (D)
- Weight: Approximately 44g

#### 2.4.4  Headphone with remote control (PSP-140(W))

- Remote Control : Play/Pause, FF, FR, Volume +/-, Hold switch
- Headphone : In-the-ear type headphone
- Recommended Retail Price 2,800 yen (2,940 yen tax inclusive)

#### 2.4.5  Soft case and hand strap (PSP-170(B))

- Recommended Retail Price 2,000 yen (2,100 yen tax inclusive)
- Soft case: Dimensions: Approximately 195mm (W) x 7.5mm (H) x 108mm (D)
- Hand strap: Dimensions: Approximately 189mm (W) x 3.3mm (H) x 9mm (D)

#### 2.4.6  USB microphone (PSP-240(X))

![images/psp240x.jpg](psp240x.jpg)

- monaural condenser microphone
- weight approximately 6 grams
- Dimensions: 50x10x10mm

#### 2.4.7  GPS receiver

![images/gps_qjpreviewth.jpg](gps_qjpreviewth.jpg)

- will feature support for GPS-enabled games such as a projected re-release or update of Hot Shot Golf, as well in Metal Gear Solid: Portable Ops.
- The GPS is set to be priced around ¥6,000, appx. \$54 USD.

#### 2.4.8  Camera

![images/psp_screen001.jpg](psp_screen001.jpg)

- add-on will support a new video and VoIP chat service, as well as photo taking.
- The camera was released in Japan in early November 2006 for around ¥5,000, appx. \$44 USD

### 2.5  Development Hardware (DEM-100)

- 64MB Main Memory instead of 32MB
