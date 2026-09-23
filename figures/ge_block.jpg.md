*[Figure: block diagram of the Graphics Engine.]*

- HOSTIF (host interface): an AHB slave port to the outside, raises the Interrupt line, and feeds both the Surface Engine and, directly, the SETUP stage of the Rendering Engine.
- Surface Engine: BLEND -> SUBDIV -> TANDL -> VSORT -> CLIP; CLIP's output goes to SETUP.
- Rendering Engine: SETUP -> DDA -> TXM -> PIXOP -> DRAMIF; DRAMIF <-> eDRAM (2MB).
- BUS MATRIX1: the AHB master port to the outside; connects to HOSTIF, TXM, PIXOP and BUS MATRIX2.
- BUS MATRIX2: connects DRAMIF, BUS MATRIX1 and a second external AHB slave port.
