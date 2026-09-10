The second half of chapter 9: the dispatch routine the vectors call, the
32-entry handler table, in which only interrupt, syscall and error are live and
every other slot points at a hang loop, the frame the error path saves
registers into, the interrupt path with its numbered interrupt list and the two
thread-manager routines it calls, the syscall path with its table header and
frame, and the debug exception vectors with their sub-handlers.

Worth opening when you need to know where a trapped register value ends up, or
what state the machine is left in after a fault; the table of hang entries is
why an unhandled exception looks like a freeze rather than a message.

All of it is annotated pseudocode from one firmware dump, at kernel addresses,
so it explains behaviour rather than offering addresses to patch. The same
interrupt list is in psptek-registers, there next to the flag and mask
registers that raise the interrupts; the two disagree on the names of the USB
entries, and PSPTEK's are the ones whose names match their descriptions.
