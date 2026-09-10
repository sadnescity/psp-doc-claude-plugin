---
name: flash0-structure
description: "What lives in flash0, the system partition: files, modules and fonts."
---

## 20  Flash Memory Structure (flash0)

`/DATA`\
`  /CERT`\
`/DIC`\
`/FONT`\
`/KD`\
`  /RESOURCE`\
`/VSH`\
`  /ETC`\
`  /MODULE`\
`  /RESOURCE`\

### 20.1  DATA Subdirectory

#### 20.1.1  CERT Subdirectory

Contains lots of certificates. They are ordinal base64 encoded certificate, not encrypted.\

+:--------------------------------------------------------------------------------------------:+
|   ---------------------- ---------- -------------- ----------------------------------- ----- |
|   **Filename**             **Size**                                                          |
|   Class1_PCA_G2_v2.cer         1122 SHA1/RSA1024   VeriSign                             \*1  |
|   Class1_PCA_G3v2.cer          1508 SHA1/RSA2048   VeriSign                             \*1  |
|   Class1_PCA_ss_v4.cer          854 MD2 /RSA1024   VeriSign                             \*1  |
|   Class2_PCA_G2_v2.cer         1126 SHA1/RSA1024   VeriSign                             \*1  |
|   Class2_PCA_G3v2.cer          1504 SHA1/RSA2048   VeriSign                             \*1  |
|   Class2_PCA_ss_v4.cer          848 MD2 /RSA1024   VeriSign                             \*1  |
|   Class3_PCA_G2_v2.cer         1122 SHA1/RSA1024   VeriSign                             \*1  |
|   Class3_PCA_G3v2.cer          1508 SHA1/RSA2048   VeriSign                             \*1  |
|   Class3_PCA_ss_v4.cer          848 MD2 /RSA1024   VeriSign                             \*1  |
|   Class4_PCA_G2_v2.cer         1122 SHA1/RSA1024   VeriSign                             \*1  |
|   Class4_PCA_G3v2.cer          1508 SHA1/RSA2048   VeriSign                             \*1  |
|   RSA1024_v1.cer               1066 SHA1/RSA1024   ValiCert                             \*2  |
|   RSA2048_v3.cer               1233 SHA1/RSA2048   RSA Security                         \*2  |
|   RSA_SecureServer.cer          840 MD2 /RSA1024   RSA Data Security                    \*2  |
|   SCE_CA01.cer                 1387 SHA1/RSA2048   SCEI                                 \*3  |
|   SCE_CA02.cer                 1387 SHA1/RSA2048   SCEI                                 \*3  |
|   SCE_CA03.cer                 1387 SHA1/RSA2048   SCEI                                 \*3  |
|   SCE_CA04.cer                 1387 SHA1/RSA2048   SCEI                                 \*3  |
|   SCE_CA05.cer                 1387 SHA1/RSA2048   SCEI                                 \*3  |
|   VeriSign_TSA_CA.cer          1402 SHA1/RSA1024   VeriSign, Time Stamping Authority    \*4  |
|   ---------------------- ---------- -------------- ----------------------------------- ----- |
+----------------------------------------------------------------------------------------------+

\
1) These are relating to \'Primary Certificate Authority\' certificates from VeriSign. They have specific groups that monitor and certify Certificate Authorities, providing direct trust to CA certificates. These form the root of the trust network for signed code. Pretty much every Windows machine has these for use in Internet Explorer and the like. 2) These are related to the BSAFE technology RSA Security provides. They are likely used for the wireless communications, as BSAFE has wireless security software packages aimed at systems like ARM for things like SSL over WiFi (sound familiar?). I don\'t know if they are linked through Verisign\'s PCAs or form their own root. It would make more sense if they were signed by either Verisign\'s PCAs or by one of Sony\'s CAs. 3) A series of certificates in Sony\'s control, very likely signed by the PCA certificates mentioned above. These are probably used to sign code certificates for developers, and those certificates are included with the games themselves. So code signatures are done by the developer, while encryption is done by Sony. The trust can still be verified by checking the signed game certificate, seeing that it belongs to SCE_CA0x, and then seeing /that/ belongs to Verisign, which is the root trust node. 4)Says exactly what it is on the tin, used to time-stamp things in such a way that it cannot be spoofed. (i.e, Verisign encrypts the time stamp of a signing with their private key, allowing everyone to verify the time stamp, but nobody can make a different time stamp that can be verified correctly without VeriSign\'s key)\
This as a whole is a trust tree, to setup a base list of trusted certificates for the PSP. Anything signed directly by the owners of these certificates, or using a key which has been signed by the owners of these certificates will be trusted. (I.E. can the certificate presented by the game/software to be run be verified as to be connected to these certificates?)

