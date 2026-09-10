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
