---
name: kernel
description: "PSP kernel chapter: device and filesystem names (msstor:, ms0:, umd0:, isofs:, flash0:, flash1:, host0:), the layout of kernel return codes with the table of error values, and the firmware history from 1.0 to 3.03 with the early exploits. Use when turning a negative return value into an error name, or when working out which device a path reads from. Nothing on threads, syscalls or sceKernel functions: see modules-and-patching."
---

Chapter 29, and the title oversells it. What is here is device and filesystem
names — msstor:, ms0:, umd0:, isofs:, flash0:, flash1:, host0: — the layout of a
return code, with bit 31 for error, bit 30 for critical, the facility in bits 16
to 27 and the error type in the low half, followed by a long table of kernel
error values; then a firmware history from 1.0 to 3.03 listing the files each
update changed, the early exploits (kxploit, TIFF, GTA savegame, LoadExec),
network update and the registry.

Two things in it earn their keep: turning a negative return value into a name,
and knowing which device a game reads from — umd0: and isofs: for disc data,
ms0: for saves.

Despite the chapter being called Kernel there is nothing on threads, syscalls or
the module API, and not one sceKernel function is documented in it. The General
Errors and Errnos tables are printed with their headers and no rows, VSH and
Game Sharing are empty headings, and several firmware sections have nothing
under them. For modules and how they are loaded see modules-and-patching; for
the order things start in, boot-process.

---

## 29  Kernel

### 29.1  Devices

#### 29.1.1  Block Devices

+:-------------------------------------------------------------------------------------------------------------:+
|   ------------- ------- ------- --------------- -------------- ---------------------------------------------- |
|   **Name**       **r**   **w**   **blocksize**   **seekable**  **description**                                |
|                                                                                                               |
|   msstor:         \*      \*          512                      Memory Stick (whole; mbr, partition1,\...)     |
|   msstor0:        \*      \*                                   alias for msstor:                              |
|   msstor0p0:                                                   partition 0                                    |
|   msstor0p1:                                                   partition 1                                    |
|                                                                                                               |
|   mscm:           \*      \*                          no       Memory Stick                                   |
|   mscm0:          \*      \*                                                                                  |
|   mscmhc:         \*      \*                                                                                  |
|   mscmhc0:        \*      \*                                                                                  |
|                                                                                                               |
|   umd:            \*                 2048                      UMD                                            |
|   umd1:                                                        alias for umd:                                 |
|   umd00:                                                       alias for umd:                                 |
|   umd01:                                                       alias for umd:                                 |
|                                                                                                               |
|   lflash:         \*      \*          512                      internal flash                                 |
|   lflash?:                                                     (?=any number) alias for lflash:               |
|   lflash0:0,0                                                  internal flash, logical partition 0 (flash0)   |
|   lflash0:0,1                                                  internal flash, logical partition 1 (flash1)   |
|                                                                                                               |
|   rda:            \*      \*          any             no       infrared Port                                  |
|   irda:           \*      \*          any             no       alias for rda:                                 |
|   irda?:          \*      \*          any             no       (?=any number) alias for rda:                  |
|                                                                                                               |
|   ------------- ------- ------- --------------- -------------- ---------------------------------------------- |
+---------------------------------------------------------------------------------------------------------------+

#### 29.1.2  Filesystems

+:-----------------------------------------------------------------------------------------:+
|   ------------ ------- ------- -------------- ------------------------------------------- |
|   **Name**      **r**   **w**   **seekable**  **description**                             |
|                                                                                           |
|   fatms0:        \*      \*                   Memorystick                                 |
|   ms0:           \*      \*                   alias for fatms0:                           |
|   fatms:         \*      \*                   alias for fatms0:                           |
|                                                                                           |
|   umd0:          \*                           UMD                                         |
|   isofs:         \*                           UMD                                         |
|   isofs0:        \*                           alias for isofs:                            |
|                                                                                           |
|   flash0:                                     internal flash, system file volume          |
|   flashfat:                                   alias for flash0:                           |
|   flashfat0:                                  alias for flash0:                           |
|                                                                                           |
|   flash1:                                     internal flash, configuration file volume   |
|   flashfat1:                                  alias for flash1:                           |
|                                                                                           |
|   host0:                                      devkit (SC) fileserver                      |
|   host1:                                      devkit (ME) fileserver                      |
|                                                                                           |
|   ------------ ------- ------- -------------- ------------------------------------------- |
+-------------------------------------------------------------------------------------------+

### 29.2  Return Codes

#### 29.2.1  Structure

+---------------------------------------------------------------------------+
|   -------- -------- -------- -------- -------- -------- -------- -------- |
|   `31`         `24` `23`         `16` `15`          `8` `7`           `0` |
|   `....`     `....` `....`     `....` `....`     `....` `....`     `....` |
|   -------- -------- -------- -------- -------- -------- -------- -------- |
+---------------------------------------------------------------------------+
| +:---------------------:+:---------------------:+-----------------------+ |
| | **bit(s)**            |                       | **description**       | |
| +-----------------------+-----------------------+-----------------------+ |
| | 31                    |                       |   --- -------         | |
| |                       |                       |    0  OK              | |
| |                       |                       |    1  Error           | |
| |                       |                       |   --- -------         | |
| +-----------------------+-----------------------+-----------------------+ |
| | 30                    |                       |   --- ----------      | |
| |                       |                       |    0  normal          | |
| |                       |                       |    1  critical        | |
| |                       |                       |   --- ----------      | |
| +-----------------------+-----------------------+-----------------------+ |
| | 28-29                 |                       | reserved/unused       | |
| +-----------------------+-----------------------+-----------------------+ |
| | 16-27                 |                       | facility              | |
| +-----------------------+-----------------------+-----------------------+ |
| | 0-15                  |                       | type of error         | |
| +-----------------------+-----------------------+-----------------------+ |
+---------------------------------------------------------------------------+

#### 29.2.2  Facilities

+:---------------------------------------------------------------------:+
|   -------------- -----------------                                    |
|      **code**    **description**                                      |
|    `0x00000000`  General                                              |
|    `0x00010000`  Errno                                                |
|    `0x00020000`  Kernel                                               |
|   -------------- -----------------                                    |
+-----------------------------------------------------------------------+

#### 29.2.3  General Errors

+:---------------------------------------------------------------------:+
|   ---------- -----------------                                        |
|    **code**  **description**                                          |
|   ---------- -----------------                                        |
+-----------------------------------------------------------------------+

