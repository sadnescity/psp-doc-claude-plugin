#!/usr/bin/env python3
"""Build the psp-doc Claude Code plugin.

Turns the chapters of "yet another PlayStationPortable Documentation"
(hitmen.c02.at/files/yapspd) into one skill per chapter, the same shape the
psx-spx plugin has for the PlayStation.

    python3 build_plugin.py fetch     # download the chapters into html/
    python3 build_plugin.py build     # html/ -> skills/<name>/SKILL.md

Needs pandoc for the HTML to markdown pass.
"""

import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

BASE = "https://hitmen.c02.at/files/yapspd/psp_doc"
HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "html")
SKILLS = os.path.join(HERE, "skills")
# Optional hand-written preamble per skill: intro/<name>.md goes in right after
# the frontmatter. The body below it stays the source text, so the chapter can
# still be quoted; the preamble is where the orientation goes.
INTRO = os.path.join(HERE, "intro")
# Skills written by us rather than converted: copied over the generated ones, so
# that wiping skills/ and rebuilding cannot lose them.
HANDWRITTEN = os.path.join(HERE, "handwritten")
HTML_UPSPD = os.path.join(HERE, "html_upspd")

# A second source: the uofw/upspd document collection. YAPSPD is the backbone,
# but it has nothing on the caches and its register chapter is thinner than
# PSPTEK. Downloaded by hand into html_upspd/ -- see README.
UPSPD = [
    ("PSPTEK.htm", "psptek-registers",
     "PSP hardware components and registers, device by device, with addresses and bit fields. Fuller than the hardware-registers chapter of YAPSPD; use it when that one comes up short."),
    ("PSP_cache-howto.html", "cache",
     "The PSP data and instruction caches: how they work, the uncached 0x40000000 mirror, writeback and invalidation, and when code has to force them. Use when memory reads stale values, when writing code at run time, or when a patch that works on the emulator does not on hardware -- the PSX has no such cache, so none of this has a PSX counterpart."),
    ("ModuleTutorialv1.pdf", "modules-and-patching",
     "PSP modules in practice: ELF, PRX and EBOOT, module entry points and module info, exports and imports, NIDs, and how a loaded module is patched at run time through its export and stub tables. Use when working out how a module is loaded or how one hooks another."),
]

