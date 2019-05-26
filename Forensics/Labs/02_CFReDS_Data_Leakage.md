## CFReDS - Data Leakage

Mounting

```root@siftworkstation -> /c/Data_Leakage_PC 
# mount -o ro,loop,show_sys_files,offset=105906176 cfreds_2015_data_leakage_pc.dd /mnt/Data_Leakage_PC_Mount/
```
Checking

```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# ls
$AttrDef  $MFTMirr      Documents and Settings  Recovery
$BadClus  $Recycle.Bin  MSOCache                System Volume Information
$Bitmap   $Secure       PerfLogs                Users
$Boot     $UpCase       Program Files           Windows
$Extend   $Volume       Program Files (x86)     hiberfil.sys
$LogFile  Config.Msi    ProgramData             pagefile.sys

```
**Q1**
```
```
**Q2**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# mmls /cases/Data_Leakage_PC/cfreds_2015_data_leakage_pc.dd 
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000206847   0000204800   NTFS / exFAT (0x07)
003:  000:001   0000206848   0041940991   0041734144   NTFS / exFAT (0x07)
004:  -------   0041940992   0041943039   0000002048   Unallocated

```

**Q3**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SOFTWARE -p winver
Launching winver v.20081210
winver v.20081210
(Software) Get Windows version

ProductName = Windows 7 Ultimate
CSDVersion  = Service Pack 1
InstallDate = Sun Mar 22 14:34:26 2015
```
**Q4**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SYSTEM -p timezone
Launching timezone v.20160318
timezone v.20160318
(System) Get TimeZoneInformation key contents

TimeZoneInformation key
ControlSet001\Control\TimeZoneInformation
LastWrite Time Wed Mar 25 10:34:25 2015 (UTC)
  DaylightName   -> @tzres.dll,-111
  StandardName   -> @tzres.dll,-112
  Bias           -> 300 (5 hours)
  ActiveTimeBias -> 240 (4 hours)
  TimeZoneKeyName-> Eastern Standard Timeard Time햸ʓH�ʓ仨5p⏿ﵬ��넗ￊ��魃盘鯯盘㻠龜߾À㯼盘À㻠龜߾ŋ߾
```
**Q5**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SYSTEM -p compname
Launching compname v.20090727
compname v.20090727
(System) Gets ComputerName and Hostname values from System hive

ComputerName    = INFORMANT-PC
TCP/IP Hostname = informant-PC
```
**Q6 & Q7**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SAM -p samparse
Launching samparse v.20160203
samparse v.20160203
(SAM) Parse SAM file for user & group mbrshp info


User Information
-------------------------
Username        : Administrator [500]
Full Name       : 
User Comment    : Built-in account for administering the computer/domain
Account Type    : Default Admin User
Account Created : Wed Mar 25 10:33:22 2015 Z
Name            :  
Last Login Date : Sun Nov 21 03:47:20 2010 Z
Pwd Reset Date  : Sun Nov 21 03:57:24 2010 Z
Pwd Fail Date   : Never
Login Count     : 6
  --> Account Disabled
  --> Normal user account
  --> Password does not expire

Username        : Guest [501]
Full Name       : 
User Comment    : Built-in account for guest access to the computer/domain
Account Type    : Default Guest Acct
Account Created : Wed Mar 25 10:33:22 2015 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Never
Pwd Fail Date   : Never
Login Count     : 0
  --> Account Disabled
  --> Password not required
  --> Normal user account
  --> Password does not expire

Username        : informant [1000]
Full Name       : 
User Comment    : 
Account Type    : Default Admin User
Account Created : Sun Mar 22 14:33:54 2015 Z
Name            :  
Password Hint   : IAMAN
Last Login Date : Wed Mar 25 14:45:59 2015 Z
Pwd Reset Date  : Sun Mar 22 14:33:54 2015 Z
Pwd Fail Date   : Wed Mar 25 14:45:43 2015 Z
Login Count     : 10
  --> Password not required
  --> Normal user account
  --> Password does not expire

Username        : admin11 [1001]
Full Name       : admin11
User Comment    : 
Account Type    : Default Admin User
Account Created : Sun Mar 22 15:51:54 2015 Z
Name            :  
Last Login Date : Sun Mar 22 15:57:02 2015 Z
Pwd Reset Date  : Sun Mar 22 15:52:10 2015 Z
Pwd Fail Date   : Sun Mar 22 15:53:02 2015 Z
Login Count     : 2
  --> Normal user account
  --> Password does not expire

Username        : ITechTeam [1002]
Full Name       : ITechTeam
User Comment    : 
Account Type    : Default Admin User
Account Created : Sun Mar 22 15:52:30 2015 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Sun Mar 22 15:52:45 2015 Z
Pwd Fail Date   : Sun Mar 22 15:53:02 2015 Z
Login Count     : 0
  --> Normal user account
  --> Password does not expire

Username        : temporary [1003]
Full Name       : temporary
User Comment    : 
Account Type    : Custom Limited Acct
Account Created : Sun Mar 22 15:53:01 2015 Z
Name            :  
Last Login Date : Sun Mar 22 15:55:57 2015 Z
Pwd Reset Date  : Sun Mar 22 15:53:11 2015 Z
Pwd Fail Date   : Sun Mar 22 15:56:37 2015 Z
Login Count     : 1
  --> Normal user account
  --> Password does not expire