#### 29.2.4  Errnos

+:---------------------------------------------------------------------:+
|   ---------- -----------------                                        |
|    **code**  **description**                                          |
|   ---------- -----------------                                        |
+-----------------------------------------------------------------------+

#### 29.2.5  Kernel Errors

\
[]{#tth_tAb1}

+-----------------------------------------------------------------------+
|   -------------- --------------------------------                     |
|      **code**    **description**                                      |
|    `0x80020001`  ERROR                                                |
|    `0x80020002`  NOTIMP                                               |
|    `0x80020032`  ILLEGAL_EXPCODE                                      |
|    `0x80020033`  EXPHANDLER_NOUSE                                     |
|    `0x80020034`  EXPHANDLER_USED                                      |
|    `0x80020035`  SYCALLTABLE_NOUSED                                   |
|    `0x80020036`  SYCALLTABLE_USED                                     |
|    `0x80020037`  ILLEGAL_SYSCALLTABLE                                 |
|    `0x80020038`  ILLEGAL_PRIMARY_SYSCALL_NUMBER                       |
|    `0x80020039`  PRIMARY_SYSCALL_NUMBER_INUSE                         |
|    `0x80020064`  ILLEGAL_CONTEXT                                      |
|    `0x80020065`  ILLEGAL_INTRCODE                                     |
|    `0x80020066`  CPUDI                                                |
|    `0x80020067`  FOUND_HANDLER                                        |
|    `0x80020068`  NOTFOUND_HANDLER                                     |
|    `0x80020069`  ILLEGAL_INTRLEVEL                                    |
|    `0x8002006a`  ILLEGAL_ADDRESS                                      |
|    `0x8002006b`  ILLEGAL_INTRPARAM                                    |
|    `0x8002006c`  ILLEGAL_STACK_ADDRESS                                |
|    `0x8002006d`  ALREADY_STACK_SET                                    |
|    `0x80020096`  NO_TIMER                                             |
|    `0x80020097`  ILLEGAL_TIMERID                                      |
|    `0x80020098`  ILLEGAL_SOURCE                                       |
|    `0x80020099`  ILLEGAL_PRESCALE                                     |
|    `0x8002009a`  TIMER_BUSY                                           |
|    `0x8002009b`  TIMER_NOT_SETUP                                      |
|    `0x8002009c`  TIMER_NOT_INUSE                                      |
|    `0x800200a0`  UNIT_USED                                            |
|    `0x800200a1`  UNIT_NOUSE                                           |
|    `0x800200a2`  NO_ROMDIR                                            |
|    `0x800200c8`  IDTYPE_EXIST                                         |
|    `0x800200c9`  IDTYPE_NOT_EXIST                                     |
|    `0x800200ca`  IDTYPE_NOT_EMPTY                                     |
|    `0x800200cb`  UNKNOWN_UID                                          |
|    `0x800200cc`  UNMATCH_UID_TYPE                                     |
|    `0x800200cd`  ID_NOT_EXIST                                         |
|    `0x800200ce`  NOT_FOUND_UIDFUNC                                    |
|    `0x800200cf`  UID_ALREADY_HOLDER                                   |
|    `0x800200d0`  UID_NOT_HOLDER                                       |
|    `0x800200d1`  ILLEGAL_PERM                                         |
|    `0x800200d2`  ILLEGAL_ARGUMENT                                     |
|    `0x800200d3`  ILLEGAL_ADDR                                         |
|    `0x800200d4`  OUT_OF_RANGE                                         |
|    `0x800200d5`  MEM_RANGE_OVERLAP                                    |
|    `0x800200d6`  ILLEGAL_PARTITION                                    |
|    `0x800200d7`  PARTITION_INUSE                                      |
|    `0x800200d8`  ILLEGAL_MEMBLOCKTYPE                                 |
|    `0x800200d9`  MEMBLOCK_ALLOC_FAILED                                |
|    `0x800200da`  MEMBLOCK_RESIZE_LOCKED                               |
|    `0x800200db`  MEMBLOCK_RESIZE_FAILED                               |
|    `0x800200dc`  HEAPBLOCK_ALLOC_FAILED                               |
|    `0x800200dd`  HEAP_ALLOC_FAILED                                    |
|    `0x800200de`  ILLEGAL_CHUNK_ID                                     |
|    `0x800200df`  NOCHUNK                                              |
|    `0x800200e0`  NO_FREECHUNK                                         |
|    `0x8002012c`  LINKERR                                              |
|    `0x8002012d`  ILLEGAL_OBJECT                                       |
|    `0x8002012e`  UNKNOWN_MODULE                                       |
|    `0x8002012f`  NOFILE                                               |
|    `0x80020130`  FILEERR                                              |
|    `0x80020131`  MEMINUSE                                             |
|    `0x80020132`  PARTITION_MISMATCH                                   |
|    `0x80020133`  ALREADY_STARTED                                      |
|    `0x80020134`  NOT_STARTED                                          |
|    `0x80020135`  ALREADY_STOPPED                                      |
|    `0x80020136`  CAN_NOT_STOP                                         |
|    `0x80020137`  NOT_STOPPED                                          |
|    `0x80020138`  NOT_REMOVABLE                                        |
|    `0x80020139`  EXCLUSIVE_LOAD                                       |
|    `0x8002013a`  LIBRARY_NOT_YET_LINKED                               |
|    `0x8002013b`  LIBRARY_FOUND                                        |
|    `0x8002013c`  LIBRARY_NOTFOUND                                     |
|    `0x8002013d`  ILLEGAL_LIBRARY                                      |
|    `0x8002013e`  LIBRARY_INUSE                                        |
|    `0x8002013f`  ALREADY_STOPPING                                     |
|    `0x80020140`  ILLEGAL_OFFSET                                       |
|    `0x80020141`  ILLEGAL_POSITION                                     |
|    `0x80020142`  ILLEGAL_ACCESS                                       |
|    `0x80020143`  MODULE_MGR_BUSY                                      |
|    `0x80020144`  ILLEGAL_FLAG                                         |
|    `0x80020145`  CANNOT_GET_MODULELIST                                |
|    `0x80020146`  PROHIBIT_LOADMODULE_DEVICE                           |
|    `0x80020147`  PROHIBIT_LOADEXEC_DEVICE                             |
|    `0x80020148`  UNSUPPORTED_PRX_TYPE                                 |
|    `0x80020149`  ILLEGAL_PERM_CALL                                    |
|    `0x8002014a`  CANNOT_GET_MODULE_INFORMATION                        |
|    `0x8002014b`  ILLEGAL_LOADEXEC_BUFFER                              |
|    `0x8002014c`  ILLEGAL_LOADEXEC_FILENAME                            |
|    `0x8002014d`  NO_EXIT_CALLBACK                                     |
|    `0x80020190`  NO_MEMORY                                            |
|    `0x80020191`  ILLEGAL_ATTR                                         |
|    `0x80020192`  ILLEGAL_ENTRY                                        |
|    `0x80020193`  ILLEGAL_PRIORITY                                     |
|    `0x80020194`  ILLEGAL_STACK_SIZE                                   |
|    `0x80020195`  ILLEGAL_MODE                                         |
|    `0x80020196`  ILLEGAL_MASK                                         |
|    `0x80020197`  ILLEGAL_THID                                         |
|    `0x80020198`  UNKNOWN_THID                                         |
|    `0x80020199`  UNKNOWN_SEMID                                        |
|    `0x8002019a`  UNKNOWN_EVFID                                        |
|    `0x8002019b`  UNKNOWN_MBXID                                        |
|    `0x8002019c`  UNKNOWN_VPLID                                        |
|    `0x8002019d`  UNKNOWN_FPLID                                        |
|    `0x8002019e`  UNKNOWN_MPPID                                        |
|    `0x8002019f`  UNKNOWN_ALMID                                        |
|    `0x800201a0`  UNKNOWN_TEID                                         |
|    `0x800201a1`  UNKNOWN_CBID                                         |
|    `0x800201a2`  DORMANT                                              |
|    `0x800201a3`  SUSPEND                                              |
|    `0x800201a4`  NOT_DORMANT                                          |
|    `0x800201a5`  NOT_SUSPEND                                          |
|    `0x800201a6`  NOT_WAIT                                             |
|    `0x800201a7`  CAN_NOT_WAIT                                         |
|    `0x800201a8`  WAIT_TIMEOUT                                         |
|    `0x800201a9`  WAIT_CANCEL                                          |
|    `0x800201aa`  RELEASE_WAIT                                         |
|    `0x800201ab`  NOTIFY_CALLBACK                                      |
|    `0x800201ac`  THREAD_TERMINATED                                    |
|    `0x800201ad`  SEMA_ZERO                                            |
|    `0x800201ae`  SEMA_OVF                                             |
|    `0x800201af`  EVF_COND                                             |
|    `0x800201b0`  EVF_MULTI                                            |
|    `0x800201b1`  EVF_ILPAT                                            |
|    `0x800201b2`  MBOX_NOMSG                                           |
|    `0x800201b3`  MPP_FULL                                             |
|    `0x800201b4`  MPP_EMPTY                                            |
|    `0x800201b5`  WAIT_DELETE                                          |
|    `0x800201b6`  ILLEGAL_MEMBLOCK                                     |
|    `0x800201b7`  ILLEGAL_MEMSIZE                                      |
|    `0x800201b8`  ILLEGAL_SPADADDR                                     |
|    `0x800201b9`  SPAD_INUSE                                           |
|    `0x800201ba`  SPAD_NOT_INUSE                                       |
|    `0x800201bb`  ILLEGAL_TYPE                                         |
|    `0x800201bc`  ILLEGAL_SIZE                                         |
|    `0x800201bd`  ILLEGAL_COUNT                                        |
|    `0x800201be`  UNKNOWN_VTID                                         |
|    `0x800201bf`  ILLEGAL_VTID                                         |
|    `0x800201c0`  ILLEGAL_KTLSID                                       |
|    `0x800201c1`  KTLS_FULL                                            |
|    `0x800201c2`  KTLS_BUSY                                            |
|    `0x80020258`  PM_INVALID_PRIORITY                                  |
|    `0x80020259`  PM_INVALID_DEVNAME                                   |
|    `0x8002025a`  PM_UNKNOWN_DEVNAME                                   |
|    `0x8002025b`  PM_PMINFO_REGISTERED                                 |
|    `0x8002025c`  PM_PMINFO_UNREGISTERED                               |
|    `0x8002025d`  PM_INVALID_MAJOR_STATE                               |
|    `0x8002025e`  PM_INVALID_REQUEST                                   |
|    `0x8002025f`  PM_UNKNOWN_REQUEST                                   |
|    `0x80020260`  PM_INVALID_UNIT                                      |
|    `0x80020261`  PM_CANNOT_CANCEL                                     |
|    `0x80020262`  PM_INVALID_PMINFO                                    |
|    `0x80020263`  PM_INVALID_ARGUMENT                                  |
|    `0x80020264`  PM_ALREADY_TARGET_PWRSTATE                           |
|    `0x80020265`  PM_CHANGE_PWRSTATE_FAILED                            |
|    `0x80020266`  PM_CANNOT_CHANGE_DEVPWR_STATE                        |
|    `0x80020267`  PM_NO_SUPPORT_DEVPWR_STATE                           |
|    `0x800202bc`  DMAC_REQUEST_FAILED                                  |
|    `0x800202bd`  DMAC_REQUEST_DENIED                                  |
|    `0x800202be`  DMAC_OP_QUEUED                                       |
|    `0x800202bf`  DMAC_OP_NOT_QUEUED                                   |
|    `0x800202c0`  DMAC_OP_RUNNING                                      |
|    `0x800202c1`  DMAC_OP_NOT_ASSIGNED                                 |
|    `0x800202c2`  DMAC_OP_TIMEOUT                                      |
|    `0x800202c3`  DMAC_OP_FREED                                        |
|    `0x800202c4`  DMAC_OP_USED                                         |
|    `0x800202c5`  DMAC_OP_EMPTY                                        |
|    `0x800202c6`  DMAC_OP_ABORTED                                      |
|    `0x800202c7`  DMAC_OP_ERROR                                        |
|    `0x800202c8`  DMAC_CHANNEL_RESERVED                                |
|    `0x800202c9`  DMAC_CHANNEL_EXCLUDED                                |
|    `0x800202ca`  DMAC_PRIVILEGE_ADDRESS                               |
|    `0x800202cb`  DMAC_NO_ENOUGHSPACE                                  |
|    `0x800202cc`  DMAC_CHANNEL_NOT_ASSIGNED                            |
|    `0x800202cd`  DMAC_CHILD_OPERATION                                 |
|    `0x800202ce`  DMAC_TOO_MUCH_SIZE                                   |
|    `0x800202cf`  DMAC_INVALID_ARGUMENT                                |
|    `0x80020320`  MFILE                                                |
|    `0x80020321`  NODEV                                                |
|    `0x80020322`  XDEV                                                 |
|    `0x80020323`  BADF                                                 |
|    `0x80020324`  INVAL                                                |
|    `0x80020325`  UNSUP                                                |
|    `0x80020326`  ALIAS_USED                                           |
|    `0x80020327`  CANNOT_MOUNT                                         |
|    `0x80020328`  DRIVER_DELETED                                       |
|    `0x80020329`  ASYNC_BUSY                                           |
|    `0x8002032a`  NOASYNC                                              |
|    `0x8002032b`  REGDEV                                               |
|    `0x8002032c`  NOCWD                                                |
|    `0x8002032d`  NAMETOOLONG                                          |
|    `0x800203e8`  NXIO                                                 |
|    `0x800203e9`  IO                                                   |
|    `0x800203ea`  NOMEM                                                |
|    `0x800203eb`  STDIO_NOT_OPENED                                     |
|    `0x8002044c`  CACHE_ALIGNMENT                                      |
|   -------------- --------------------------------                     |
+-----------------------------------------------------------------------+

#### 29.2.6  Network Errors

+:---------------------------------------------------------------------:+
|   ---------- -----------------                                        |
|    **code**  **description**                                          |
|   ---------- -----------------                                        |
+-----------------------------------------------------------------------+

#### 29.2.7  unspecified Errors

+:---------------------------------------------------------------------:+
|   -------------- --------------------                                 |
|      **code**    **description**                                      |
|    `0xfffffed0`  ?                                                    |
|    `0xfffffed3`  prx tag not found?                                   |
|    `0xfffffed5`  descramble error?                                    |
|   -------------- --------------------                                 |
+-----------------------------------------------------------------------+

### 29.3  Versions

#### 29.3.1  1.0

- The first batch of PSPs was shipped with this firmware in Japan.
- 1.0 will run an unsigned binary in a PBP file without worry.

#### 29.3.2  1.5

- 1.5 will refuse to run an unsigned binary in a PBP file, but will execute a bare elf file if you can provide that file after the PSP has already loaded the PBP.
- the 1.50-US and the 1.50 JP flash0 are identical

Files added/modified from 1.0:\
`flash0:/kd/ata.prx `\
`flash0:/kd/audio.prx `\
`flash0:/kd/audiocodec.prx`\
`flash0:/kd/blkdev.prx`\
`flash0:/kd/chkreg.prx `\
`flash0:/kd/clockgen.prx `\
`flash0:/kd/codec.prx `\
`flash0:/kd/ctrl.prx `\
`flash0:/kd/display.prx `\
`flash0:/kd/dmacman.prx`\
`flash0:/kd/dmacplus.prx `\
`flash0:/kd/emc_ddr.prx`\
`flash0:/kd/emc_sm.prx`\
`flash0:/kd/exceptionman.prx `\
`flash0:/kd/fatmsmod.prx `\
`flash0:/kd/ge.prx `\
`flash0:/kd/gpio.prx `\
`flash0:/kd/hpremote.prx`\
`flash0:/kd/i2c.prx `\
`flash0:/kd/idstorage.prx`\
`flash0:/kd/ifhandle.prx `\
`flash0:/kd/impose.prx `\
`flash0:/kd/init.prx`\
`flash0:/kd/interruptman.prx `\
`flash0:/kd/iofilemgr.prx`\
`flash0:/kd/isofs.prx `\
`flash0:/kd/lcdc.prx`\
`flash0:/kd/led.prx `\
`flash0:/kd/lfatfs.prx`\
`flash0:/kd/lflash_fatfmt.prx `\
`flash0:/kd/libatrac3plus.prx`\
`flash0:/kd/libhttp.prx `\
`flash0:/kd/libparse_http.prx`\
`flash0:/kd/libparse_uri.prx `\
`flash0:/kd/libupdown.prx`\
`flash0:/kd/loadcore.prx`\
`flash0:/kd/loadexec.prx`\
`flash0:/kd/me_for_vsh.prx`\
`flash0:/kd/me_wrapper.prx `\
`flash0:/kd/mebooter.prx `\
`flash0:/kd/mebooter_umdvideo.prx `\
`flash0:/kd/mediaman.prx `\
`flash0:/kd/mediasync.prx`\
`flash0:/kd/memab.prx `\
`flash0:/kd/memlmd.prx `\
`flash0:/kd/mesg_led.prx `\
`flash0:/kd/mgr.prx`\
`flash0:/kd/modulemgr.prx `\
`flash0:/kd/mpeg_vsh.prx`\
`flash0:/kd/mpegbase.prx `\
`flash0:/kd/msaudio.prx`\
`flash0:/kd/mscm.prx `\
`flash0:/kd/msstor.prx `\
`flash0:/kd/openpsid.prx`\
`flash0:/kd/peq.prx `\
`flash0:/kd/power.prx `\
`flash0:/kd/pspbtcnf.txt `\
`flash0:/kd/pspbtcnf_game.txt`\
`flash0:/kd/pspbtcnf_updater.txt `\
`flash0:/kd/pspcnf_tbl.txt `\
`flash0:/kd/pspnet.prx`\
`flash0:/kd/pspnet_adhoc.prx`\
`flash0:/kd/pspnet_adhoc_auth.prx `\
`flash0:/kd/pspnet_adhoc_download.prx `\
`flash0:/kd/pspnet_adhoc_matching.prx `\
`flash0:/kd/pspnet_adhocctl.prx `\
`flash0:/kd/pspnet_ap_dialog_dummy.prx`\
`flash0:/kd/pspnet_apctl.prx `\
`flash0:/kd/pspnet_inet.prx `\
`flash0:/kd/pspnet_resolver.prx `\
`flash0:/kd/pwm.prx `\
`flash0:/kd/reboot.prx`\
`flash0:/kd/registry.prx`\
`flash0:/kd/rtc.prx `\
`flash0:/kd/semawm.prx`\
`flash0:/kd/sircs.prx `\
`flash0:/kd/stdio.prx `\
`flash0:/kd/sysclib.prx `\
`flash0:/kd/syscon.prx `\
`flash0:/kd/sysmem.prx `\
`flash0:/kd/sysmem_uart4.prx (removed, only in 1.00-JP)`\
`flash0:/kd/sysreg.prx `\
`flash0:/kd/systimer.prx `\
`flash0:/kd/threadman.prx `\
`flash0:/kd/uart4.prx `\
`flash0:/kd/umd9660.prx`\
`flash0:/kd/umdman.prx `\
`flash0:/kd/usb.prx `\
`flash0:/kd/usbstor.prx `\
`flash0:/kd/usbstorboot.prx `\
`flash0:/kd/usbstormgr.prx `\
`flash0:/kd/usbstorms.prx `\
`flash0:/kd/usersystemlib.prx `\
`flash0:/kd/utility.prx `\
`flash0:/kd/utils.prx `\
`flash0:/kd/vaudio.prx`\
`flash0:/kd/vaudio_game.prx `\
`flash0:/kd/videocodec.prx `\
`flash0:/kd/vshbridge.prx `\
`flash0:/kd/wlan.prx `\
`flash0:/kd/resource/impose.rsc (only in 1.50-US )`\
`flash0:/vsh/etc/index.dat `\
`flash0:/vsh/etc/jis2ucs.bin `\
`flash0:/vsh/etc/jis2ucs.cbin `\
`flash0:/vsh/etc/version.txt `\
`flash0:/vsh/module/auth_plugin.prx `\
`flash0:/vsh/module/chnnlsv.prx `\
`flash0:/vsh/module/common_gui.prx `\
`flash0:/vsh/module/common_util.prx `\
`flash0:/vsh/module/dialogmain.prx `\
`flash0:/vsh/module/game_plugin.prx `\
`flash0:/vsh/module/heaparea1.prx `\
`flash0:/vsh/module/heaparea2.prx `\
`flash0:/vsh/module/impose_plugin.prx `\
`flash0:/vsh/module/msgdialog_plugin.prx`\
`flash0:/vsh/module/msvideo_plugin.prx `\
`flash0:/vsh/module/music_plugin.prx `\
`flash0:/vsh/module/netconf_plugin.prx `\
`flash0:/vsh/module/netplay_client_plugin.prx`\
`flash0:/vsh/module/netplay_server_utility.prx `\
`flash0:/vsh/module/opening_plugin.prx`\
`flash0:/vsh/module/osk_plugin.prx `\
`flash0:/vsh/module/paf.prx `\
`flash0:/vsh/module/pafmini.prx `\
`flash0:/vsh/module/photo_plugin.prx`\
`flash0:/vsh/module/savedata_auto_dialog.prx `\
`flash0:/vsh/module/savedata_plugin.prx `\
`flash0:/vsh/module/savedata_utility.prx `\
`flash0:/vsh/module/sysconf_plugin.prx `\
`flash0:/vsh/module/update_plugin.prx`\
`flash0:/vsh/module/video_plugin.prx`\
`flash0:/vsh/module/vshmain.prx `\
`flash0:/vsh/resource/auth_plugin.rco `\
`flash0:/vsh/resource/game_plugin.rco `\
`flash0:/vsh/resource/impose_plugin.rco `\
`flash0:/vsh/resource/msgdialog_plugin.rco`\
`flash0:/vsh/resource/msvideo_plugin.rco `\
`flash0:/vsh/resource/music_plugin.rco `\
`flash0:/vsh/resource/netconf_dialog.rco`\
`flash0:/vsh/resource/netplay_plugin.rco `\
`flash0:/vsh/resource/opening_plugin.rco`\
`flash0:/vsh/resource/osk_plugin.rco`\
`flash0:/vsh/resource/osk_utility.rco `\
`flash0:/vsh/resource/photo_plugin.rco `\
`flash0:/vsh/resource/savedata_plugin.rco`\
`flash0:/vsh/resource/savedata_utility.rco`\
`flash0:/vsh/resource/sysconf_plugin.rco `\
`flash0:/vsh/resource/system_plugin.rco`\
`flash0:/vsh/resource/system_plugin_bg.rco `\
`flash0:/vsh/resource/system_plugin_fg.rco `\
`flash0:/vsh/resource/topmenu_plugin.rco`\
`flash0:/vsh/resource/update_plugin.rco `\
`flash0:/vsh/resource/video_plugin.rco`\
`flash0:/vsh/resource/video_plugin_videotoolbar.rco `\

#### 29.3.3  1.51

- The ability to run unencrypted, unsigned binaries was removed in this Firmware.

#### 29.3.4  1.52

- The first batch of european PSPs was shipped with this firmware

#### 29.3.5  2.0

##### 29.3.5.1 [  new Features]{#sec29.3.5.1}

- Network
  - Internet browser was added. (Doesn\'t yet support Macromedia Flash, some webpages will not be displayed correctly)
- Video
  - Jump function was added (UMD Video and UMD Music).
  - A-B repeat function was added (UMD Video, UMD Music and Memory Stick Duo)
  - 4:3 screen mode was added (Memory Stick Duo)
  - Voice switch function was added (Memory Stick Duo)
  - MP4 AVC support was added (Memory Stick Duo)
- Music
  - SonicStage version 3.2 now supports using ATRAC3plus with the Memory Stick PRO Duo on the PSP.
  - MP4 AAC and WAV PCM support added (Memory Stick Duo)
- Photo
  - Wallpaper function was added.
  - Sending and receiving of images was added.
  - TIFF, GIF, PNG and BMP support added.
- Settings
  - Korean language was added.
  - Theme setting was added.
  - Security setting was added.
  - WPA-PSK support added.

##### 29.3.5.2 [  updated Files]{#sec29.3.5.2}

+:-------------------------------------------------------------------------:+
|   ----------------------------------------------------------------------- |
|   `flash0:/data/cert/Equifax_S_CA.cer `\                                  |
|   `flash0:/data/cert/Equifax_S_eBiz_CA-1.cer `\                           |
|   `flash0:/data/cert/GeoTrust_G_CA.cer `\                                 |
|   `flash0:/font/shadow.pgf `\                                             |
|   `flash0:/kd/cert_loader.prx `\                                          |
|   `flash0:/kd/http_storage.prx `\                                         |
|   `flash0:/kd/libdnas.prx `\                                              |
|   `flash0:/kd/libdnas_core.prx `\                                         |
|   `flash0:/kd/libssl.prx `\                                               |
|   `flash0:/kd/mcctrl.prx `\                                               |
|   `flash0:/kd/pspnet_adhoc_transfer_int.prx `\                            |
|   `flash0:/kd/resource `\                                                 |
|   `flash0:/kd/resource/big5_table.dat `\                                  |
|   `flash0:/kd/resource/cp949_table.dat `\                                 |
|   `flash0:/kd/resource/gbk_table.dat `\                                   |
|   `flash0:/vsh/etc/cp1251ucs.bin `\                                       |
|   `flash0:/vsh/etc/cp1252ucs.bin `\                                       |
|   `flash0:/vsh/etc/ucs2uhc.bin `\                                         |
|   `flash0:/vsh/etc/uhc2ucs.bin `\                                         |
|   `flash0:/vsh/module `\                                                  |
|   `flash0:/vsh/module/dnas_plugin.prx `\                                  |
|   `flash0:/vsh/module/htmlviewer_plugin.prx `\                            |
|   `flash0:/vsh/module/htmlviewer_ui.prx `\                                |
|   `flash0:/vsh/module/htmlviewer_utility.prx `\                           |
|   `flash0:/vsh/module/libfont_hv.prx `\                                   |
|   `flash0:/vsh/module/libslim.prx `\                                      |
|   `flash0:/vsh/module/libwww.prx `\                                       |
|   `flash0:/vsh/module/netconf_plugin_auto_bfl.prx `\                      |
|   `flash0:/vsh/module/netconf_plugin_auto_nec.prx `\                      |
|   `flash0:/vsh/module/netfront.prx `\                                     |
|   `flash0:/vsh/resource/dnas_plugin.rco `\                                |
|   `flash0:/vsh/resource/htmlviewer.fbm `\                                 |
|   `flash0:/vsh/resource/htmlviewer.gim `\                                 |
|   `flash0:/vsh/resource/htmlviewer.msg `\                                 |
|   `flash0:/vsh/resource/htmlviewer.res `\                                 |
|   `flash0:/vsh/resource/htmlviewer.snd `\                                 |
|   `flash0:/vsh/resource/htmlviewer_plugin.rco `\                          |
|   `flash0:/vsh/resource/netfront.rc `\                                    |
|   `flash0:/vsh/resource/netfront.skn `\                                   |
|   `flash0:/vsh/resource/netfront.uhc `\                                   |
|   `flash1:/net/http `\                                                    |
|   `ipl:/psp_ipl.bin`                                                      |
|                                                                           |
|   ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------+

**29.3.5.3 [  ]{#sec29.3.5.3}  **

#### 29.3.6  2.01

##### 29.3.6.1 [  new Features]{#sec29.3.6.1}

This was a quick release by Sony to fix the TIFF overflow exploit found in the previous version

##### 29.3.6.2 [  updated Files]{#sec29.3.6.2}

+:-------------------------------------------------------------------------:+
|   ----------------------------------------------------------------------- |
|   `paf.prx`\                                                              |
|   `index.dat`\                                                            |
|   `version.txt`                                                           |
|                                                                           |
|   ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------+

#### 29.3.7  2.5

##### 29.3.7.1 [  new Features]{#sec29.3.7.1}

- Streaming Video Support
- Unicode support in the Browser with automatic Encoding Detection
- Save your text size settings in the Browser
- Save your Browser input history (URLs)
- Videos with DRM can be played
- NTP (Network Time Protocol) support
- WPA and PSK have been added to network setting
- Korean input keyboard method

#### 29.3.8  2.6

##### 29.3.8.1 [  new Features]{#sec29.3.8.1}

- Revisions to strengthen security have been added
- \[LocationFree Player\] has been added as a feature under \[Network\]
- \[Auto-Select\] and \[Unicode (UTF-8)\] have been added as options to \[Encoding\] under \[View\] in the \[Internet Browser\] menu bar
- \[Text Size\] and \[Display Mode\] settings of the \[Internet Browser\] can now be saved
- The input history of online forms accessed through the \[Internet Browser\] can now be saved
- Copyright-protected video can now be played under \[Video\]. (This applies to video data saved on Memory Stick)
- \[Set via Internet\] has been added as an option to \[Date & Time Settings\] under \[Settings\]
- WPA-PSK (AES) has been added as a security method under \[Network Settings\]
- Korean input mode has been added to the on-screen keyboard
- \[RSS Channel\] has been added as a feature under \[Network\]
- \[Simplified Chinese (GB18030)\] and \[Traditional Chinese (Big5)\] have been added as options to \[Encoding\] under \[View\] in the \[Internet Browser\] menu bar
- \[Volume Adjustment\] has been added as a feature to \[LocationFree Player\]
- You can now download video data that supports copyright protection using the \[Internet Browser\]
- WMA has been added as a codec that can be played under \[Music\]. (This applies to music data saved on the Memory Stick)

#### 29.3.9  2.7

- GTA exploit has been patched (\"Load failed. Savegame is corrupted\" is message displayed during launch).

##### 29.3.9.1 [  new Features]{#sec29.3.9.1}

- \[Internet Browser\] now supports Macromedia Flash contents playback.
  - You need to enable the Flash contents playback in the \[System Settings\].
  - The version of the flash player is Macromedia Flash Player 6 (a part of the functions is not supported).
- The settings of the \[Internet Browser\] is added into \[Settings\] -\> \[Connection Settings\]
- The audio contents from channels in the \[RSS Channel\] section now can be saved into your memory stick.
- \[Auto\] option added to \[Rate Change\] in \[Location Free Player\].
- Added file extension to playable AAC format.
- You can simply put a JPEG file in the same folder as the music, creating the art for the playlist.
- Added \[Enable Flash Player\] in \[System Settings\].
  - To change this option, you need to connect to the Internet
- \"Simplified Chinese\" and \"Traditional Chinese\" added to \[System Settings\] -\> \[System Language\].
- Added \[RSS Channel Settings\].
- Added \[UMD Video L & R Button\] into \[Video Settings\].
- Fixed some issues when using a memory stick with more than 2GB free space.

##### 29.3.9.2 [  new modules]{#sec29.3.9.2}

`amctrl.prx `\
`avcodec.prx `\
`game_install_plugin.prx `\
`iofilemgr_dnas.prx `\
`irda.prx `\
`mm_flash.prx `\
`psheet.prx `\
`usbacc.prx `\
`usbcam.prx `\
`usbgps.prx `\
`usbgps_serial.prx `\
`usbmic.prx `\
`usbpspcm.prx `\
`video_main_plugin.prx`\

#### 29.3.10  2.71

#### 29.3.11  2.8

\[Network\]

- In \[RSS Channel\], the download function for animation contents and image contents is now supported.
- In \[Location Free Player\], it is now possible to login via wireless LAN access point.

\[Music\]

- AAC files in \".3gp\" extension can now be played.

\[Misc\]

- Supporting saving to \"MUSIC\", \"PICTURE\" and \"VIDEO\" folders in \"Memory Stick Duo\".
- Adding the next downloadable game demo to the \"Memory Stick Duo\".

#### 29.3.12  2.81

#### 29.3.13  2.82

- Ability to play Flash content in the Internet Browser (Connection to internet required for license)
- Connection Settings added under Settings in Internet Browser
- Ability to save content added in RSS to Memory Stick
- Automatic has been added under Rate in Location Free Player
- UMD Video L/R button added under Video Settings in Settings
- Ability to disable Chapter Skip feature of the L/R Buttons (UMD Video)
- New playable extension - AAC
- Simplified Chinese, Tradition Chinese added as new languages
- RSS channel Settings added in Settings
- Demos can now be downloaded from Browser and saved on Memory Stick
- Video output can now be displayed correctly when an external tuner is selected in Location Free Player
- Ability to download Video and Image content under RSS Channel
- Ability to register devices via a wireless LAN access point under Location Free Player
- Ability to play AAC files with .3gp extension under Music
- Ability to play content saved in MUSIC, PICTURE and VIDEO folders on a Memory Stick
- Added security strengthening revisions.

#### 29.3.14  3.0

- Remote Play - Remote play is a new feature in Firmware 3.00 that allows you to remotely control your PlayStation 3 from your PSP. This also includes the display of PS3 content on the PSP. \"You can display a PLAYSTATION®3 system screen on a PSP system and play content that is on the PS3 system. To use this feature, you must adjust the necessary settings on the PSP system and the PS3 system.\" Using this new mode of playback, one can control the Photo, Music, Video, and Internet Browser features of the PlayStation 3 from a remote location via their Playstation Portable.
- Video Compatibility - In this updated version of the Playstation Portable firmware, you are also able to play a few new video formats. The Motion JPEG format (M-JPEG), is an \"informal name for multimedia formats where each video frame or interlaced field of a digital video sequence is separately compressed as a JPEG image\". The PlayStation Portable plays both the Linear PCM and the u-Law Versions of the Motion JPEG video format.
- In addition, you will now be able to access the Camera (functionality) from the photo option menus, for quicker easier access when taking photos or video.
- Another nifty function is the ability to finally turn off Auto Play for inserted UMD Discs via UMD Auto Boot.
- PlayStation Games - Here\'s the big tip you\'ve been waiting for. Finally, Sony is going to drop their highly anticipated PlayStation One emulator onto the PSP. From the manual however, there seems to be a unavoidable catch. If you don\'t have a PS3, your not going to be enjoying PlayStation One games emulating on Sony\'s PlayStation One emulator for PSP anytime soon. From the manual it states that you must connect to the Playstation Online store with your PSP connected to the PlayStation 3 in order to download and play the games. In addition, they mention that you can in fact share the games, but you must activate the other system in the Friends menu as a PS3 Network Account.

#### 29.3.15  3.01

- security fixes

#### 29.3.16  3.02

#### 29.3.17  3.03

### 29.4  Exploits

#### 29.4.1  Kxploit (Code Execution)

found and Proof of Concept by: spanish PSPDEV team

##### 29.4.1.1 [  Overview]{#sec29.4.1.1}

##### 29.4.1.2 [  Details]{#sec29.4.1.2}

All kxploit does is create two directories, like this:\
`/MYPROG%`\
`/MYPROG` \
 \
or, to hide the \'broken data\' items, like this: \
 \
`/MYPROG~1%` (exactly 8 characters including \~1) `/MYPROG_________________________1` (exactly 32 characters)\
The first contains an \'empty\' PBP file (no actual executable) and the second the real unsigned binary. The PSP sees one as corrupt (and shows the corrupt icon) and one as valid. Once you launch the valid one, the PSP incorrectly parses the \"%\" sign as part of a standard printf-style formatting string, and so removes it, and then finds the elf file and loads it. Memory stick swap works in the same way - it finds the pbp first on the first memory stick, and then finds the elf on the second after having run the pbp from the menu.\
note: the filename hack to hide the broken icons has a subtle problem:\
if you copy `MYPROG~1%` first: `MYPROG~1` is the short name for `MYPROG~1%` `MYPROG~2` is the short name for `MYPROG_________________________1`\
if you copy `MYPROG_________________________1` first: `MYPROG~1` is the short name for `MYPROG_________________________1` `MYPROG~2` is the short name for `MYPROG~1%`\
The second case works properly. The first does not. Remember why the kxploit trick works at all: the vsh sees a nicely formed file in \"`MYPROG~1%`\", but then passes \"`MYPROG~1`\" to the bootstrap, which executes the bare ELF. If \"`MYPROG~1`\" is the short name for the wrong directory, of course it won\'t work. **29.4.1.3 [  \_\_SCE\_\_ variant (\"SCEKxploit\")]{#sec29.4.1.3}  ** a simelar bug can be exploited, name the two directories like this:\
`%__SCE__MYPROG`\
`__SCE__MYPROG`\
this variation of the Kxploit has the advantage that it hides the corrupted icons without having the above mentioned subtle problem (since the shortened filenames of the two directories can not be confused).

#### 29.4.2  TIFF Exploit (Code Execution)

found and Proof of Concept by: Niacin, Skylark works in firmware version 2.0.

##### 29.4.2.1 [  Overview]{#sec29.4.2.1}

The exploit involves using a wallpaper and a TIFF image file containing a buffer overflow. Since the data from the wallpaper is in a known location(VRAM) we can use the TIFF overflow to jump to the known VRAM location and execute code.

##### 29.4.2.2 [  Details]{#sec29.4.2.2}

#### 29.4.3  GTA Savegame Exploit (Code Execution)

found and Proof of Concept by: Edison Carter works in firmware version 2.0 (required to run GTA) up to 2.6 (2.7 fixes the GTA exploit) .The Exploit was patched in a second batch of GTA.\
German Version:

- ULES 00182 - Unpatched

Europe (UK/EU) Version:

- ULES-00151# - Unpatched - Contains fw 2.0 Update on UMD
- ULES-00151#2 - Patched - Contains the 2.60 update on UMD

North American (US) Version:

- ULUS 10041 - Patched - Contails UPDL 010050 on the UMD.
- ULUS 10041 - Unpatched - Contains UPDL 0048501A 5, plus IFPI L332 in very small letters.
- ULUS 10041 Unpatched, and Patched UMDs look exactly the same\... Only the small codes are different.

Another slight variation that is also on the spine of the UMD case. The18 logo in a red circle is present in the pre 2.6 version, but in the patched 2.6 game the 18 red circle logo isn\'t present on the spine. Another indication is the copyright Date, if its 2005 then its unpatched, if its 2006 then its patched.

##### 29.4.3.1 [  Overview]{#sec29.4.3.1}

The GTA exploit is a classic stack buffer overflow, in the savedata processing.

##### 29.4.3.2 [  Details]{#sec29.4.3.2}

In essence, the savedata mostly consists of a large structure, with an element indicating the total size. GTA allocates a statically-sized buffer for this to be read into, on the stack - presumably using sizeof(savestruct) or similar. But it copies the number of bytes given by the .size element from the savedata into the stack buffer. By editing the .size element in the saved data, we can therefore force a buffer overflow. The .size element is at offset 0004 in the DATA.BIN file, in the savegame folder. Note that the DATA.BIN is encrypted, so you need to use something like the savedata sample from the pspsdk in order to modify it.

#### 29.4.4  LoadExec Exploit (gain Kernel access)

found and Proof of Concept by: Hitchhikr works in firmware version 2.5 and 2.6

##### 29.4.4.1 [  Overview]{#sec29.4.4.1}

##### 29.4.4.2 [  Details]{#sec29.4.4.2}

The exploit is located in a function which can be found in the loadexec.prx file at address `0x88064C94` (game mode) in the firmware 2.6 (the same bug is also present in the firmware 2.5), a module located in the kernel space memory (therefore running in kernel mode). The purpose of this procedure (used in other functions like \"sceLoadExec\") is to check that the drive part of a filename is valid & legit. It allocates 48 bytes of stack and the return address to the calling function is stored at the end of it (from 44th to 47th bytes). It starts by checking the first char of the string to see if it\'s an empty drive name, if it\'s not, the routine extracts the part of the filename that contain the drive name and copies it into the allocated stack, it only stops when it encounters a \':\' char. Since it doesn\'t check any string length during the copy, if the drive name we supply is big enough it\'ll overwrite the rest of the stack based values, like the return address for example. That\'s why a drive name of 48 chars (+ an extra \':\' char to let the loop ends) containing an address to an arbitrary position in memory (pointing to a function of ours for example) located from the 44th to 47th chars in the filename will allow us to run any code we want in the context of the executing routine (kernel mode) as when it ends, it reloads the return address from the stack and directly jumps to it.

### 29.5  Network Update

When you select \"Network Update\" in the PSP menu, it will fetch a file from the web, this file currently has the following contents:

- Japanese PSP (JP Region) fetches from `http://fj01.psp.update.playstation.org/update/jp/psp-updatelist.txt` \
   \
  +:----------------------------------------------------------------------------------------------------------------:+
  |   -------------------------------------------------------------------------------------------------------------- |
  |   `# JP`\                                                                                                        |
  |   `Dest=00;ImageVersion=00000000;CDN=http://dj01.psp.update.playstation.org/update/jp/ nodata;CDN_Timeout=30;`   |
  |                                                                                                                  |
  |   -------------------------------------------------------------------------------------------------------------- |
  +------------------------------------------------------------------------------------------------------------------+

   \
   \
  `or` \
   \
  +:--------------------------------------------------------------------------------------------------------------------------------------------------------------:+
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  |   `# JP`\                                                                                                                                                      |
  |   `Dest=00;ImageVersion=000002d5;CDN=http://dj01.psp.update.playstation.org/update/jp/ 2005_0824_50c7032754835b588319c1a6c652cdc0/EBOOT.PBP;CDN_Timeout=30;`   |
  |                                                                                                                                                                |
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------+

   \
- American PSP (US Region) fetches from `http://fj01.psp.update.playstation.org/update/us/psp-updatelist.txt` \
   \
  +:--------------------------------------------------------------------------------------------------------------------------------------------------------------:+
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  |   `# US`\                                                                                                                                                      |
  |   `Dest=01;ImageVersion=000002d5;CDN=http://du01.psp.update.playstation.org/update/us/ 2005_0824_50c7032754835b588319c1a6c652cdc0/EBOOT.PBP;CDN_Timeout=30;`   |
  |                                                                                                                                                                |
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------+

   \
- European PSP (EU Region) fetches from `http://fj01.psp.update.playstation.org/update/eu/psp-updatelist.txt`\
  \
  +:--------------------------------------------------------------------------------------------------------------------------------------------------------------:+
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  |   `# EU`\                                                                                                                                                      |
  |   `Dest=02;ImageVersion=000002d5;CDN=http://de01.psp.update.playstation.org/update/eu/ 2005_0824_50c7032754835b588319c1a6c652cdc0/EBOOT.PBP;CDN_Timeout=30;`   |
  |                                                                                                                                                                |
  |   ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------+

If an image with a higher version than what is currently installed is available, the PSP can download it from the URL specified after CDN= and install it. The upgrade image consists of a game file in the PBP format, which should reflash the system software when run.

### 29.6  Network Test

In order for the PSP to check for updates, you must make sure you have valid Wi-Fi settings. In the \"SETTINGS-\>Network Settings-\>Infrastructure Mode\", if you selection the triangle button while the cursor is on a connection name, you can select the \"Test Connection\" and the PSP will actually try to reach this URL: http://fj00.psp.update.playstation.org/networktest/trial.txt

+:---------------------------------------------------------------------:+
|   ---                                                                 |
|   p                                                                   |
|   ---                                                                 |
+-----------------------------------------------------------------------+

### 29.7  Registry

The PSP stores some non-critical settings (fonts, language, owners name, WEP passwords, user password) in a set of 2 files. Those files, named \'system.dreg\' and \'system.ireg\' can be called \"the registry\", not unlike the Windows one. Since the registry is placed on Flash1, it can be accessed by userland code in any version from 1.50 to 2.60. For some reason (possibly wear leveling the Flash), the PSP registry is pretty awkwardly defined. Namely, the DREG part (data) consists of 512-byte sectors, not unlike hardware sectors on a hard disk. The IREG part (info) contains information on finding those sectors, since some blocks can be longer than 1 sector. This is very similar to a filesystem - IREG part works as a \"FAT\" and DREG part works as the data area.

### 29.8  VSH

### 29.9  Game Sharing
