*[Figure: PSP system block diagram.]*

- Main system bus, connecting:
  - Mobile DDR I/F, to the Main Memory (DDR DRAM, 32MB / 256Mbit)
  - Graphics Core, 166MHz, with VRAM (eDRAM, 2MB), which drives the TFT (480x272)
  - DMAC
  - CPU Core (MIPS R4000, 333MHz) with data and instruction caches, and the Vector FPU and FPU attached to it
  - AVC Decoder (MPEG4, labelled "H.246")
  - VME (Virtual Mobile Engine) sound core, reconfigurable DSP, 166MHz
  - Media Engine (MIPS R4000, 333MHz) with data and instruction caches
  - Sub Memory (eDRAM, 2MB)
- A dashed arrow runs from the AVC Decoder to the Media Engine.
- A peripheral bus beside the DMAC carries the RTC, Timer, Security System (AES Crypto) and the I/O lines: Communication, Sensor/Actuator, Memory Stick/USB, Keypad/Analog Joystick, Future Extension.
