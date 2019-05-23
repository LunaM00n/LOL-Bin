## Windows Forensics with Hacking Case 

The CFReDS Project - > https://www.cfreds.nist.gov/  
Hacking Case -> https://www.cfreds.nist.gov/Hacking_Case.html  
Answers -> https://www.cfreds.nist.gov/images/TestAnswers.pdf  

**Setup :floppy_disk:**

E01 file to ewf
```
root@siftworkstation -> /cases 
# ls
4Dell Latitude CPi.E01  4Dell Latitude CPi.E02
root@siftworkstation -> /cases 
# ewfmount 4Dell\ Latitude\ CPi.E01 /mnt/ewf_mount
ewfmount 20140608

root@siftworkstation -> /cases 
# cd /mnt/ewf_mount
root@siftworkstation -> /m/ewf_mount 
# ls
ewf1
```
Partition List
```
root@siftworkstation -> /m/ewf_mount 
# mmls ewf1
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000000062   0000000063   Unallocated
002:  000:000   0000000063   0009510479   0009510417   NTFS / exFAT (0x07)
003:  -------   0009510480   0009514259   0000003780   Unallocated
```
Mounting ewf ( the value of offset = 63*512 bytes)
```
root@siftworkstation -> /m/ewf_mount 
# mount -o ro,loop,show_sys_files,streams_interface=windows,offset=32256 /mnt/ewf_mount/ewf1 /mnt/windows_mount
root@siftworkstation -> /m/ewf_mount 
# cd /mnt/windows_mount
root@siftworkstation -> /m/windows_mount 
# ls
$AttrDef  $LogFile  AUTOEXEC.BAT  CONFIG.SYS              MSDOS.---      RECYCLER                   Temp          hiberfil.sys
$BadClus  $MFTMirr  BOOTLOG.PRV   DETLOG.TXT              MSDOS.SYS      SETUPLOG.TXT               VIDEOROM.BIN  ntdetect.com
$Bitmap   $Secure   BOOTLOG.TXT   Documents and Settings  My Documents   SUHDLOG.DAT                WIN98         ntldr
$Boot     $UpCase   BOOTSECT.DOS  FRUNLOG.TXT             NETLOG.TXT     SYSTEM.1ST                 WINDOWS       pagefile.sys
$Extend   $Volume   COMMAND.COM   IO.SYS                  Program Files  System Volume Information  boot.ini
```
Registrys

```
WINDOWS/system32/config/SAM
WINDOWS/system32/config/software
WINDOWS/system32/config/system
WINDOWS/system32/config/security
Documents and Settings/Mr. Evil/NTUSER.DAT
```

**Questions & Answers :floppy_disk:**

Q1. What is the image hash? Does the acquisition and verification hash match? 

```
root@siftworkstation -> /m/ewf_mount 
# md5sum ewf1
aee4fcd9301c03b3b054623ca261959a  ewf1
```
A1 : aee4fcd9301c03b3b054623ca261959a

---

Q2. What operating system was used on the computer?

```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p product
Launching product v.20100325
product v.20100325
(Software) Get installed product info


Microsoft\Windows\CurrentVersion\Installer\UserData

S-1-5-18
Fri Aug 20 15:12:43 2004 Z
  Powertoys For Windows XP v.1.00.0000, 20040820
Thu Aug 19 23:04:50 2004 Z
  WebFldrs XP v.9.50.5318, 20040819
```
A2 : WIndows XP

---

Q3. When was the install date?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p winver
Launching winver v.20081210
winver v.20081210
(Software) Get Windows version

ProductName = Microsoft Windows XP
InstallDate = Thu Aug 19 22:48:27 2004
```

A3 : Thu Aug 19 23:04:50 2004

---
Q4. What is the timezone settings?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/system -p timezone
Launching timezone v.20160318
timezone v.20160318
(System) Get TimeZoneInformation key contents

TimeZoneInformation key
ControlSet001\Control\TimeZoneInformation
LastWrite Time Thu Aug 19 17:20:02 2004 (UTC)
  DaylightName   -> Central Daylight Time
  StandardName   -> Central Standard Time
  Bias           -> 360 (6 hours)
  ActiveTimeBias -> 300 (5 hours)
```

A4 : Central Standard Time

---
Q5. Who is the registered owner?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p winnt_cv 
Launching winnt_cv v.20161123
winnt_cv v.20161123
(Software) Get & display the contents of the Windows NT\CurrentVersion key

WinNT_CV
Microsoft\Windows NT\CurrentVersion
LastWrite Time Fri Aug 27 15:08:22 2004 (UTC)

  RegDone : 
  RegisteredOrganization : N/A
  CurrentVersion : 5.1
  SourcePath : D:\
  CurrentBuildNumber : 2600
  SoftwareType : SYSTEM
  SystemRoot : C:\WINDOWS
  PathName : C:\WINDOWS
  RegisteredOwner : Greg Schardt
  CurrentType : Uniprocessor Free
  ProductName : Microsoft Windows XP
  ProductId : 55274-640-0147306-23684
  BuildLab : 2600.xpclient.010817-1148
  InstallDate : Thu Aug 19 22:48:27 2004 (UTC)
  CurrentBuild : 1.511.1 () (Obsolete data - do not use)
  LicenseInfo : 34 54 ae dc c7 2e 3d e5 8b 15 06 1a 8c 74 a6 55 8c 9b 49 a9 3f 24 2b 04 44 ef 79 88 c1 32 38 cf 52 0c d7 57 da 9b 35 aa d9 44 b3 64 b9 21 6d 76 74 56 d2 4e 91 6e 7f ac 
  DigitalProductId : a4 00 00 00 03 00 00 00 35 35 32 37 34 2d 36 34 30 2d 30 31 34 37 33 30 36 2d 32 33 36 38 34 00 2e 00 00 00 41 32 32 2d 30 30 30 30 31 00 00 00 00 00 00 00 14 b3 4b cc f7 44 da 3a 75 65 93 26 b6 f4 00 00 00 00 00 00 f1 dc 24 41 cc b2 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 35 35 32 30 30 00 00 00 00 00 00 00 94 10 00 00 9b 8d b1 6c 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 c8 7b fc 7c 
```
A5 : Greg Schardt

---





Q6. What is the computer account name?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/system -p compname
Launching compname v.20090727
compname v.20090727
(System) Gets ComputerName and Hostname values from System hive

ComputerName    = N-1A9ODN6ZXK4LQ
TCP/IP Hostname = n-1a9odn6zxk4lq
```
A6 : N-1A9ODN6ZXK4LQ

---
Q7. What is the primary domain name?  
```
todo
```
A7 : 

---
Q8. When was the last recorded computer shutdown date/time?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/system -p shutdown
Launching shutdown v.20080324
shutdown v.20080324
(System) Gets ShutdownTime value from System hive

ControlSet001\Control\Windows key, ShutdownTime value
ControlSet001\Control\Windows
LastWrite Time Fri Aug 27 15:46:33 2004 (UTC)
  ShutdownTime = Fri Aug 27 15:46:33 2004 (UTC)
```
A8 : Fri Aug 27 15:46:33 2004 (UTC)

---
Q9. How many accounts are recorded (total number)?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/SAM -p samparse
Launching samparse v.20160203
samparse v.20160203
(SAM) Parse SAM file for user & group mbrshp info


User Information
-------------------------
Username        : Administrator [500]
Full Name       : 
User Comment    : Built-in account for administering the computer/domain
Account Type    : Default Admin User
Account Created : Thu Aug 19 16:59:24 2004 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Thu Aug 19 17:17:29 2004 Z
Pwd Fail Date   : Never
Login Count     : 0
  --> Normal user account
  --> Password does not expire

Username        : Guest [501]
Full Name       : 
User Comment    : Built-in account for guest access to the computer/domain
Account Type    : Default Guest Acct
Account Created : Thu Aug 19 16:59:24 2004 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Never
Pwd Fail Date   : Never
Login Count     : 0
  --> Password not required
  --> Normal user account
  --> Password does not expire

Username        : HelpAssistant [1000]
Full Name       : Remote Desktop Help Assistant Account
User Comment    : Account for Providing Remote Assistance
Account Type    : Custom Limited Acct
Account Created : Thu Aug 19 22:28:24 2004 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Thu Aug 19 22:28:24 2004 Z
Pwd Fail Date   : Never
Login Count     : 0
  --> Normal user account
  --> Password does not expire

Username        : SUPPORT_388945a0 [1002]
Full Name       : CN=Microsoft Corporation,L=Redmond,S=Washington,C=US
User Comment    : This is a vendor's account for the Help and Support Service
Account Type    : Custom Limited Acct
Account Created : Thu Aug 19 22:35:19 2004 Z
Name            :  
Last Login Date : Never
Pwd Reset Date  : Thu Aug 19 22:35:19 2004 Z
Pwd Fail Date   : Never
Login Count     : 0
  --> Normal user account
  --> Account Disabled
  --> Password does not expire

Username        : Mr. Evil [1003]
Full Name       : 
User Comment    : 
Account Type    : Default Admin User
Account Created : Thu Aug 19 23:03:54 2004 Z
Name            :  
Last Login Date : Fri Aug 27 15:08:23 2004 Z
Pwd Reset Date  : Thu Aug 19 23:03:54 2004 Z
Pwd Fail Date   : Never
Login Count     : 15
  --> Normal user account
  --> Password does not expire

-------------------------
Group Membership Information
-------------------------
Group Name    : Network Configuration Operators [0]
LastWrite     : Thu Aug 19 16:59:25 2004 Z
Group Comment : Members in this group can have some administrative privileges to manage configuration of networking features
Users         : None

Group Name    : Users [2]
LastWrite     : Thu Aug 19 17:01:55 2004 Z
Group Comment : Users are prevented from making accidental or intentional system-wide changes.  Thus, Users can run certified applications, but not most legacy applications
Users :
  S-1-5-4
  S-1-5-11

Group Name    : Backup Operators [0]
LastWrite     : Thu Aug 19 16:59:24 2004 Z
Group Comment : Backup Operators can override security restrictions for the sole purpose of backing up or restoring files
Users         : None

Group Name    : Administrators [2]
LastWrite     : Thu Aug 19 23:03:54 2004 Z
Group Comment : Administrators have complete and unrestricted access to the computer/domain
Users :
  S-1-5-21-2000478354-688789844-1708537768-500
  S-1-5-21-2000478354-688789844-1708537768-1003

Group Name    : Guests [1]
LastWrite     : Thu Aug 19 16:59:24 2004 Z
Group Comment : Guests have the same access as members of the Users group by default, except for the Guest account which is further restricted
Users :
  S-1-5-21-2000478354-688789844-1708537768-501

Group Name    : Replicator [0]
LastWrite     : Thu Aug 19 16:59:24 2004 Z
Group Comment : Supports file replication in a domain
Users         : None

Group Name    : Power Users [0]
LastWrite     : Thu Aug 19 16:59:24 2004 Z
Group Comment : Power Users possess most administrative powers with some restrictions.  Thus, Power Users can run legacy applications in addition to certified applications
Users         : None

Group Name    : Remote Desktop Users [0]
LastWrite     : Thu Aug 19 16:59:25 2004 Z
Group Comment : Members in this group are granted the right to logon remotely
Users         : None

Analysis Tips:
 - For well-known SIDs, see http://support.microsoft.com/kb/243330
     - S-1-5-4  = Interactive
     - S-1-5-11 = Authenticated Users
 - Correlate the user SIDs to the output of the ProfileList plugin
```
A9 : 5

