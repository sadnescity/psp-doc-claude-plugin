---
name: memory-map
description: "PSP address space: RAM, VRAM, scratchpad, hardware registers, kernel and user segments, cached and uncached mirrors. Use when working out what an address is, or why a pointer has 0x40000000 added to it."
---

Chapter 7: the six segment prefixes with their cached or uncached character
and the privilege each needs, the physical layout of scratchpad, video memory
and main memory, what sits where in kernel and user RAM, and a long list of
hardware register blocks given as address ranges tagged with the modules that
use them.

For patching, this is the chapter that says which window an address belongs
to. BOOT.BIN's loaded image lives in the user segment that starts at
0x08800000, so that is what an address read out of a PSP debugger normally is;
where in that window it lands is settled at load time, which is what the PRX
relocations are for (file-formats). Adding 0x40000000 to a pointer gives the
uncached alias of the same memory rather than a second buffer, and cache
explains why code does that.

Three things read oddly from the PSX. Video memory is plain CPU-addressable
RAM here, not something reachable only through GPU ports. The scratchpad is 16
kB, not a kilobyte. And every segment maps onto the same physical address, so
decoding an address means masking off the top three bits and nothing else.

Two limits. The hardware section gives blocks and their users, not bit fields;
psptek-registers has those. And the map is the 32 MB machine throughout — the
only 64 MB in YAPSPD is the DEM-100 dev kit, over in system-overview.

---

## 7  Memory Map

### 7.1  Segments

+:---------------------------------------------------------------------------------------------------------------------:+
|   --------------------- --------- ---------------------- ---------- ---------- ------------- ------------------------ |
|    **virtual address**   **msb**   **physical address**   **size**   **type**  **comment**   **mode(s)**              |
|       `0x0.......`        `000`        `0x0.......`       1024 MB      KU0     cached        user/supervisor/kernel   |
|       `0x4.......`        `010`        `0x0.......`       1024 MB      KU1     uncached      user/supervisor/kernel   |
|       `0x8.......`        `100`        `0x0.......`        512 MB       K0     cached        kernel                   |
|       `0xA.......`        `101`        `0x0.......`        512 MB       K1     uncached      kernel                   |
|       `0xC.......`        `110`        `0x0.......`        512 MB     K2/KS    cached        supervisor/kernel        |
|       `0xE.......`        `111`        `0x0.......`        512 MB       K3     cached        kernel                   |
|   --------------------- --------- ---------------------- ---------- ---------- ------------- ------------------------ |
+-----------------------------------------------------------------------------------------------------------------------+

 \
 \
note: K2 and K3 segments seem to be unused

### 7.2  physical Memory

+:-----------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ---------------------------------- |
|     **start**       **end**      **size**  **description**                    |
|    `0x00010000`   `0x00013fff`     16kb    scratchpad                         |
|    `0x04000000`   `0x041fffff`     2mb     Video Memory / Frame Buffer        |
|    `0x08000000`   `0x09ffffff`     32mb    Main Memory                        |
|    `0x1c000000`   `0x1fbfffff`             Hardware i/o                       |
|    `0x1fc00000`   `0x1fcfffff`     1mb     Hardware Exception Vectors (RAM)   |
|    `0x1fd00000`   `0x1fffffff`             Hardware i/o                       |
|   -------------- -------------- ---------- ---------------------------------- |
+-------------------------------------------------------------------------------+

### 7.3  Ram usage

+:-------------------------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ------------- ---------------------------------- |
|     **start**       **end**      **size**   **segment**  **description**                    |
|    `0x04000000`   `0x041fffff`     2mb          KU0      Video Memory / Frame Buffer        |
|                                                                                             |
|    `0x88000000`   `0x887fffff`     8mb          K0       Kernel Memory                      |
|    `0x08800000`   `0x09ffffff`     24mb         KU0      Userspace Memory                   |
|                                                                                             |
|    `0xbfc00000`   `0xbfcfffff`     1mb          K1       Hardware Exception Vectors (RAM)   |
|   -------------- -------------- ---------- ------------- ---------------------------------- |
+---------------------------------------------------------------------------------------------+

#### 7.3.1  Kernel

##### 7.3.1.1 [  K0]{#sec7.3.1.1}

