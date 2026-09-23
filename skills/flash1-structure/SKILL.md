---
name: flash1-structure
description: "What lives in flash1, the PSP settings partition: dictionaries, the system registry and VSH themes. Use when looking for system settings in a flash dump."
---

## 21  Flash Memory Structure (flash1)

`/DIC`\
`/REGISTRY`\
`/VSH`\
`  /THEME`\

### 21.1  DIC Subdirectory

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   atokl0.dat          15360                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

### 21.2  REGISTRY Subdirectory

contains the System Registry

+:---------------------------------------------------------------------:+
|   -------------- ----------                                           |
|   **Filename**     **Size**                                           |
|   system.ireg             ?                                           |
|   system.dreg             ?                                           |
|   -------------- ----------                                           |
+-----------------------------------------------------------------------+

### 21.3  VSH Subdirectory

#### 21.3.1  THEME Subdirectory
