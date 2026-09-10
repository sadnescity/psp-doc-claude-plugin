YAPSPD's chapter 5, and one of the thinnest in the book: four observations
hedged with "appears to", the Media Engine's physical and virtual memory maps
(2MB of RAM of its own, main memory shared at the address the main CPU uses),
and its COP0 register list. The COP0 control-register and COP1 sections are
headings with nothing under them.

What it settles directly is the question of which core code is running on: one
COP0 register reads 0 on the main CPU and 1 on the ME, and the reset vector in
exceptions branches on exactly that. Whether a routine could run on the ME at
all is better answered from psptek-registers, whose spec sheet is where it says
the ME has an FPU but no VFPU.

Starting the ME and handing work to it is not documented here. The registers
involved, the cross-CPU interrupt, the shared semaphore and the reset and
bus-clock enables, are in hardware-registers under system config, and exceptions
walks the ME reset handler step by step. Note also that the block YAPSPD labels
ME Control at 0xBCC00000 is what psptek-registers calls the VirtualMobileEngine
controller; both describe the same four offsets and both are nearly empty.