+:-----------------------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ---------------------------------------------- |
|     **start**       **end**      **size**  **description**                                |
|    `0x88000000`   `0x8837ffff`    3.5mb    kernel modules are loaded here                 |
|                                                                                           |
|    `0x88380000`                            ME Resetcode                                   |
|    `0x883d6000`   `0x883fffff`     168k    seems to be unused                             |
|                                                                                           |
|    `0x88400000`   `0x887fffff`     4mb     Module/Threadmanager Memory (v1.5 FW only ?)   |
|                                                                                           |
|    `0x88C00000`                            Loadexec Stage 2                               |
|   -------------- -------------- ---------- ---------------------------------------------- |
+-------------------------------------------------------------------------------------------+

##### 7.3.1.2 [  K1]{#sec7.3.1.2}

+:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   -------------- -------------- ------------- ----------------------------------------------------------------------------------------------------------------------------------- |
|     **start**       **end**          **size** **description**                                                                                                                     |
|    `0xbfc00000`                               Reset Vector? (cop0.9:EXC31_ErrVec)                                                                                                 |
|    `0xbfc00040`   `0xbfc000ff`                ME Handler                                                                                                                          |
|    `0xbfc00160`                               (mebooter, mebooter_umdvideo)                                                                                                       |
|    `0xbfc00400`                               (sysreg)                                                                                                                            |
|    `0xbfc00600`                               ME RPC-Call struct (s1, s2, s3, s4, s5, s6, s7, fp, arg0) (me_wrapper)                                                              |
|    `0xbfc00700`                               Exception struct (flag, COP0.EPC, COP0.EPC.err, COP0.Status, COP0.Cause, COP0.BadVAddr) (mebooter, mebooter_umdvideo, me_wrapper)   |
|    `0xbfc00ffc`                               (sysreg)                                                                                                                            |
|    `0xbfc01000`   `0xbfc01fff`     16\*0x0100 Exception Vectors? (cop0.10:?)                                                                                                      |
|    `0xbfc02000`   `0xbfcfffff`    254\*0x1000 Exception Vectors? (cop0.9:EXC31_ErrVec)                                                                                            |
|   -------------- -------------- ------------- ----------------------------------------------------------------------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

#### 7.3.2  Userspace

##### 7.3.2.1 [  KU0]{#sec7.3.2.1}

+:-----------------------------------------------------------------------:+
|   -------------- --------- ---------- --------------------------------- |
|     **start**     **end**   **size**  **description**                   |
|    `0x08800000`                                                         |
|    `0x08900000`                       user main program start address   |
|   -------------- --------- ---------- --------------------------------- |
+-------------------------------------------------------------------------+

##### 7.3.2.2 [  KU1]{#sec7.3.2.2}

all Memory that can be acessed from KU0 segment, which is cached, can also be acessed from the KU1 segment, which is uncached.

### 7.4  Hardware

