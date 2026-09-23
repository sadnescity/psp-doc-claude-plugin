---
name: file-formats
description: "PSP file formats: PRX sections, export and import tables, the custom relocation format and the ~PSP header of encrypted executables, then PBP, PARAM.SFO, PSAR and the PGF font format. Use when reading or rebuilding an executable, or when a relocation has to be resolved by hand."
---

Chapter 26, a catalogue of formats whose centre of gravity is the PRX section:
program headers, the .lib.ent and .lib.stub tables, .rodata.sceModuleInfo and
.rodata.sceResident, the ~PSP header an encrypted executable carries, and the
custom relocation format — section type 0x700000A0, entries of two words, with
the offset base and the address base packed into r_info beside the MIPS
relocation type. PBP, PARAM.SFO, PSAR, the PGF bitmap font format and a long
tail of registry and media formats follow it.

This is where the relocation entries are actually written down, which is what
decides whether an instruction added or moved inside BOOT.BIN still resolves
once the loader has relocated the module: r_offset is measured from one program
header, and the value already stored there is relocated from another.

The chapter is uneven. ELF gets three lines and a pointer to the standard ELF
documentation. .rodata.sceNid is a heading with nothing under it. Gamesave, AT3
and DIC are empty, and ISO, DAX and CSO get one line each, so there is nothing
here on ISO9660 or on the sector layout of a UMD. What the export and stub
tables are for once the module is running is in modules-and-patching; where
BOOT.BIN sits on the disc is in umd-game-structure.

---

## 26  File Formats

Note on the Tools Sections: at the bottom of every Fileformats Section there might be a list of some related Tools.

### 26.1  ELF (Executable & Linkable Fileformat)

this is an Industry-Standard Fileformat used by many Operating Systems, Compilers etc. (refer to one of the many free Documentations for Details)

#### 26.1.1  Tools

since this is a widely accepted standard, many available (non PSP specific) tools support it, for example

- `psp-objdump` (GNU) show contents, structure, disassemble\...

### 26.2  PRX (PSP Relocateble eXecutable)

Sony\'s PRX (PSP Relocation eXecutable?) format is a relocation executable based on the standard ELF format. It is distinguised from a normal ELF file by having customised Program Headers, Non-standard MIPS relocation sections and a unique ELF type.

#### 26.2.1  Program Headers

A valid PRX must have at least one program header in order to be loadable, due to the way the relocation entries work. In all program headers the Physical address is not used in the way it is described in the ELF documentation. In the first program header in the list the physical address is actually set to the offset of the .rodata.sceModuleInfo in the PRX file. It is not the load address in memory. In any subsequent program headers the physical address is set to 0. Just to slightly complicate matters if the PRX file is a kernel module then the most significant bit must be set in the phsyical address of the first program header. As a side note the data referenced by the Program Headers must at least be aligned to 16 byte boundaries otherwise the kernel ELF loader will fail (tested on v1.0 and v1.5).

#### 26.2.2  special Sections

##### 26.2.2.1 [  .sceStub.text (Systemcall Stubs)]{#sec26.2.2.1}

+:-------------------------------------------------------------------------:+
|   ----------------------------------------------------------------------- |
|   `sceXXX:`\                                                              |
|   `        jr $ra`\                                                       |
|   `        nop`                                                           |
|                                                                           |
|   ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------+

##### 26.2.2.2 [  .lib.ent.top (Marks Beginning of Entry Section)]{#sec26.2.2.2}

contains one 32bit word with the value 0x00000000

##### 26.2.2.3 [  .lib.ent:]{#sec26.2.2.3}

\_library_entry:

+:---------------------------------------------------------------------:+
|   ------------ ---------------------------------------------          |
|                **description**                                        |
|    32bit word  Addr: Name of Export Library (default: 0)              |
|       u16      BCD Version                                            |
|       u16      module attributes                                      |
|        u8      size of export entry in dwords                         |
|        u8      number of variables                                    |
|       u16      number of Functions                                    |
|    32bit word  Addr: \_\_entrytable in .rodata.sceResident            |
|   ------------ ---------------------------------------------          |
+-----------------------------------------------------------------------+

##### 26.2.2.4 [  .lib.ent.btm (Marks End of Entry Section)]{#sec26.2.2.4}

contains one 32bit word with the value 0x00000000

##### 26.2.2.5 [  .lib.stub.top (Marks Beginning of Stub Section)]{#sec26.2.2.5}

contains one 32bit word with the value 0x00000000

##### 26.2.2.6 [  .lib.stub (Stub Entries)]{#sec26.2.2.6}

\_\_stub_module_sceXXX:

