---
name: boot-process
description: "From power on to the game: IPL, the loaders and the order modules start in."
---

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

---

## 28  Boot Process

### 28.1  Cold Boot

#### 28.1.1  embedded Bootstrap

does minimal initialization, copies Stage 1 to RAM and executes it.

#### 28.1.2  IPL Stage 1

decrypts and executes Stage 2

#### 28.1.3  IPL Stage 2

initializes the System, boots PRXs in \'VSH Mode\' (from `/kd/pspbtcnf.txt)`and finally launches the VSH.

### 28.2  Load Exec

#### 28.2.1  Stage 1

sceKernelLoadExec

- do some sanity checks\
  return 0x80020064 if called from interrupt handler\
  0x800200d3 on \*file==NULL or other error
- call LoadExec

LoadExec

- start \"LoadExecBody\" as new thread

LoadExecBody

- call LoadExecAction

LoadExecAction

- call sub_FCC

sub_FCC LoadExecAction

- gunzip to `0x88C00000`\
- call `0x88C00000`, execution continues here (no return)

#### 28.2.2  Stage 2

initializes the System, boots PRXs in \'Game Mode\' (from `/kd/pspbtcnf_game.txt)` ,or \'Updater Mode\' (from `/kd/pspbtcnf_updater.txt`) if the Executable is launched from an updater directory, and finally launches the Game or Updater. Similar to IPL Stage 2

### 28.3  Exit Game

initializes the System, boots PRXs in \'VSH Mode\' (from `/kd/pspbtcnf.txt)`and finally launches the VSH.

### 28.4  reboot.prx