# chapter number -> (skill name, description). The description is what Claude
# reads to decide whether the chapter is worth opening, so it says what is in
# it and when it helps.
CHAPTERS = {
    1:  ("about", "What this PSP documentation covers and how it was put together. Background only; the technical chapters are the other skills."),
    2:  ("system-overview", "PSP-1000 specification sheet: CPU and bus clocks, memory sizes, screen, model and box codes, and accessories. Use for the shape of the machine. Later models are covered in psptek-registers."),
    3:  ("hardware-overview", "PSP mainboard revisions and chips, the WiFi daughterboard, the headphone remote, Memory Stick and Talkman microphone hardware. Use when identifying a component or tracing a signal on the board."),
    4:  ("cpu", "PSP CPU (Allegrex, MIPS32 R4000-based): registers, debug registers, COP0 system control, COP1 FPU, COP2 VFPU, instruction format, MIPS and Allegrex-only instructions. Use when writing or reading MIPS assembly for the PSP, decoding an opcode, or checking how an instruction differs from the PSX R3000A."),
    5:  ("media-engine", "The Media Engine, the PSP's second Allegrex core: its memory maps, its COP0 registers, and how code tells which core it runs on. Use when code runs on the ME rather than the main CPU. Starting the ME and signalling between the CPUs are in hardware-registers and exceptions."),
    6:  ("vme", "The Virtual Mobile Engine, the reconfigurable coprocessor. Use when tracing work that is neither on the CPU nor on the ME."),
    7:  ("memory-map", "PSP address space: RAM, VRAM, scratchpad, hardware registers, kernel and user segments, cached and uncached mirrors. Use when working out what an address is, or why a pointer has 0x40000000 added to it."),
    8:  ("hardware-registers", "The hardware register blocks device by device, with addresses and bit meanings. Use when code writes to a register in the 0xBC000000 range and you need to know what it does."),
    9:  ("exceptions", "CPU exception processing: vectors, causes, the exception handler and how the kernel dispatches. Use when the machine traps and you need to read the cause."),
    10: ("video", "PSP VRAM basics: VRAM at 0x04000000, the 16- and 32-bit pixel formats, the 480x272 screen inside a 512-pixel virtual width, and the four VRAM mirrors, one of which hands back a linearised depth buffer. Use when turning a framebuffer or texture address into pixels or back, or reading the depth buffer out of VRAM. Display modes and the LCD controller are not here: see psptek-registers."),
    11: ("graphics-3d", "The Graphics Engine: display list commands, vertex formats, texture and blending state. Use when following what the GE draws, or reading a GE command list."),
    12: ("audio", "Audio hardware and the sound output path. Use when working with samples, channels or the audio ring buffer."),
    13: ("infrared", "The infrared port and its protocol."),
    14: ("wlan", "The WLAN hardware and its interface."),
    15: ("usb", "The USB port, its controller and the device modes the PSP offers."),
    16: ("umd", "The UMD drive: commands, sectors and how discs are read."),
    17: ("memory-stick", "The Memory Stick interface and its controller."),
    18: ("headphone-remote", "The PSP headphone and remote control port: audio input and the remote's serial communication. Use when working with the remote or its SIO protocol."),
    19: ("flash-memory", "The PSP internal NAND flash: physical layout, user and spare areas, the IPL area, ID storage and the FAT partitions. Use when reading a NAND dump or locating the IPL or ID storage in it."),
    20: ("flash0-structure", "What lives in flash0, the PSP system partition: certificates, dictionaries, system fonts, kernel modules and boot configurations (pspbtcnf), VSH modules and resources. Use when looking for a firmware module, a system font or a boot configuration file."),
    21: ("flash1-structure", "What lives in flash1, the PSP settings partition: dictionaries, the system registry and VSH themes. Use when looking for system settings in a flash dump."),
    22: ("memory-stick-structure", "The directory layout the PSP expects on a Memory Stick: saves, games, music, photos and the other root folders. Use when locating save data or a game on a Memory Stick."),
    23: ("umd-game-structure", "How a PSP UMD game disc is laid out: the PSP_GAME tree, UMD_DATA.BIN, the XMB metadata files and PARAM.SFO, SYSDIR with BOOT.BIN and EBOOT.BIN, and USRDIR. Use when finding the executable to patch or the game's data files on a UMD image. Nothing on ISO9660 or the sector layout."),
    24: ("umd-video-structure", "How a PSP UMD video disc is laid out."),
    25: ("umd-audio-structure", "How a PSP UMD audio disc is laid out."),
    26: ("file-formats", "PSP file formats: PRX sections, export and import tables, the custom relocation format and the ~PSP header of encrypted executables, then PBP, PARAM.SFO, PSAR and the PGF font format. Use when reading or rebuilding an executable, or when a relocation has to be resolved by hand."),
    27: ("graphic-formats", "PSP pixel formats: the bit layout of the direct colour formats (1555, 4444, 565 and 8888), texture swizzling, and the PSP's DXT1/DXT3/DXT5 block layout. Use when decoding a texture or CLUT dumped from VRAM, or when a swizzled texture comes out shredded. Font formats (PGF) are in file-formats."),
    28: ("boot-process", "PSP boot sequence: cold boot through the embedded bootstrap and the IPL stages to the VSH, and Load Exec, the full reboot into game mode off pspbtcnf_game.txt. Use when working out which kernel modules a game runs against, or what happens between sceKernelLoadExec and the game. How BOOT.BIN itself is loaded is not covered."),
    29: ("kernel", "PSP kernel chapter: device and filesystem names (msstor:, ms0:, umd0:, isofs:, flash0:, flash1:, host0:), the layout of kernel return codes with the table of error values, and the firmware history from 1.0 to 3.03 with the early exploits. Use when turning a negative return value into an error name, or when working out which device a path reads from. Nothing on threads, syscalls or sceKernel functions: see modules-and-patching."),
    30: ("modchips", "PSP hardware modifications: Undiluted Platinum, the Multi Firmware Module and homemade flash interfaces. Historical."),
    31: ("appendix", "PSP appendix: a GCC and binutils quick how-to (compile, link, strip, convert to a plain binary, addr2line, building a cross compiler, linker script, startup code), plus lists of games and developers. Use when setting up a toolchain to build PSP code."),
    32: ("references", "Where the documentation's own information came from."),
    33: ("credits", "Who wrote the documentation."),
}