+:---------------------------------------------------------------------:+
|   ------------ -------------------------------------------------      |
|                **description**                                        |
|    32bit word  Addr: \_\_stub_modulestr in .rodata.sceResident        |
|       u16      Import Flags                                           |
|       u16      Library Version                                        |
|       u16      Number of Stubs to Import                              |
|       u16      Size of the Stub itself (in 32bit words)               |
|    32bit word  Addr: \_\_stub_nidtable in .rodata.sceNid              |
|    32bit word  Addr: sceXXX stub in .sceStub.text                     |
|   ------------ -------------------------------------------------      |
+-----------------------------------------------------------------------+

##### 26.2.2.7 [  .lib.stub.btm (Marks End of Stub Section)]{#sec26.2.2.7}

contains one 32bit word with the value 0x00000000

##### 26.2.2.8 [  .rodata.sceModuleInfo:]{#sec26.2.2.8}

module_info:

+:-----------------------------------------------------------------------------------:+
| +:---------------------------------:+---------------------------------------------+ |
| |                                   | **description**                             | |
| +-----------------------------------+---------------------------------------------+ |
| | u16                               | Module Attributes                           | |
| +-----------------------------------+---------------------------------------------+ |
| |                                   |   ---------- ------------------------------ | |
| |                                   |   `0x0000`   Module starts in User Mode     | |
| |                                   |   `0x1000`   Module starts in Kernel Mode   | |
| |                                   |   ---------- ------------------------------ | |
| +-----------------------------------+---------------------------------------------+ |
| | u16                               | Module Version (2 chars)                    | |
| +-----------------------------------+---------------------------------------------+ |
| | 28 bytes                          | Module Name (0 terminated)                  | |
| +-----------------------------------+---------------------------------------------+ |
| | 32bit word                        | Addr: GP                                    | |
| +-----------------------------------+---------------------------------------------+ |
| | 32bit word                        | Addr:.lib.ent                               | |
| +-----------------------------------+---------------------------------------------+ |
| | 32bit word                        | Addr:.lib.ent.btm                           | |
| +-----------------------------------+---------------------------------------------+ |
| | 32bit word                        | Addr:.lib.stub                              | |
| +-----------------------------------+---------------------------------------------+ |
| | 32bit word                        | Addr:.lib.stub.btm                          | |
| +-----------------------------------+---------------------------------------------+ |
+-------------------------------------------------------------------------------------+

##### 26.2.2.9 [  .rodata.sceResident (magic words and their memory offsets)]{#sec26.2.2.9}

1.  first comes a list of magic words (\_\_entrytable),a PRX (PSP module) can have \
     \
    +:---------------------------------------------------------------------:+
    |   -------------- ----------------------                               |
    |     **Magic**    **description**                                      |
    |    `0xd3744be0`  module_bootstart                                     |
    |    `0x2f064fa6`  module_reboot_before                                 |
    |    `0xadf12745`  module_reboot_phase                                  |
    |    `0xd632acdb`  module_start                                         |
    |    `0xcee8593c`  module_stop                                          |
    |    `0xf01d73a7`  module_info                                          |
    |    `0x0f7c276c`                                                       |
    |   -------------- ----------------------                               |
    +-----------------------------------------------------------------------+
2.  now immediatly follows a list of the memory offsets for the magic (referenced in .lib.stub)

##### 26.2.2.10 [  .rodata.sceNid (Import stubs hashes; referenced in .lib.stub)]{#sec26.2.2.10}

#### 26.2.3  Custom Relocation Format

The first customisation is the section type of the PRX relocation entries differ from that used in standard ELFs. In standard ELFs a relocation section is of type 9, in a PRX they are of type 0x700000A0. The second customisation is in the entries themselves. Each entry is 2 32bit words, the first word is the offset field of the relocation, the second is a compound structure consisting of the standard MIPS relcocation type and a custom base selection field.\
This is represented in C like this:\

+:-------------------------------------------------------------------------:+
|   ----------------------------------------------------------------------- |
|   `// Defines for the r_info field`\                                      |
|   `#define ELF32_R_ADDR_BASE(i) (((i)> >16) & 0xFF)`\                     |
|   `#define ELF32_R_OFS_BASE(i) (((i)> >8) & 0xFF)`\                       |
|   `#define ELF32_R_TYPE(i) (i&0xFF)`                                      |
|                                                                           |
|                                                                           |
|                                                                           |
|   `typedef struct {`\                                                     |
|   `    Elf32_Addr r_offset;`\                                             |
|   `    Elf32_Word r_info;`\                                               |
|   `} Elf32_Rel;`                                                          |
|                                                                           |
|                                                                           |
|                                                                           |
|   `// MIPS Reloc Entry Types`\                                            |
|   `#define R_MIPS_NONE 0`\                                                |
|   `#define R_MIPS_16 1`\                                                  |
|   `#define R_MIPS_32 2`\                                                  |
|   `#define R_MIPS_REL32 3`\                                               |
|   `#define R_MIPS_26 4`\                                                  |
|   `#define R_MIPS_HI16 5`\                                                |
|   `#define R_MIPS_LO16 6`\                                                |
|   `#define R_MIPS_GPREL16 7`\                                             |
|   `#define R_MIPS_LITERAL 8`\                                             |
|   `#define R_MIPS_GOT16 9`\                                               |
|   `#define R_MIPS_PC16 10`\                                               |
|   `#define R_MIPS_CALL16 11`\                                             |
|   `#define R_MIPS_GPREL32 12`                                             |
|   ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------+