-------------------------
Group Membership Information
-------------------------
Group Name    : Replicator [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Supports file replication in a domain
Users         : None

Group Name    : Network Configuration Operators [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Members in this group can have some administrative privileges to manage configuration of networking features
Users         : None

Group Name    : Distributed COM Users [0]
LastWrite     : Tue Jul 14 04:45:47 2009 Z
Group Comment : Members are allowed to launch, activate and use Distributed COM objects on this machine.
Users         : None

Group Name    : Administrators [4]
LastWrite     : Sun Mar 22 15:52:30 2015 Z
Group Comment : Administrators have complete and unrestricted access to the computer/domain
Users :
  S-1-5-21-2425377081-3129163575-2985601102-1000
  S-1-5-21-2425377081-3129163575-2985601102-1002
  S-1-5-21-2425377081-3129163575-2985601102-1001
  S-1-5-21-2425377081-3129163575-2985601102-500

Group Name    : Users [5]
LastWrite     : Sun Mar 22 15:53:01 2015 Z
Group Comment : Users are prevented from making accidental or intentional system-wide changes and can run most applications
Users :
  S-1-5-21-2425377081-3129163575-2985601102-1001
  S-1-5-11
  S-1-5-4
  S-1-5-21-2425377081-3129163575-2985601102-1002
  S-1-5-21-2425377081-3129163575-2985601102-1003

Group Name    : Power Users [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Power Users are included for backwards compatibility and possess limited administrative powers
Users         : None

Group Name    : Remote Desktop Users [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Members in this group are granted the right to logon remotely
Users         : None

Group Name    : Guests [1]
LastWrite     : Wed Mar 25 10:15:19 2015 Z
Group Comment : Guests have the same access as members of the Users group by default, except for the Guest account which is further restricted
Users :
  S-1-5-21-2425377081-3129163575-2985601102-501

Group Name    : IIS_IUSRS [1]
LastWrite     : Tue Jul 14 04:45:47 2009 Z
Group Comment : Built-in group used by Internet Information Services.
Users :
  S-1-5-17

Group Name    : Performance Log Users [0]
LastWrite     : Tue Jul 14 04:45:46 2009 Z
Group Comment : Members of this group may schedule logging of performance counters, enable trace providers, and collect event traces both locally and via remote access to this computer
Users         : None

Group Name    : Performance Monitor Users [0]
LastWrite     : Tue Jul 14 04:45:46 2009 Z
Group Comment : Members of this group can access performance counter data locally and remotely
Users         : None

Group Name    : Backup Operators [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Backup Operators can override security restrictions for the sole purpose of backing up or restoring files
Users         : None

Group Name    : Cryptographic Operators [0]
LastWrite     : Wed Mar 25 10:15:37 2015 Z
Group Comment : Members are authorized to perform cryptographic operations.
Users         : None

Group Name    : Event Log Readers [0]
LastWrite     : Tue Jul 14 04:45:47 2009 Z
Group Comment : Members of this group can read event logs from local machine
Users         : None

Analysis Tips:
 - For well-known SIDs, see http://support.microsoft.com/kb/243330
     - S-1-5-4  = Interactive
     - S-1-5-11 = Authenticated Users
 - Correlate the user SIDs to the output of the ProfileList pluginQ6 & Q7
```
**Q8**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SYSTEM -p shutdown
Launching shutdown v.20080324
shutdown v.20080324
(System) Gets ShutdownTime value from System hive

ControlSet001\Control\Windows key, ShutdownTime value
ControlSet001\Control\Windows
LastWrite Time Wed Mar 25 15:31:05 2015 (UTC)
  ShutdownTime = Wed Mar 25 15:31:05 2015 (UTC)
```
**Q9**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SYSTEM -p nic2
Launching nic2 v.20150812
nic2 v.20150812
(System) Gets NIC info from System hive

Adapter: {846ee342-7039-11de-9d20-806e6f6e6963}
LastWrite Time: Wed Mar 25 10:33:18 2015 Z

ControlSet001\Services\Tcpip\Parameters\Interfaces has no subkeys.
Adapter: {E2B9AEEC-B1F7-4778-A049-50D7F2DAB2DE}
LastWrite Time: Wed Mar 25 15:24:51 2015 Z
  UseZeroBroadcast             0                   
  EnableDeadGWDetect           1                   
  EnableDHCP                   1                   
  NameServer                                       
  Domain                                           
  RegistrationEnabled          1                   
  RegisterAdapterName          0                   
  DhcpIPAddress                10.11.11.129        
  DhcpSubnetMask               255.255.255.0       
  DhcpServer                   10.11.11.254        
  Lease                        1800                
  LeaseObtainedTime            Wed Mar 25 15:19:50 2015 Z
  T1                           Wed Mar 25 15:34:50 2015 Z
  T2                           Wed Mar 25 15:46:05 2015 Z
  LeaseTerminatesTime          Wed Mar 25 15:49:50 2015 Z
  AddressType                  0                   
  IsServerNapAware             0                   
  DhcpConnForceBroadcastFlag   0                   
  DhcpInterfaceOptions         ,ÙU


ÙU


ÙU



ÙUlocaldomainÙUÿÿÿ6ÙU


þ5ÙUüÜÒU3ÙU
  DhcpGatewayHardware          


PVë²,      
  DhcpGatewayHardwareCount     1                   
  DhcpNameServer               10.11.11.2          
  DhcpDefaultGateway           10.11.11.2          
  DhcpDomain                   localdomain         
  DhcpSubnetMaskOpt            255.255.255.0       

ControlSet001\Services\Tcpip\Parameters\Interfaces has no subkeys.
```
**Q10**
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SOFTWARE -p uninstall
Launching uninstall v.20140512
uninstall v.20140512
(Software, NTUSER.DAT) Gets contents of Uninstall keys from Software, NTUSER.DAT hives

Uninstall
Microsoft\Windows\CurrentVersion\Uninstall

Wed Mar 25 14:57:31 2015 (UTC)
  Eraser 6.2.0.2962 v.6.2.2962

Wed Mar 25 14:54:33 2015 (UTC)
  Microsoft .NET Framework 4 Extended v.4.0.30319

Wed Mar 25 14:54:06 2015 (UTC)
  Microsoft .NET Framework 4 Extended v.4.0.30319

Wed Mar 25 14:52:06 2015 (UTC)
  Microsoft .NET Framework 4 Client Profile v.4.0.30319

Wed Mar 25 14:51:39 2015 (UTC)
  Microsoft .NET Framework 4 Client Profile v.4.0.30319

Wed Mar 25 10:15:21 2015 (UTC)
  DXM_Runtime
  MPlayer2

Mon Mar 23 20:00:58 2015 (UTC)
  Bonjour v.3.0.0.10

Sun Mar 22 15:04:14 2015 (UTC)
  Microsoft Office Professional Plus 2013 v.15.0.4420.1017

Sun Mar 22 15:03:33 2015 (UTC)
  Microsoft Office Professional Plus 2013 v.15.0.4420.1017

Sun Mar 22 15:01:46 2015 (UTC)
  Microsoft Office 32-bit Components 2013 v.15.0.4420.1017

Sun Mar 22 15:01:38 2015 (UTC)
  Microsoft Word MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:37 2015 (UTC)
  Microsoft Outlook MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:34 2015 (UTC)
  Microsoft Office OSM MUI (English) 2013 v.15.0.4420.1017
  Microsoft Office OSM UX MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:32 2015 (UTC)
  Microsoft Office Proofing (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:31 2015 (UTC)
  Microsoft Office Proofing Tools 2013 - English v.15.0.4420.1017

Sun Mar 22 15:01:30 2015 (UTC)
  Outils de vérification linguistique 2013 de Microsoft Office - Français v.15.0.4420.1017

Sun Mar 22 15:01:14 2015 (UTC)
  Microsoft Office Proofing Tools 2013 - Español v.15.0.4420.1017

Sun Mar 22 15:01:13 2015 (UTC)
  Microsoft OneNote MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:12 2015 (UTC)
  Microsoft Groove MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:11 2015 (UTC)
  Microsoft DCF MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:10 2015 (UTC)
  Microsoft Publisher MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:09 2015 (UTC)
  Microsoft PowerPoint MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:07 2015 (UTC)
  Microsoft Excel MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:05 2015 (UTC)
  Microsoft Lync MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:04 2015 (UTC)
  Microsoft Office Shared 32-bit MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:03 2015 (UTC)
  Microsoft InfoPath MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:02 2015 (UTC)
  Microsoft Access MUI (English) 2013 v.15.0.4420.1017
  Microsoft Access Setup Metadata MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:01:01 2015 (UTC)
  Microsoft Office Shared Setup Metadata MUI (English) 2013 v.15.0.4420.1017

Sun Mar 22 15:00:59 2015 (UTC)
  Microsoft Office Shared MUI (English) 2013 v.15.0.4420.1017

Tue Jul 14 04:53:26 2009 (UTC)
  AddressBook
  Connection Manager
  DirectDrawEx
  Fontcore
  IE40
  IE4Data
  IE5BAKEX
  IEData
  MobileOptionPack
  SchedulingAgent
  WIC

Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall

Mon Mar 23 20:02:46 2015 (UTC)
  Google Drive v.1.20.8672.3137

Mon Mar 23 20:01:01 2015 (UTC)
  Apple Software Update v.2.1.3.127

Mon Mar 23 20:00:45 2015 (UTC)
  Apple Application Support v.3.0.6

Sun Mar 22 15:16:03 2015 (UTC)
  Google Update Helper v.1.3.26.9

Sun Mar 22 15:11:51 2015 (UTC)
  Google Chrome v.41.0.2272.101

Tue Jul 14 04:53:25 2009 (UTC)
  AddressBook
  Connection Manager
  DirectDrawEx
  Fontcore
  IE40
  IE4Data
  IE5BAKEX
  IEData
  MobileOptionPack
  SchedulingAgent
  WIC

```
**Q11**
userassist
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Users/informant/NTUSER.DAT -p userassist
Launching userassist v.20170204
UserAssist
Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist
LastWrite Time Sun Mar 22 14:35:01 2015 (UTC)

{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}
Wed Mar 25 15:28:47 2015 Z
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\xpsrchvw.exe (1)
Wed Mar 25 15:24:48 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Office\Office15\WINWORD.EXE (4)
Wed Mar 25 15:21:30 2015 Z
  {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Google\Drive\googledrivesync.exe (1)
Wed Mar 25 15:15:50 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\CCleaner\CCleaner64.exe (1)
Wed Mar 25 15:12:28 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\Eraser\Eraser.exe (1)
Wed Mar 25 14:57:56 2015 Z
  C:\Users\informant\Desktop\Download\ccsetup504.exe (1)
Wed Mar 25 14:50:14 2015 Z
  C:\Users\informant\Desktop\Download\Eraser 6.2.0.2962.exe (1)
Wed Mar 25 14:46:05 2015 Z
  Microsoft.InternetExplorer.Default (5)
Wed Mar 25 14:42:47 2015 Z
  Microsoft.Windows.MediaPlayer32 (1)
Wed Mar 25 14:41:03 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Office\Office15\OUTLOOK.EXE (5)
Tue Mar 24 21:05:38 2015 Z
  Chrome (7)
Tue Mar 24 18:31:55 2015 Z
  Microsoft.Windows.StickyNotes (13)
Tue Mar 24 14:16:37 2015 Z
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\rundll32.exe (1)
Mon Mar 23 20:27:33 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Office\Office15\POWERPNT.EXE (2)
Mon Mar 23 20:26:50 2015 Z
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Office\Office15\EXCEL.EXE (1)
Mon Mar 23 20:10:19 2015 Z
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe (4)
Sun Mar 22 15:24:47 2015 Z
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\slui.exe (3)
Sun Mar 22 15:12:32 2015 Z
  C:\Users\informant\Desktop\Download\IE11-Windows6.1-x64-en-us.exe (1)
Sun Mar 22 14:33:13 2015 Z
  Microsoft.Windows.GettingStarted (14)
  Microsoft.Windows.MediaCenter (13)
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\calc.exe (12)
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\SnippingTool.exe (10)
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\mspaint.exe (9)
  Microsoft.Windows.RemoteDesktop (8)
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\magnify.exe (7)
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Games\Solitaire\solitaire.exe (6)

Value names with no time stamps:
  UEME_CTLCUACount:ctor
  Microsoft.Windows.ControlPanel
  {F38BF404-1D43-42F2-9305-67DE0B28FC23}\explorer.exe
  Microsoft.Windows.Shell.RunDialog
  {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\GUMBAD6.tmp\GoogleUpdate.exe
  {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Google\Update\GoogleUpdate.exe
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\wscript.exe
  Microsoft.Office.OUTLOOK.EXE.15
  Microsoft.Windows.ControlPanel.Taskbar
  {6D809377-6AF0-444B-8957-A3773F02200E}\Microsoft Office\Office15\FIRSTRUN.EXE
  C:\Users\informant\Downloads\icloudsetup.exe
  Microsoft.Windows.WindowsInstaller
  {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\GUMA94B.tmp\GoogleUpdate.exe
  {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\Common Files\Apple\Internet Services\iCloud.exe
  {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\taskmgr.exe
  Microsoft.Windows.PhotoViewer
  C:\Users\informant\AppData\Local\Temp\eraserInstallBootstrapper\dotNetFx40_Full_setup.exe
  C:\Users\informant\AppData\Local\Temp\~nsu.tmp\Au_.exe

{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}
Wed Mar 25 15:21:30 2015 Z
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Google Drive\Google Drive.lnk (1)
Wed Mar 25 15:15:50 2015 Z
  C:\Users\Public\Desktop\CCleaner.lnk (1)
Wed Mar 25 15:12:28 2015 Z
  C:\Users\Public\Desktop\Eraser.lnk (1)
Wed Mar 25 14:46:05 2015 Z
  {9E3995AB-1F9C-4F13-B827-48B24B6C7174}\TaskBar\Internet Explorer.lnk (5)
Wed Mar 25 14:42:47 2015 Z
  {9E3995AB-1F9C-4F13-B827-48B24B6C7174}\TaskBar\Windows Media Player.lnk (1)
Wed Mar 25 14:41:03 2015 Z
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Microsoft Office 2013\Outlook 2013.lnk (5)
Tue Mar 24 21:05:38 2015 Z
  {9E3995AB-1F9C-4F13-B827-48B24B6C7174}\TaskBar\Google Chrome.lnk (5)
Tue Mar 24 18:32:15 2015 Z
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Microsoft Office 2013\Word 2013.lnk (1)
Tue Mar 24 18:31:55 2015 Z
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Sticky Notes.lnk (13)
Tue Mar 24 18:29:07 2015 Z
  ::{ED228FDF-9EA8-4870-83B1-96B02CFE0D52}\{00D8862B-6453-4957-A821-3D98D74C76BE} (7)
Mon Mar 23 17:26:50 2015 Z
  C:\Users\Public\Desktop\Google Chrome.lnk (2)
Sun Mar 22 14:33:13 2015 Z
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Welcome Center.lnk (14)
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Media Center.lnk (13)
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Calculator.lnk (12)
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Snipping Tool.lnk (10)
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Paint.lnk (9)
  {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Remote Desktop Connection.lnk (8)
  {A77F5D77-2E2B-44C3-A6A2-ABA601054A51}\Accessories\Accessibility\Magnify.lnk (7)

Value names with no time stamps:
  UEME_CTLCUACount:ctor


```
shimcache
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# rip.pl -r Windows/System32/config/SYSTEM -p shimcache
Launching shimcache v.20180311
shimcache v.20180311
(System) Parse file refs from System hive AppCompatCache data

*** ControlSet001 ***
ControlSet001\Control\Session Manager\AppCompatCache
LastWrite Time: Wed Mar 25 15:31:05 2015 Z
Signature: 0xbadc0fee
Num_entries: 292
Data Length: 60816 bytes
Win2K8R2/Win7, 64-bit
C:\Program Files\Windows Mail\WinMail.exe  Tue Jul 14 01:39:53 2009 Z  Executed
C:\Windows\Explorer.EXE  Sun Nov 21 03:24:11 2010 Z  Executed
C:\Program Files (x86)\Google\Update\Install\{7965FA88-DF76-445A-BB63-45BD0E547356}\41.0.2272.101_chrome_installer.exe  Thu Mar 19 21:35:59 2015 Z  Executed
C:\Windows\System32\Dism.exe  Tue Jul 14 01:39:06 2009 Z
C:\Windows\system32\taskhost.exe  Sun Mar 22 15:15:47 2015 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\misc.exe  Sun Mar 22 15:03:28 2015 Z
C:\Windows\system32\xpsrchvw.exe  Tue Jul 14 01:39:59 2009 Z  Executed
C:\Windows\system32\recdisc.exe  Sun Nov 21 03:25:06 2010 Z
C:\Windows\ehome\ehshell.exe  Tue Jul 14 01:39:09 2009 Z
C:\Program Files\Windows Photo Viewer\PhotoViewer.dll  Sun Nov 21 03:25:06 2010 Z
C:\Windows\WinSxS\amd64_microsoft-windows-i..eoptionalcomponents_31bf3856ad364e35_11.2.9600.16428_none_e410f56f6c4ee930\ConfigureIEOptionalComponents.exe  Sun Mar 22 15:16:56 2015 Z  Executed
C:\Windows\system32\taskeng.exe  Sun Nov 21 03:24:27 2010 Z  Executed
C:\Windows\System32\netsh.exe  Tue Jul 14 01:39:25 2009 Z  Executed
C:\Windows\system32\msiexec.exe  Sun Nov 21 03:24:15 2010 Z  Executed
C:\Windows\SysWOW64\ntshrui.dll  Sun Nov 21 03:24:01 2010 Z
C:\Program Files\Windows Media Player\WMPNSSUI.dll  Tue Jul 14 01:41:57 2009 Z
C:\Windows\System32\rshx32.dll  Tue Jul 14 01:41:53 2009 Z
C:\Program Files\Microsoft Office\Office15\msohtmed.exe  Tue Oct  2 00:35:44 2012 Z  Executed
C:\Windows\System32\SNTSearch.dll  Tue Jul 14 01:41:54 2009 Z
C:\Windows\SysWOW64\wusa.exe  Sun Nov 21 03:24:08 2010 Z  Executed
C:\Windows\System32\mctadmin.exe  Tue Jul 14 01:39:17 2009 Z  Executed
C:\Windows\system32\SearchProtocolHost.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Windows\syswow64\lodctr.exe  Tue Jul 14 01:14:22 2009 Z  Executed
C:\Windows\System32\sdiagnhost.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Program Files (x86)\Internet Explorer\ieproxy.dll  Sun Mar 22 15:16:59 2015 Z
C:\Program Files (x86)\Windows Defender\MpOAV.dll  Tue Jul 14 01:15:41 2009 Z
C:\Users\INFORM~1\AppData\Local\Temp\1B451BF0-844E-487B-869F-B8BF0DC63399\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\System32\zipfldr.dll  Sun Nov 21 03:24:01 2010 Z
C:\Program Files\Microsoft Office\Office15\EXCEL.EXE  Tue Oct  2 00:36:36 2012 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\mscorsvw.exe  Thu Mar 18 18:27:13 2010 Z  Executed
C:\Windows\System32\RegisterIEPKEYs.exe  Sun Mar 22 15:16:56 2015 Z  Executed
C:\Windows\System32\ExplorerFrame.dll  Sun Nov 21 03:24:09 2010 Z
C:\Windows\system32\mcbuilder.exe  Sun Nov 21 03:24:26 2010 Z  Executed
C:\Windows\system32\SearchIndexer.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Windows\Microsoft.NET\Framework\v4.0.30319\mscorsvw.exe  Thu Mar 18 17:16:28 2010 Z  Executed
C:\Windows\WinSxS\amd64_netfx-clrgc_b03f5f7f11d50a3a_6.1.7601.17514_none_ad7a390fa131c970\clrgc.exe  Sun Nov 21 03:24:15 2010 Z  Executed
C:\Windows\WinSxS\x86_microsoft-windows-ie-gc-registeriepkeys_31bf3856ad364e35_11.2.9600.16428_none_ae214da780801b0f\RegisterIEPKEYs.exe  Sun Mar 22 15:17:01 2015 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\dfsvc.exe  Wed Jun 10 20:39:48 2009 Z  Executed
C:\Program Files (x86)\Google\Update\1.3.26.9\GoogleUpdateComRegisterShell64.exe  Sun Mar 22 15:11:26 2015 Z  Executed
C:\Program Files\Windows Sidebar\sidebar.exe  Sun Nov 21 03:24:51 2010 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\pptico.exe  Sun Mar 22 15:03:28 2015 Z
C:\Windows\bfsvc.exe  Sun Nov 21 03:24:22 2010 Z  Executed
C:\Windows\SysWOW64\unlodctr.exe  Sun Nov 21 03:24:01 2010 Z  Executed
C:\Windows\SysWOW64\ping.exe  Tue Jul 14 01:14:28 2009 Z  Executed
C:\Program Files (x86)\Apple Software Update\SoftwareUpdate.exe  Wed Jun  1 21:57:16 2011 Z  Executed
C:\Windows\system32\DeviceDisplayObjectProvider.exe  Tue Jul 14 01:39:02 2009 Z  Executed
C:\Windows\syswow64\schtasks.exe  Sun Nov 21 03:23:51 2010 Z  Executed
C:\Windows\System32\powercfg.exe  Tue Jul 14 01:39:27 2009 Z  Executed
C:\Windows\System32\shdocvw.dll  Sun Nov 21 03:23:54 2010 Z
C:\Program Files (x86)\Internet Explorer\iexplore.exe  Sun Nov 21 03:25:08 2010 Z  Executed
C:\Users\informant\Desktop\Download\IE11-Windows6.1-x64-en-us.exe  Sun Mar 22 15:11:04 2015 Z  Executed
C:\Windows\System32\XPSSHHDR.dll  Tue Jul 14 01:41:59 2009 Z
C:\Windows\system32\Dwm.exe  Tue Jul 14 01:39:08 2009 Z  Executed
C:\Windows\SysWOW64\networkexplorer.dll  Sun Nov 21 03:24:15 2010 Z
C:\Windows\System32\usercpl.dll  Sun Nov 21 03:24:03 2010 Z
C:\Windows\system32\unlodctr.exe  Tue Jul 14 01:39:48 2009 Z  Executed
C:\Windows\System32\wpdshext.dll  Sun Nov 21 03:24:52 2010 Z
C:\Windows\Microsoft.NET\Framework\v2.0.50727\ngen.exe  Sun Nov 21 03:23:48 2010 Z  Executed
C:\Windows\system32\slui.exe  Sun Nov 21 03:24:16 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework\v4.0.30319\ngen.exe  Thu Mar 18 17:16:28 2010 Z  Executed
C:\Windows\System32\SetIEInstalledDate.exe  Sun Mar 22 15:16:55 2015 Z  Executed
C:\Windows\System32\mydocs.dll  Sun Nov 21 03:24:01 2010 Z
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\msouc.exe  Sun Mar 22 15:03:28 2015 Z
C:\Users\informant\AppData\Local\Apps\2.0\AAEE5TR8.1PL\3ZO8K226.LA4\goog...app_86fd5b6b43e66935_0001.0003_02e0d8611226c884\clickonce_bootstrap.exe  Sun Mar 22 15:11:21 2015 Z  Executed
C:\Windows\SysWOW64\EhStorShell.dll  Tue Jul 14 01:15:14 2009 Z
C:\Windows\TEMP\IE1BEEB.tmp\IE11-SUPPORT\IEXPLORE.EXE  Mon Oct 14 22:48:14 2013 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe  Thu Mar 18 21:23:04 2010 Z  Executed
C:\Windows\system32\services.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Windows\system32\wbem\mofcomp.exe  Tue Jul 14 01:14:24 2009 Z
C:\Users\informant\Desktop\Download\ccsetup504.exe  Wed Mar 25 14:48:28 2015 Z  Executed
C:\Program Files (x86)\Common Files\Apple\Apple Application Support\APSDaemon.exe  Thu Jul 31 16:15:54 2014 Z  Executed
C:\Windows\WinSxS\x86_microsoft-windows-ie-pdm_31bf3856ad364e35_8.0.7601.17514_none_0a379bcfbdcffb74\PDMSetup.exe  Sun Nov 21 03:25:08 2010 Z  Executed
C:\Windows\system32\cmd.exe  Sun Nov 21 03:24:03 2010 Z
C:\Program Files\Common Files\Apple\Internet Services\ShellStreams64.dll  Fri Nov 21 17:20:44 2014 Z
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\wordicon.exe  Sun Mar 22 15:03:28 2015 Z
C:\Users\INFORM~1\AppData\Local\Temp\59A8D48B-4602-4A22-AA17-A7BD9AE21821\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Users\informant\Downloads\icloudsetup.exe  Mon Mar 23 19:56:53 2015 Z  Executed
C:\Program Files (x86)\Common Files\Apple\Internet Services\iCloud.exe  Tue Dec  2 02:26:10 2014 Z  Executed
C:\Windows\system32\verclsid.exe  Tue Jul 14 01:39:49 2009 Z  Executed
C:\Windows\system32\mstsc.exe  Sun Nov 21 03:23:56 2010 Z
C:\Users\INFORM~1\AppData\Local\Temp\3ACE2160-3FD0-48A6-9016-1960C62C7510\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Program Files\CCleaner\CCleaner.exe  Fri Mar 13 11:10:25 2015 Z  Executed
C:\Windows\System32\dskquoui.dll  Sun Nov 21 03:24:26 2010 Z
C:\Windows\System32\tquery.dll  Sun Nov 21 03:25:09 2010 Z
C:\Windows\system32\oobe\windeploy.exe  Sun Nov 21 03:24:24 2010 Z  Executed
C:\Windows\System32\DeviceCenter.dll  Sun Nov 21 03:23:51 2010 Z
C:\Windows\System32\sdclt.exe  Sun Nov 21 03:25:06 2010 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\osmclienticon.exe  Sun Mar 22 15:03:28 2015 Z
C:\Program Files (x86)\Google\Update\1.3.26.9\GoogleCrashHandler64.exe  Sun Mar 22 15:11:26 2015 Z  Executed
C:\Windows\Microsoft.NET\Framework\v4.0.30319\aspnet_regiis.exe  Thu Mar 18 20:47:22 2010 Z  Executed
C:\Windows\system32\svchost.exe  Tue Jul 14 01:39:46 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\24A9C488-909C-4D74-9ACC-4CE55CF36395\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\GUMA150.tmp\GoogleUpdate.exe  Mon Mar 23 20:02:07 2015 Z  Executed
C:\Windows\system32\wuauclt.exe  Sun Nov 21 03:24:25 2010 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\xlicons.exe  Sun Mar 22 15:03:28 2015 Z
C:\Windows\System32\powercpl.dll  Sun Nov 21 03:24:09 2010 Z
C:\Windows\System32\dinotify.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\SysWOW64\ExplorerFrame.dll  Sun Nov 21 03:24:23 2010 Z
C:\Users\informant\Downloads\googledrivesync.exe  Mon Mar 23 19:56:33 2015 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\GUMADBC.tmp\GoogleUpdate.exe  Sun Mar 22 15:11:22 2015 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\mscorsvw.exe  Wed Jun 10 20:39:58 2009 Z  Executed
C:\Windows\system32\sppsvc.exe  Sun Nov 21 03:23:56 2010 Z  Executed
C:\Windows\system32\cmd.exe  Sun Nov 21 03:23:55 2010 Z  Executed
C:\Windows\System32\prnfldr.dll  Sun Nov 21 03:23:48 2010 Z
C:\Program Files (x86)\Google\Update\1.3.26.9\GoogleUpdateOnDemand.exe  Sun Mar 22 15:11:26 2015 Z  Executed
C:\Windows\servicing\TrustedInstaller.exe  Sun Nov 21 03:24:03 2010 Z  Executed
C:\Program Files\Microsoft Office\Office15\OUTLOOK.EXE  Tue Oct  2 00:36:36 2012 Z  Executed
C:\Program Files (x86)\Common Files\Apple\Internet Services\ApplePhotoStreams.exe  Fri Nov 21 17:20:38 2014 Z  Executed
C:\Windows\System32\EhStorShell.dll  Tue Jul 14 01:40:36 2009 Z
C:\Windows\System32\wscui.cpl  Tue Jul 14 01:38:52 2009 Z
C:\Users\INFORM~1\AppData\Local\Temp\B558AAEA-69B7-4E87-8B4D-1DED544E0433\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\sscicons.exe  Sun Mar 22 15:03:29 2015 Z
C:\Program Files\Microsoft Games\solitaire\solitaire.exe  Tue Jul 14 01:39:42 2009 Z  Executed
C:\Users\informant\Desktop\Download\Eraser 6.2.0.2962.exe  Wed Mar 25 14:47:40 2015 Z  Executed
C:\Windows\System32\SearchFolder.dll  Sun Nov 21 03:24:28 2010 Z
C:\Windows\system32\StikyNot.exe  Tue Jul 14 01:39:46 2009 Z  Executed
C:\Windows\system32\wevtutil.exe  Tue Jul 14 01:14:44 2009 Z
C:\Users\informant\AppData\Local\Apps\2.0\AAEE5TR8.1PL\3ZO8K226.LA4\goog...app_86fd5b6b43e66935_0001.0003_02e0d8611226c884\GoogleUpdateSetup.exe  Sun Mar 22 15:11:21 2015 Z  Executed
C:\Windows\system32\schtasks.exe  Sun Nov 21 03:24:26 2010 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\9118625E-5635-4BA3-8FB7-D4E9A3A181CE\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\System32\ie4uinit.exe  Sun Mar 22 15:16:54 2015 Z  Executed
D:\SETUP.EXE  Tue Oct  2 00:25:32 2012 Z
C:\Windows\system32\wbem\wmiprvse.exe  Sun Nov 21 03:24:15 2010 Z  Executed
C:\Users\informant\AppData\Local\Microsoft\Windows\Burn\Burn\IE11-Windows6.1-x64-en-us.exe  Sun Mar 22 15:11:04 2015 Z
c:\program files\windows defender\MpCmdRun.exe  Tue Jul 14 01:39:20 2009 Z  Executed
C:\Windows\WinSxS\amd64_microsoft-windows-i..-setieinstalleddate_31bf3856ad364e35_11.2.9600.16428_none_eace14b8d6178cca\SetIEInstalledDate.exe  Sun Mar 22 15:16:55 2015 Z  Executed
C:\Windows\Microsoft.NET\Framework\v4.0.30319\ServiceModelReg.exe  Thu Mar 18 17:16:28 2010 Z  Executed
C:\Windows\system32\taskhost.exe  Sun Nov 21 03:24:08 2010 Z  Executed
C:\Windows\system32\taskmgr.exe  Sun Nov 21 03:24:24 2010 Z  Executed
C:\Windows\System32\syncui.dll  Sun Nov 21 03:24:51 2010 Z
C:\Windows\system32\defrag.exe  Tue Jul 14 01:39:02 2009 Z  Executed
C:\Windows\system32\vssvc.exe  Sun Nov 21 03:23:55 2010 Z  Executed
C:\Program Files\Common Files\Microsoft Shared\OFFICE15\MSOXEV.DLL  Tue Oct  2 00:36:02 2012 Z
C:\Windows\Installer\{789A5B64-9DD9-4BA5-915A-F0FC0A1B7BFE}\AppleSoftwareUpdateIco.exe  Mon Mar 23 20:00:59 2015 Z
C:\Windows\system32\magnify.exe  Tue Jul 14 01:39:16 2009 Z
C:\Program Files (x86)\Windows Mail\WinMail.exe  Tue Jul 14 01:14:45 2009 Z  Executed
C:\Windows\Installer\MSI5911.tmp  Sun Mar 22 15:04:27 2015 Z  Executed
C:\Windows\System32\control.exe  Tue Jul 14 01:39:01 2009 Z  Executed
C:\Windows\System32\networkexplorer.dll  Sun Nov 21 03:24:02 2010 Z
C:\Windows\Microsoft.NET\Framework\v2.0.50727\mscorsvw.exe  Wed Jun 10 21:23:09 2009 Z  Executed
C:\Windows\system32\mspaint.exe  Tue Jul 14 01:39:24 2009 Z
C:\Windows\SysWOW64\wbem\mofcomp.exe  Tue Jul 14 01:14:24 2009 Z  Executed
C:\Program Files (x86)\Google\Drive\googledrivesync64.dll  Thu Feb 19 18:24:25 2015 Z
C:\Windows\system32\lodctr.exe  Tue Jul 14 01:39:15 2009 Z  Executed
C:\Program Files\Windows Media Player\wmpnetwk.exe  Sun Nov 21 03:25:05 2010 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\Microsoft .NET Framework 4 Setup_4.0.30319\TMP5B99.tmp.exe  Fri Mar 19 00:51:07 2010 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\outicon.exe  Sun Mar 22 15:03:29 2015 Z
C:\Windows\System32\diskcopy.dll  Tue Jul 14 01:40:31 2009 Z
C:\Program Files\Microsoft Office\Office15\MsoSync.exe  Tue Oct  2 00:36:04 2012 Z  Executed
C:\Windows\System32\appwiz.cpl  Sun Nov 21 03:24:00 2010 Z
C:\Program Files (x86)\Google\Update\1.3.26.9\GoogleCrashHandler.exe  Sun Mar 22 15:11:26 2015 Z  Executed
C:\Windows\system32\WFS.exe  Sun Nov 21 03:25:07 2010 Z
C:\Windows\system32\ping.exe  Tue Jul 14 01:14:28 2009 Z
C:\Windows\system32\WBEM\mofcomp.exe  Tue Jul 14 01:39:20 2009 Z  Executed
C:\Windows\WinSxS\x86_microsoft-windows-ie-pdm-configuration_31bf3856ad364e35_11.2.9600.16428_none_d6876629731ce419\PDMSetup.exe  Sun Mar 22 15:16:59 2015 Z  Executed
C:\Windows\System32\mssvp.dll  Sun Nov 21 03:25:08 2010 Z
C:\Users\INFORM~1\AppData\Local\Temp\1DA984E0-EA4C-44D3-B249-F1F74EC2D2B3\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\osmadminicon.exe  Sun Mar 22 15:03:28 2015 Z
C:\Windows\Installer\{91150000-0011-0000-1000-0000000FF1CE}\dbcicons.exe  Sun Mar 22 15:03:29 2015 Z
C:\Windows\syswow64\cmd.exe  Sun Nov 21 03:24:03 2010 Z  Executed
C:\Windows\WinSxS\amd64_microsoft-windows-ie-gc-registeriepkeys_31bf3856ad364e35_11.2.9600.16428_none_0a3fe92b38dd8c45\RegisterIEPKEYs.exe  Sun Mar 22 15:16:56 2015 Z  Executed
C:\Windows\System32\cryptext.dll  Tue Jul 14 01:40:24 2009 Z
C:\Windows\system32\wusa.exe  Sun Nov 21 03:24:08 2010 Z
C:\Program Files\Eraser\Eraser.exe  Mon Jan 12 22:56:35 2015 Z  Executed
C:\Windows\system32\LogonUI.exe  Sun Nov 21 03:24:09 2010 Z  Executed
C:\Program Files\Microsoft Office\Office15\WINWORD.EXE  Tue Oct  2 00:36:38 2012 Z  Executed
C:\Program Files\Microsoft Office\Office15\POWERPNT.EXE  Tue Oct  2 00:36:36 2012 Z  Executed
C:\Windows\System32\unregmp2.exe  Tue Jul 14 01:39:48 2009 Z  Executed
D:\proplusr.ww\ose.exe  Tue Oct  2 00:44:32 2012 Z
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\cvtres.exe  Sun Nov 21 03:24:28 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regtlibv12.exe  Thu Mar 18 18:27:13 2010 Z  Executed
C:\Windows\system32\NOTEPAD.EXE  Tue Jul 14 01:39:25 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\474DC71A-3ABD-430F-995D-741E5434BF2C\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Program Files\Common Files\System\wab32.dll  Tue Jul 14 01:41:56 2009 Z
C:\Users\INFORM~1\AppData\Local\Temp\04C57E4D-5506-4B2E-A121-CB96388F903E\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\SysWOW64\shdocvw.dll  Sun Nov 21 03:24:07 2010 Z
C:\Windows\System32\mobsync.exe  Sun Nov 21 03:24:51 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ServiceModelReg.exe  Thu Mar 18 18:27:13 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\csc.exe  Wed Jun 10 20:39:47 2009 Z  Executed
C:\Users\informant\Desktop\temp\IE11-Windows6.1-x64-en-us.exe  Sun Mar 22 15:11:04 2015 Z
C:\Windows\system32\calc.exe  Tue Jul 14 01:38:57 2009 Z
C:\Windows\System32\cscui.dll  Sun Nov 21 03:24:41 2010 Z
C:\Windows\System32\wevtutil.exe  Tue Jul 14 01:39:51 2009 Z  Executed
C:\Program Files\Windows Media Player\wmpnscfg.exe  Tue Jul 14 01:39:56 2009 Z  Executed
C:\Windows\System32\ntshrui.dll  Sun Nov 21 03:23:51 2010 Z
C:\Users\INFORM~1\AppData\Local\Temp\Microsoft .NET Framework 4 Setup_4.0.30319\TMPFF8D.tmp.exe  Thu Mar 18 23:32:37 2010 Z  Executed
C:\Windows\System32\Display.dll  Sun Nov 21 03:24:32 2010 Z
C:\Windows\system32\consent.exe  Sun Nov 21 03:24:08 2010 Z  Executed
C:\Program Files\Internet Explorer\iexplore.exe  Sun Mar 22 15:16:56 2015 Z  Executed
C:\Windows\system32\userinit.exe  Sun Nov 21 03:24:28 2010 Z  Executed
C:\Windows\system32\runonce.exe  Sun Nov 21 03:24:27 2010 Z  Executed
C:\Windows\SysWOW64\SetIEInstalledDate.exe  Sun Mar 22 15:16:58 2015 Z  Executed
C:\Windows\system32\SearchFilterHost.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Windows\System32\rundll32.exe  Tue Jul 14 01:39:31 2009 Z  Executed
C:\Program Files\Common Files\Microsoft Shared\OFFICE15\FLTLDR.EXE  Tue Oct  2 00:35:42 2012 Z  Executed
C:\Windows\WinSxS\amd64_microsoft-windows-ie-pdm_31bf3856ad364e35_8.0.7600.16385_none_6425238b793ee910\PDMSetup.exe  Tue Jul 14 01:39:26 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\CR_0CFC1.tmp\setup.exe  Sun Mar 22 15:11:43 2015 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\IXP374.TMP\SetupAdmin.exe  Tue Dec  2 02:29:30 2014 Z  Executed
C:\Windows\System32\ie4uinit.exe  Tue Jul 14 01:39:12 2009 Z  Executed
C:\Program Files\DVD Maker\DVDMaker.exe  Tue Jul 14 01:39:08 2009 Z
C:\Windows\SysWOW64\DllHost.exe  Tue Jul 14 01:14:18 2009 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v3.5\addinutil.exe  Sun Nov 21 03:25:05 2010 Z  Executed
C:\Program Files (x86)\Google\Drive\googledrivesync.exe  Thu Feb 19 18:24:23 2015 Z  Executed
C:\Windows\system32\msiexec.exe  Sun Nov 21 03:24:28 2010 Z
C:\Windows\system32\lsass.exe  Tue Jul 14 01:39:16 2009 Z  Executed
C:\Program Files (x86)\GUMBAD6.tmp\GoogleUpdate.exe  Sun Mar 22 15:11:26 2015 Z  Executed
D:\IE11-Windows6.1-x64-en-us.exe  Sun Mar 22 15:11:04 2015 Z
C:\Windows\system32\schtasks.exe  Sun Nov 21 03:23:51 2010 Z
C:\Program Files\Microsoft Office\Office15\msoia.exe  Mon Oct  1 22:59:44 2012 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\GUMA150.tmp\GoogleUpdateSetup.exe  Mon Mar 23 19:56:33 2015 Z  Executed
C:\Windows\SysWOW64\ieframe.dll  Sun Mar 22 15:17:00 2015 Z
C:\Program Files\Microsoft Office\Office15\MAPISHELL.DLL  Tue Oct  2 00:36:36 2012 Z
C:\Program Files\CCleaner\uninst.exe  Fri Mar 13 13:55:38 2015 Z  Executed
C:\Windows\system32\msra.exe  Tue Jul 14 01:39:24 2009 Z
C:\Program Files (x86)\Windows Media Player\wmplayer.exe  Sun Nov 21 03:25:10 2010 Z  Executed
C:\Windows\system32\SnippingTool.exe  Tue Jul 14 01:39:41 2009 Z
C:\Windows\System32\docprop.dll  Tue Jul 14 01:40:32 2009 Z
C:\Windows\system32\wbem\WMIADAP.EXE  Tue Jul 14 01:39:55 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\~nsu.tmp\Au_.exe  Fri Mar 13 13:55:38 2015 Z  Executed
C:\Program Files\Bonjour\mDNSResponder.exe  Wed Aug 31 03:05:32 2011 Z  Executed
C:\Program Files (x86)\GUMA94B.tmp\GoogleUpdate.exe  Mon Mar 23 20:02:09 2015 Z  Executed
C:\Windows\system32\DrvInst.exe  Tue Jul 14 01:39:07 2009 Z  Executed
C:\Program Files (x86)\Internet Explorer\IEXPLORE.EXE  Sun Mar 22 15:17:01 2015 Z  Executed
C:\Windows\WinSxS\x86_microsoft-windows-i..eoptionalcomponents_31bf3856ad364e35_11.2.9600.16428_none_87f259ebb3f177fa\ConfigureIEOptionalComponents.exe  Sun Mar 22 15:17:01 2015 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\EBC7C45E-1272-4954-8FEA-21BD794BAEB0\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\ose00000.exe  Tue Oct  2 00:44:32 2012 Z  Executed
C:\Windows\SysWOW64\ie4uinit.exe  Sun Nov 21 03:25:08 2010 Z  Executed
C:\Windows\System32\twext.dll  Sun Nov 21 03:24:16 2010 Z
C:\Windows\system32\ipconfig.exe  Tue Jul 14 01:39:13 2009 Z  Executed
C:\Program Files\Microsoft Office\Office15\FIRSTRUN.EXE  Tue Oct  2 00:34:44 2012 Z  Executed
C:\Windows\system32\oobe\msoobe.exe  Sun Nov 21 03:23:52 2010 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\GUMADBC.tmp\GoogleUpdateSetup.exe  Sun Mar 22 15:11:21 2015 Z  Executed
C:\Windows\System32\timedate.cpl  Sun Nov 21 03:24:28 2010 Z
C:\Program Files (x86)\Google\Chrome\Application\41.0.2272.101\Installer\chrmstp.exe  Sun Mar 22 15:11:43 2015 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\eraserInstallBootstrapper\dotNetFx40_Full_setup.exe  Wed Mar 25 14:50:15 2015 Z  Executed
C:\Windows\System32\ieframe.dll  Sun Nov 21 03:24:42 2010 Z
C:\Windows\System32\stobject.dll  Sun Nov 21 03:24:07 2010 Z
C:\Program Files\Common Files\Microsoft Shared\Office15\OLicenseHeartbeat.exe  Tue Oct  2 00:36:04 2012 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ngen.exe  Thu Mar 18 18:27:13 2010 Z  Executed
C:\Windows\SysWOW64\twext.dll  Sun Nov 21 03:24:32 2010 Z
C:\Program Files (x86)\Google\Drive\contextmenu64.dll  Thu Feb 19 18:24:27 2015 Z
C:\Windows\SysWOW64\rundll32.exe  Tue Jul 14 01:14:31 2009 Z  Executed
C:\Windows\SysWOW64\explorer.exe  Sun Nov 21 03:24:25 2010 Z  Executed
C:\Program Files\Windows Sidebar\sbdrop.dll  Tue Jul 14 01:41:53 2009 Z
C:\a5df94fcac8e62a530d048042c2a\SetupUtility.exe  Thu Mar 18 19:58:36 2010 Z  Executed
C:\Program Files (x86)\Google\Update\GoogleUpdate.exe  Sun Mar 22 15:11:26 2015 Z  Executed
C:\Windows\System32\regsvr32.exe  Tue Jul 14 01:39:29 2009 Z  Executed
C:\Program Files\Common Files\Microsoft Shared\OFFICE15\msoshext.dll  Tue Oct  2 00:35:44 2012 Z
C:\Windows\System32\DfsShlEx.dll  Tue Jul 14 01:40:28 2009 Z
C:\Windows\SysNative\dism.exe  Tue Jul 14 01:39:06 2009 Z
C:\Program Files\CCleaner\CCleaner64.exe  Fri Mar 13 11:10:25 2015 Z  Executed
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe  Sat Mar 14 10:12:39 2015 Z  Executed
C:\$Recycle.Bin\S-1-5-21-2425377081-3129163575-2985601102-1000\$RJEMT64.exe  Sun Mar 22 15:11:04 2015 Z
C:\Windows\Microsoft.NET\Framework\v4.0.30319\regtlibv12.exe  Thu Mar 18 17:16:28 2010 Z  Executed
C:\Windows\System32\sendmail.dll  Tue Jul 14 01:41:53 2009 Z
C:\Windows\SysWOW64\RegisterIEPKEYs.exe  Sun Mar 22 15:17:01 2015 Z  Executed
C:\Windows\syswow64\wevtutil.exe  Tue Jul 14 01:14:44 2009 Z  Executed
C:\Windows\system32\lpremove.exe  Tue Jul 14 01:39:16 2009 Z  Executed
C:\Windows\system32\sc.exe  Tue Jul 14 01:39:35 2009 Z  Executed
C:\Windows\System32\ieframe.dll  Sun Mar 22 15:16:54 2015 Z
C:\Windows\system32\oobe\oobeldr.exe  Tue Jul 14 01:39:26 2009 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\E18D498E-FB03-4DE7-8F99-A4EC29957FF4\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Program Files (x86)\Windows Media Player\setup_wm.exe  Sun Nov 21 03:25:10 2010 Z  Executed
C:\Windows\system32\winsat.exe  Sun Nov 21 03:24:35 2010 Z  Executed
C:\Windows\TEMP\IE1BEEB.tmp\IE11-SUPPORT\IENRCORE.EXE  Mon Oct 14 23:27:54 2013 Z  Executed
C:\Windows\System32\powercfg.cpl  Sun Nov 21 03:24:10 2010 Z
C:\Windows\WinSxS\amd64_microsoft-windows-ie-pdm-configuration_31bf3856ad364e35_11.2.9600.16428_none_32a601ad2b7a554f\PDMSetup.exe  Sun Mar 22 15:16:52 2015 Z  Executed
C:\Windows\system32\wermgr.exe  Tue Jul 14 01:39:51 2009 Z  Executed
C:\Windows\system32\wuapp.exe  Sun Nov 21 03:24:09 2010 Z
C:\Windows\System32\gameux.dll  Sun Nov 21 03:24:49 2010 Z
C:\Windows\syswow64\MsiExec.exe  Sun Nov 21 03:24:28 2010 Z  Executed
C:\Windows\System32\PhotoMetadataHandler.dll  Tue Jul 14 01:41:53 2009 Z
C:\a5df94fcac8e62a530d048042c2a\Setup.exe  Thu Mar 18 20:16:28 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\ngen.exe  Sun Nov 21 03:24:32 2010 Z  Executed
C:\Windows\system32\aitagent.EXE  Sun Nov 21 03:24:08 2010 Z  Executed
C:\Windows\WinSxS\x86_microsoft-windows-i..-setieinstalleddate_31bf3856ad364e35_11.2.9600.16428_none_8eaf79351dba1b94\SetIEInstalledDate.exe  Sun Mar 22 15:16:58 2015 Z  Executed
C:\Windows\system32\DllHost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Program Files\Internet Explorer\iexplore.exe  Sun Nov 21 03:24:43 2010 Z
C:\Windows\System32\spoolsv.exe  Sun Nov 21 03:24:27 2010 Z  Executed
C:\Users\INFORM~1\AppData\Local\Temp\0228221A-4DE5-4769-9174-040EA5CB020A\dismhost.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\System32\sbe.dll  Sun Nov 21 03:24:51 2010 Z
C:\Windows\SysWOW64\dism.exe  Tue Jul 14 01:39:06 2009 Z  Executed
C:\Windows\System32\acppage.dll  Sun Nov 21 03:24:23 2010 Z
C:\Windows\system32\explorer.exe  Sun Nov 21 03:24:25 2010 Z
C:\Windows\SysWOW64\WerFault.exe  Tue Jul 14 01:14:44 2009 Z  Executed
C:\Windows\system32\lsm.exe  Sun Nov 21 03:23:53 2010 Z  Executed
C:\Windows\System32\mf.dll  Sun Nov 21 03:24:52 2010 Z
C:\Windows\System32\wsqmcons.exe  Sun Nov 21 03:24:49 2010 Z  Executed
C:\Windows\System32\wmpshell.dll  Sun Nov 21 03:24:52 2010 Z
C:\Program Files\Common Files\Microsoft Shared\OfficeSoftwareProtectionPlatform\OSPPSVC.EXE  Tue Oct  2 00:34:38 2012 Z  Executed
C:\Windows\SysWOW64\acppage.dll  Sun Nov 21 03:24:32 2010 Z
C:\Windows\System32\WScript.exe  Tue Jul 14 01:39:57 2009 Z  Executed

*** ControlSet002 ***
ControlSet002\Control\Session Manager\AppCompatCache
LastWrite Time: Wed Mar 25 10:18:30 2015 Z
Signature: 0xbadc0fee
Num_entries: 13
Data Length: 2384 bytes
Win2K8R2/Win7, 64-bit
C:\Windows\system32\SearchIndexer.exe  Tue Jul 14 01:39:37 2009 Z  Executed
C:\Windows\bfsvc.exe  Sun Nov 21 03:24:22 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\mscorsvw.exe  Wed Jun 10 20:39:58 2009 Z  Executed
C:\Windows\system32\LogonUI.exe  Sun Nov 21 03:24:09 2010 Z  Executed
C:\Windows\WinSxS\amd64_netfx-clrgc_b03f5f7f11d50a3a_6.1.7601.17514_none_ad7a390fa131c970\clrgc.exe  Sun Nov 21 03:24:15 2010 Z  Executed
C:\Windows\System32\netsh.exe  Tue Jul 14 01:39:25 2009 Z  Executed
C:\Windows\system32\svchost.exe  Tue Jul 14 01:39:46 2009 Z  Executed
C:\Windows\System32\gameux.dll  Sun Nov 21 03:24:49 2010 Z
C:\Windows\system32\DrvInst.exe  Tue Jul 14 01:39:07 2009 Z  Executed
C:\Windows\system32\sppsvc.exe  Sun Nov 21 03:23:56 2010 Z  Executed
C:\Windows\Microsoft.NET\Framework\v2.0.50727\mscorsvw.exe  Wed Jun 10 21:23:09 2009 Z  Executed
C:\Windows\system32\vssvc.exe  Sun Nov 21 03:23:55 2010 Z  Executed
C:\Windows\system32\wbem\wmiprvse.exe  Sun Nov 21 03:24:15 2010 Z  Executed
```
**Q12**

4608 = Starting up
1100 = service shutdown
4624 = success logon
4634 = logoff
4625 = login failure
4647 = a user initiated logoff process

Dump evtx to XML file
```
root@siftworkstation -> /m/Data_Leakage_PC_Mount 
# evtx_dump.py Windows/System32/winevt/Logs/Security.evtx > /cases/eventlog_system.xml
```

Todo ...

