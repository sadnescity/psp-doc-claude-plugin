---
name: headphone-remote
description: "The PSP headphone and remote control port: audio input and the remote's serial communication. Use when working with the remote or its SIO protocol."
---

## 18  Headphone/Remote Control

### 18.1  Audio Input

### 18.2  Serial Communications

The PSP communicates with the microcontroller inside the remote control using RS232 serial communication (although the voltages are different of course, 0V and +2.5V) using 8N1 framing at 4800bps. The protocol consists of command packages which can be send by either the PSP or the remote control. A package is exchanged as follows:\

+:---------------------------------------------------------------------:+
|   ------------ -------------- --------------------------------------  |
|   **Sender**    **Reciever**  **description**                         |
|   0xF0                        Request to transmit                     |
|                     0xF8      Clearance to transmit                   |
|   0xFD                        Packet starts                           |
|   cmd                         Command code + phase                    |
|   params                      Zero or more bytes of parameter data    |
|   checksum                    XOR of the cmd and params bytes         |
|   0xFE                        Packet ends                             |
|                  0xFA/0xFB    Packet received correctly               |
|   ------------ -------------- --------------------------------------  |
+-----------------------------------------------------------------------+

 \
 \
If the packet is not received correctly, or the receiver is too busy to allow the packet to be transmitted, the corresponding 0xFA/0xFB/0xF8 is not sent, in which case the sender should wait a while (60 ms) and then try again from the 0xF0. If no answer is received in a long time (\> 1s), a BREAK can be sent to reset the communication channel, after which the state should be the same as if the remote control had been disconnected and reconnected again. The least significant bit of the cmd byte is the phase indicator, which is used to differentiate a new command from the retransmission of an old one. The first packet sent from a particular device has phase 0 (LSB = 0), and is acknowledged with 0xFA. Then the phase is inverted each time a new packets is sent. Packets with phase 1 are acknowledged with 0xFB. Phase is not shared, so when the PSP sends a packet it does not affect the phase of the remote control, and vice versa. Note that there seems to be no particular way to know how many parameter bytes are contained in the message, as the parameter bytes or the checksum could contain an 0xFE as well. It is therefore necessary to know how many parameter bytes each command takes. The command sent by the remote control to inform the PSP of what buttons are pressed is 0x84. It takes two parameter bytes, which if interpreted as a 16-bit integer (little endian) forms a bitfield like so:\

+:---------------------------------------------------------------------:+
|   --------- ----------- --------------                                |
|    **bit**   **value**  **button**                                    |
|       0      `0x0001`   Play/Pause                                    |
|       1      `0x0002`   ? (unused)                                    |
|       2      `0x0004`   Fast Forward                                  |
|       3      `0x0008`   Rewind                                        |
|       4      `0x0010`   Vol +                                         |
|       5      `0x0020`   Vol -                                         |
|       6      `0x0040`   ? (unused)                                    |
|       7      `0x0080`   Hold                                          |
|   --------- ----------- --------------                                |
+-----------------------------------------------------------------------+

 \
 \
Buttons that are pressed have their corresponding bits set to 1. Buttons that are not pressed or do not exist have their corresponding bits set to 0.\
The 0x80 command has some parameter bytes, and I\'m guessing these are used to identify the type of device connected. There could also be any number (well, a bit over 100 at least) of commands to request specific kinds of services from the PSP.