\
OFS_BASE determines which program header the r_offset field is based from. So if r_offset is 0x100 and OFS_BASE is 0 (which is a PH starting at address 0) then the address to read is at 0x100. ADDR_BASE determines which program header the current address value in memory should be relocated from. So for example if ADDR_BASE was 1, program header 1 is loaded to 0x1000 and the current address stored in the ELF is 0xF0 then the resulting address is 0x10F0.

#### 26.2.4  Unique ELF type

PRX files report the value 0xFFA0 as their type in the header instead of 0x0002 which is usual for normal MIPS ELF files.

#### 26.2.5  Tools

- `prxtool` (Tyranid) show content, structure, convert prx to elf, create idc script\...
- `psp-prxgen` (Tyranid) create prx from elf
- `nidattack` (adresd, djhuevo) bruteforce NID cracker
- `prxdecrypt` (MrBrown, Tyranid, John Kelley) decrypt \[runs on PSP\]

### 26.3  PBP

A PBP file collects the files needed for a game executable from a MemoryStick into a single file, for easier transfer. The files are simply concatenated with a small index at the start. There does not seem to be any alignment requirements.\
All the offsets are in bytes from the beginning of the PBP file, and store in unsigned little endian 32 bit format (ul32).\

+:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- ----------------------------------------------------------------------------------------------------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                                                                                                                       |
|        0          3         4      0 \"PBP\" A file type identification cookie. A zero byte is followed by the three uppercase ASCII characters \"PBP\"                                  |
|        4          7         4      0 0 1 0 This might be some kind of indication of the PBP version. Currently it\'s always two 0 bytes followed by a 1 byte and then one more 0 byte.   |
|        8         11         4      ul32 Offset of param.sfo data                                                                                                                         |
|       12         15         4      ul32 Offset of icon0.png data (thumbnail icon)                                                                                                        |
|       16         19         4      ul32 Offset of icon1.pmf data (movie icon highlighted)                                                                                                |
|       20         23         4      ul32 Offset of PNG image of unknown purpose (thumbnail icon highlighted ?)                                                                            |
|       24         27         4      ul32 Offset of pic1.png data (background image)                                                                                                       |
|       28         31         4      ul32 Offset of snd0.at3 data (ambient sound)                                                                                                          |
|       32         35         4      ul32 Offset of PSP data                                                                                                                               |
|       36         39         4      ul32 Offset of PSAR data                                                                                                                              |
|   ----------- --------- ---------- ----------------------------------------------------------------------------------------------------------------------------------------------------- |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

#### 26.3.1  Tools

- `unpack-pbp` (Dan Peori aka Oopo) show content, structure, extract \...
- `pack-pbp` (Dan Peori aka Oopo) create pbp file

### 26.4  PSF (SFO)

PSF files are used in various places on the PSP to store metadata about other files. It contains a list of keys, and the values associated with these keys. This can be information such as parental level, and language. Numerical data is stored in little endian format, I will use the notation ul32 for \"unsigned little endian 32 bit\" etc.\
The file starts with a header, giving the number of key/value pairs and the offsets for the main parts of the file:\

+:------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- ------------------------------------------------------------------------------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                                                                                                 |
|        0          3         4      0 \"PSF\" A file type identification cookie. A zero byte is followed by the three uppercase ASCII characters \"PSF\".           |
|        4          7         4      1 1 0 0 This might be some kind of indication of the PSF version. Currently it\'s always two 1 bytes followed by two 0 bytes.   |
|        8         11         4      ul32 Offset from the start of the file to the start of the key table (in bytes)                                                 |
|       12         15         4      ul32 Offset from the start of the file to the start of the value table (in bytes)                                               |
|       16         19         4      ul32 Number of key/value pairs in the index                                                                                     |
|   ----------- --------- ---------- ------------------------------------------------------------------------------------------------------------------------------- |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+

 \
 \
This header is immediately followed by the index table, which has one entry per key/value pair. This table seems to always be sorted alphabetically on the key string, allowing binary search to be used, although it is unknown if this is actually guaranteed. The entries look like this:\

+:---------------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- ---------------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                                  |
|        0          1         2      ul16 Offset of the key name into the key table (in bytes)        |
|        2          2         1      4 Unknown, always 4. Maybe alignment requirement for the data?   |
|        3          3         1      ul8 Datatype of the value, see below.                            |
|        4          7         4      ul32 Size of value data, in bytes                                |
|        8         11         4      ul32 Size of value data plus padding, in bytes                   |
|       12         15         4      ul32 Offset of the data value into the value table (in bytes)    |
|   ----------- --------- ---------- ---------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------+

 \