---
Q10. What is the account name of the user who mostly uses the computer?  
```
Login Count     : 15
```
A10 : Mr. Evil

---
Q11. Who was the last user to logon to the computer?  
```
Last Login Date : Fri Aug 27 15:08:23 2004 Z
```
A11 : Mr. Evil

---
Q12. A search for the name of “G=r=e=g S=c=h=a=r=d=t” reveals multiple hits. One of these proves that G=r=e=g S=c=h=a=r=d=t is Mr. Evil and is also the administrator of this computer. What file is it? What software program does this file relate to?  

```
root@siftworkstation -> /m/windows_mount 
# grep -iR "Greg Schardt" *
grep: $Extend/$ObjId: No such file or directory
grep: $Extend/$Quota: No such file or directory
grep: $Extend/$Reparse: No such file or directory
Program Files/Look@LAN/irunin.ini:%REGOWNER%=Greg Schardt
Program Files/Look@LAN/irunin.ini:%USERNAME%=Greg Schardt

root@siftworkstation -> /m/windows_mount 
# cat Program\ Files/Look\@LAN/irunin.ini 
[Config]
ConfigFile=C:\Program Files\Look@LAN\irunin.dat
LanguageFile=C:\Program Files\Look@LAN\irunin.lng
ImageFile=C:\Program Files\Look@LAN\irunin.bmp
LangID=9
IsSelective=0
InstallType=0
[Variables]
%LANHOST%=N-1A9ODN6ZXK4LQ
%LANDOMAIN%=N-1A9ODN6ZXK4LQ
%LANUSER%=Mr. Evil
%LANIP%=192.168.1.111
%LANNIC%=0010a4933e09
%ISWIN95%=FALSE
%ISWIN98%=FALSE
%ISWINNT3%=FALSE
%ISWINNT4%=FALSE
%ISWIN2000%=FALSE
%ISWINME%=FALSE
%ISWINXP%=TRUE
%ISUSERNTADMIN%=TRUE
%TEMPLAUNCHDIR%=C:\DOCUME~1\MRD51E~1.EVI\LOCALS~1\Temp
%WINDIR%=C:\WINDOWS
%SYSDRV%=C:
%SYSDIR%=C:\WINDOWS\System32
%TEMPDIR%=C:\DOCUME~1\MRD51E~1.EVI\LOCALS~1\Temp
%SCREENWIDTH%=800
%SCREENHEIGHT%=600
%REGOWNER%=Greg Schardt
%REGORGANIZATION%=N/A
%DATE%=08/25/04
%CURRENTMONTH%=8
%CURRENTDAY%=25
%CURRENTYEAR%=2004
%CURRENTHOUR%=10
%CURRENTMINUTE%=55
%CURRENTSECOND%=34
%JULIANDATE%=2453243
%ISODATE%=2004-08-25
%EUROPEANDATE%=25/08/04
%FONTDIR%=C:\WINDOWS\Fonts
%DESKTOP%=C:\Documents and Settings\Mr. Evil\Desktop
%DESKTOPNT%=C:\Documents and Settings\All Users\Desktop
%STARTMENU%=C:\Documents and Settings\Mr. Evil\Start Menu
%STARTMENUNT%=C:\Documents and Settings\All Users\Start Menu
%STARTMENUPROGRAMS%=C:\Documents and Settings\Mr. Evil\Start Menu\Programs
%STARTMENUPROGRAMSNT%=C:\Documents and Settings\All Users\Start Menu\Programs
%STARTUP%=C:\Documents and Settings\Mr. Evil\Start Menu\Programs\Startup
%STARTUPNT%=C:\Documents and Settings\All Users\Start Menu\Programs\Startup
%COMMONFILES%=C:\Program Files\Common Files
%PROGRAMFILES%=C:\Program Files
%MYDOCUMENTSDIR%=C:\Documents and Settings\Mr. Evil\My Documents
%DAOPATH%=C:\Program Files\Common Files\Microsoft Shared\DAO
%BDEPATH%=C:\idapi
%SYSTEMRAM%=128
%MOUSEPRESENT%=TRUE
%SOUNDCARDPRESENT%=TRUE
%SETUPCMDLINEARGS%=
%SRCFILE%=C:\Documents and Settings\Mr. Evil\Desktop\lalsetup250.exe
%SRCDIR%=C:\Documents and Settings\Mr. Evil\Desktop
%SRCDRV%=C:
%APPDIR%=C:\Program Files\Look@LAN
%APPDRV%=C:
%SCFOLDERTITLE%=Look@LAN
%SCFOLDERPATH%=C:\Documents and Settings\All Users\Start Menu\Programs\Look@LAN
%PRODUCTNAME%=Look@LAN
%PRODUCTVER%=2.50 Build 29
%PRODUCTTAGLINE%=The Best Network Monitor
%COMPANYNAME%=Carlo Medas
%COPYRIGHT%=Copyright � 2004
%INFOURL%=http://www.lookatlan.com
%DOINGREBOOT%=FALSE
%SHOWFILECALCPROGRESSDLG%=FALSE
%SHOWACTIONPROGRESSDLG%=TRUE
%COLORDEPTH%=24
%SILENTMODE%=FALSE
MSG_GEN_FAILED=Operation Failed
MSG_GEN_PACKAGE_SIZE=Package size
MSG_GEN_TOTAL_SIZE=Total install size
LANG_NAME=English
BTN_CANCEL=Cancel
BTN_OK=OK
BTN_BROWSE=Browse...
BTN_START=Start
BTN_CLOSE=Close
BTN_YES_TO_ALL=Yes to All
BTN_NO_TO_ALL=No to All
BTN_YES=Yes
BTN_NO=No
BTN_NEXT=Next >
BTN_BACK=< Back
BTN_FINISH=Finish
BTN_RETRY=Retry
BTN_ABORT=Abort
BTN_REBOOT=Reboot
BTN_WEB_SITE=Web site
BTN_MORE_INFO=More Info
BTN_IGNORE=Ignore
BTN_EXIT=Exit
BTN_CHANGE=Change
DLG_NOTICE=Notice
DLG_ERROR=Error
DLG_FATAL=Fatal Error
DLG_CONFIRM=Confirm Action
DLG_PROGRESS=Installing Files
DLG_INSERTDISK=Insert Disk
DLG_WARNING=Warning
DLG_IMPORTANT=Important
ELEM_PATH=Path
ELEM_SEARCH_FILE=Searching for file
ELEM_SEARCH_MASK=Search
ELEM_SEARCH_ALL=All Files
CAPTION_NAME=Name
CAPTION_FIRST_NAME=First name
CAPTION_LAST_NAME=Last name
CAPTION_COMPANY=Company
CAPTION_INSTALL_TO=Install %ProductName% to
CAPTION_SPACE_REQUIRED=Space required on drive
CAPTION_SPACE_AVAILABLE=Space available on selected drive
CAPTION_SHORTCUT_FOLDER=Shortcut Folder
CAPTION_SELECT_ONE=Please select one of the following options
CAPTION_SELECT_MULTI=Please select the options below
CAPTION_REBOOT=Yes, restart my computer now.
CAPTION_DRIVE=Drive
CAPTION_FREE_SPACE=Free space on selected drive
CAPTION_SERIAL_NUMBER=Serial Number
INST_TYPICAL=Typical
INST_TYPICAL_DESCRIPTION=Installs the most common program features. Recommended for most users.
INST_COMPLETE=Complete
INST_COMPLETE_DESCRIPTION=All program features will be installed. (Requires the most disk space.)
INST_MINIMUM=Minimum
INST_MINIMUM_DESCRIPTION=Only required features will be installed.
INST_CUSTOM=Custom
INST_CUSTOM_DESCRIPTION=Lets you choose which program features you want installed. Recommended for advanced users only.
UNIN_WIN_TITLE=Removing Programs From Your Computer
UNIN_MAIN='%s' will now be removed from your computer. Please wait while the uninstallation is performed.
UNIN_COMPLETE=Uninstall complete.
UNIN_REMOVE_SHARED=The uninstaller would like to remove the following shared system file:
UNIN_NO_APP_USE=No other application has registered their use of it, however there\nis still a possibility that another application requires it in order to work.
UNIN_OK_TO_REMOVE=Is it OK to remove the file?
UNIN_CONFIRM_DEL=Confirm File Delete
UNIN_CONFIRM=Are you sure that you want to remove '%s' and all of its components?
UNIN_HEADING=Uninstalling Software
UNIN_SUBHEADING=Please wait while the software is uninstalled.
MSG_PROG_DLOAD_GENERAL=Downloading file
MSG_PROG_EXTRACT_FILES=Extracting files
MSG_PROG_EXECUTE_FILE=Executing file
MSG_PROG_OPEN_FILE=Opening file
MSG_PROG_CLOSE_PROGRAM=Closing program
MSG_PROG_DISPLAY_DIALOG=Displaying dialog
MSG_PROG_WRITE_DATA=Writing data
MSG_PROG_CREATE_DIR=Creating directory
MSG_PROG_REMOVE_DIR=Removing directory
MSG_PROG_COPY_FILE=Copying files
MSG_PROG_DELETE_FILES=Deleting files
MSG_PROG_MOVE_FILES=Moving files
MSG_PROG_RENAME_FILE=Renaming file
MSG_PROG_READ_REGISTRY=Reading from Registry
MSG_PROG_READ_INI=Reading from INI file
MSG_PROG_READ_FILEINFO=Reading file information
MSG_PROG_COMMUNICATE_WEB=Communicating with Web site
MSG_PROG_READ_FILE=Reading from file
MSG_PROG_SENT=sent
MSG_PROG_OF=of
MSG_PROG_RECEIVED=received
MSG_PROG_MEGABYTE=MB
MSG_PROG_KILOBYTE=KB
MSG_PROG_BYTES=bytes
MSG_PROG_CREATE_SHORTCUT=Creating shortcut
MSG_PROG_REMOVE_SHORTCUT=Removing shortcut
MSG_PROG_INSTALLING_FILE=Installing file
MSG_PROG_REGISTERING_CONTROL=Registering control
MSG_PROG_REGISTERING_FONT=Registering font
MSG_PROG_CHANGE_FILE_ATTRIB=Changing file attributes
MSG_PROG_CHECKING_CONNECTION=Checking Internet connection
MSG_PROG_QUERY_SERVICE=Checking service status
MSG_PROG_STOP_SERVICE=Stopping service
MSG_PROG_START_SERVICE=Starting service
MSG_PROG_PAUSE_SERVICE=Pausing service
MSG_PROG_CONTINUE_SERVICE=Continuing service
MSG_PROG_DELETE_SERVICE=Deleting service
MSG_PROG_CREATE_SERVICE=Creating service
MSG_PROG_PARSE_STRING=Parsing string
MSG_PROG_SEARCHING_FILES=Searching for files
STAT_INSTALL_FILES=The program files are being installed.
STAT_INSTALL=Installing...
STAT_SKIP=Skipping...
STAT_INIT=Initializing...
STAT_PERFORMING_ACTIONS=Please wait while setup actions are performed on your system.
STAT_ACTIONS_TITLE=Performing Setup Actions
STAT_ACTIONS_SUBHEADING=Installation actions are now being performed.
STAT_ACTIONS_HEADING=Setup
STAT_REG_FONTS=Registering fonts...
STAT_REG_FILES=Registering files...
STAT_REG_UNINSTALL=Creating uninstall...
STAT_REG_ICONS=Creating program icons...
CONFIRM_ABORT=The setup is not finished! Do you really want to abort?
EXIST_NEWER=The installer would like to install a file, but a newer file with the same name already exists on your system.
EXIST_OVER=Do you want to overwrite the following file?
EXIST_ANY=The installer would like to install a file, but a file with the same name already exists on your system.
EXIST_INUSE=The following file is in use and cannot be updated:
EXIST_RETRY=Close all other applications and choose Retry, or choose Cancel to install this file on the next reboot.
RESTART_RETRY=The installer could not restart the system. Please close all open applications and choose Retry.
INSTALL_ASKDISK=Please insert disk #
INSTALL_NEWLOC=If the files on this disk can be found in another location (for example, on another drive), enter the full path to the files, or click the Browse button to select a path.
SCRN_FREESPACE=You do not have enough free space on the selected drive to install the software.
SCRN_BADDIR=You have not entered a valid directory name.\nTry using the Browse button, or choose the default directory if you are having trouble.
SCRN_EDITCHARS=Your response must be between %d and %d characters long.
SCRN_EDITNUM=Please enter a number between %d and %d.
SCRN_BADSCFOLDER=Your shortcut folder name must not contain any of the following characters: /:*?"<>|
SCRN_WIZ_INSTALLING=Please wait while the necessary files are installed.
ERR_INTEGRITY=Archive integrity check failed.\nThe expected setup file size is: %s bytes\nThe actual setup file size is: %s bytes\n\nSetup aborted.
ERR_OPENARC=Cannot open the following archive file (you may have inserted the wrong disk):
ERR_MEM0=Memory allocation error.\nPlease restart your system and close all applications before running the setup again.
ERR_MEM1=Cannot allocate enough memory to decompress files. Setup aborted.
ERR_MAKEDIR=Cannot create the following directory:
ERR_FONTREG=Unable to register the following font:
ERR_SKIP=Error skipping over file
ERR_DECOMP=A decompression error has been detected.
ERR_DECOMP_RW=Read/Write failure
ERR_DECOMP_CRC=File CRC mismatch - Data integrity error
ERR_DECOMP_DEF=General decompression problem
DLL_REGERR=ActiveX registration error #
DLL_REGERR_LOAD=Failure in LoadLibrary()
DLL_REGERR_GETPROC=Failure in GetProcAddress(DllRegisterServer)
DLL_REGERR_FAIL=Failure code returned by DllRegisterServer
TLB_ERR=TypeLib registration error #
TLB_ERR_MEM=Out of Memory
TLB_ERR_ARGS=One or more of the arguments is invalid.
TLB_ERR_IO=The function could not write to the file.
TLB_ERR_STATE=The type library could not be opened.
TLB_ERR_READ=The function could not read from the file.
TLB_ERR_FORMAT=The type library has an older format.
TLB_ERR_LCID=The LCID could not be found in the OLE-supported DLLs.
TLB_ERR_LOAD=The type library or DLL could not be loaded.
TLB_ERR_REG=The system registration database could not be opened.
TLB_ERR_DEF=Default FACILITY_STORAGE error.
ERR_FILENOTFOUND=Please make sure your disk is in the drive!\n\nThe following file cannot be found:
ERR_OPEN_INPUT=Could not open input file
ERR_OPEN_OUTPUT=Could not open output file
ERR_FILE_READ=Error reading from file
ERR_FILE_WRITE=Error writing to file
ERR_COPY_GENERAL=A general I/O error occured during file copy.
MSG_ERR_WINDOW_TITLE=Error
MSG_ERR_NOCONNECT=Could not connect to the Internet.
MSG_ERR_DOWNLOADING=Error downloading file.
MSG_ERR_FILE_NOT_FOUND=The specified file was not found.
MSG_ERR_EXTRACTING=Error extracting file.
MSG_ERR_EXECUTE=Error executing file.
MSG_ERR_OPENING_FILE=Error opening file.
MSG_ERR_CLOSEPROGRAM=Failed to close program.
MSG_ERR_INVALID_HOSTNAME=Invalid hostname.
MSG_ERR_INVALID_HOSTNAME_FORMAT=Improper hostname format.
MSG_ERR_CONNECT_GENERAL=Connection failed.
MSG_ERR_NORESPONSE_SERVER=No response from server.
MSG_ERR_NEGRESPONSE_SERVER=Negative response received from server.
MSG_ERR_INVALID_USERNAME=Invalid username.
MSG_ERR_INVALID_PASSWORD=Invalid password.
MSG_ERR_UNKNOWN=Unknown error.
MSG_ERR_REQUEST_DENIED_SERVER=Request denied by server.
MSG_ERR_INVALID_TYPE=An invalid type has been specified.
MSG_ERR_NOOPEN_DATAPORT=Data port could not be opened.
MSG_ERR_PORT_FAILED=PORT command failed.
MSG_ERR_RETR_FAILED=RETR command failed.
MSG_ERR_CONN_TERMINATED=Connection terminated before operation complete.
MSG_ERR_FILE_VERIFICATION=Failed file verification.
MSG_ERR_FILE_SIZE=File size is incorrect.
MSG_ERR_FILE_CRC=File CRC is incorrect.
MSG_ERR_WEB_DOWNLOAD=Failed to download file from Web.
MSG_ERR_NOCONNECT_SERVER_PROXY=Unable to connect to server or proxy server.
MSG_ERR_INVALID_URL=Invalid URL supplied.
MSG_ERR_OPERATION_TERMINATED=Operation terminated before completion.
MSG_ERR_UNABLE_OPENDATASOURCE=Unable to open specified data source.
MSG_ERR_TIMEOUT=Timeout occurred.
MSG_ERR_SOCKET_RECEIVE=Socket receive error occurred.
MSG_ERR_DATASOURCE_WRITE=Data source write error.
MSG_ERR_OPERATION_ABORTED=Operation aborted.
MSG_ERR_INVALID_PARAMETER=Invalid parameter.
MSG_ERR_CONNECTION_TIMEOUT=Connection timeout.
MSG_ERR_SETPORT=Failed to set port.
MSG_ERR_PATH_NOT_FOUND=The specified path was not found.
MSG_ERR_INVALID_EXE=The .exe file is invalid.
MSG_ERR_ACCESS_DENIED_OS=The operating system denied access to the specified file.
MSG_ERR_INCOMP_FILE_ASSOC=The file name association is incomplete or invalid.
MSG_ERR_DDE_INUSE=The DDE transaction could not be completed because other DDE transactions were being processed.
MSG_ERR_DDE_FAILED=The DDE transaction failed.
MSG_ERR_DDE_TIMEOUT=The DDE transaction could not be completed because the request timed out.
MSG_ERR_DLL_NOT_FOUND=The specified dynamic-link library was not found.
MSG_ERR_NO_ASSOC=There is no application associated with the given file name extension.
MSG_ERR_NO_MEMORY=There was not enough memory to complete the operation.
MSG_ERR_SHARE_VIOLATION=A sharing violation occurred.
MSG_ERR_ZIP_FILE=Failed to extract zip file.
MSG_ERR_EXTRACT_STAGE=Extract stage failed.
MSG_ERR_CREATE_DIR=Could not create directory.
MSG_ERR_REGISTRY_MODIFY=Could not modify the Registry.
MSG_ERR_INIFILE_MODIFY=Could not modify INI file.
MSG_ERR_REGISTRY_READ=Could not read from the Registry.
MSG_ERR_NO_OPEN_KEY=Could not open key.
MSG_ERR_READ_VALUE=Could not read value.
MSG_ERR_INI_READ=Could not read from INI file.
MSG_ERR_CREATE_KEY=Could not create key.
MSG_ERR_DELETE_KEY=Could not delete key.
MSG_ERR_SET_VALUE=Could not set value.
MSG_ERR_DELETE_VALUE=Could not delete value.
MSG_ERR_DELETE_SECTION=Could not delete section.
MSG_ERR_MESSAGE_BOX=Could not display message box.
MSG_ERR_COPY_FILE=Could not copy file(s).
MSG_ERR_NOCOPY_ONEORMORE=One or more files could not be copied.
MSG_ERR_NOMOVE_ONEORMORE=One or more files could not be moved.
MSG_ERR_NODELETE_ONEORMORE=One or more files could not be deleted.
MSG_ERR_DELETE_FILE=Could not delete file(s).
MSG_ERR_RENAME_FILE=Could not rename file.
MSG_ERR_REMOVE_DIR=Could not remove directory.
MSG_ERR_INVALID_SOURCE=Invalid source specified.
MSG_ERR_INVALID_DESTINATION=Invalid destination specified.
MSG_ERR_DESTINATION_EXISTS=Destination already exists.
MSG_ERR_EVALUATING=Error evaluating expression.
MSG_ERR_MISSING_VALUE=Missing value. A value was expected at position %d.
MSG_ERR_MISSING_OPERATOR=Missing operator before open parenthesis. There is an operator missing before the open parenthesis at position %d.
MSG_ERR_READ_FILE_INFO=Could not read file information.
MSG_ERR_READ_CRC=Could not calculate file CRC.
MSG_ERR_READ_VER=Could not read file version.
MSG_ERR_READ_SIZE=Could not determine file size.
MSG_ERR_READ_FILE_ASSOC=Could not read file association.
MSG_ERR_FILETYPE=Invalid file type.
MSG_ERR_ENDLOOP_NF=End of loop not found.
MSG_ERR_IF=Syntax error in IF statement.
MSG_ERR_WHILE=Syntax error in WHILE statement.
MSG_ERR_GOTO=Could not GOTO label.
MSG_ERR_LABEL_NOT_FOUND=Label not found.
MSG_ERR_LINE=Line
MLMSG_ERR_CLOSE_PROGRAM=The program "%s" must be closed for this setup to be successful.\n\nPlease close the program and click Retry to continue.
MSG_ERR_NOTICE=Notice
MSG_ERR_SEND_EMAIL=Failed to send email.
MSG_ERR_INVALID_ADDRESS=Invalid address.
MSG_ERR_HELO_FAILED=HELO command was rejected or not responded to by the server.
MSG_ERR_ATTEMPT_CONNECT_FAILED=Attempt to connect to the server failed.
MSG_ERR_NO_CONNECTION=No connection.
MSG_ERR_DATA_FAILED=DATA command failed.
MSG_ERR_SOCKET_SEND_FAILED=Socket send command failed.
MSG_ERR_GET_TEMPFILE=Get temporary file name failed.
MSG_ERR_INVALID_PARAMETERS=Invalid parameter value(s).
MSG_ERR_MESG_TOOBIG=Message body is too big.
MSG_ERR_ATTACHMENT_ADD=Failed to add attachments to the message.
MSG_ERR_OPEN_ENCODING=Unable to open file for attachment encoding.
MSG_ERR_MOVE_FILE=Could not move file(s).
MSG_ERR_SERVER_ERRORCODE=Error code returned by server.
MSG_ERR_SUBMITTO_WEB=Submit to Web failed.
MSG_ERR_FILE_TOO_LARGE=The file is too large to be read.
MSG_ERR_READ_TEXT_FILE=Could not read text file.
MSG_ERR_WRITE_TEXT_FILE=Could not write to text file.
MSG_ERR_STOR_FAILED=STOR command failed.
MSG_ERR_INVALID_CHARS=Name contains invalid characters.
MSG_ERR_CORRUPT_FILE=Invalid or corrupt file.
MSG_ERR_CREATE_SHORTCUT=Failed to create shortcut.
MSG_ERR_SHORTCUT_SYSTEM=The shortcut could not be created by the system.
MSG_ERR_INSTALL_FILE=Failed to install file.
MSG_ERR_INVALID_FONTNAME=Invalid font name specified.
MSG_ERR_ADDFONT_FONTTABLE=Failed to add font to system font table.
MSG_ERR_ADDFONT_REGISTRY=Failed to add font to registry.
MSG_ERR_REGISTER_FONT=Failed to register font.
MSG_ERR_SET_FILEATTRIB=Failed to set file attributes.
MSG_ERR_QUERY_SERVICE=Failed to query service.
MSG_ERR_STOP_SERVICE=Failed to stop service.
MSG_ERR_START_SERVICE=Failed to start service.
MSG_ERR_PAUSE_SERVICE=Failed to pause service.
MSG_ERR_ITERATE_SERVICES=Iterate services failed.
MSG_ERR_QUERY_SERVICES=Query service failed.
MSG_ERR_SERVICE_NOTFOUND=Service not found.
MSG_ERR_COMMAND_FAILED=Command failed.
MSG_ERR_CONTINUE_SERVICE=Failed to continue service.
MSG_ERR_DELETE_SERVICE=Failed to delete service.
MSG_ERR_CREATE_SERVICE=Failed to create service.
MSG_ERR_MOVE_REBOOT=Move file on reboot failed.
MSG_ERR_DELETE_REBOOT=Delete file on reboot failed.
MSG_ERR_RUN_REBOOT=Run file on reboot failed.
MSG_ERR_COUNT_TEXT_LINES=Failed to count text lines.
MSG_ERR_DELETE_TEXT_LINES=Failed to delete text line.
MSG_ERR_LINE_OUT_OF_RANGE=Line number is out of range.
MSG_ERR_FIND_TEXT_LINE=Failed to find text line.
MSG_ERR_GET_TEXT_LINE=Failed to get text line.
MSG_ERR_INSERT_TEXT_LINE=Failed to insert text line.
MSG_ERR_CALL_DLL=Failed to call DLL function.
MSG_ERR_FAILED_LOAD_DLL=Could not load DLL.
MSG_ERR_FAILED_FIND_FUNCTION=Could not find function.
%SYSLANGUAGE%=9
%NEEDSREBOOT%=FALSE
%DOREBOOT%=FALSE
%LASTERRORNUM%=0
%LASTCOMMAND%=17
%LASTERRORMSG%=
%LASTERRORDETAILS%=
%PREVENTNEXTPAGE%=FALSE
%LINGUA%=EN
%RADIOSELECTIONINDEX%=0
%USERNAME%=Greg Schardt
%USERCOMPANY%=N/A
```
A12 : C://Program Files/Look@LAN/irunin.ini