# Chapters too big to be one skill. Each entry is a list of
# (name, description, first heading kept, first heading of the next piece);
# None means "from the top" or "to the end". The same idea psx-spx uses.
SPLITS = {
    "cpu": [
        ("cpu", "PSP CPU registers: the 32 general purpose registers and their calling convention, the debug registers, and COP0 system control. Use when reading MIPS assembly for the PSP or when code touches a coprocessor 0 register.", None, "### 4.4"),
        ("cpu-fpu-vfpu", "The PSP floating point units: COP1 (FPU) status and control registers, and COP2 (VFPU) registers and matrices. Use when a routine does floating point or vector work.", "### 4.4", "### 4.6"),
        ("cpu-instructions", "PSP instruction encoding: the instruction format, the MIPS instructions YAPSPD documents, the Allegrex-only ones (halt, mfic, mtic) and the VFPU instruction set. Use when decoding an opcode by hand. For what the Allegrex has and the PSX R3000A has not, read allegrex-vs-r3000a first: this chapter is thin on that.", "### 4.6", "### 4.10"),
        ("cpu-cache", "YAPSPD's cache chapter, which reproduces Jeremy Fitzhardinge's HOWTO almost verbatim and drops its opening section along the way. Read the cache skill instead: it is the same text, complete and without the transcription slips. Kept only so the chapter is not missing.", "### 4.10", None),
    ],
    "graphics-3d": [
        ("ge-overview", "Graphics Engine basics: command format, the GE float encoding, pointers, and the registers that switch features on. Read this before any of the ge-* command skills.", None, "#### 11.5.1"),
        ("ge-flow-and-vertices", "GE commands for display list flow and geometry: VADDR, IADDR, PRIM, BEZIER, SPLINE, BBOX, JUMP, BJUMP, CALL, RET, END, SIGNAL, FINISH, BASE, vertex type, regions, bones, the world/view/projection matrices, and scale and offset. Use when following what a display list draws.", "#### 11.5.1", "#### 11.5.47"),
        ("ge-lighting", "GE commands for lighting and materials: shading mode, material colours, ambient, diffuse, specular, light types, positions, directions, attenuation and per-light colours. Use when a model is lit or coloured wrongly, or when reading the lighting commands of a display list.", "#### 11.5.47", "#### 11.5.118"),
        ("ge-textures", "GE commands for buffers and textures: frame and depth buffer addresses, the eight texture buffers and their widths, CLUT, texture sizes, mapping, mode, pixel format, filtering, wrapping, and the fog registers. Use when working out where a texture is in VRAM or how it is sampled.", "#### 11.5.118", "#### 11.5.169"),
        ("ge-raster", "GE commands for rasterisation and testing: pixel format, clear mode, scissor, depth range, colour and alpha tests, stencil, blending, dithering, logic op, masks, and the block transfer commands. Also the texture cache and memory bandwidth notes. Use when working out why pixels are clipped, discarded, blended or copied the way they are.", "#### 11.5.169", None),
    ],
    "exceptions": [
        ("exceptions", "PSP exception processing: the cause register and its codes, the reset vector, the EBASE vector for interrupts and syscalls, and the error handler. Use when the machine traps and you need to read why.", None, "### 9.5"),
        ("exception-handler", "The exception handler itself, disassembled and annotated, and the debug exception vectors. Use when following what the firmware does after a trap.", "### 9.5", None),
    ],
    "hardware-registers": [
        ("hardware-registers", "PSP hardware registers, first half: memory protection, system config, interrupt controller, profiler, Media Engine control and NAND flash, with addresses and bit fields. Use when a routine stores somewhere in the 0xBC000000-0xBFFFFFFF range and you need the device behind it; psptek-registers is fuller on most of these.", None, "### 8.7"),
        ("hardware-registers-crypto-io", "PSP hardware registers, second half: the KIRK decryption engine, GPIO and the two UARTs, including the headphone/remote SIO. Use when following how an EBOOT, a save or a UMD is decrypted, or when working with the remote's serial port.", "### 8.7", None),
    ],
}