\
[]{#tth_tAb1}

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   -------------- --------- ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     **start**     **end**  **description**                                                                                                                                            |
|    `0xbc0000xx`            memory interface ?? (mpeg_vsh, sysmem, sysreg, threadman, usb)                                                                                             |
|    `0xbc1000xx`            System Control (IPL, dmacman, emc_ddr, memlmd, mscm, syscon, sysmem, sysreg, exceptionman, ata, mebooter, mebooter_umdvideo , me_wrapper, reboot, uart4)   |
|    `0xbc20000x`            irq?? (sysreg)                                                                                                                                             |
|    `0xbc3000xx`            irq?? (interruptman)                                                                                                                                       |
|    `0xbc400000`            Hardware Profiler (threadman, utils)                                                                                                                       |
|    `0xbc500000`            irq, Timer? (systimer)                                                                                                                                     |
|    `0xbc6000xx`            (threadman)                                                                                                                                                |
|    `0xbc8000xx`            DMA control (dmacplus)                                                                                                                                     |
|    `0xbc9000xx`            DMA control (dmacman)                                                                                                                                      |
|    `0xbca00000`            DMA control (dmacman)                                                                                                                                      |
|    `0xbcc00000`            ME Control (mebooter, mebooter_umdvideo, me_wrapper)                                                                                                       |
|    `0xbd0000xx`            systemcontrol, watchdog, sram controller ?? (emc_ddr, mpeg_vsh, usb, syscon)                                                                               |
|    `0xbd100000`            NAND Flash (ems_sm, mpeg_vsh, reboot)                                                                                                                      |
|    `0xbd1010xx`            NAND Flash (ems_sm)                                                                                                                                        |
|    `0xbd101200`            NAND Flash (ems_sm)                                                                                                                                        |
|    `0xbd101300`            NAND Flash (ems_sm)                                                                                                                                        |
|    `0xbd200000`            memstick? (mscm, mpeg_vsh)                                                                                                                                 |
|    `0xbd300000`            WLAN (wlan)                                                                                                                                                |
|    `0xbd40000x`            Graphics engine (ge)                                                                                                                                       |
|    `0xbd4001xx`            (ge)                                                                                                                                                       |
|    `0xbd400200`            (ge)                                                                                                                                                       |
|    `0xbd4003xx`            (ge)                                                                                                                                                       |
|    `0xbd400400`            (ge)                                                                                                                                                       |
|    `0xbd4008xx`            (ge)                                                                                                                                                       |
|    `0xbd400900`            (ge)                                                                                                                                                       |
|    `0xbd400acx`            (ge)                                                                                                                                                       |
|    `0xbd400b10`            (ge)                                                                                                                                                       |
|    `0xbd5000x0`            (ge)                                                                                                                                                       |
|    `0xbd6000xx`            atapi? (ata, umdman)                                                                                                                                       |
|    `0xbd70000x`            ATA (ata, umdman)                                                                                                                                          |
|    `0xbd800000`            USB regs (usb, mpeg_vsh)                                                                                                                                   |
|    `0xbd800214`            USB regs (usb, mpeg_vsh)                                                                                                                                   |
|    `0xbd8004xx`            USB regs (usb, mpeg_vsh)                                                                                                                                   |
|    `0xbde000xx`            Crypt Engine (IPL, memlmd, reboot)                                                                                                                         |
|    `0xbdf000xx`            umd stuff (umdman)                                                                                                                                         |
|    `0xbe0000xx`            audio stuff (audio, mpeg_vsh)                                                                                                                              |
|    `0xbe100000`            (mgr)                                                                                                                                                      |
|    `0xbe1400xx`            LCDC (display?) (lcdc)                                                                                                                                     |
|    `0xbe2000xx`            IIC stuff, (which component uses i2c at all -\> clock generator and the WM8750 audio codec ) (i2c)                                                         |
|    `0xbe2400xx`            general purpose IO (gpio, syscon)                                                                                                                          |
|    `0xbe300000`            power management (pwm)                                                                                                                                     |
|    `0xbe3400xx`            IRDA (sircs)                                                                                                                                               |
|    `0xbe4c00xx`            UART4 Uart4/kernel debug(?) UART (IPL, uart4, reboot)                                                                                                      |
|    `0xbe5000xx`            UART3(?) headphone remote SIO (hpremote)                                                                                                                   |
|    `0xbe5400xx`            UART2(?) IRDA ? (sircs)                                                                                                                                    |
|    `0xbe5800xx`            UART1(?) Serial EPROM(?) system control ? (syscon)                                                                                                         |
|    `0xbe7400xx`            display controler (display)                                                                                                                                |
|    `0xbf000000`            (mpeg_vsh, pspnet_inet)                                                                                                                                    |
|    `0xbfa00000`            (power)                                                                                                                                                    |
|   -------------- --------- ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

[]{#tth_tAb1}

+-----------------------------------------------------------------------------------------------------------------------------------+
|   -------------- -------------- ------------------------------------------------------------------------------------------------- |
|     **start**       **end**     **description**                                                                                   |
|    `0xbfe00000`   `0xbfffffff`  ? all accessable, but all 0 and can not be written to?                                            |
|    `0xbff00000`                 Nand DMA User Data Buf (rw), 512 bytes buffer to hold DMA data for a user page (emc_sm, reboot)   |
|    `0xbff00800`                 Nand User ECC Reg (rw), 32bit Hardware calculated ECC for a user page (emc_sm)                    |
|    `0xbff00900`                 Nand DMA Spare Data Buf start (rw), 16 bytes buffer to hold DMA data for a spare page (emc_sm)    |
|    `0xbfff0000`                 (power, pspnet, sysmem, threadman)                                                                |
|    `0xbfffffff`                 (threadman, power, sysmem)                                                                        |
|   -------------- -------------- ------------------------------------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------------------------+
