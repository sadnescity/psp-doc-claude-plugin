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