### 20.2  DIC Subdirectory

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   apotp.dic         1346880                                           |
|   atokp.dic          939166                                           |
|   aux0.dic            14886                                           |
|   aux1.dic             9647                                           |
|   aux2.dic             4631                                           |
|   aux3.dic            13172                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

### 20.3  FONT Subdirectory

contains various Fonts used by the PSP OS

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   jpn0.pgf          1679100                                           |
|   ltn0.pgf           123896                                           |
|   ltn1.pgf           113200                                           |
|   ltn10.pgf           58256                                           |
|   ltn11.pgf           55924                                           |
|   ltn12.pgf           61816                                           |
|   ltn13.pgf           58788                                           |
|   ltn14.pgf           64100                                           |
|   ltn15.pgf           59924                                           |
|   ltn2.pgf           129652                                           |
|   ltn3.pgf           115940                                           |
|   ltn4.pgf           132536                                           |
|   ltn5.pgf           121548                                           |
|   ltn6.pgf           138472                                           |
|   ltn7.pgf           124868                                           |
|   ltn8.pgf            56512                                           |
|   ltn9.pgf            54484                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

### 20.4  KD Subdirectory

#### 20.4.1  Kernel Modules

[]{#tth_tAb1}

+-----------------------------------------------------------------------------------------------------------------------------+
|   ---------------------------- ----------------------------- ------------ ---------- ------------- ---------- ------------- |
|   **Module Filename**          **API-Module**                **Format**     **v1.0**                **v1.5**                |
|                                                                             **size**  **version**   **size**   **version**  |
|   ata.prx                      sceATA_ATAPI_driver           \~PSP             13232                               1.2      |
|   audio.prx                    sceAudio_Driver               \~PSP              9040                               1.2      |
|   audiocodec.prx               sceAudiocodec_Driver          \~PSP              3248      1.1                      1.1      |
|   blkdev.prx                   sceBLK_driver                 \~PSP              3712      1.1                      1.1      |
|   chkreg.prx                   sceChkreg                     \~PSP              3488                               1.2      |
|   clockgen.prx                 sceClockgen_Driver            \~PSP              2416      1.1                      1.1      |
|   codec.prx                    sceWM8750_Driver              \~PSP              4096                               1.2      |
|   ctrl.prx                     sceController_Service         \~PSP              5600                               1.2      |
|   display.prx                  sceDisplay_Service            \~PSP              7248                               1.2      |
|   dmacman.prx                  sceDMAManager                 \~PSP              6032                               1.2      |
|   dmacplus.prx                 sceDMACPLUS_Driver            \~PSP              8768                               1.2      |
|   emc_ddr.prx                  sceDDR_Driver                 \~PSP              2384      1.1                      1.1      |
|   emc_sm.prx                   sceNAND_Driver                \~PSP              8080      1.1                      1.1      |
|   exceptionman.prx             sceExceptionManager           \~PSP              3248                               1.2      |
|   fatmsmod.prx                 sceMSFAT_Driver               \~PSP             71760                               1.2      |
|   ge.prx                       sceGE_Manager                 \~PSP              8720                               1.2      |
|   gpio.prx                     sceGPIO_Driver                \~PSP              3184                               1.2      |
|   hpremote.prx                 sceHP_Remote_Driver           \~PSP              6800                               1.2      |
|   i2c.prx                      sceI2C_Driver                 \~PSP              4368      1.1                      1.1      |
|   idstorage.prx                sceIdStorage_Service          \~PSP              7072      1.1                      1.1      |
|   ifhandle.prx                 sceNetIfhandle_Service        \~PSP             10848      1.1                      1.1      |
|   impose.prx                   sceImpose_Driver              \~PSP             32480                               1.2      |
|   init.prx                     sceInit                       \~PSP              7056                               1.2      |
|   interruptman.prx             sceInterruptManager           \~PSP              9872                               1.2      |
|   iofilemgr.prx                sceIOFileManager              \~PSP             11520                               1.2      |
|   isofs.prx                    sceIsofs_driver               \~PSP             23520                               1.2      |
|   lcdc.prx                     sceLCDC_Driver                \~PSP              3328      1.1                      1.1      |
|   led.prx                      sceLED_Service                \~PSP              2448      1.1                      1.1      |
|   lfatfs.prx                   sceLFatFs_Driver              \~PSP             37472                               1.2      |
|   lflash_fatfmt.prx            sceLflashFatfmt               \~PSP              6192      1.1                      1.1      |
|   libatrac3plus.prx            sceATRAC3plus_Library         \~PSP             10192      1.1                      1.1      |
|   libhttp.prx                  SceHttp_Library               \~PSP             36896      1.1                      1.1      |
|   libparse_http.prx            SceParseHTTPheader_Library    \~PSP              3008      1.1                      1.1      |
|   libparse_uri.prx             SceParseURI_Library           \~PSP              8112      1.1                      1.1      |
|   libupdown.prx                SceUpdateDL_Library           \~PSP             10928      1.1                      1.1      |
|   loadcore.prx                 sceLoaderCore                 \~PSP             41168                               1.2      |
|   loadexec.prx                 sceLoadExec                   \~PSP              8016                               1.2      |
|   me_for_vsh.prx               me_for_vsh                    \~PSP              1040      1.1                      1.1      |
|   me_wrapper.prx               sceMeCodecWrapper             \~PSP             13008      1.1                      1.1      |
|   mebooter.prx                 sceMeBooter                   \~PSP            285856      1.1                      1.1      |
|   mebooter_umdvideo.prx        sceMeBooter                   \~PSP            126448      1.1                      1.1      |
|   mediaman.prx                 sceUmd_driver                 \~PSP              8240                               1.2      |
|   mediasync.prx                sceMediaSync                  \~PSP              2816                               1.2      |
|   memab.prx                    sceMemab                      \~PSP             15216                               1.2      |
|   memlmd.prx                   sceMemlmd                     \~PSP              8800                               1.2      |
|   mesg_led.prx                 sceMesgLed                    \~PSP             14128                               1.2      |
|   mgr.prx                      sceMgr_Driver                 \~PSP             20720                               1.2      |
|   modulemgr.prx                sceModuleManager              \~PSP             13824                               1.2      |
|   mpeg_vsh.prx                 sceMpeg_library               \~PSP             19664                               1.2      |
|   mpegbase.prx                 sceMpegbase_Driver            \~PSP              4304                               1.2      |
|   msaudio.prx                  sceMsAudio_Service            \~PSP              8112                               1.2      |
|   mscm.prx                     sceMScm_Driver                \~PSP             16048                               1.2      |
|   msstor.prx                   sceMSstor_Driver              \~PSP             20352                               1.2      |
|   openpsid.prx                 sceOpenPSID_Service           \~PSP              3136                               1.2      |
|   peq.prx                      scePEQ_Library_driver         \~PSP              1728      1.1                      1.1      |
|   power.prx                    scePower_Service              \~PSP             12608                               1.2      |
|   pspnet.prx                   sceNet_Library                \~PSP             27472      1.1                      1.1      |
|   pspnet_adhoc.prx             sceNetAdhoc_Library           \~PSP             20080                               1.2      |
|   pspnet_adhoc_auth.prx        sceNetAdhocAuth_Service       \~PSP             10832                               1.2      |
|   pspnet_adhoc_download.prx    sceNetAdhocDownload_Library   \~PSP              7904      1.1                      1.1      |
|   pspnet_adhoc_matching.prx    sceNetAdhocMatching_Library   \~PSP              9088      1.1                      1.1      |
|   pspnet_adhocctl.prx          sceNetAdhocctl_Library        \~PSP             17968                               1.2      |
|   pspnet_ap_dialog_dummy.prx   sceNetApDialogDummy_Library   \~PSP              2608      1.1                      1.1      |
|   pspnet_apctl.prx             sceNetApctl_Library           \~PSP             22784                               1.2      |
|   pspnet_inet.prx              sceNetInet_Library            \~PSP            130944                               1.2      |
|   pspnet_resolver.prx          sceNetResolver_Library        \~PSP              6880      1.1                      1.1      |
|   pwm.prx                      scePWM_Driver                 \~PSP              1904      1.1                      1.1      |
|   reboot.prx                   sceReboot                     \~PSP             53136                               1.2      |
|   registry.prx                 sceRegistry_Service           \~PSP             16896                               1.2      |
|   rtc.prx                      sceRTC_Service                \~PSP             11136                               1.2      |
|   semawm.prx                   sceSemawm                     \~PSP             34768                               1.2      |
|   sircs.prx                    sceSIRCS_IrDA_Driver          \~PSP              6464      1.1                      1.1      |
|   stdio.prx                    sceStdio                      \~PSP              3744                               1.2      |
|   sysclib.prx                  sceSysclib                    \~PSP              6032                               1.2      |
|   syscon.prx                   sceSYSCON_Driver              \~PSP              9936      1.1                      1.1      |
|   sysmem.prx                   sceSystemMemoryManager        \~PSP             72304                               1.2      |
|   sysmem_uart4.prx             sceSystemMemoryManager        \~PSP             27536                               1.2      |
|   sysreg.prx                   sceSYSREG_Driver              \~PSP              5808      1.1                      1.1      |
|   systimer.prx                 sceSystimer                   \~PSP              2736      1.1                      1.1      |
|   threadman.prx                sceThreadManager              \~PSP             44512                               1.2      |
|   uart4.prx                    sceUart4                      \~PSP              2288                               1.2      |
|   umd9660.prx                  sceUmd9660_driver             \~PSP             17504                               1.2      |
|   umdman.prx                   sceUmdMan_driver              \~PSP             34864                               1.2      |
|   usb.prx                      sceUSB_Driver                 \~PSP             29248                               1.2      |
|   usbstor.prx                  sceUSB_Stor_Driver            \~PSP              8656      1.1                      1.1      |
|   usbstorboot.prx              sceUSB_Stor_Boot_Driver       \~PSP             13088                               1.2      |
|   usbstormgr.prx               sceUSB_Stor_Mgr_Driver        \~PSP             10720                               1.2      |
|   usbstorms.prx                sceUSB_Stor_Ms_Driver         \~PSP              9328      1.1                      1.1      |
|   usersystemlib.prx            sceKernelLibrary              \~PSP              1168      1.1                      1.1      |
|   utility.prx                  sceUtility_Driver             \~PSP              9216                               1.2      |
|   utils.prx                    sceKernelUtils                \~PSP             10272                               1.2      |
|   vaudio.prx                   sceVaudio_driver              \~PSP              2784      1.1                      1.1      |
|   vaudio_game.prx              sceVaudio_driver              \~PSP              1088      1.1                      1.1      |
|   videocodec.prx               sceVideocodec_Driver          \~PSP              3824      1.1                      1.1      |
|   vshbridge.prx                sceVshBridge_Driver           \~PSP              2704      1.1                      1.1      |
|   wlan.prx                     sceWlan_Driver                \~PSP            114480                               1.2      |
|   ---------------------------- ----------------------------- ------------ ---------- ------------- ---------- ------------- |
+-----------------------------------------------------------------------------------------------------------------------------+

\[PSP\] means \~PSP type encrypted file

#### 20.4.2  Boot Configurations

+:-------------------------------------------------------------------------------------------------------------------------:+
|   ---------------------- --------------------------------- ------------ ---------- ------------- ---------- ------------- |
|   **Filename**           **Description**                   **Format**     **v1.0**                **v1.5**                |
|                                                                           **size**  **version**   **size**   **version**  |
|   pspcnf_tbl.txt         List of Possible Configurations   \~PSP               432                                        |
|   pspbtcnf.txt           VSH Configuration                 \~PSP              1584                                        |
|   pspbtcnf_game.txt      Game Configuration                \~PSP              1376                                        |
|   pspbtcnf_updater.txt   Updater Configuration             \~PSP              1600                                        |
|   ---------------------- --------------------------------- ------------ ---------- ------------- ---------- ------------- |
+---------------------------------------------------------------------------------------------------------------------------+

##### 20.4.2.1 [  Configuration Table]{#sec20.4.2.1}

pspcnf_tbl.txt

  -----------------------------------------------------------------------
  `vsh /kd/pspbtcnf.txt`\
  `game /kd/pspbtcnf_game.txt`\
  `updater /kd/pspbtcnf_updater.txt`

  -----------------------------------------------------------------------

##### 20.4.2.2 [  VSH Configuration]{#sec20.4.2.2}

##### 20.4.2.3 [  Game Configuration]{#sec20.4.2.3}

##### 20.4.2.4 [  Updater Configuration]{#sec20.4.2.4}

### 20.5  VSH Subdirectory

#### 20.5.1  ETC Subdirectory

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   jis2ucs.bin        131072                                           |
|   jis2ucs.cbin        16182                                           |
|   ucs2jis.bin        131072                                           |
|   ucs2jis.cbin        33672                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

##### 20.5.1.1 [  Version Info]{#sec20.5.1.1}

+:---------------------------------------------------------------------:+
|   -------------- ------------ ----------                              |
|   **Filename**     **Format**   **Size**                              |
|   index.dat             \~PSP        480                              |
|   version.txt           plain        135                              |
|   -------------- ------------ ----------                              |
+-----------------------------------------------------------------------+

index.dat is used to store version/built information about the current firmware. version.txt is simply the decrypted (plaintext) version of the same data. All the firmware revisions from 1.00 to 2.01 can load decrypted index.dat (aka version.txt) and share the very same index.dat decryption keys while 2.50+ cannot load decrypted index.dat and cannot load old index.dat (featuring another encryption) either. That move was done by sony to prevent downgrading by swapping the index.dat (as it has been done on 2.00) Having a corrupted index.dat in flash0:/vsh/etc/ will result on the psp viewing any eboot/umd (including updaters) as corrupted data and wont load those (this happends on all versions up to 2.50 as far as I could test \<Ookm\>) When using the 2.50 index.dat with 2.00 firmware revision it will see it as corrupted, as the 2.00 firmware does not have the required keys to decrypt the new index.dat files as well as the newer firmwares no longer possess the keys required to decrypt older index.dat or the ability to load those decrypted. The hexadecimal Number in the system: line is exactly the value returned by the `sceKernelDevkitVersion` Syscall.\
    **[20.5.1.1.1  1.0]{#sec20.5.1.1.1}  **

  -----------------------------------------------------------------------
  `release:1.00:`\
  `build:106,1:root@psp-vsh`\
  `system:16214,0x00100000:`\
  `vsh:2004_1104_s16214_p3883_v8335:`

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  `release:1.00: `\
  `build:228,0,3,1,0:root@psp-vsh `\
  `system:17919@release_103a,0x01000300: `\
  `vsh:p4029@special_day1,v9972@special_day1,20041201:`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.2  1.5]{#sec20.5.1.1.2}  **

  -----------------------------------------------------------------------
  `release:1.50:`\
  `build:376,0,3,1,0:root@psp-vsh`\
  `system:20182@release_150,0x01050001:`\
  `vsh:p4201@release_150,v11079@release_150,20050201:`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.3  1.51]{#sec20.5.1.1.3}  **

  -----------------------------------------------------------------------
  `release:1.51:`\
  `build:513,0,3,1,0:root@psp-vsh`\
  `system:22984@release_151,0x01050100:`\
  `vsh:p4388@release_151_sc,v12875@release_151_sc,20050507:`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.4  1.52]{#sec20.5.1.1.4}  **

  -----------------------------------------------------------------------
  `release:1.52:`\
  `build:555,0,3,1,0:root@psp-vsh`\
  `system:23740@release_152,0x01050200:`\
  `vsh:p4421@release_152,v13394@release_152,20050525:`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.5  2.0]{#sec20.5.1.1.5}  **

  -----------------------------------------------------------------------
  `release:2.00:`\
  `build:725,0,3,1,0:root@psp-vsh`\
  `system:26084@release_200,0x02000010:`\
  `vsh:p4705@release_200,v15867@release_200,20050726:`\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.6  2.01]{#sec20.5.1.1.6}  **

  -----------------------------------------------------------------------
  `release:2.01:`\
  `build:822,0,3,1,0:root@psp-vsh`\
  `system:26084@release_200,0x02000010:`\
  `vsh:p4793@release_201,v18444@release_201,20050928:`\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.7  2.5]{#sec20.5.1.1.7}  **

  -----------------------------------------------------------------------
  `release:2.50:`\
  `build:863,0,3,1,0:root@vsh-build`\
  `system:28611@release_250,0x02050010:`\
  `vsh:p4810@release_250,v19039@release_250,20051011:`\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.8  2.6]{#sec20.5.1.1.8}  ** from update eboot:

  -----------------------------------------------------------------------
  `release:2.60:`\
  `build:962,0,3,1,0:root@vsh-build`\
  `system:29904@release_260,0x02060010:`\
  `vsh:p5029@release_260,v20391@release_260,20051125:`\
  `target::WorldWide`

  -----------------------------------------------------------------------

from retail (version I) PSP:

  -----------------------------------------------------------------------
  `release:2.60:`\
  `build:985,0,3,1,0:root@vsh-build`\
  `system:29904@release_260,0x02060010:`\
  `vsh:p5029@release_260,v20603@release_260_2,20051209:`\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.9  2.7]{#sec20.5.1.1.9}  **

  -----------------------------------------------------------------------
  `release:2.70: `\
  `build:1238,0,3,1,0:builder@vsh-build2 `\
  `system:33151@release_270,0x02070010: `\
  `vsh:p5186@release_270,v22631@release_270,20060420: `\
  `target::WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.10  2.71]{#sec20.5.1.1.10}  **

  -----------------------------------------------------------------------
  `release:2.71:`\
  `build:1299,0,3,1,0:builder@vsh-build2`\
  `system:33696@release_271,0x02070110:`\
  `vsh:p5218@release_271,v22873@release_271,20060529:`\
  `target::WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.11  2.8]{#sec20.5.1.1.11}  **\
    **[20.5.1.1.12  2.81]{#sec20.5.1.1.12}  **

  -----------------------------------------------------------------------
  `build:1450,0,3,1,0:builder@vsh-build2`\
  `system:35536@release_281,0x02080110:`\
  `vsh:p5291@release_281,v24983@release_281,20060828:`\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

\
    **[20.5.1.1.13  3.0]{#sec20.5.1.1.13}  **\
    **[20.5.1.1.14  3.01]{#sec20.5.1.1.14}  **

  -----------------------------------------------------------------------
  `release:3.01: `\
  `build:1628,0,3,1,0:builder@vsh-build2 `\
  `system:36993@release_301,0x03000110: `\
  `vsh:p5403@release_301,v27265@release_301,20061122: `\
  `target:1:WorldWide`

  -----------------------------------------------------------------------

#### 20.5.2  MODULE Subdirectory

+:--------------------------------------------------------------------------------------------------------------------:+
|   ---------------------------- ------------------------- --------- ---------- ------------- ---------- ------------- |
|   **Module Filename**          **API-Module**                        **v1.0**                **v1.5**                |
|                                                                      **size**  **version**   **size**   **version**  |
|   auth_plugin.prx              auth_plugin_module          \[PSP\]       5856      1.1                      1.1      |
|   chnnlsv.prx                  sceChnnlsv                  \[PSP\]       8464                               1.2      |
|   common_gui.prx               sceVshCommonGui_Module      \[PSP\]      16944      1.1                      1.1      |
|   common_util.prx              sceVshCommonUtil_Module     \[PSP\]      15392      1.1                      1.1      |
|   dialogmain.prx               sceDialogmain_Module        \[PSP\]      22784      1.1                      1.1      |
|   game_plugin.prx              game_plugin_module          \[PSP\]      33168      1.1                      1.1      |
|   heaparea1.prx                scePafHeaparea_Module       \[PSP\]       1952      1.1                      1.1      |
|   heaparea2.prx                scePafHeaparea_Module       \[PSP\]       1952      1.1                      1.1      |
|   impose_plugin.prx            impose_plugin_module        \[PSP\]       4256      1.1                      1.1      |
|   msgdialog_plugin.prx         sceVshMSDPlugin_Module        plain       8996      1.1                      1.1      |
|   msvideo_plugin.prx           msvideo_plugin_module       \[PSP\]     149184      1.1                      1.1      |
|   music_plugin.prx             music_plugin_module         \[PSP\]     204608      1.1                      1.1      |
|   netconf_plugin.prx           sceVshNetconf_Module        \[PSP\]      39744      1.1                      1.1      |
|   netplay_client_plugin.prx    sceVshGSPlugin_Module       \[PSP\]      16432      1.1                      1.1      |
|   netplay_server_utility.prx   sceVshGSUtility_Module      \[PSP\]      10592                               1.2      |
|   opening_plugin.prx           opening_plugin_module       \[PSP\]       4960      1.1                      1.1      |
|   osk_plugin.prx               sceVshOSK_Module            \[PSP\]      35520      1.1                      1.1      |
|   paf.prx                      scePaf_Module               \[PSP\]     599072      1.1                      1.1      |
|   pafmini.prx                  scePaf_Module               \[PSP\]     513184      1.1                      1.1      |
|   photo_plugin.prx             photo_plugin_module         \[PSP\]      79056      1.1                      1.1      |
|   savedata_auto_dialog.prx     sceVshSDAuto_Module         \[PSP\]      60224      1.1                      1.1      |
|   savedata_plugin.prx          sceVshSDPlugin_Module       \[PSP\]      61344      1.1                      1.1      |
|   savedata_utility.prx         sceVshSDUtility_Module      \[PSP\]      59344      1.1                      1.1      |
|   sysconf_plugin.prx           sysconf_plugin_module       \[PSP\]      42464      1.1                      1.1      |
|   update_plugin.prx            update_plugin_module        \[PSP\]      15840      1.1                      1.1      |
|   video_plugin.prx             video_plugin_module         \[PSP\]     137936      1.1                      1.1      |
|   vshmain.prx                  vsh_module                  \[PSP\]      67040      1.1                      1.1      |
|   ---------------------------- ------------------------- --------- ---------- ------------- ---------- ------------- |
+----------------------------------------------------------------------------------------------------------------------+

#### 20.5.3  RESOURCE Subdirectory

##### 20.5.3.1 [  Background Images]{#sec20.5.3.1}

The background images of the VSH. (60x34 bitmaps).

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   01.bmp               6176                                           |
|   02.bmp               6176                                           |
|   03.bmp               6176                                           |
|   04.bmp               6176                                           |
|   05.bmp               6176                                           |
|   06.bmp               6176                                           |
|   07.bmp               6176                                           |
|   08.bmp               6176                                           |
|   09.bmp               6176                                           |
|   10.bmp               6176                                           |
|   11.bmp               6176                                           |
|   12.bmp               6176                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

##### 20.5.3.2 [  Localized Resources]{#sec20.5.3.2}

+:---------------------------------------------------------------------:+
|   ------------------------------- ----------                          |
|   **Filename**                      **Size**                          |
|   auth_plugin.rco                       4556                          |
|   game_plugin.rco                      57148                          |
|   gameboot.pmf                        200704                          |
|   impose_plugin.rco                    87828                          |
|   msgdialog_plugin.rco                  7028                          |
|   msvideo_plugin.rco                  158124                          |
|   music_plugin.rco                    220976                          |
|   netconf_dialog.rco                   68552                          |
|   netplay_plugin.rco                   12560                          |
|   opening_plugin.rco                  254480                          |
|   osk_plugin.rco                      318548                          |
|   osk_utility.rco                     121384                          |
|   photo_plugin.rco                    182604                          |
|   savedata_plugin.rco                  68328                          |
|   savedata_utility.rco                 64428                          |
|   sysconf_plugin.rco                  151540                          |
|   system_plugin.rco                    98136                          |
|   system_plugin_bg.rco                 10776                          |
|   system_plugin_fg.rco                 45508                          |
|   topmenu_plugin.rco                  216320                          |
|   update_plugin.rco                    14048                          |
|   video_plugin.rco                     26464                          |
|   video_plugin_videotoolbar.rco       115888                          |
|   ------------------------------- ----------                          |
+-----------------------------------------------------------------------+