Value data is always aligned to a 4 byte boundary, so if the size of the data is not dividable by four, the data is padded with zero bytes. The two size fields in the index entry gives the size with and without this padding, respectively. It is allowed to add arbitrary amounts of extra padding (as long as alignment is ensured), which makes it easier to modify data in place. Some games seem to take advantage of this to update the text descriptions as the player progresses in the game. After the index table comes the key table, at the offset (from the beginning of the file) indicated in the file header. Each key is a NUL-terminated ASCII string. The keys are referenced from the index table by offset from tge key table start, so the first key will have offset 0. The last part of the file is the value table, again at an offset indicated in the file header. Since value data is required to be aligned, zero padding may exist between the key table and the value table. The offset in the file header will indicate the true start of the value table though. The type of data in the value table depends on the type field of the index entry that references that particular value. The known types are:\

+:----------------------------------------------------------------------------------------------------:+
|   ---------- ---------- ---------------------------------------------------------------------------- |
|    **Code**   **Type**  **description**                                                              |
|       0         BIN     Arbitrary binary data, interpretation depending on key                       |
|       2         TXT     UTF-8 text string, NUL-terminated. (The NUL is included in the data size.)   |
|       4         INT     An sl32 integer                                                              |
|   ---------- ---------- ---------------------------------------------------------------------------- |
+------------------------------------------------------------------------------------------------------+

 \
Before listing the various known keys, the key CATEGORY should be mentioned. This key exists in all PSF files, and indicate the type of entity described by the PSF file. It has TXT data, and the currertly known values are:\

+:-----------------------------------------------------------------------:+
|   -------------- ------------------- ---------------------------------- |
|    **category**  **description**                                        |
|         WG       WLAN Game           a game runable via Gamesharing     |
|         MS       MemoryStick Save    a savegame                         |
|         MG       MemoryStick Game    a game runnable from MemoryStick   |
|         UG       UMD Game            a game runnable from UMD           |
|         UV       UMD Video                                              |
|         UA       UMD Audio                                              |
|         UC       UMD Cleaning Disc                                      |
|   -------------- ------------------- ---------------------------------- |
+-------------------------------------------------------------------------+

 \
Depending on the category, different keys may be relevant. In the following table of observed keys, an \* indicates that the key occurs in that category of PSF.\

+:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   -------------------- ---------- -------- -------- -------- -------- ----------------------------------------------------------------------------------------------------------------------------------- |
|   **key**               **type**   **WG**   **MS**   **MG**   **UG**  **description**                                                                                                                     |
|   BOOTABLE                INT                          \*       \*    Setting this to 1 seems to indicate that the game should be autolaunched at bootup.                                                 |
|   CATEGORY                TXT                 \*       \*       \*    Category of PSF, as per the table above                                                                                             |
|   DISC_ID                 TXT                          \*       \*    Product number of the game(?), e.g. \"ABCD-00000\"                                                                                  |
|   DISC_NUMBER             INT                                   \*    Which disc (out of DISC_TOTAL) is this? (Counts from 1.)                                                                            |
|   DISC_TOTAL              INT                                   \*    Total number of UMD discs for this game.                                                                                            |
|   DISC_VERSION            TXT                          \*       \*    Version of the game(?), e.g. \"1.00\"                                                                                               |
|   DRIVER_PATH             TXT                          \*             Unknown.                                                                                                                            |
|   LANGUAGE                TXT                          \*             Language of the game. \"JP\" indicates Japanese, even though this is not the proper ISO 639 code\...                                |
|   PARENTAL_LEVEL          INT                 \*       \*       \*    Minimum parental control level needed to access this file (1-11, 1=general audience, 5=12 years, 7=15 years, 9=18 years)            |
|   PSP_SYSTEM_VER          TXT                          \*       \*    Version of PSP system software required to run the game(?), e.g. \"1.00\"                                                           |
|   REGION                  INT                          \*       \*    Bitmask of allowed regions. 0x8000 is region 2?                                                                                     |
|   SAVEDATA_DETAIL         TXT                 \*                      Text shown under the \"Details\" heading in the save game menu. Can contain multiple lines of text by embedding CR LF.              |
|   SAVEDATA_DIRECTORY      TXT                 \*                      The name of the subdirectory to savedata where this game stores its savefiles (e.g. UCJS10001)                                      |
|   SAVEDATA_FILE_LIST      BIN                 \*                      A list of filenames the game uses for the actual save data (typically something like \"DATA.BIN\"). Data format currently unknown   |
|   SAVEDATA_PARAMS         BIN                 \*                      Additional parameters of unknown function and data format.                                                                          |
|   SAVEDATA_TITLE          TXT                 \*                      Text shown under the \"Saved Data\" heading in the save game menu.                                                                  |
|   TITLE                   TXT                 \*       \*       \*    Text shown under the \"Game\" heading in the save game menu.                                                                        |
|   TITLE_0                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Japanese                                                                                  |
|   TITLE_2                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: French                                                                                    |
|   TITLE_3                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Spanish                                                                                   |
|   TITLE_4                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: German                                                                                    |
|   TITLE_5                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Italian                                                                                   |
|   TITLE_6                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Dutch                                                                                     |
|   TITLE_7                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Portuguese                                                                                |
|   TITLE_8                 TXT                 \*       \*       \*    Localized version of the TITLE attribute: Russian                                                                                   |
|   UPDATER_VER             TXT                          \*             Used by the firmware updater program to denote the version it upgrades the firmware to.                                             |
|   -------------------- ---------- -------- -------- -------- -------- ----------------------------------------------------------------------------------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

#### 26.4.1  Tools

- `SFOParse` (Chris Barrera a.k.a. Gorim) show contents
- `mksfo` (MrBrown) create file

### 26.5  PSP

+:-----------------------------------------------------------------------------------------------------------------------------------:+
| +:---------------:+:---------------:+:---------------:+---------------------------------------------------------------------------+ |
| | **start**       | **end**         | **size**        | **description**                                                           | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x00`          | 3               | 4               | \'\~PSP\'                                                                 | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x04`          |                 | 2               | attribute                                                                 | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| |                 |                 |                 |   --- ---------------------------                                         | |
| |                 |                 |                 |    1  SCE_MODULE_ATTR_CANT_STOP                                           | |
| |                 |                 |                 |    2  SCE_MODULE_ATTR_LOAD                                                | |
| |                 |                 |                 |    4  SCE_MODULE_ATTR_START                                               | |
| |                 |                 |                 |   --- ---------------------------                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x06`          |                 | 2               | comp_attribute                                                            | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| |                 |                 |                 |   --- ---------------------------------------                             | |
| |                 |                 |                 |    1  FLAG_COMPRESS                                                       | |
| |                 |                 |                 |    2  FLAG_NORELOC (ie. norel=PFX; rel=PRX)                               | |
| |                 |                 |                 |   --- ---------------------------------------                             | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x08`          |                 | 1               | module version lo                                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x09`          |                 | 1               | module version hi                                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x0a`          |                 | 28              | name                                                                      | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x26`          |                 | 1               | fileformat version (=1)                                                   | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x27`          |                 | 1               | nsegments                                                                 | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x28`          |                 | 4               | elf_size (unencrypted)                                                    | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x2c`          |                 | 4               | psp_size (encrypted)                                                      | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x30`          |                 | 4               | entry                                                                     | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x34`          |                 | 4               | modinfo_offset (high 8 bits are substracted from low 24 bits)             | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x38`          |                 | 4               | bss_size                                                                  | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x3c`          |                 |                 | alignment (4 16bit values)                                                | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x44`          |                 |                 | address (4 32bit values)                                                  | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x54`          |                 |                 | size (4 32bit values)                                                     | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x64`          |                 |                 | ? (6 32bit values)                                                        | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x7c`          |                 | 1               | type                                                                      | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x7d`          |                 | 3               | ? (3 8bit values)                                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0x80`          |                 | 0x30            | ?                                                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0xb0`          |                 | 4               | elf_size_comp; (\*1) psp_size - 0x150 ( == elf_size if uncompressed file) | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0xb4`          |                 | 4               | ? always 0x00000080 ?                                                     | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0xb8`          |                 | 0x18            | ? always 0x00 ?                                                           | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0xd0`          |                 | 4               | ID ?                                                                      | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
| | `0xd4`          |                 | 0x7c            | ?                                                                         | |
| +-----------------+-----------------+-----------------+---------------------------------------------------------------------------+ |
+-------------------------------------------------------------------------------------------------------------------------------------+

 \
\*1) elf_size_comp is the size of the compressed elf; if the file is not compressed, it is equal to elf_size; rounded up to the next align boundary, is equal to psp_size - 0x150

#### 26.5.1  Tools

- `psardump` (PspPet) decrypt \[runs on PSP\]

### 26.6  PSAR

#### 26.6.1  Structure

- 1\. Header
- 2\. type A section a. Header b. Data
- 3\. type A section a. Header b. Data
- 4\. type B section a. Header b. Data

\... alternating type A and type B sections \...

- N-1.type A section a. Header b. Data
- N. type B section a. Header b. Data

Type A : 272 bytes (0x110) Type B : Variable size data

#### 26.6.2  Header

+:---------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- ---------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                            |
|        0          3         4      \'PSAR\'                                                   |
|        4          7         4      0x01, 0x00, 0x00, 0x00                                     |
|        8         11         4      Size of the archive file (not including the PSAR header)   |
|       12         15         4      0x01, 0x00, 0x00, 0x00                                     |
|   ----------- --------- ---------- ---------------------------------------------------------- |
+-----------------------------------------------------------------------------------------------+

