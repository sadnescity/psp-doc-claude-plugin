# psp-doc

The PSP counterpart of the `psx-spx` plugin: one skill per chapter of
**yet another PlayStationPortable Documentation**, so the hardware reference is
at hand while working on PSP code instead of in a browser.

    python3 build_plugin.py fetch     # chapters -> html/
    python3 build_plugin.py build     # html/ and html_upspd/ -> skills/<name>/SKILL.md

`html/` holds the YAPSPD chapters, fetched by the script. `html_upspd/` holds
three documents from the uofw/upspd collection, downloaded by hand from
https://uofw.github.io/upspd/docs/ because YAPSPD has nothing on the caches and
its register chapter is thinner than PSPTEK.

Thirty-eight skills. Most are generated from a chapter; the four biggest
chapters — CPU, Graphics Engine, exceptions and hardware registers — are split
at their own section boundaries, and seven chapters left as stubs by the
original authors are skipped rather than shipped empty.

Two things are ours rather than converted. `handwritten/allegrex-vs-r3000a.md`
is a skill we wrote, because both sources stop short exactly where it matters:
YAPSPD documents three MIPS instructions and leaves the rest to the MIPS
manuals. And `intro/<name>.md` holds a short preamble that the build puts
between the frontmatter and the archived text — what the chapter really covers,
what it is good for, and where it is thin or overlaps another skill. The text
below the preamble stays as it was written, so it can still be quoted.

The source's images are not shipped. `figures/<file>.md` holds a text rendering
of each one (pin tables and block diagrams transcribed, photos described), and
the build puts it where the `![](file)` reference was; an image without one
stops the build.

## Why it is worth having

The PSP is not a PSX with a bigger screen: the CPU is an Allegrex, a MIPS32
R4000-based core, where the PSX has an R3000A. It has instructions the PSX has
not — the branch-likely `beql`/`bnel` above all, plus `ext`, `ins`, `seb`,
`seh`, `rotr`, `movz`, `movn` — and reading one of those as data is how a patch
silently breaks a jump. `skills/cpu` is the chapter that settles those
questions; `skills/memory-map` and `skills/file-formats` cover the address
space and the PRX/ELF layout the relocations live in.

## Sources

- YAPSPD: https://hitmen.c02.at/files/yapspd/psp_doc/index.html
- uofw/upspd documents: https://uofw.github.io/upspd/docs/ — PSPTEK (registers),
  the cache HOWTO by Jeremy Fitzhardinge, and the module/patching tutorial.
  `psp_doc.pdf` there is YAPSPD itself in PDF, so it is not used twice.
- worth keeping beside it, not included here:
  - PSDevWiki, Allegrex: https://www.psdevwiki.com/psp/Allegrex
  - uofw/upspd wiki: https://github.com/uofw/upspd/wiki
  - VFPU: https://pspdev.github.io/vfpu-docs/

## Credit

The chapters are not ours. **YAPSPD** was written by groepaz/hitmen and the
documents under `html_upspd/` come from the uofw/upspd collection: PSPTEK by
Alex Marshall, the cache HOWTO by Jeremy Fitzhardinge, and the module tutorial
by Anissian. None of them carries a licence; they are reproduced here whole and
credited, and every skill says at the top which document it comes from. What is
ours is the packaging: the build script, the preambles under `intro/`, and the
hand-written `allegrex-vs-r3000a`. If an author would rather not be mirrored
here, say so and the chapter goes.