---
Q13.  List the network cards used by this computer  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p ssid
Launching ssid v.20100301
ssid v.20100301
(Software) Get WZCSVC SSID Info

SSID
Microsoft\WZCSVC\Parameters\Interfaces

NIC: Compaq WL110 Wireless LAN PC Card
Key LastWrite: Fri Aug 27 15:46:19 2004 UTC

Thu Jan  1 00:00:00 1970 MAC: 00-C0-02-B9-00-78  SpeedStream

Microsoft\EAPOL\Parameters\Interfaces

NIC: Xircom CardBus Ethernet 100 + Modem 56 (Ethernet Interface)
LastWrite time: Thu Aug 19 22:52:00 2004 UTC
1    "3"3"3"3"3"3"3"3"3"3"

NIC: Compaq WL110 Wireless LAN PC Card
LastWrite time: Fri Aug 27 15:32:35 2004 UTC
1    "3"3"3"3"3"3"3"3"3"3"

root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p networkcards
Launching networkcards v.20080325
networkcards v.20080325
(Software) Get NetworkCards

NetworkCards
Microsoft\Windows NT\CurrentVersion\NetworkCards

Compaq WL110 Wireless LAN PC Card  [Fri Aug 27 15:31:44 2004]
Xircom CardBus Ethernet 100 + Modem 56 (Ethernet Interface)  [Thu Aug 19 17:07:19 2004]

