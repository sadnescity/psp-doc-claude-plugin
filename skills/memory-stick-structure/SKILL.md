---
name: memory-stick-structure
description: "The directory layout the PSP expects on a Memory Stick: saves, games, music, photos and the other root folders. Use when locating save data or a game on a Memory Stick."
---

Chapter 22, a directory map of the Memory Stick as early firmware used it: /PSP
with GAME, MUSIC, PHOTO and SAVEDATA, MP_ROOT for video clips, HIFI and CONTROL
for DRM-protected ATRAC3, DCIM and MISC left behind by a Sony camera. The
savedata part is the most detailed: one directory per product code, holding
ICON0.PNG, an optional ICON1.PMF, PIC1.PNG and SND0.AT3, a PARAM.SFO of category
MS, and the game's own save files under whatever names it chose.

For patching a game executable this is peripheral. It matters for where a
rebuilt EBOOT.PBP goes, and for what a save directory has to look like when
checking that a patched build still reads its saves.

It describes the stock layout and stops there. SYSTEM and BROWSER appear in the
directory tree at the top with no section describing them, and the folders that
custom firmware conventions introduced are absent — PSP/GAME150 turns up only in
passing, in the tutorial under modules-and-patching. The author records
ICON1.PMF as an unknown format and admits never having got a video clip to play.
The formats of the files themselves, PBP, PARAM.SFO and AT3, are in
file-formats.

---

## 22  Memory Stick Structure

`/PSP`\
`  /GAME`\
`    /UPDATE`\
`  /MUSIC`\
`  /PHOTO`\
`  /SAVEDATA`\
`  /SYSTEM`\
`    /BROWSER`\
`/MP_ROOT`\
`  /100MNV01`\
`  /01MAQ100`\
`  /100MAQ10`\
`/HIFI`\
`/CONTROL`\
`  /PACKAGES`\
`    /PKGxxxxx`\
`/DCIM`\
`  /101MSDCF`\
`/MISC`\

### 22.1  Root Directory

In the root directory there are three entries which are of relevance to the PSP. The first is the file `MEMSTICK.IND` (or `MSTK_PRO.IND`) which just seems to be a indication that the stick is formatted (it is not specific to the PSP). The second is the directory psp which contains subdirectories for the different types of data used by the PSP. These are game, music, photo, and savedata. Not all subdirectories may exist if no data of the corresponding type is stored. The contents of the subdirectories are detailed in the following sections. In addition, there may be a mp_root directory in the root. This directory is for storing video, and should contain only a subdirectory called 100mnv01.

#### 22.1.1  PSP Subdirectory

##### 22.1.1.1 [  Game Subdirectory]{#sec22.1.1.1}

The game directory is for PSP software to be run directly from the memory stick. The Files are in PBP format (see Fileformats Section)\
    **[22.1.1.1.1  Update Subdirectory]{#sec22.1.1.1.1}  ** official Firmware Updates should be placed here.

##### 22.1.1.2 [  Music Subdirectory]{#sec22.1.1.2}

The music directory contains audio tracks for the music player. MPEG layer 3 files can be used as long as their filenames end with \".mp3\". ID3 tags are supported and will be displayed by the player. It is possible to create subdirectories to put the tracks in, but only one level of subdirectories is supported.

##### 22.1.1.3 [  Photo Subdirectory]{#sec22.1.1.3}

This directory contains picture files that can be viewed in the photo viewer. The files should be in JPEG format, and the filenames should end with \".jpg\". Like with the music directory, one level of subdirectories is possible.

##### 22.1.1.4 [  Savedata Subdirectory]{#sec22.1.1.4}

This is where the data saved by games goes. Each game creates a subdirectory with the product code of the game (e.g. ILJS00002) to get a private namespace, and then adds the following files to it:

- `ICON0.PNG`\
  A still picture icon in PNG format (24 bits per pixel, 144×80 pixels (standard); 300x170 (maximum))
- `ICON1.PMF`\
  An animated version of the same icon, file format currently unknown. (Optional.)
- `PIC1.PNG`\
  A full-screen background picture for the file manager in PNG format (24 bits per pixel, 480×272 pixels) (Optional.)
- `SND0.AT3`\
  Background music to play in the file manager, ATRAC3plus encoded in a WAV file. (Optional.) must not be larger than 500kb, and not longer than 55 seconds.
- `PARAM.SFO`\
  Metadata about the game, such as parental rating information. This is a PSF file with a category of MS. In addition to this, the game will of course have its actual save data, typically in a file called data.bin although any name could be used as well as multiple files.

#### 22.1.2  MP_Root Subdirectory

##### 22.1.2.1 [  100MNV01 Subdirectory]{#sec22.1.2.1}

Here video clips can be stored for viewing in the video player. According to the manual, the clip should be encoded using MPEG-4 (H.264/AVC MP Level3), but I have not yet found one that works\... The maximum allowed bitrate is specified as 768kbps. Filenames must be on the format m4vnnnnn.mp4, where nnnnn is a 5 digit number. Remember that the mp_root directory should be in the root directory and not in the psp subdirectory. A thumbnail file can optionally be included, and will give a visual indication of the video\'s contents, as well as include any custom title. It must share the filename of the video it belongs to, but ends in a .THM extension instead of .MP4.

##### 22.1.2.2 [  01maq100 Subdirectory]{#sec22.1.2.2}

##### 22.1.2.3 [  100maq10 Subdirectory]{#sec22.1.2.3}

used for AVC on Firmware 2.0 and newer

#### 22.1.3  HIFI Subdirectory

used for DRM Protected ATRAC3 files

- `A3xxxxxx.MSA `\
  ATRAC3 or ATRAC3PLUS song files
- `GPxxxxx.MSF `\
  ATRAC3 or ATRAC3PLUS group info and names
- `PBLIST.MSF `\
- `GPLIST.MSF `\
- `MGCRL.MSF `\
- `0001000A.MSF `\

#### 22.1.4  CONTROL Subdirectory

used for DRM Protected ATRAC3 files

- `NAME.MSF `\

##### 22.1.4.1 [  PACKAGES Subdirectory]{#sec22.1.4.1}

- `DEVICE.SAL `\

    **[22.1.4.1.1  PKGxxxxx Subdirectory]{#sec22.1.4.1.1}  **

- `package.xml `\
  Song information in XML format similar in function to ID3V2 tags

#### 22.1.5  DCIM Subdirectory

used by the Sony Cybershot Camera for Photos in jpg format

#### 22.1.6  MISC Subdirectory

used by the Sony Cybershot Camera, ignored by the PSP
