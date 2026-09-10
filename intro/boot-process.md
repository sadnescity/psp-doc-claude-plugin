Chapter 28, one of the shortest in YAPSPD: cold boot in three stages, where the
embedded bootstrap copies stage 1 to RAM, stage 1 decrypts stage 2, and stage 2
boots the PRXs listed in /kd/pspbtcnf.txt before launching the VSH; then Load
Exec, the path from sceKernelLoadExec down through LoadExecAction to code
gunzipped to 0x88C00000 and jumped to, which brings the machine back up in Game
Mode off /kd/pspbtcnf_game.txt.

The point worth taking away is that starting a game is a full reboot into a
different module set, not an exec inside the running system, so the kernel
modules a game runs against are the ones that file names.

It stops there. Everything after "launches the Game" is missing: nothing on how
BOOT.BIN is read off the UMD, decrypted, relocated, or where its segments land,
which is exactly the part that matters for patching one. Section 28.4,
reboot.prx, is a heading with no text under it. The address space those segments
land in is in memory-map, the shape of the executable in file-formats, and the
linking the loader performs in modules-and-patching.