#### 26.6.3  Section Header

+:-------------------------------------------------------------------------:+
|   ----------- --------- ---------- -------------------------------------- |
|    **start**   **end**   **size**  **description**                        |
|        0                   0xb0    ??                                     |
|                             4      `u32 Size of data (without padding)`   |
|                           `0x04`   `[0] always 0x80 ??`                   |
|                           `0x18`   `[*] Always 0x00 ??`                   |
|                           `0x04`   `[3] always 0x06 ??`                   |
|                           `0x0C`   ??                                     |
|                           `0x70`   ??                                     |
|   ----------- --------- ---------- -------------------------------------- |
+---------------------------------------------------------------------------+

#### 26.6.4  Type A Section (Data Block)

Data in Sections is padded to 16 bytes alignment. A \"type 1\" Section always contains 0x110 bytes of Data, and 0x260 bytes total (including Header).

#### 26.6.5  Type B Section (compressed Data Block)

A \"type 2\" Section contains variable amount of Data.

#### 26.6.6  Tools

- `psardump` (PspPet) extract, unpack and decrypt files \[runs on PSP\]

### 26.7  Gamesave

#### 26.7.1  Tools

### 26.8  PMF (PSMF)

PSMF, or PlayStation Movie Format, is a proprietary movie format created by Sony for the PSP. PSMF videos can be as small as 64x64 pixels, and have a framerate of 29.97fps. The video codec used is H.264, also known as MPEG-4 Part 10 AVC. The audio codec is the Sony proprietary ATRAC3plus.

+:-------------------------------------------------------------------------------------------------------------:+
|   ----------- --------- ---------- -------------------------------------------------------------------------- |
|    **start**   **end**   **size**  **description**                                                            |
|     `0x00`     `0x03`       4      \'PSMF\'                                                                   |
|     `0x04`     `0x07`       4      \'0012\' (icon) or \'0014\' (movie)                                        |
|                                                                                                               |
|     `0x0c`     `0x0f`       4      the filesize without the header (Filesize of pmf in bytes - 2,048 bytes)   |
|                                                                                                               |
|     `0x5c`     `0x5f`       4      Total time (take the total value and then div it by 60 then 30 then 60)    |
|                                                                                                               |
|     `0x76`     `0x79`       4      Total time (take the total value and then div it by 60 then 30 then 60)    |
|                                                                                                               |
|     `0x8d`     `0x8e`       2      width of the movie (add a zero)                                            |
|     `0x8f`     `0x90`       2      height of the movie (add a zero)                                           |
|                                                                                                               |
|   ----------- --------- ---------- -------------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------------------------------+

The PMF file has a 2048 byte header, the actual MPEG-2 Program Stream starts with a 32-bit \"pack code\" which is 0x000001BA; this appears 2048 bytes into the file.

### 26.9  PGF

The PSP font format (.PGF files) is a bitmap based font format. Each letter (as well as its shadow) is a single, 4bpp bitmap, saved in the font file in a RLE compressed form. The bitmaps are encoded using either vertical or horizontal rows, depending on a certain 2-bit field in character metrics. Every \[character, shadow\] bitmap pair is preceded by a character metrics record. For Latin fonts the length of this record appears to be 12 bytes (with an optional 7-byte extension), for other families it\'s different. It\'s not known at this time what is the determinant of the record length. The metrics record contains the following fields:

- 14-bit offset of the shadow header record
- 7-bit width
- 7-bit height
- 7-bit signed horizontal adjustment
- 7-bit ascender
- 2-bit transposition (1 - horizontal rows, 2 - vertical rows)
- 1-bit modified record field (adds a 7-byte extension to the 12-byte header for ltn0.pgf)
- 46 bits of unknown data
- 5-bit horizontal advance

To find the character metrics one has to read the main pointer table. The table is constructed of N-bit pointers, where N is found in the file header at offset 0x1C. The number of pointers (and characters) can be found in the file header at offset 0x14. It is not known yet how to locate the main pointer table. The RLE compression works on 4-bit nibbles (the low nibble of a byte is considered to precede the high nibble in the stream). There are two sequences defined for this RLE:

- a nibble N\<8: take next nibble and replicate N+1 times into the output stream
- a nibble N\>7: take next 16-N nibbles and copy directly into the output stream

#### 26.9.1  Tools

- `ttf2pgf` (Skylark) convert Truetype to pgf format
- `mkfontset` (Skylark) create a set of fonts suitable for the PSP Firmware

### 26.10  THM

THM files, or \"thumbnail\" files, are nothing more than JPEG images. Specifically, they are 160x120 pixels, and use the .THM file extension.

### 26.11  MP4

note: this refers to MP4 files as required by the player in the VSH

