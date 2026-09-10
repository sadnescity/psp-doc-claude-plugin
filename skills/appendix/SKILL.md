---
name: appendix
description: "Tables and odds and ends that did not fit the other chapters."
---

## 31  Appendix

### 31.1  GCC Quick How To

note: the instructions in this chapter are only for dyhards that want to bootstrap their own GCC from vanilla sources. For everyone else a toolchain containing allegrex specific patches is highly recommended. For short: you dont need this :)

#### 31.1.1  compile ASM to object:

`<GCCROOT>/bin/???-elf-as -c `\
`-I <GCCROOT>/???-elf/include -I <additional includes> `\
`testasm.s -o testasm.o`\

#### 31.1.2  compile C to object:

`<GCCROOT>/bin/???-elf-gcc -c `\
`-I <GCCROOT>/???-elf/include -I <additional includes> `\
`-nostdlib testc.c -o testc.o`\

#### 31.1.3  compile C++ to object:

`<GCCROOT>/bin/???-elf-g++ -c `\
`-I <GCCROOT>/???-elf/include -I <additional includes> `\
`-nostdlib -fno-exceptions testcpp.cpp -o testcpp.o`\

#### 31.1.4  link objects

`<GCCROOT>/bin/???-elf-ld -T mips-pspbin.x -o test.elf crt0.o `\
`<GCCROOT>/lib/gcc-lib/???-elf/3.3/crtbegin.o `\
`<GCCROOT>/lib/gcc-lib/???-elf/3.3/crtend.o `\
`testasm.o testc.o testcpp.o -lg -lstdc++ -lm -lc -lnosys` \
 \
you only need to link against crtbegin.o/crtend.o if you are using c++, and you only need -lg,-lstdc++,-lc,-lm if you are actually using these libraries (of course:)). however if you do so, linking against -lnosys as well is essential.

#### 31.1.5  remove unneeded sections (debug info etc) from object

`<GCCROOT>/bin/???-elf-strip -s test.elf`\

#### 31.1.6  convert object to plain binary

`<GCCROOT>/bin/???-elf-objcopy -O binary test.elf test.bin`\

#### 31.1.7  convert absolute address into filename/line number/function

compile with \"-g\" flag, then use\
`<GCCROOT>/bin/???-elf-addr2line -f -e test.elf <address>`\

#### 31.1.8  Building a Crosscompiler

configure options:\
`--target=misel-elf`\
`--with-cpu=r4000`\
`--disable-threads`\
`--enable-languages=c`\
`--disable-shared`\
`--disable-nls`\
`--with-newlib` \
 \
note: a specialised \'allegrex\' port is highly recommended. r4000 (or r5900) will work, but is suboptimal

#### 31.1.9  Linker Script

to do

#### 31.1.10  Startup Code

to do

### 31.2  Games

- AC Formula Front - FromSoftware
- Ape Escape - SCEJ
- Axel Impact - Axis Entertainment Inc.
- Bomberman - Hudson Soft
- BBG - SEED9
- Darkstalkers Chronicle - Capcom
- Derby - SCEJ
- Detective Adventure Jinguji - WorkJam
- Devil May Cry - Capcom
- DoraSlot - Dorasu Corp.
- Dokodemo Issho - SCEJ
- Dynasty Warriors - Koei
- The Evil Village - Now Production
- Far East of Eden - Hudson Soft
- The Gagharv - Bandai
- Ghost in the Shell Stand Alone Complex - SCEJ
- Gran Turismo 4 Mobile - SCEJ
- \- Marvelous Interactive
- Harvest Moon - Marvelous Interactive
- Hot Shots Golf (AKA Everybody\'s Golf) - SCEJ
- Kollon - CyberFront Corp.
- Legend of River King - Marvelous Interactive
- License of Intelligence - Now Production
- \- Marvelous Interactive
- Mah-Jong Fight Club - Konami
- Mah-jong Mate - Success Corp
- Mahjong - Koei
- Makai Wars - Nippon Ichi Software
- Metal Gear Acid - Konami
- Mobile Suit Gundam - Bandai
- Moji-Pittan - Namco
- Monkey Games - SCEJ
- Need For Speed Underground - EA
- New Ridge Racer - Namco
- Pilot Academy - Marvelous Interactive
- Popolocrois Story - SCEJ
- Powerful Proyakyu - Konami
- Pro-wrestling - Yuke\'s
- Project S - Sega
- Puyo Pop Fever - Sega
- Puzzle Bobble - Taito
- RS Revolution - Spike
- \- Hudson Soft
- Romance of the Three Kingdoms - Koei
- Shintenmakai - Idea Factory
- \- Marvelous Interactive
- Shutkou Battle - Genki
- Super Robot Wars - Banpresto
- TGM-K - Akira
- T.O.E. - Namco
- Talkman - SCEJ
- Techniccute - Akira
- Ten No Kagi, Chi No Mon - SCEJ
- Tiger Woods PGA Tour - EA
- Viewtiful Joe - Capcom
- Vulcanus Online - Zepetto Studios
- Winning Eleven (aka Pro-Evolution Soccer) - Konami
- Ys VI - The Ark of Napishtim - Konami

### 31.3  Developers

- FromSoftware
- Axis Entertainment Inc.
- SEED9
- WorkJam
- Capcom
- Dorasu Corp.
- CyberFront Corp.
- Now Production
- Success Corp
- Nippon Ichi Software
- Bandai
- Yuke\'s
- Sega
- Taito
- Spike
- Hudson Soft
- Koei
- Idea Factory
- Marvelous Interactive
- Genki
- Banpresto
- Namco
- Akira
- SCEJ
- EA
- Zepetto Studios
- Konami
- UBI Soft