def taglia(corpo, inizio, fine):
    """The piece of corpo between two headings, with the chapter title kept."""
    righe = corpo.split("\n")
    titolo = righe[0] if righe and righe[0].startswith("#") else None

    def indice(p):
        if p is None:
            return None
        for i, r in enumerate(righe):
            if r.startswith(p):
                return i
        raise SystemExit("confine non trovato: %s" % p)

    a = indice(inizio)
    b = indice(fine)
    pezzo = righe[(a if a is not None else 0):(b if b is not None else len(righe))]
    if titolo and a is not None:
        pezzo = [titolo, ""] + pezzo
    return "\n".join(pezzo).strip() + "\n"


def fetch():
    os.makedirs(HTML, exist_ok=True)
    for n in sorted(CHAPTERS):
        dest = os.path.join(HTML, "chap%d.html" % n)
        if os.path.exists(dest):
            continue
        url = "%s/chap%d.html" % (BASE, n)
        with urllib.request.urlopen(url, timeout=30) as r:
            open(dest, "wb").write(r.read())
        print("scaricato", url)
        time.sleep(0.3)


def pulisci(t):
    """pandoc leaves the anchors and the index links of the source behind."""
    t = re.sub(r'\[([\d.]+)\]\{#sec[\d.]+\}', r'\1', t)     # [4.1]{#sec4.1} -> 4.1
    t = re.sub(r'\n::: idx\n.*?\n:::\n', '\n', t, flags=re.S)  # the "index" box
    t = re.sub(r'\n:::+[^\n]*\n', '\n', t)
    t = re.sub(r'\[index\]\(index\.html[^)]*\)', '', t)
    t = re.sub(r'\n\\\n', '\n', t)                          # stray line breaks
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip() + "\n"


def build_upspd():
    for src, nome, descr in UPSPD:
        p = os.path.join(HTML_UPSPD, src)
        if not os.path.exists(p):
            print("manca", p); continue
        if src.endswith(".pdf"):
            corpo = subprocess.run(["pdftotext", "-layout", p, "-"],
                                   capture_output=True, text=True, check=True).stdout
            corpo = re.sub(r'\n{3,}', '\n\n', corpo).strip() + "\n"
        else:
            md = subprocess.run(
                ["pandoc", "-f", "html", "--wrap=none",
                 "-t", "markdown-raw_html-native_divs-native_spans", p],
                capture_output=True, text=True, check=True).stdout
            corpo = pulisci(md)
        scrivi(nome, descr, corpo)


def build():
    for n, (nome, descr) in sorted(CHAPTERS.items()):
        src = os.path.join(HTML, "chap%d.html" % n)
        if not os.path.exists(src):
            print("manca", src); continue
        md = subprocess.run(
            ["pandoc", "-f", "html", "--wrap=none",
             "-t", "markdown-raw_html-native_divs-native_spans", src],
            capture_output=True, text=True, check=True).stdout
        corpo = pulisci(md)
        if corpo.count("\n") < 20:
            # some chapters were left as stubs in 2006: a skill with nothing in
            # it only gets in the way when Claude picks one
            print("%-26s saltato, e' uno stub" % nome)
            continue
        if nome in SPLITS:
            for nome2, descr2, a, b in SPLITS[nome]:
                scrivi(nome2, descr2, taglia(corpo, a, b))
        else:
            scrivi(nome, descr, corpo)


def scrivi(nome, descr, corpo):
    cappello = os.path.join(INTRO, nome + ".md")
    if os.path.exists(cappello):
        corpo = open(cappello, encoding="utf-8").read().strip() + "\n\n---\n\n" + corpo
    d = os.path.join(SKILLS, nome)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("---\nname: %s\ndescription: \"%s\"\n---\n\n%s" % (nome, descr, corpo))
    print("%-26s %6d righe" % (nome, corpo.count("\n")))


if __name__ == "__main__":
    # skills/allegrex-vs-r3000a is written by hand, not generated: YAPSPD's own
    # instruction chapter documents three MIPS instructions and stops there.
    azione = sys.argv[1] if len(sys.argv) > 1 else "build"
    if azione == "fetch":
        fetch()
    else:
        build()
        build_upspd()
        for f in sorted(os.listdir(HANDWRITTEN)) if os.path.isdir(HANDWRITTEN) else []:
            if not f.endswith(".md"):
                continue
            nome = f[:-3]
            d = os.path.join(SKILLS, nome)
            os.makedirs(d, exist_ok=True)
            shutil.copyfile(os.path.join(HANDWRITTEN, f), os.path.join(d, "SKILL.md"))
            print("%-26s scritta a mano" % nome)
