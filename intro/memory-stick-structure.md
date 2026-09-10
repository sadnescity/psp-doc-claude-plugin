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