- Video Limitation Resolution: 320 x 240 (QVGA), Nonstandard resolutions can be used but are still limited to the 76,800 pixel resolution of QVGA. Codec: MPEG-4 SP (Simple Profile), which has different headers than the more common MPEG-4 formats.
- Audio Limitation Codec: AAC Sampling Rate: 24000hz Bitrate Limitation: 1-768kb/s & 1500kb/s. Any combination of video and audio bitrate that is equal to or less than 768kb/s is acceptable (i.e. 640kb/s video + 128kb/s audio = 768kb/s total, or 300kb/s video + 32kb/s audio = 332kb/s total). The PSP also supports a bitrate of 1500kb/s, but no bitrates inbetween 768kb/s and 1500kb/s.

note: ffmpeg can create PSP compatible mpeg4 files using the \'3gp\' profile

### 26.12  AT3

### 26.13  PNG

these are standard PNG image files.

### 26.14  RCO

.rco files are localized resources.

### 26.15  IREG

Block Mapping File for the System Registry

#### 26.15.1  Header

IREG starts with a 0x5C-byte header

+:-----------------------------------------------------------------------------------------------------------------------------:+
|   ------------ ---------- --------------------------------------------------------------------------------------------------- |
|    **offset**   **size**  **description**                                                                                     |
|       0x00         4      ?                                                                                                   |
|       0x04         4      ?                                                                                                   |
|       0x08        0x14    full SHA-1 checksum, possibly of the whole file (with checksum bytes cleared before checksumming)   |
|       0x1c                ?                                                                                                   |
|       0x58         4      ?                                                                                                   |
|   ------------ ---------- --------------------------------------------------------------------------------------------------- |
+-------------------------------------------------------------------------------------------------------------------------------+

#### 26.15.2  Entries

IREG entries are - for a change - 0x3a-byte and there are 256 of them (after the header). Only a few fields of the IREG entry are known, the most important being:

+:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:+
|   ------------ ---------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    **offset**   **size**  **description**                                                                                                                                                            |
|                                                                                                                                                                                                      |
|       0x04        0x02    parent index (16-bit, little endian) - it\'s the index of the parent entry in the IREG (1.5 and 2.0 firmwares differ about the \"no parent\" value - 0x0000 or 0xFFFF :)   |
|                                                                                                                                                                                                      |
|       0x0a        0x02    number of entries in the DREG block described by this IREG entry (16-bit, little endian)                                                                                   |
|       0x0c        0x02    number of DREG sectors used by this IREG entry (16-bit, little endian)                                                                                                     |
|       0x10        0x1c    entry name (28 bytes, null-terminated)                                                                                                                                     |
|       0x2c                                                                                                                                                                                           |
|                                                                                                                                                                                                      |
|       0x2c      7\*0x0e   7-sector chain description                                                                                                                                                 |
|   ------------ ---------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

##### 26.15.2.1 [  Sector chains]{#sec26.15.2.1}

Sector chains are described by the 14-byte field, made up of 7 16-bit little endian DREG sector indices. Those indicate the sequence of DREG sectors in a given DREG block.

+:---------------------------------------------------------------------:+
|   ------------ ---------- ---------------------                       |
|    **offset**   **size**  **description**                             |
|       0x00         2      DREG sector index 1                         |
|       0x02         2      DREG sector index 2                         |
|       0x04         2      DREG sector index 3                         |
|       0x06         2      DREG sector index 4                         |
|       0x08         2      DREG sector index 5                         |
|       0x0a         2      DREG sector index 6                         |
|       0x0c         2      DREG sector index 7                         |
|   ------------ ---------- ---------------------                       |
+-----------------------------------------------------------------------+

### 26.16  DREG

Every 512-byte DREG sector contains a certain number (specified in the IREG and in the DREG header) of 32-byte entries.

+:---------------------------------------------------------------------:+
|   ------------ ---------- -----------------                           |
|    **offset**   **size**  **description**                             |
|        0        16\*0x20  DREG Entry                                  |
|   ------------ ---------- -----------------                           |
+-----------------------------------------------------------------------+

#### 26.16.1  Entry

+:---------------------------------------------------------------------:+
|   ---------- -----------------                                        |
|    **Type**  **description**                                          |
|       1      Subdirectory                                             |
|       2      Integer                                                  |
|       3      String                                                   |
|       4      Secret                                                   |
|      0x0f    Block Header                                             |
|   ---------- -----------------                                        |
+-----------------------------------------------------------------------+

##### 26.16.1.1 [  Block header]{#sec26.16.1.1}

Only the first sector in a block (as defined in the IREG) contains a block header, and it is always the first entry.

