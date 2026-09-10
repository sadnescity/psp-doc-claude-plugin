---
name: flash-memory
description: "The internal flash: chips, partitions and how they are addressed."
---

## 19  Flash Memory

### 19.1  Physical Layout

The PSP MCP uses a 32MB NAND with the following layout:

- 512+16 bytes per page
- 32 pages per block (16K+512)
- 2048 blocks per device (32MB+1MB)

A block is the smallest erasable unit, a page the smallest writable (programmable). A Block holds 32 pages (for the latest small page NAND devices, including the MCP used for the PSP).

### 19.2  User Area (Main Data)

The IPL doesn\'t seem to be part of any kind of FS (blocks appear at fixed physical locations). Everything else (above 1MiB phys) is FAT12 with a SmartMedia style Block mapping but with a custom mapping area (i.e. different layout from what is/was mandated for SM). Only FAT organized area of on-board flash chip, system file volume and configuration file volume, can be accessed via FAT Filesystem. The bootstrap area is unreachable by the flash and lflash drivers. (lflash returns all 0x00)

#### 19.2.1  Physical Layout (unmapped)

+:---------------------------------------------------------------------:+
|   -------------- -------------- ---------- -----------------          |
|     **start**       **end**      **size**  **description**            |
|    `0x00000000`   `0x000FFFFF`     1MB     bootstrap Area             |
|    `0x00100000`   `0x01ffffff`    `31MB`   mapped Area                |
|   -------------- -------------- ---------- -----------------          |
+-----------------------------------------------------------------------+

 \

#### 19.2.2  Logical Layout (mapped)

When the Flashdriver starts up it reads all the extra data sections (usually from the first page of each block). From this data it extracts the logical block number which in turn is used to build up a table (index is LBN, value is PBN). Reading from logical Blocks works by simple address translation (LBN-\>PBN). Writing is usually done using a write before erase strategy, i.e. an emtpy block is filled with the data (new/replacement), then the LBN entry is remapped to the new PBN and the old physical block is erased (and goes either back to the free pool are becomes a bad block). \
 \

+:-------------------------------------------------------------------------------------:+
|   -------------- --------- --------- ------- ---------- ----------------------------- |
|     **start**               **end**           **size**  **description**               |
|       Offset       Block    Offset    Block                                           |
|    `0x00000000`   `0x000`                               Master Boot Record (MBR)      |
|    `0x00008000`   `0x002`                               Partition Boot Record (PBR)   |
|    `0x0000c000`   `0x003`                      24MiB    FAT12 Partition #1 (flash0)   |
|    `0x01808000`   `0x602`                                                             |
|    `0x0180C000`   `0x603`                      `4MiB`   FAT12 Partition #2 (flash1)   |
|    `0x01C08000`   `0x702`                                                             |
|    `0x01C0C000`   `0x703`                               FAT12 Partition #3 (empty)    |
|    `0x01D08000`   `0x742`                                                             |
|    `0x01D0C000`   `0x743`                               FAT12 Partition #4 (empty)    |
|    `0x01DF8000`   `0x77e`                                                             |
|    `0x01DFC000`   `0x77f`                               Last Block                    |
|   -------------- --------- --------- ------- ---------- ----------------------------- |
+---------------------------------------------------------------------------------------+

 \

#### 19.2.3  Bootstrap (IPL Area)

The IPL, region and serial number are located within the nand non-fat area (using an ecrypted form)

+:----------------------------------------------------------------------------------------------------------------:+
|   -------------- -------------- ---------- ----------- --------------------------------------------------------- |
|     **start**       **end**      **size**   **block**  **description**                                           |
|    `0x00000000`                    64k         1-3     ? (all 0xff)                                              |
|    `0x00010000`   `0x00013fff`     16k          4      physical block numbers of IPL                             |
|    `0x00014000`                                 5      block numbers of IPL (duplicated)                         |
|    `0x00018000`                                 6      block numbers of IPL (duplicated)                         |
|    `0x0001c000`                                 7      block numbers of IPL (duplicated)                         |
|    `0x00020000`                                 8      block numbers of IPL (duplicated)                         |
|    `0x00024000`                                 9      block numbers of IPL (duplicated)                         |
|    `0x00028000`                                10      block numbers of IPL (duplicated)                         |
|    `0x0002c000`                                11      block numbers of IPL (duplicated)                         |
|    `0x00030000`   `0x0003ffff`                         all 0xff                                                  |
|    `0x00040000`                    16k        16-29    encrypted IPL (encrypted chunks of `0x1000` bytes each)   |
|                   `0x000bffff`                         rest 0xff (max 0x20 blocks free for IPL)                  |
|    `0x000c0000`                                        ID Storage Area                                           |
|    `0x000d4180`   `0x000FFFFF`                         rest 0xff                                                 |
|   -------------- -------------- ---------- ----------- --------------------------------------------------------- |
+------------------------------------------------------------------------------------------------------------------+

##### 19.2.3.1 [  IPL Block Mapping]{#sec19.2.3.1}

Physical blocks 4-11 hold mapping information. Each block contains the same information, for redundancy presumably. If one of these blocks becomes invalid, the next one is used etc. If all these blocks are bad the PSP might be dead

#### 19.2.4  ID Storage Area

