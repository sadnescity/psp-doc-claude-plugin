---
name: umd-game-structure
description: "How a UMD game disc is laid out: the ISO, PARAM.SFO, the EBOOT and the data files."
---

Chapter 23, fifty lines of which half are a file list: the /PSP_GAME tree, the
field table of UMD_DATA.BIN whose entries are separated by 0x7c, the XMB
metadata in PSP_GAME (ICON0.PNG, ICON1.PMF, PARAM.SFO, SND0.AT3, PIC0.PNG,
PIC1.PNG), SYSDIR with EBOOT.BIN encrypted beside BOOT.BIN in the clear, and
USRDIR, whose contents are whatever the game put there.

It settles one question worth settling: the executable to patch is
PSP_GAME/SYSDIR/BOOT.BIN, and everything else on the disc is game-specific.

The rest is thin. The UMD_DATA.BIN table has columns for start, end and size but
only start and size are filled, and the range from 0x11 to 0x1c is left
undescribed. There is nothing here on ISO9660, on the sector layout, or on
taking an image apart and putting it back together, and no other chapter covers
that either. PARAM.SFO is listed without a description; its format, and the ~PSP
header of the encrypted EBOOT, are in file-formats. Video and audio discs are
separate chapters, umd-video-structure and umd-audio-structure.

---

## 23  UMD Game Structure

`/PSP_GAME`\
`  /SYSDIR`\
`  /USRDIR`\

### 23.1  Root Directory

- `UMD_DATA.BIN` \
   \
  +:----------------------------------------------------------------------------:+
  |   ----------- --------- ---------- ----------------------------------------- |
  |    **start**   **end**   **size**  **description**                           |
  |     `0x00`                `0x0b`   Gamecode (terminated by `0x7c`)           |
  |     `0x0b`                `0x11`   unique disk id (terminated by `0x7c`)     |
  |     `0x1c`                `0x05`   number of disk ? (terminated by `0x7c`)   |
  |     `0x21`                `0x0f`   ? (terminated by `0x7c`)                  |
  |   ----------- --------- ---------- ----------------------------------------- |
  +------------------------------------------------------------------------------+

#### 23.1.1  PSP_GAME Subdirectory

- `ICON0.PNG` \
  thumbnail icon
- `ICON1.PNG` \
  thumbnail icon highlighted
- `ICON1.PMF` \
  movie icon highlighted
- `PARAM.SFO`\
- `SND0.AT3` \
  ambient sound
- `PIC0.PNG`\
- `PIC1.PNG`\
  background image

note: the files in this directory resemble the contents of the PBP fileformat (see fileformats section)

##### 23.1.1.1 [  Sysdir Subdirectory]{#sec23.1.1.1}

- `EBOOT.BIN`\
  encrypted main executable
- `BOOT.BIN`\
  main executable

##### 23.1.1.2 [  Usrdir Subdirectory]{#sec23.1.1.2}

contains the \'user\' game files which can be different for any game.