```

A13 : Xircom CardBus Ethernet 100 + Modem 56 & Compaq WL110 Wireless LAN PC Card

---
Q14. This same file reports the IP address and MAC address of the computer. What are they?  
```
Keyword Search Result
%LANIP%=192.168.1.111
%LANNIC%=0010a4933e09
```
A14 : 192.168.1.111 & 0010a4933e09

---
Q15. An internet search for vendor name/model of NIC cards by MAC address can be used to find out which network interface was used. In the above answer, the first 3 hex characters of the MAC address report the vendor of the card. Which NIC card was used during the installation and set-up for LOOK@LAN?  
```
Use OUI lookup tool 
https://aruljohn.com/mac/0010A4933E09
```
A15 : XIRCOM

---
Q16. Find 6 installed programs that may be used for hacking.  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r WINDOWS/system32/config/software -p uninstall
Launching uninstall v.20140512
uninstall v.20140512
(Software, NTUSER.DAT) Gets contents of Uninstall keys from Software, NTUSER.DAT hives

Uninstall
Microsoft\Windows\CurrentVersion\Uninstall

Fri Aug 27 15:29:19 2004 (UTC)
  Ethereal 0.10.6 v.0.10.6

Fri Aug 27 15:15:19 2004 (UTC)
  WinPcap 3.01 alpha

Fri Aug 27 15:12:15 2004 (UTC)
  Network Stumbler 0.4.0 (remove only)

Wed Aug 25 15:56:11 2004 (UTC)
  Look@LAN 2.50 Build 29

Fri Aug 20 15:13:08 2004 (UTC)
  123 Write All Stored Passwords

Fri Aug 20 15:12:43 2004 (UTC)
  Powertoys For Windows XP v.1.00.0000

Fri Aug 20 15:10:04 2004 (UTC)
  mIRC

Fri Aug 20 15:09:03 2004 (UTC)
  CuteHTML

Fri Aug 20 15:09:02 2004 (UTC)
  CuteFTP

Fri Aug 20 15:08:19 2004 (UTC)
  Forté Agent

Fri Aug 20 15:07:25 2004 (UTC)
  Faber Toys v.2.4 Build 216

Fri Aug 20 15:05:58 2004 (UTC)
  Cain & Abel v2.5 beta45

Fri Aug 20 15:05:09 2004 (UTC)
  Anonymizer Bar 2.0 (remove only)

Thu Aug 19 23:04:50 2004 (UTC)
  WebFldrs XP v.9.50.5318

Thu Aug 19 23:04:36 2004 (UTC)
  Microsoft NetShow Player 2.0
  MPlayer2

Thu Aug 19 22:37:31 2004 (UTC)
  Branding

Thu Aug 19 22:32:06 2004 (UTC)
  PCHealth

Thu Aug 19 22:31:52 2004 (UTC)
  DirectAnimation
  NetMeeting

Thu Aug 19 22:31:51 2004 (UTC)
  AddressBook
  ICW
  OutlookExpress

Thu Aug 19 22:31:32 2004 (UTC)
  DirectDrawEx
  Fontcore
  IE40
  IE4Data
  IE5BAKEX
  IEData
  MobileOptionPack
  SchedulingAgent

Thu Aug 19 22:21:41 2004 (UTC)
  Connection Manager
```
A16 : 
 - Cain & Abel v2.5 beta45 (password sniffer & cracker) 
 - Ethereal (packet sniffer) 
 - 123 Write All Stored Passwords (finds passwords in registry) 
 - Anonymizer (hides IP tracks when browsing) CuteFTP (FTP software) 
 - Look&LAN_1.0 (network discovery tool) 
 - NetStumbler (wireless access point discovery tool

---
Q17. What is the SMTP email address for Mr. Evil?  
```
root@siftworkstation -> /m/windows_mount 
# rip.pl -r Documents\ and\ Settings/Mr.\ Evil/NTUSER.DAT -p unreadmail
Launching unreadmail v.20100218
unreadmail v.20100218
(NTUSER.DAT) Gets contents of Unreadmail key

LastWrite Time Fri Aug 20 21:18:30 2004 (UTC)

whoknowsme@sbcglobal.net
LastWrite Time Fri Aug 20 21:18:30 2004 (UTC)
  MessageCount: 0
  Application : msimn
  TimeStamp   : Fri Aug 20 21:18:30 2004 (UTC)
```
A17 : whoknowsme@sbcglobal.net

---
Q18. What are the NNTP (news server) settings for Mr. Evil?  
```
root@siftworkstation -> /m/windows_mount 
# cat Program\ Files/Agent/Data/AGENT.INI

[Servers]
NewsServer="news.dallas.sbcglobal.net"
MailServer="smtp.sbcglobal.net"
POPServer=""
NNTPPort=119
SMTPPort=25
POPPort=110
SMTPServerPort=25
```
A19 : news.dallas.sbcglobal.net

---
Q19. What two installed programs show this information?  
```
root@siftworkstation -> /m/windows_mount 
# grep -iR --color=auto "news.dallas.sbcglobal.net" *
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.cardz.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.codez.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.crackz.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.hackerz.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.phreakz.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.2600.programz.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.binaries.hacking.beginner.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.binaries.hacking.computers.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.dss.hack.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.hacking.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/alt.nl.binaries.hack.dbx matches
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/Folders.dbx matches
Binary file Documents and Settings/Mr. Evil/NTUSER.DAT matches
grep: $Extend/$ObjId: No such file or directory
grep: $Extend/$Quota: No such file or directory
grep: $Extend/$Reparse: No such file or directory
Program Files/Agent/Data/AGENT.INI:NewsServer="news.dallas.sbcglobal.net"
grep: $Secure: No such file or directory
```
A19 : Microsoft Outlook & Forte Agent

---
Q20. List 5 newsgroups that Mr. Evil has subscribed to?  
```
According to this link -> https://www.mailxaminer.com/blog/outlook-express-email-forensics/
I searched Inbox.dbx file

root@siftworkstation -> /m/windows_mount 
# grep -iR "Inbox.dbx"
Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/cleanup.log:CLEANUP: 16:13:57 [db]    Inbox.dbx, CompactAt: 20%, Wasted: 22%, File: 000142036, Records: 00000001, Allocated: 000011648, Freed: 00002660, Streams: 00010560, RemovedRead: 0, RemovedExpired: 0, JunkDeleted: 0
Binary file Documents and Settings/Mr. Evil/Local Settings/Application Data/Identities/{EF086998-1115-4ECD-9B13-9ADC067B4929}/Microsoft/Outlook Express/Folders.dbx matches

root@siftworkstation -> /m/w/D/M/L/A/I/{/M/Outlook Express 
# ls
alt.2600.cardz.dbx                  alt.binaries.hacking.utilities.dbx   free.binaries.hacking.beginner.dbx
alt.2600.codez.dbx                  alt.binaries.hacking.websites.dbx    free.binaries.hacking.computers.dbx
alt.2600.crackz.dbx                 alt.dss.hack.dbx                     free.binaries.hacking.talentless.troll_haven.dbx
alt.2600.dbx                        alt.hacking.dbx                      free.binaries.hacking.talentless.troll-haven.dbx
alt.2600.hackerz.dbx                alt.nl.binaries.hack.dbx             free.binaries.hacking.utilities.dbx
alt.2600.moderated.dbx              alt.stupidity.hackers.malicious.dbx  free.binaries.hacking.websites.dbx
alt.2600.phreakz.dbx                cleanup.log                          Inbox.dbx
alt.2600.programz.dbx               Deleted Items.dbx                    Offline.dbx
alt.binaries.hacking.beginner.dbx   Folders.dbx                          Outbox.dbx
alt.binaries.hacking.computers.dbx  free.binaries.hackers.malicious.dbx
```
A20 : 
 - alt.2600.cardz                
 - alt.binaries.hacking.utilities 
 -  free.binaries.hacking.beginner
 - alt.2600.codez             
 - alt.binaries.hacking.websites
 - free.binaries.hacking.computers

---

Q21. A popular IRC (Internet Relay Chat) program called MIRC was installed.  What are the user settings that was shown when the user was online and in a chat channel?  
```
According to this link -> https://ir3e.com/chapter-14-additional-im-clients/
I searched at Application Data for Windows XP but work with following

root@siftworkstation -> /m/w/Program Files 
# ls
123WASP      CHAT                  Ethereal           Look@LAN             MSN               Outlook Express        Windows NT
Accessories  Common Files          Faber Toys         Messenger            MSN Gaming Zone   PLUS!                  WindowsUpdate
Agent        ComPlus Applications  folder.htt         microsoft frontpage  NetMeeting        Uninstall Information  WinPcap
Anonymizer   desktop.ini           GlobalSCAPE        mIRC                 Network Stumbler  Whois                  xerox
Cain         DirectX               Internet Explorer  Movie Maker          Online Services   Windows Media Player

root@siftworkstation -> /m/w/P/mIRC 
# ls
aliases.ini  download      logs      mirc.hlp  popups.ini  servers.ini  urls.ini
channels     ircintro.hlp  mirc.exe  mirc.ini  readme.txt  sounds       versions.txt
root@siftworkstation -> /m/w/P/mIRC 
# cat mirc.ini 
[chanfolder]
n0=#AllNiteCafe
n1=#Beginner
n2=#Cafebleu
n3=#Casual
n4=#CasualChat
n5=#Chat-World
n6=#Chataholics
n7=#Chataway
n8=#chatbuddies
n9=#Chatterz,"Fun chat for all =)"
n10=#Chatzone
n11=#Cheers
n12=#Cybar
n13=#CyberCafe
n14=#CyberChat
n15=#CyberFriends
n16=#CyberParty
n17=#CyberWorld
n18=#DewDropInn
n19=#Family_Chat
n20=#FunChat
n21=#Funfactory
n22=#FunnyWorld
n23=#Funshack,"The Fun and Friendly, All Welcome, Funchannel"
n24=#Giggles
n25=#Help
n26=#HelpDesk
n27=#Hottub,"Relaxing Chat"
n28=#IRCAddicts
n29=#ircbar
n30=#irchelp,"General IRC Help"
n31=#irclub
n32=#ircnewbies,"IRC/mIRC Questions Answered with a Smile :-)"
n33=#ircpassage
n34=#ircsupport
n35=#irctalk
n36=#IRCWavPlayers,"mIRC Wavs & Ascii"
n37=#JustChillin
n38=#mIRC,"Ask mIRC Questions Here! (no chatting)"
n39=#mIRC4Dummies
n40=#mIRCAide
n41=#mIRCBeginners
n42=#mIRChat,"A Family Channel For All Ages on mIRC :-)"
n43=#mIRCHelp,"mIRC Questions Welcomed! :)"
n44=#mIRCIntro
n45=#mIRCLife,"Relax & Enjoy Life!"
n46=#mIRCScripts
n47=#mIRCSetUp
n48=#mIRCsupport
n49=#mIRC_Colors
n50=#mIRC_HelpDesk
n51=#mIRC_Lounge
n52=#mIRC_Rainbow,"mIRC Help, Colours, and Popups!"
n53=#mIRC_Wavs'N'Text
n54=#NetChat
n55=#new2irc
n56=#new2mIRC
n57=#newbiehelp,"Friendly chat and help for beginners"
n58=#newbies
n59=#NewsTalk
n60=#PartyHouse,"Party Party Party!"
n61=#PlanetChat
n62=#PopInn,"Friendly Chat, Popups & Colours help"
n63=#SpeakEasy
n64=#Speaker's_corner
n65=#Teen
n66=#TeenConnection
n67=#TeenFactory
n68=#TeenLounge
n69=#TeenParty
n70=#Teens
n71=#TeenWorld
n72=#TeenZone
n73=#TwilightTavern
n74=#Txtworld,"mIRC help, texts & wavs, Ascii, classes"
n75=#UserGuide,"The official Undernet help channel"
n76=#UserHelp
n77=#Wasteland
n78=#Windows95
n79=#Winsock
n80=#WiredPatrol,"Internet Help and Safety Education"
n81=#Wobblyworld
n82=#Worldchat

[text]
accept=*.bmp,*.gif,*.jpg,*.log,*.mid,*.mp3,*.png,*.txt,*.wav,*.wma,*.zip
ignore=*.exe,*.com,*.bat,*.dll,*.ini,*.mrc,*.vbs,*.js,*.pif,*.scr,*.lnk,*.pl,*.shs,*.htm,*.html
network=All
commandchar=/
linesep=-
timestamp=[HH:nn]
theme=mIRC Classic



[dirs]
logdir=logs\
waves=sounds\
midis=sounds\
mp3s=sounds\
wmas=sounds\
oggs=sounds\
[options]
n0=0,1,0,1,0,0,300,1,0,0,1,0,0,0,0,0,1,0,0,0,4096,0,1,0,0,0,1,1,0,50,0,1,0,1,0
n1=5,100,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,5,0,0,0,0,0,1,0,0,0,1,10
n2=0,1,0,1,1,1,1,1,0,60,120,0,0,1,0,0,1,1,1,120,20,10,0,1,1,0,1,1,0,0,0,0,0,0,1
n3=5000,0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,1,3,180,0,1
n4=1,0,1,0,0,0,9999,0,0,0,1,0,1024,1,1,99,60,0,0,1,1,1,1,0,1,5000,1,5,0,0,3,0,1,1,0
n5=1,1,1,1,1,1,1,1,1,1,6667,0,0,0,1,0,1,0,300,30,10,0,1,26,0,0,1,8192,1,0,0,82,0,1
n6=0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,100,1,1,0,1,1,0,0,4,1,0,1,0
n7=1,0,0,0,1,1,0,1,1,1,1,1,0,1,0,0,1,70,0,3,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1
[about]
version=6.12
[ports]
random=off
bind=off
[ident]
active=yes
userid=Mrevil
system=UNIX
port=113
[socks]
enabled=no
port=1080
method=4
dccs=no
useip=yes
[language]
sjis=0
multibyte=0
[clicks]
status=/lusers
query=/whois $$1
channel=/channel
nicklist=/query $$1
notify=/whois $$1
message=/whois $$1
[dde]
ServerStatus=on
ServiceName=mIRC
CheckName=off
[marker]
show=off
size=3
colour=4
method=1
[warn]
dcc=on
fserve=on
link=off
[fileserver]
homedir=C:\Temp
[dccserver]
n0=1,59,0,0,0,1
[agent]
enable=0,0,0
char=merlin.acs
lang=0x0409
options=1,1,1,100,0
speech=150,60,100,1,180,10,50,1,1,1,0,50,1
channel=1,1,1,1,1,1,1,1,1
private=1,1,1,1
other=1,1,1,1,1,1,1
pos=20,20
[mirc]
user=Mini Me
email=none@of.ya
nick=Mr
anick=mrevilrulez
host=Undernet: US, CA, LosAngelesSERVER:losangeles.ca.us.undernet.org:6660GROUP:Undernet
[files]
servers=servers.ini
finger=finger.txt
urls=urls.ini
addrbk=addrbk.ini
[styles]
thin=1
font=1
hide=1
color=default
size=2
buttons=0
[channelslist]
last=channels.txt
[windows]
wlist=-1,764,-1,358,0,1,0
wchannel=3,795,21,287,0,1,0
main=100,600,41,490,2,1,0
wquery=21,665,21,358,0,1,0
[pfiles]
n0=popups.ini
n1=popups.ini
n2=popups.ini
n3=popups.ini
n4=popups.ini
[waves]
send=Event Beep
[dragdrop]
n0=*.wav:/sound $1 $2-
n1=*.*:/dcc send $1 $2-
s0=*.*:/dcc send $1 $2-
[extensions]
n0=defaultEXTDIR:download\
n1=*.wav,*.mid,*.mp3,*.wma,*.oggEXTDIR:sounds\
[colors]
n0=mIRC Classic,0,6,4,5,2,3,3,3,3,3,3,1,5,7,6,1,3,2,3,5,1,0,1,0,1,15,6,0
n1=mIRC Modern,0,6,4,7,2,3,4,3,3,3,3,1,5,2,6,1,14,2,3,5,1,0,1,0,1,14,5,0
n2=Monochrome State,1,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,1,15,1,15,15,15,14
n3=Placid Hues,0,2,4,7,2,3,3,3,3,15,3,1,5,7,6,1,3,2,3,5,1,0,1,0,1,15,6,0
n4=Rainbow Sky,0,7,4,5,1,1,3,3,8,13,3,14,2,7,13,5,3,8,3,4,14,0,5,0,3,14,10,0
[palettes]
n0=16777215,0,8323072,37632,255,127,10223772,32764,65535,64512,9671424,16776960,16515072,16711935,8355711,13816530
n1=16777215,0,11010048,3299627,240,4737160,8388720,26832,1632504,57344,94740,16776960,16515072,16711935,8355711,13816530
n2=16777215,0,8323072,37632,255,127,10223772,32764,65535,64512,9671424,16776960,16515072,16711935,8355711,13816530
n3=15658734,0,12140,1508038,255,10964547,6579262,33023,65535,4227072,9474048,9920537,16711680,16711935,6579300,8553090
n4=16777215,3618615,12087408,16744448,255,32764,65535,43008,9671424,16776960,16515072,16711935,8355711,16711808,8355711,13816530
[afiles]
n0=aliases.ini
[rfiles]
n0=remote.ini
n1=remote.ini


```
A21 : user=Mini Me
email=none@of.ya
nick=Mr
anick=mrevilrulez
host=Undernet: US, CA, LosAngelesSERVER:losangeles.ca.us.undernet.org:6660GROUP:Undernet

---
Q22. This IRC program has the capability to log chat sessions. List 3 IRC channels that the user of this computer accessed.  
```
root@siftworkstation -> /m/w/P/mIRC 
# ls logs/
#Chataholics.UnderNet.log    #evilfork.EFnet.log    #ISO-WAREZ.EFnet.log    #mp3xserv.UnderNet.log
#CyberCafe.UnderNet.log      #funny.UnderNet.log    #LuxShell.UnderNet.log  #thedarktower.AfterNET.log
#Elite.Hackers.UnderNet.log  #houston.UnderNet.log  m5tar.UnderNet.log      #ushells.UnderNet.log

```
A22 :

- Chataholics.UnderNet.log    
-  evilfork.EFnet.log    
- ISO-WAREZ.EFnet.log    
- mp3xserv.UnderNet.log
- CyberCafe.UnderNet.log      
- funny.UnderNet.log    
- LuxShell.UnderNet.log  
- thedarktower.AfterNET.log
- Elite.Hackers.UnderNet.log  
- houston.UnderNet.log  
- m5tar.UnderNet.log      
- ushells.UnderNet.log

---
Q23. Ethereal, a popular “sniffing” program that can be used to intercept wired and wireless internet packets was also found to be installed. When TCP packets are collected and re-assembled, the default save directory is that users \My Documents directory. What is the name of the file that contains the intercepted data?  
```
root@siftworkstation -> /m/w/D/M/A/Ethereal 
# cat recent 
# Recent settings file for Ethereal 0.10.6.
#
# This file is regenerated each time Ethereal is quit.
# So be careful, if you want to make manual changes here.

######## Recent capture files (latest last) ########

recent.capture_file: C:\Documents and Settings\Mr. Evil\interception

######## Recent display filters (latest last) ########

recent.display_filter: (ip.addr eq 192.168.254.2 and ip.addr eq 207.68.174.248) and (tcp.port eq 1337 and tcp.port eq 80)

# Main Toolbar show (hide).
# TRUE or FALSE (case-insensitive).
gui.toolbar_main_show: TRUE

# Filter Toolbar show (hide).
# TRUE or FALSE (case-insensitive).
gui.filter_toolbar_show: TRUE

# Packet list show (hide).
# TRUE or FALSE (case-insensitive).
gui.packet_list_show: TRUE

# Tree view show (hide).
# TRUE or FALSE (case-insensitive).
gui.tree_view_show: TRUE

# Byte view show (hide).
# TRUE or FALSE (case-insensitive).
gui.byte_view_show: TRUE

# Statusbar show (hide).
# TRUE or FALSE (case-insensitive).
gui.statusbar_show: TRUE

# Timestamp display format.
# One of: RELATIVE, ABSOLUTE, ABSOLUTE_WITH_DATE, DELTA
gui.time_format: RELATIVE

# Zoom level.
# A decimal number.
gui.zoom_level: 0

# Main window geometry.
# Decimal integers.
gui.geometry_main_x: 20
gui.geometry_main_y: 20
gui.geometry_main_width: 800
gui.geometry_main_height: 553

# Main window maximized (GTK2 only).
# TRUE or FALSE (case-insensitive).
gui.geometry_main_maximized: TRUE

# Main window panes (GTK2 only).
# Decimal numbers.
gui.geometry_main_upper_pane: 280
gui.geometry_main_lower_pane: 68
gui.geometry_status_pane: 141

# Last directory navigated to in File Open dialog.
gui.fileopen_remembered_dir: C:\Documents and Settings\Mr. Evil\


```
A23 : interception

---
Q24. Viewing the file in a text format reveals much information about who and what was intercepted. What type of wireless computer was the victim (person who had his internet surfing recorded) using?  
```
root@siftworkstation -> /m/w/D/Mr. Evil 
# cat interception 

We got User Agent String in HTTP request

User-Agent: Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; 240x320)

Here is User Agent to OS Lookup tool -> https://userstack.com/

os: Object {}

name: "Windows CE"

code: "windows_ce"

url: "https://en.wikipedia.org/wiki/Windows_CE"

family: "Windows"

family_code: "windows"

family_vendor: "Microsoft Corporation."
```
A24 : Windows CE

---
Q25. What websites was the victim accessing?  
```
Opened interception file with wireshark
Filtered http.request
Apply Host as column to clear vision
```
A25 : 
 - mobile.msn.com
 - passportimages.com
 - login.passport.com
 - login.passport.net

---
Q26. Search for the main users web based email address. What is it?  
```
I thought it was in pcap file. 
Finding email with wireshark -> https://osqa-ask.wireshark.org/questions/49666/how-to-look-up-email-addresses-in-a-packet
Regular Expression Tested with -> https://regex101.com/
My Pattern -> [a-zA-Z0-9]+@+[a-zA-Z]+.+[a-zA-Z]{2,3}

But i found only 3 mails that are not equal to official answer.

root@siftworkstation -> /m/w/D/Mr. Evil 
# egrep -rohI "[a-zA-Z0-9]+@+[a-zA-Z]+.+[a-zA-Z]{2,3}" * > /home/sansforensics/Desktop/emails.txt

root@siftworkstation -> /m/w/D/Mr. Evil 
# sort -r /home/sansforensics/Desktop/emails.txt 
you@your-name.com, if available</li
Ultr@VNC</a></b> - <small
Ultr@VNC</a></b> - <small
teandson@aol.com&gt; wrote in<BR
T50admin@usa.net>Email Webmaster</a> - we receive a lot of mail, but we will try to reply to allmesgs within a reasonable amount of time.<P><BR><BR><BR><font color=ffffff size=2 face=arial>Copyright &copy; 1998-2001 T50.com All Rights Reserved.<BR>Reproduction  in whole or in part or in any form or medium without express written permission of T50.com is prohibited! </TD></TR></TABLE><BR><font size=1></body></html><P>CGI Script Copyright 1998 <A HREF=http://www.splitinfinity.com/cgi-bin/topsites/topvlog.cgi?974294527>Splitinfinity</A></CENTER></BODY></HTML
suckme@oyea.lick&gt;&nbsp; wrote :<BR
suckme@oyea.lick&gt;&nbsp; wrote :<BR
slim532@hotmail.com&gt; wrote in message <BR
slim532@hotmail.com&gt; wrote in message<BR
seabach@shaw.ca&gt; wrote in message<BR
Rating@Mail.ru COUNTER--><script language="JavaScript
Rating@Mail.ru COUNTER--><script language="JavaScript
Rating@Mail.ru COUNTER--><script language="JavaScript
president@whitehouse.gov&gt; wrote in message <BR
PASSCODE@HOTMAIL.COM&gt;<BR
PASSCODE@HOTMAIL.COM&gt;<BR
PASSCODE@HOTMAIL.COM&gt;<BR
PASSADMINBOT@HOTMAIL.COM<BR
PASSADMINBOT@HOTMAIL.COM<BR
PASSADMINBOT@HOTMAIL.COM<BR
O8R9W@VN8|K&lt;%2/2D9$ELGD&lt;MA:ZLLXD&lt;Z&amp;),3G!,?%BS)B27U|<BR
nightwolf@confine.com?subject=UA>CONTACT</a></font
name@@@@index#@@" class="reuse"></span
mrevilrulez@yahoo.com</title
mrevilrulez@yahoo.com</title
mrevilrulez@yahoo.com</title
mrevilrulez@yahoo.com</title
mrevilrulez@yahoo.com</td></tr
mrevilrulez@yahoo.com</font></b></font></td></tr
mrevilrulez@yahoo.com,<br><br
mrevilrulez@yahoo.com</b></font
mrevilrulez@yahoo.com</b> [<a href="/ym/Logout?YY=90802&.first=1&order=down&sort=date&pos=0&YY=90802">Sign Out
mrevilrulez@yahoo.com</b> [<a href="/ym/Logout?YY=78169&.first=1&YY=78169">Sign Out
mrevilrulez@yahoo.com</b> [<a href="/ym/Logout?YY=60138&.first=1&inc=25&order=down&sort=date&pos=0&view=&head=&box=Inbox&YY=60138">Sign Out
mrevilrulez@yahoo.com</b> [<a href="/ym/Logout?YY=27630&.first=1&inc=25&order=down&sort=date&pos=0&view=&head=&box=Inbox&YY=27630">Sign Out
mikelee@yahoo-inc.com
mauddib@dune.com&gt; wrote in message<BR
mailbot@yahoo.com
Look@LAN will automatically start in a few seconds...<br><A HREF="downloadget.php?id=3365&file=1&evp=8c4e1708b75a9fdf7d2def11ad57d070">Click here if it does not
Look@LAN, Look@Lan, Management, Monitor, Network, Profile, Profiles, Reporting, Scan-Ranges, Scanning, Settings, Statistics, Trapping, World's, advanced, auto-detect, available, discovering, download, features, monitor, network, network's, relevant, statistics
Look@Lan is an advanced network monitor that allows you to monitor your net in few clicks. Extremely easy to use and very fast in discovering your network's active nodes. Full of relevant features such as: auto-detect of network configuration, monitoring, reporting, trapping, statist<br /><b>Limitations:</b> Look@LAN Network Monitor 2.50 Build 29 is still available for download but is no more supported
Look@LAN</a></b> - <small
Look@LAN</a></b> - <small
Look@LAN 2.50 Build 29</title
Look@LAN 2.50 Build
logaritmo50@yahoo.com &amp; logaritmo50@hotmail.com<BR
LmT@marijuana.com">..</a></font></font></font
jim@mcmahon.cc) on
jim@mcmahon.cc) on
jim@mcmahon.cc) on
jim@mcmahon.cc) on
jfoster3@ec.rr.com&gt; wrote in message<BR
info@mosnews.com" id=db><b>info@mosnews.com</b></a><br
info@mosnews.com" id=db><b>info@mosnews.com</b></a><br
info@mosnews.com" id=db><b>info@mosnews.com</b></a><br
hp01@mailadded.com<BR
heyjude18@hotmail.com...as<BR
HERE@HOTMAIL.COM&gt;<BR
HERE@HOTMAIL.COM&gt;<BR
HERE@HOTMAIL.COM&gt;<BR
frisco@blackant.net, which he used to map Ann Arbor, MI<br
fred@wardriving.com-NOSPAM">Email Contact</a><br
fred@wardriving.com-NOSPAM">Contact</a><br
fred@wardriving.com-NOSPAM">Contact</a><br
eliteh@V" target=_blank>Sex Movies<br>Instant Access!</a></b></tt></center
eliteh@F" TARGET="_blank">Forbidden Asian</a></b></tt></center
ECJ@O/&quot;<BR
drudge@drudgereport.com">EMAIL: DRUDGE@DRUDGEREPORT.COM</a><hr
DI10022@esus5" target=_blank>Euro Teen Sluts</a></tt></b></center
corenode01a@yahoo.removethisfirst.com&gt; wrote:<BR
chris@splitinfinity.com
chillen@hoo.com&gt; wrote in message<BR
cathomas@msn.com&gt; wrote in message<BR
beatnik@mail.gr&gt;<BR
a30aac9@posting.google.com...<BR
a30aac9@posting.google.com...<BR
42522@pd7tw2no...<BR
11@fed1read04...<BR
10237466@twister.southeast.rr.com...<BR

```
A26 : mrevilrulez@yahoo.com

---
Q27. Yahoo mail, a popular web based email service, saves copies of the email under what file name?  
```
root@siftworkstation -> /m/w/D/Mr. Evil 
# grep -iR "yahoo"

After Login 

Local Settings/Temporary Internet Files/Content.IE5/PN0J7OQM/ShowLetter[1].htm
```

A27 : ShowLetter[1].htm

---
Q28. How many executable files are in the recycle bin? 
```
root@siftworkstation -> /m/windows_mount 
# ls -l RECYCLER/S-1-5-21-2000478354-688789844-1708537768-1003/
total 12103
-rwxrwxrwx 1 root root 2160043 Aug 25  2004 Dc1.exe
-rwxrwxrwx 1 root root 1324940 Aug 27  2004 Dc2.exe
-rwxrwxrwx 1 root root  442417 Aug 27  2004 Dc3.exe
-rwxrwxrwx 1 root root 8460502 Aug 27  2004 Dc4.exe
-rwxrwxrwx 1 root root      65 Aug 25  2004 desktop.ini
-rwxrwxrwx 1 root root    3220 Aug 27  2004 INFO2
``` 
A28 : 4

---
Q29. Are these files really deleted?  

A29 : No

---
Q30. How many files are actually reported to be deleted by the file system?  
```
# cat RECYCLER/S-1-5-21-2000478354-688789844-1708537768-1003/INFO2 
 >�C:\Documents and Settings\Mr. Evil\Desktop\lalsetup250.exe�%���� C:\Documents and Settings\Mr. Evil\Desktop\lalsetup250.exeC:\Documents and Settings\Mr. Evil\Desktop\netstumblerinstaller_0_4_0.exe�-�EH��8C:\Documents and Settings\Mr. Evil\Desktop\netstumblerinstaller_0_4_0.exeC:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exe`�H���C:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exeC:\Documents and Settings\Mr. Evil\Desktop\ethereal-setup-0.10.6.exe���J����C:\Documents and Settings\Mr. Evil\Desktop\ethereal-setup-0.10.6.exe
```
A30 : 4

---
Q31. Perform a Anti-Virus check. Are there any viruses on the computer?
```
root@siftworkstation -> /m/windows_mount 
# clamscan -ir . > /home/sansforensics/Desktop/av_result.txt

i -> infected only

root@siftworkstation -> /m/windows_mount 
# cat /home/sansforensics/Desktop/av_result.txt 
./My Documents/COMMANDS/enum.exe: Win.Tool.EnumPlus-1 FOUND
./My Documents/COMMANDS/SAMDUMP.EXE: Win.Trojan.Pwdump-2 FOUND
./My Documents/COMMANDS/snitch.exe: Win.Trojan.Snitch-1 FOUND
./My Documents/ENUMERATION/NT/enum/enum.tar.gz: Win.Tool.EnumPlus-1 FOUND
./My Documents/ENUMERATION/NT/enum/files/enum.exe: Win.Tool.EnumPlus-1 FOUND
./My Documents/ENUMERATION/NT/Legion/Chrono.dl_: Win.Trojan.Bruteforce-3 FOUND
./My Documents/ENUMERATION/NT/Legion/NetTools.ex_: Win.Trojan.Spion-4 FOUND
./My Documents/ENUMERATION/NT/ntreskit.zip: Win.Trojan.Nemo-1 FOUND
./My Documents/EXPLOITATION/NT/Brutus/BrutusA2.exe: Win.Tool.Brutus-3 FOUND
./My Documents/EXPLOITATION/NT/brutus.zip: Win.Tool.Brutus-3 FOUND
./My Documents/EXPLOITATION/NT/Get Admin/GetAdmin.exe: Win.Exploit.WinNT-3 FOUND
./My Documents/EXPLOITATION/NT/lsadump2/lsadump2.exe: Win.Trojan.Lsadump-1 FOUND
./My Documents/EXPLOITATION/NT/lsadump2/lsadump2.zip: Win.Trojan.Lsadump-1 FOUND
./My Documents/EXPLOITATION/NT/netbus/NetBus170.zip: Win.Trojan.Netbus-2 FOUND
./My Documents/EXPLOITATION/NT/sechole/SECHOLE.EXE: Win.Trojan.Sehole-1 FOUND
./My Documents/EXPLOITATION/NT/sechole/sechole3.zip: Win.Trojan.Sehole-1 FOUND
./My Documents/EXPLOITATION/NT/WinVNC/Windows/vnc-3.3.3r7_x86_win32.zip: Win.Tool.Winvnc-10 FOUND
./My Documents/FOOTPRINTING/NT/superscan/superscan.exe: Win.Trojan.Agent-6240252-0 FOUND
./Program Files/Cain/Abel.dll: Win.Trojan.Cain-9 FOUND
./Program Files/Online Services/MSN50/MSN50.CAB: Txt.Malware.CMSTPEvasion-6664831-0 FOUND
./WIN98/WIN98_OL.CAB: Txt.Malware.CMSTPEvasion-6664831-0 FOUND
./WINDOWS/system32/ahui.exe: Win.Virus.Virut-6804272-0 FOUND
./WINDOWS/system32/dllcache/ahui.exe: Win.Virus.Virut-6804272-0 FOUND
./WINDOWS/system32/dllcache/mmc.exe: Win.Virus.Virut-6804520-0 FOUND
./WINDOWS/system32/mmc.exe: Win.Virus.Virut-6804520-0 FOUND

----------- SCAN SUMMARY -----------
Known viruses: 6136447
Engine version: 0.99.4
Scanned directories: 767
Scanned files: 11240
Infected files: 25
Total errors: 71
Data scanned: 1468.10 MB
Data read: 1794.54 MB (ratio 0.82:1)
Time: 1118.606 sec (18 m 38 s)

```

A31 : Yes

---
**Tips & Tricks :floppy_disk:**

 - Find the keyword in regripper plugin lists ( http://hexacorn.com/tools/3r.html )
 - rip.pl -l > plugins.txt
cat plugins.txt | grep "something"
 - Searching google like [this](https://www.google.com/search?client=ubuntu&channel=fs&q=registry%20forensics&ie=utf-8&oe=utf-8) 

---

**References :floppy_disk:**

```
https://brettshavers.com/brett-s-blog/entry/regripper
http://what-when-how.com/windows-forensic-analysis/
http://network-forensics.blogspot.com/2010/01/nist-forensic-challenge_04.html
http://hetzellconsulting.com/CCFE%20Certification%20Practical%20Exam.pdf
https://www.geeksforgeeks.org/sort-command-linuxunix-examples/
https://resources.infosecinstitute.com/recycle-bin-forensics/#gref
https://www.clamav.net/documentation
```