+:--------------------------------------------------------------------------------------------------:+
|   ------------ ---------- ------------------------------------------------------------------------ |
|    **offset**   **size**  **description**                                                          |
|        0           1      =0x0F (Entry Type)                                                       |
|        1           1      ?                                                                        |
|        2           2      The short (or byte? not sure) is block size in 512-byte units            |
|       4-5          2      allocation unit (size of keys? always 32)                                |
|       6-7          2      (unsigned 16-bit little-endian) - number of free entries in the block    |
|        8           2      Number of tags - 1 (start of free space?)                                |
|        10          2      Number of tag slots (i.e. deducting strings at the end)                  |
|        12          2      (Short) number of keys following                                         |
|      14-17         4      reduced SHA-1 checksum for integrity verification (\*)                   |
|       18-?                (MSB of byte 18 - entry 0) - allocation map (1 for an allocated entry)   |
|   ------------ ---------- ------------------------------------------------------------------------ |
+----------------------------------------------------------------------------------------------------+

\*) The bytes are computed as follows: calculate SHA1 of a block with checksum bytes zeroed, and then XOR the 20 bytes of the SHA-1 into 4 bytes of checksum. Basically, those bytes are the only protection for data contents (DREG).

##### 26.16.1.2 [  Subdirectory]{#sec26.16.1.2}

To enter the directory, a lookup in IREG to retrieve the sector indices is required.

+:---------------------------------------------------------------------:+
|   ------------ ---------- ------------------------------------------  |
|    **offset**   **size**  **description**                             |
|        0           1      =0x01 (Entry Type)                          |
|        1           31     directory name (null-terminated string )    |
|   ------------ ---------- ------------------------------------------  |
+-----------------------------------------------------------------------+

##### 26.16.1.3 [  Integer]{#sec26.16.1.3}

+:---------------------------------------------------------------------:+
|   ------------ ---------- -------------------------------             |
|    **offset**   **size**  **description**                             |
|        0           1      =0x02 (Entry Type)                          |
|        1           27     name                                        |
|        28          4      (little-endian, signed) value               |
|   ------------ ---------- -------------------------------             |
+-----------------------------------------------------------------------+

##### 26.16.1.4 [  String]{#sec26.16.1.4}

+:-------------------------------------------------------------------------------------------------:+
|   ------------ ---------- ----------------------------------------------------------------------- |
|    **offset**   **size**  **description**                                                         |
|        0           1      =0x03 (Entry Type)                                                      |
|        1           27     name                                                                    |
|        28          2      (little endian, unsigned) length value (includes the terminating NUL)   |
|        30          1      flag byte of unknown content                                            |
|        31          1      starting DREG entry index                                               |
|   ------------ ---------- ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------------------+

The starting index is the index of the (32-byte) DREG entry in the current block that holds the beginning of the string contents. Remember that string contents can span arbitrarily many entries, and even sectors - they just have to fit in a single block.

+:---------------------------------------------------------------------:+
|   ------------ ---------- -----------------                           |
|    **offset**   **size**  **description**                             |
|        0           32     String Contents                             |
|   ------------ ---------- -----------------                           |
+-----------------------------------------------------------------------+

##### 26.16.1.5 [  Secret]{#sec26.16.1.5}

+:-------------------------------------------------------------------------------------------------:+
|   ------------ ---------- ----------------------------------------------------------------------- |
|    **offset**   **size**  **description**                                                         |
|        0           1      =0x04 (Entry Type)                                                      |
|        1           27     name                                                                    |
|        28          2      (little endian, unsigned) length value (includes the terminating NUL)   |
|        30          1      flag byte of unknown content                                            |
|        31          1      starting DREG entry index                                               |
|   ------------ ---------- ----------------------------------------------------------------------- |
+---------------------------------------------------------------------------------------------------+

The starting index is the index of the (32-byte) DREG entry in the current block that holds the beginning of the string contents. Remember that string contents can span arbitrarily many entries, and even sectors - they just have to fit in a single block.

+:---------------------------------------------------------------------:+
|   ------------ ---------- -----------------                           |
|    **offset**   **size**  **description**                             |
|        0           32     String Contents                             |
|   ------------ ---------- -----------------                           |
+-----------------------------------------------------------------------+

#### 26.16.2  Tools

- `parsedreg2` (Skylark, Freeplay)
- `fixupdreg2` (Skylark, Freeplay) recalculate SHA1 hashes used to ensure data integrity

### 26.17  CER

ordinal base64 encoded certificate, not encrypted.

### 26.18  DIC

### 26.19  flash

raw flash image format used by the \"Undiluted Platinum\" Modchip flasher. Contains a linear image of the full Flashrom content (data and spare areas interleaved for each physical page)

### 26.20  ISO

plain UMD Image. contains a linear image of all sectors of a UMD (unused sectors at the end might be omitted)

### 26.21  DAX

compressed ISO Image used by \"DAX ISO Loader\"

### 26.22  CSO

compressed ISO Image used by \"Devhook\"

### 26.23  ezip

compressed ISO Image used by \"Epsilon BIOS\"