Various subsystems in the PSP make use of the id-storage including usb, wlan, umd, etc. (The firmware provides a driver in idstorage.prx to facilitate manipulations. ) The id-storage area begins at 0xc0000 and appears to be used to store low-level information. The id-storage area is an associative array and information is stored using key/value pairs. The id-storage seems a little coupled to the the physical storage as each key maps to an area of 512-bytes, which is equal to the pagesize of the PSP standard nand-flash, and it seems 512-byte page operations are intended. key 0x100-0x11F same as key 0x120-0x13F old ver psp haven\'t key 0x046, 0x047 old old ver psp haven\'t key 0x140

##### 19.2.4.1 [  Index]{#sec19.2.4.1}

The keys are stored in an index which consists of two nand pages of 512 bytes. The index is identified by byte 6 of the spare area being 0x73. Byte 7 might be the id-storage version number. Byte 8 must be 1 (or possibly 0) and might indicate whether the storage is formatted or not, and a value greater than 1 in byte 9 indicates that the id-storage is read-only. Keys are 16-bit integers. The location of the data associated with a key is identified by the key\'s position in the index. For instance, a key appearing at position 97 (byte 194) in the index will find its associated data at location: 0xc0000 + (97 \* 512) = 0xcc200.

##### 19.2.4.2 [  key 0x041 : USB Descriptor]{#sec19.2.4.2}

+:---------------------------------------------------------------------:+
|   ------------ ---------------------- --------------------------      |
|    **offset**  **description**                                        |
|     `0x0000`   idVendor               4C 05                           |
|     `0x0002`                          00 00                           |
|     `0x0004`   bLength                0A                              |
|     `0x0005`                          03                              |
|     `0x0006`   iManufacturer String   \'S.o.n.y.\'                    |
|     `0x0044`   ? bNum                 05                              |
|     `0x0045`                          00 00 00                        |
|     `0x0048`   idProduct              C8 01                           |
|     `0x004A`                          00 00                           |
|     `0x004C`   bLength                16                              |
|     `0x004D`   ? bDescriptorType      03                              |
|     `0x004E`   iProduct String        \'P.S.P. .T.y.p.e. .A.\'        |
|     `0x008C`   idProduct              C9 01                           |
|     `0x008E`                          00 00                           |
|     `0x0090`   bLength                16                              |
|     `0x0091`   ? bDescriptorType      03                              |
|     `0x0092`   iProduct String        \'P.S.P. .T.y.p.e. .B.\'        |
|     `0x00D0`   idProduct              CA 01                           |
|     `0x00D2`                          00 00                           |
|     `0x00D4`   bLength                16                              |
|     `0x00D5`   ? bDescriptorType      03                              |
|     `0x00D6`   iProduct String        \'P.S.P. .T.y.p.e. .C.\'        |
|     `0x0114`   idProduct              CB 01                           |
|     `0x0116`                          00 00                           |
|     `0x0118`   bLength                16                              |
|     `0x0119`   ? bDescriptorType      03                              |
|     `0x011A`   iProduct String        \'P.S.P. .T.y.p.e. .D.\'        |
|     `0x0158`   idProduct              CC 01                           |
|     `0x015A`                          00 00                           |
|     `0x015C`   bLength                16                              |
|     `0x015D`   ? bDescriptorType      03                              |
|     `0x015E`   iProduct String        \'P.S.P. .T.y.p.e. .E.\'        |
|   ------------ ---------------------- --------------------------      |
+-----------------------------------------------------------------------+

##### 19.2.4.3 [  key 0x044 : MAC Address]{#sec19.2.4.3}

##### 19.2.4.4 [  key 0x050 : Serial Number]{#sec19.2.4.4}

#### 19.2.5  FAT Area

FAT12 with a cluster size of 16K which conveniently matches the erase block size.

### 19.3  Spare Area (extra Data)

+:-------------------------------------------------------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- ----------------- -------------------------------------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                                                                          |
|     `0x00`                 `4`     user_ecc          calculated per 512 byte page of user data (byte 3 is always 0x00)                      |
|     `0x04`                 `1`     block_fmt         0xff = IPL, 0x00 = FAT                                                                 |
|     `0x05`                 `1`     block_stat        0xff = valid block                                                                     |
|     `0x06`                 `2`     block_addr        logical block number for FAT, mostly 0xff 0xff for IPL, 0x73 0x01 = ID-Storage Index   |
|     `0x08`                 `2`     ?                 ID-Storage Index =0x01 0x01 / IPL = 0x38 0x4a or 0x01 0x01 / others 0x00 0x00          |
|     `0x0a`                 `2`     ?                 ID-Storage Index =0xff 0xff / IPL = 0xc6 0x6d or 0xff 0xff / others 0x00 0x00          |
|     `0x0c`                 `2`     spare_ecc         calculated from bytes 0x04-0x0b of spare area (12 bit, high nybble always 0xf)         |
|     `0x0e`                 `2`     ?                 always 0xff 0xff                                                                       |
|   ----------- --------- ---------- ----------------- -------------------------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------------------------------------------------------------+

note: If reading a dump from a live PSP, it is important to verify the ECC. Hardware automatically reclaims single-bit errors in the user-area, but for the spare area this must be done manually.

### 19.4  Tools

- `dumpipl` (MrBrown, Tyranid, John Kelley) dump IPL from Flash to Memstick \[runs on PSP\]
