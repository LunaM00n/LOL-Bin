## Android Memory Analysis

**Challenge Files**
```
- Bin file of Memory Dump
- module.dwarf & system.map
```

Goal : *"Retrieve Some Encrypted Information from Android Memory Dump"*

Before we learn memory analysis on Android , we need to read some papers and tutorials for Android Memory Analysis.
[ [Here](https://www1.informatik.uni-erlangen.de/filepool/publications/Live_Memory_Forensics_on_Android_with_Volatility.pdf) ] is the Paper for Android Live Memory Forensics Paper.

**Volatility Installation**

Read [this](https://dfironthemountain.wordpress.com/2018/10/29/installing-volatility-on-windows/) 

**Creating Profile for Volatility**

 - We need to create volatility profile for Android because of the following reasons.
```
First, Volatility development has
started from a Microsoft Windows point of view. So because Linux and Android
support is quite new, there are less corresponding proles available by default.
Second, there are a lot more dierent 
avours of dierent kernels available in the
Linux and Android market. For Windows, there is basically always just one most
recent version available. Being it Windows 8, Windows 7 or Windows 2000
```
According to paper, we can check our volatility profile.

 - Volatility Profiles
```
$volatility.exe --info
Volatility Foundation Volatility Framework 2.3.1


Profiles
--------
VistaSP0x64     - A Profile for Windows Vista SP0 x64
VistaSP0x86     - A Profile for Windows Vista SP0 x86
VistaSP1x64     - A Profile for Windows Vista SP1 x64
VistaSP1x86     - A Profile for Windows Vista SP1 x86
VistaSP2x64     - A Profile for Windows Vista SP2 x64
VistaSP2x86     - A Profile for Windows Vista SP2 x86
Win2003SP0x86   - A Profile for Windows 2003 SP0 x86
Win2003SP1x64   - A Profile for Windows 2003 SP1 x64
Win2003SP1x86   - A Profile for Windows 2003 SP1 x86
Win2003SP2x64   - A Profile for Windows 2003 SP2 x64
Win2003SP2x86   - A Profile for Windows 2003 SP2 x86
Win2008R2SP0x64 - A Profile for Windows 2008 R2 SP0 x64
Win2008R2SP1x64 - A Profile for Windows 2008 R2 SP1 x64
Win2008SP1x64   - A Profile for Windows 2008 SP1 x64
Win2008SP1x86   - A Profile for Windows 2008 SP1 x86
Win2008SP2x64   - A Profile for Windows 2008 SP2 x64
Win2008SP2x86   - A Profile for Windows 2008 SP2 x86
Win7SP0x64      - A Profile for Windows 7 SP0 x64
Win7SP0x86      - A Profile for Windows 7 SP0 x86
Win7SP1x64      - A Profile for Windows 7 SP1 x64
Win7SP1x86      - A Profile for Windows 7 SP1 x86
WinXPSP1x64     - A Profile for Windows XP SP1 x64
WinXPSP2x64     - A Profile for Windows XP SP2 x64
WinXPSP2x86     - A Profile for Windows XP SP2 x86
WinXPSP3x86     - A Profile for Windows XP SP3 x86
```
In my installed volatility only have the profiles for Windows Machine.

**Linux Kernel Analysis**

- system.map
```
The System.map contains the name and addresses of static data structures in
the Linux kernel.
```
- module.dwarf
```
The module.dwarf emerges by compiling a module against the target kernel
and afterwards extracting the DWARF debugging information out of it. DWARF
is a standardized debugging format used by some source level debuggers to establish
a logical connection between a output binary and the actual source code
(Eager & Consulting, 2007)
```
 - creating profile 
```
$ zip <profile_name>.zip <path_to_module.dwarf> \
<path_to_System.map>
```
We have to compressed this two file , I used WinRar.
 - Copying zip files to volatility/plugins/overlays/linux/

```
vol.py --info
Volatility Foundation Volatility Framework 2.6.1


Profiles
--------
LinuxAndroidARM       - A Profile for Linux Android ARM
```
**Memory Analysis**
Help me
```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM -h
Volatility Foundation Volatility Framework 2.6.1
Usage: Volatility - A memory forensics analysis platform.

Options:
  -h, --help            list all available options and their default values.
                        Default values may be set in the configuration file
                        (/etc/volatilityrc)
  --conf-file=.volatilityrc
                        User based configuration file
  -d, --debug           Debug volatility
  --plugins=PLUGINS     Additional plugin directories to use (semi-colon
                        separated)
  --info                Print information about all registered objects
  --cache-directory=C:\Users\Luna/.cache\volatility
                        Directory where cache files are stored
  --cache               Use caching
  --tz=TZ               Sets the (Olson) timezone for displaying timestamps
                        using pytz (if installed) or tzset
  -f FILENAME, --filename=FILENAME
                        Filename to use when opening an image
  --profile=LinuxAndroidARM
                        Name of the profile to load (use --info to see a list
                        of supported profiles)
  -l file:///D:/Android%20Images/Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13/i9100-CM.bin, --location=file:///D:/Android%20Images/Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13/i9100-CM.bin
                        A URN location from which to load an address space
  -w, --write           Enable write support
  --dtb=DTB             DTB Address
  --shift=SHIFT         Mac KASLR shift address
  --output=text         Output in this format (support is module specific, see
                        the Module Output Options below)
  --output-file=OUTPUT_FILE
                        Write output in this file
  -v, --verbose         Verbose information
  --physical_shift=PHYSICAL_SHIFT
                        Linux kernel physical shift address
  --virtual_shift=VIRTUAL_SHIFT
                        Linux kernel virtual shift address
  -g KDBG, --kdbg=KDBG  Specify a KDBG virtual address (Note: for 64-bit
                        Windows 8 and above this is the address of
                        KdCopyDataBlock)
  --force               Force utilization of suspect profile
  --cookie=COOKIE       Specify the address of nt!ObHeaderCookie (valid for
                        Windows 10 only)
  -k KPCR, --kpcr=KPCR  Specify a specific KPCR address

        Supported Plugin Commands:

                imagecopy       Copies a physical address space out as a raw DD image
                limeinfo        Dump Lime file format information
                linux_apihooks  Checks for userland apihooks
                linux_arp       Print the ARP table
                linux_aslr_shift        Automatically detect the Linux ASLR shift
                linux_banner    Prints the Linux banner information
                linux_bash      Recover bash history from bash process memory
                linux_bash_env  Recover a process' dynamic environment variables
                linux_bash_hash Recover bash hash table from bash process memory
                linux_check_afinfo      Verifies the operation function pointers of network protocols
                linux_check_creds       Checks if any processes are sharing credential structures
                linux_check_evt_arm     Checks the Exception Vector Table to look for syscall table hooking
                linux_check_fop Check file operation structures for rootkit modifications
                linux_check_idt Checks if the IDT has been altered
                linux_check_inline_kernel       Check for inline kernel hooks
                linux_check_modules     Compares module list to sysfs info, if available
                linux_check_syscall     Checks if the system call table has been altered
                linux_check_syscall_arm Checks if the system call table has been altered
                linux_check_tty Checks tty devices for hooks
                linux_dentry_cache      Gather files from the dentry cache
                linux_dmesg     Gather dmesg buffer
                linux_dump_map  Writes selected memory mappings to disk
                linux_dynamic_env       Recover a process' dynamic environment variables
                linux_elfs      Find ELF binaries in process mappings
                linux_enumerate_files   Lists files referenced by the filesystem cache
                linux_find_file Lists and recovers files from memory
                linux_getcwd    Lists current working directory of each process
                linux_hidden_modules    Carves memory to find hidden kernel modules
                linux_ifconfig  Gathers active interfaces
                linux_info_regs It's like 'info registers' in GDB. It prints out all the
                linux_iomem     Provides output similar to /proc/iomem
                linux_kernel_opened_files       Lists files that are opened from within the kernel
                linux_keyboard_notifiers        Parses the keyboard notifier call chain
                linux_ldrmodules        Compares the output of proc maps with the list of libraries from libdl
                linux_library_list      Lists libraries loaded into a process
                linux_librarydump       Dumps shared libraries in process memory to disk
                linux_list_raw  List applications with promiscuous sockets
                linux_lsmod     Gather loaded kernel modules
                linux_lsof      Lists file descriptors and their path
                linux_malfind   Looks for suspicious process mappings
                linux_memmap    Dumps the memory map for linux tasks
                linux_moddump   Extract loaded kernel modules
                linux_mount     Gather mounted fs/devices
                linux_mount_cache       Gather mounted fs/devices from kmem_cache
                linux_netfilter Lists Netfilter hooks
                linux_netscan   Carves for network connection structures
                linux_netstat   Lists open sockets
                linux_pidhashtable      Enumerates processes through the PID hash table
                linux_pkt_queues        Writes per-process packet queues out to disk
                linux_plthook   Scan ELF binaries' PLT for hooks to non-NEEDED images
                linux_proc_maps Gathers process memory maps
                linux_proc_maps_rb      Gathers process maps for linux through the mappings red-black tree
                linux_procdump  Dumps a process's executable image to disk
                linux_process_hollow    Checks for signs of process hollowing
                linux_psaux     Gathers processes along with full command line and start time
                linux_psenv     Gathers processes along with their static environment variables
                linux_pslist    Gather active tasks by walking the task_struct->task list
                linux_pslist_cache      Gather tasks from the kmem_cache
                linux_psscan    Scan physical memory for processes
                linux_pstree    Shows the parent/child relationship between processes
                linux_psxview   Find hidden processes with various process listings
                linux_recover_filesystem        Recovers the entire cached file system from memory
                linux_route_cache       Recovers the routing cache from memory
                linux_sk_buff_cache     Recovers packets from the sk_buff kmem_cache
                linux_slabinfo  Mimics /proc/slabinfo on a running machine
                linux_strings   Match physical offsets to virtual addresses (may take a while, VERY verbose)
                linux_threads   Prints threads of processes
                linux_tmpfs     Recovers tmpfs filesystems from memory
                linux_truecrypt_passphrase      Recovers cached Truecrypt passphrases
                linux_vma_cache Gather VMAs from the vm_area_struct cache
                linux_volshell  Shell in the memory image
                linux_yarascan  A shell in the Linux memory image
                mbrparser       Scans for and parses potential Master Boot Records (MBRs)
                patcher         Patches memory based on page scans
                raw2dmp         Converts a physical memory sample to a windbg crash dump
                vmwareinfo      Dump VMware VMSS/VMSN information
```
 Process List

```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_pslist
Volatility Foundation Volatility Framework 2.6.1
Offset     Name                 Pid             PPid            Uid             Gid    DTB        Start Time
---------- -------------------- --------------- --------------- --------------- ------ ---------- ----------
0xe4044000 init                 1               0               0               0      0x62a1c000 2017-03-20 08:56:20 UTC+0000
0xe4044420 kthreadd             2               0               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4044840 ksoftirqd/0          3               2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe40454a0 migration/0          6               2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe40458c0 watchdog/0           7               2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4047180 khelper              12              2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4095080 sync_system_wor      19              2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe40979c0 sync_supers          370             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41f8420 bdi-default          372             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4100000 kblockd              374             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41fb9c0 khubd                389             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe43994a0 irq/359-max8997      425             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41f9080 cfg80211             478             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41f94a0 khungtaskd           580             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41f98c0 kswapd0              581             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41f9ce0 fsnotify_mark        633             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41fa100 ecryptfs-kthrea      652             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41fa520 crypto               656             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4101080 s3c-fb               823             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41014a0 s3c-fb-vsync         829             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41018c0 mali_dvfs            848             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4101ce0 sec_jack_wq          908             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4102100 irq/378-sec_hea      912             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4102520 irq/367-pn544        918             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4102d60 spi_gpio.3           923             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4100c60 f_mtp                952             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4100840 file-storage         957             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4100420 irq/356-mxt224_      971             2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4103180 sii9234_msc_wq       1020            2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41035a0 sii9234_tmds_of      1021            2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe41039c0 irq/397-sii9234      1022            2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4305080 irq/371-max1704      1037            2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe43058c0 kpegasusq            1044            2               0               0      ---------- 2017-03-20 08:56:20 UTC+0000
0xe4306940 irq/380-s3c-sdh      1060            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe43e14a0 binder               1102            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4176100 irq/353-k3g          1120            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe41779c0 mmcqd/0              1126            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4094c60 irq/354-proximi      1143            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4095ce0 cm3663_light_wq      1146            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4096520 cm3663_prox_wq       1147            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe43e2100 krfcommd             1185            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4175080 s5p-tmu              1195            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4174840 mmcqd/1              1197            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4174420 usb_tx_wq            1203            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4176d60 linkpmd              1205            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4304420 irq/389-sec_tou      1234            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4304c60 fimc0_iqr_wq_na      1237            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe43079c0 fimc1_iqr_wq_na      1239            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4307180 fimc2_iqr_wq_na      1241            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe439b9c0 fimc3_iqr_wq_na      1243            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4398840 hdcp work            1245            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe43e0420 tvout resume wo      1259            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe43e2520 sec-battery          1265            2               0               0      ---------- 2017-03-20 08:56:21 UTC+0000
0xe4176940 ueventd              1285            1               0               0      0x62a2c000 2017-03-20 08:56:21 UTC+0000
0xe2abf9c0 jbd2/mmcblk0p9-      1819            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abf180 ext4-dio-unwrit      1820            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abe520 flush-179:0          1823            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abe100 jbd2/mmcblk0p7-      1828            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abd8c0 ext4-dio-unwrit      1829            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abdce0 jbd2/mmcblk0p1-      1833            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abd080 ext4-dio-unwrit      1834            2               0               0      ---------- 2017-03-20 08:56:22 UTC+0000
0xe2abc000 jbd2/mmcblk0p10      1839            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe2abc420 ext4-dio-unwrit      1840            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe2abc840 jbd2/mmcblk0p12      1842            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe2abd4a0 ext4-dio-unwrit      1843            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe2abe940 Si4709_wq            1848            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe43e0840 logd                 1854            1               1036            1036   0x62c3c000 2017-03-20 08:56:23 UTC+0000
0xe43e35a0 healthd              1855            1               0               0      0x62c6c000 2017-03-20 08:56:23 UTC+0000
0xe43e39c0 lmkd                 1856            1               0               0      0x62c68000 2017-03-20 08:56:23 UTC+0000
0xe43e0000 servicemanager       1858            1               1000            1000   0x62c78000 2017-03-20 08:56:23 UTC+0000
0xe43e2d60 vold                 1859            1               0               0      0x62c74000 2017-03-20 08:56:23 UTC+0000
0xe43e0c60 surfaceflinger       1860            1               1000            1003   0x62c7c000 2017-03-20 08:56:23 UTC+0000
0xe43e1080 auditd               1861            1               1049            1049   0x62c9c000 2017-03-20 08:56:23 UTC+0000
0xe43e2940 netd                 1862            1               0               0      0x62cd8000 2017-03-20 08:56:23 UTC+0000
0xe43e1ce0 debuggerd            1863            1               0               0      0x62ca0000 2017-03-20 08:56:23 UTC+0000
0xe43e3180 rild                 1864            1               1001            1001   0x62cf0000 2017-03-20 08:56:23 UTC+0000
0xe40479c0 drmserver            1865            1               1019            1019   0x62cc4000 2017-03-20 08:56:23 UTC+0000
0xe4096100 mediaserver          1866            1               1013            1005   0x62c98000 2017-03-20 08:56:23 UTC+0000
0xe4096940 installd             1867            1               1012            1012   0x62c84000 2017-03-20 08:56:23 UTC+0000
0xe4094840 keystore             1868            1               1017            1017   0x62c80000 2017-03-20 08:56:23 UTC+0000
0xe4094420 cbd                  1869            1               1001            1001   0x62d18000 2017-03-20 08:56:23 UTC+0000
0xe4097180 main                 1871            1               0               0      0x62d38000 2017-03-20 08:56:23 UTC+0000
0xe4096d60 kauditd              1873            2               0               0      ---------- 2017-03-20 08:56:23 UTC+0000
0xe181a520 system_server        2253            1871            1000            1000   0x62e2c000 2017-03-20 08:57:33 UTC+0000
0xe11514a0 ndroid.systemui      3024            1871            -               10015  0x623f0000 2017-03-20 09:02:51 UTC+0000
0xe15cc000 sdcard               3218            1               1023            1023   0x4d2bc000 2017-03-20 09:02:52 UTC+0000
0xe25e5ce0 putmethod.latin      3261            1871            -               10044  0x61c6c000 2017-03-20 09:02:52 UTC+0000
0xe1f3b5a0 ogenmod.audiofx      3366            1871            10000           10000  0x4d32c000 2017-03-20 09:02:54 UTC+0000
0xcd374420 ndroid.incallui      3374            1871            -               10007  0x4d37c000 2017-03-20 09:02:54 UTC+0000
0xe1715ce0 m.android.phone      3398            1871            1001            1001   0x61e38000 2017-03-20 09:02:54 UTC+0000
0xe1335ce0 sdcard               3413            1               1023            1023   0x613ac000 2017-03-20 09:02:54 UTC+0000
0xe1a318c0 mod.setupwizard      3468            1871            1000            1000   0x613f8000 2017-03-20 09:02:54 UTC+0000
0xce4dc840 e.process.gapps      3623            1871            -               10020  0x4f4c0000 2017-03-20 09:02:58 UTC+0000
0xce4dd080 android.vending      3649            1871            -               10024  0x4f4fc000 2017-03-20 09:02:59 UTC+0000
0xe15194a0 .gms.persistent      3722            1871            -               10020  0x4f744000 2017-03-20 09:03:03 UTC+0000
0xd10a1ce0 android.smspush      3768            1871            -               10060  0x5108c000 2017-03-20 09:03:04 UTC+0000
0xcf7a3180 com.svox.pico        3810            1871            -               10054  0x61718000 2017-03-20 09:03:05 UTC+0000
0xe14e2100 enmod.trebuchet      3907            1871            -               10017  0x61898000 2017-03-20 09:03:08 UTC+0000
0xe1f38420 viders.calendar      4185            1871            -               10003  0x61f3c000 2017-03-20 09:03:14 UTC+0000
0xe128ad60 m.android.email      4376            1871            -               10038  0x4f720000 2017-03-20 09:03:17 UTC+0000
0xce4dc420 themes.provider      4415            1871            -               10016  0x5cd68000 2017-03-20 09:03:17 UTC+0000
0xcf646100 droid.gallery3d      4435            1871            -               10041  0x5d8b4000 2017-03-20 09:03:17 UTC+0000
0xdd9094a0 enmod.lockclock      4458            1871            -               10047  0x61aa4000 2017-03-20 09:03:18 UTC+0000
0xdf4af5a0 oadcastreceiver      4495            1871            -               10004  0x4e234000 2017-03-20 09:03:18 UTC+0000
0xdf62f180 d.process.acore      4510            1871            -               10005  0x5c040000 2017-03-20 09:03:18 UTC+0000
0xdd90a520 droid.deskclock      4536            1871            -               10035  0x5cec0000 2017-03-20 09:03:19 UTC+0000
0xe1bcd080 d.process.media      4867            1871            -               10008  0x62fc8000 2017-03-20 09:03:58 UTC+0000
0xe1a775a0 nogenmod.eleven      4973            1871            -               10037  0x55ce4000 2017-03-20 09:04:33 UTC+0000
0xdeebe520 kworker/0:0          5302            2               0               0      ---------- 2017-03-20 09:20:36 UTC+0000
0xe113f180 kworker/u:4          5341            2               0               0      ---------- 2017-03-20 09:30:09 UTC+0000
0xe1bccc60 kworker/u:5          5342            2               0               0      ---------- 2017-03-20 09:30:09 UTC+0000
0xe179ed60 kworker/u:14         5351            2               0               0      ---------- 2017-03-20 09:30:09 UTC+0000
0xe4304000 kworker/0:3          5365            2               0               0      ---------- 2017-03-20 09:31:49 UTC+0000
0xde180c60 kworker/0:4          5366            2               0               0      ---------- 2017-03-20 09:31:49 UTC+0000
0xde1814a0 flush-179:8          5369            2               0               0      ---------- 2017-03-20 09:31:50 UTC+0000
0xde182520 gle.android.gms      5375            1871            -               10020  0x4f7bc000 2017-03-20 09:39:52 UTC+0000
0xe1380840 ackageinstaller      5638            1871            -               10050  0x62c10000 2017-03-20 09:46:38 UTC+0000
0xe1f394a0 id.defcontainer      5670            1871            -               10006  0x4ad38000 2017-03-20 09:46:41 UTC+0000
0xce3014a0 id.partnersetup      5701            1871            -               10023  0x4ad94000 2017-03-20 09:46:49 UTC+0000
0xc36dd080 ndroid.settings      5777            1871            1000            1000   0x4d1c8000 2017-03-20 09:47:10 UTC+0000
0xe1a118c0 genmod.profiles      5871            1871            -               10056  0x5c930000 2017-03-20 09:48:19 UTC+0000
0xe1bcc420 .scrt.secr3tmgr      5912            1871            -               10063  0x476e4000 2017-03-20 09:48:33 UTC+0000
0xe17b6520 adbd                 5969            1               0               0      0x61afc000 2017-03-20 09:49:49 UTC+0000
0xe17154a0 logcat               5980            5969            0               0      0x4ee24000 2017-03-20 09:49:51 UTC+0000
0xc36de520 sh                   5997            5969            0               0      0x42808000 2017-03-20 09:49:58 UTC+0000
0xc36df5a0 insmod               6003            5997            0               0      0x42820000 2017-03-20 09:50:12 UTC+0000
0xda2e2d60 migration/1          6013            2               -               -      ---------- 2017-03-20 09:50:35 UTC+0000
0xda2e2520 kworker/1:0          6014            2               -               -      ---------- 2017-03-20 09:50:35 UTC+0000
0xe113c840 migration/1          6020            2               -               -      ---------- 2017-03-20 09:50:38 UTC+0000
0xe113e520 kworker/1:0          6021            2               -               -      ---------- 2017-03-20 09:50:38 UTC+0000
0xdba22520 watchdog/1           6115            2               -               -      ---------- 2017-03-20 09:51:22 UTC+0000
0xdba21ce0 watchdog/1           6129            2               1036            1036   ---------- 2017-03-20 09:51:28 UTC+0000
0xde180840 workqueue_trust      6145            2               -               -      ---------- 2017-03-20 09:51:35 UTC+0000
```
Ifconfig
```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_ifconfig
Volatility Foundation Volatility Framework 2.6.1
Interface        IP Address           MAC Address        Promiscous Mode
---------------- -------------------- ------------------ ---------------
lo               127.0.0.1            00:00:00:00:00:00  False
```

Route cache
```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_route_cache
Volatility Foundation Volatility Framework 2.6.1
Interface        Destination          Gateway
---------------- -------------------- -------
lo               127.0.0.1            127.0.0.1
lo               127.0.0.1            127.0.0.1
```
Process Map
```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_proc_maps
[Huge Data]

vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_proc_maps -p PID
```
Process Env
I used 5912 pid ( target application pid )
```
vol.py -f "D:\Android Images\Secr3tMgr_680932f10ed4bb347dec46bdd8a34de487df1d13\i9100-CM.bin" --profile=LinuxAndroidARM linux_psenv -p 5912
Volatility Foundation Volatility Framework 2.6.1
Name   Pid    Environment
.scrt.secr3tmgr   5912   PATH=/sbin:/vendor/bin:/system/sbin:/system/bin:/system/xbin ANDROID_BOOTLOGO=1 ANDROID_ROOT=/system ANDROID_ASSETS=/system/app ANDROID_DATA=/data ANDROID_STORAGE=/storage ASEC_MOUNTPOINT=/mnt/asec LOOP_MOUNTPOINT=/mnt/obb BOOTCLASSPATH=/system/framework/core-libart.jar:/system/framework/conscrypt.jar:/system/framework/okhttp.jar:/system/framework/core-junit.jar:/system/framework/bouncycastle.jar:/system/framework/ext.jar:/system/framework/framework.jar:/system/framework/telephony-common.jar:/system/framework/voip-common.jar:/system/framework/ims-common.jar:/system/framework/mms-common.jar:/system/framework/android.policy.jar:/system/framework/apache-xml.jar SYSTEMSERVERCLASSPATH=/system/framework/org.cyanogenmod.platform.jar:/system/framework/org.cyanogenmod.hardware.jar:/system/framework/services.jar:/system/framework/ethernet-service.jar:/system/framework/wifi-service.jar LD_PRELOAD=libsigchain.so EXTERNAL_STORAGE=/storage/sdcard0 SECONDARY_STORAGE=/storage/sdcard1 ANDROID_CACHE=/cache TERMINFO=/system/etc/terminfo ANDROID_PROPERTY_WORKSPACE=9,0 ANDROID_SOCKET_zygote=10
```
**Dumping File System**
I can't dump file system with my Windows.It occurs "Object has no attribute :chown" error. Then i switch to SIFT VM.

Profile built again
```
cp Android.zip /usr/lib/python2.7/dist-packages/volatility/plugins/overlays/linux/
```
I crated the FS directory and dumped filesystem 
```
root@siftworkstation -> /cases
# sudo vol.py -f i9100-CM.bin --profile=LinuxAndroidARM linux_recover_filesystem --dump-dir=FS
Volatility Foundation Volatility Framework 2.6
Recovered 9438 files
```
**Exploring System Files**
What is inside?
```
root@siftworkstation -> /cases
# ls -l FS
total 44
drwxr-xr-x  43 root          root          4096 Jun  7 21:48 acct
drwxrwx---   4 sansforensics          2001 4096 Jun  7 21:45 cache
drwxrwx--x  13 sansforensics sansforensics 4096 Jun  7 21:45 data
drwxr-xr-x  13 root          root          4096 Jun  7 21:45 dev
drwxrwx--x   6          1001 sansforensics 4096 Jun  7 21:48 efs
drwxr-xr-x   6 root          root          4096 Jun  7 21:48 mnt
drwxrwxrwx   2 sansforensics sansforensics 4096 Sep 29  2012 preload
dr-xr-xr-x 129 root          root          4096 Jun  7 21:48 proc
drwxr-xr-x   4 root          root          4096 Jun  7 21:50 storage
drwxr-xr-x  10 root          root          4096 Jun  7 21:27 sys
drwxr-xr-x  17 root          root          4096 Jun  7 21:36 system
```
Pattern Lock
```
sansforensics@siftworkstation -> /c/FS
$ ls -l data/systemls -l data/system/gesture.key
-rw------- 1 sansforensics sansforensics 20 Mar 20  2017 data/system/gesture.key
```
understand gesture.key
 - SHA1 data as hex
```
sansforensics@siftworkstation -> /c/FS
$ xxd -p data/system/gesture.key
da39a3ee5e6b4b0d3255bfef95601890afd80709
```
Cracking Pattern Lock ( failed in this example )
```
sansforensics@siftworkstation -> /c/FS
$ androidpatternlock/aplc.py data/system/gesture.key

################################
# Android Pattern Lock Cracker #
#             v0.2             #
# ---------------------------- #
#  Written by Chema Garcia     #
#     http://safetybits.net    #
#     chema@safetybits.net     #
#          @sch3m4             #
################################

[i] Taken from: http://forensics.spreitzenbarth.de/2012/02/28/cracking-the-pattern-lock-on-android/

[:(] The pattern was not found...
```
Password Cracking
 - password file in FS
```
sansforensics@siftworkstation -> /c/FS
$ ls -l data/system/password.key
-rw------- 1 sansforensics sansforensics 72 Mar 20  2017 data/system/password.key
```
 - concatenating key file
```
$ cat data/system/password.key
A66A4A34A78AEC1A7058C8FA3BB3B0F1CC537DD042F0F3F909F87D0706DCF139AB37F86E
```
 - salt for hash
```
sansforensics@siftworkstation -> /c/FS
$ file data/system/locksettings.db
data/system/locksettings.db: SQLite 3.x database
```
 - exploring sqlite3 db

```
sansforensics@siftworkstation -> /c/FS
$ sqlite3 data/system/locksettings.db
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .tables
android_metadata  locksettings
sqlite> select * from locksettings;                                                                                     ####################........................]
1|lockscreen.disabled|0|0
2|migrated|0|true
3|migrated_user_specific|0|true
4|lockscreen.enabledtrustagents|0|org.cyanogenmod.profiles/.ProfilesTrustAgent,com.google.android.gms/.auth.trustagent.GoogleTrustAgent
5|lockscreen.password_salt|0|-6140990771726895285
6|lock_pattern_autolock|0|0
8|lockscreen.password_type_alternate|0|0
9|lockscreen.password_type|0|327680
10|lockscreen.passwordhistory|0|
```
 - Device Policy
```
sansforensics@siftworkstation -> /c/FS
$ cat data/system/device_policies.xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<policies setup-complete="true">
<active-password quality="327680" length="10" uppercase="5" lowercase="2" letters="7" numeric="1" symbols="2" nonletter="3" />
</policies>
```
- *password.key ( 72 Characters ) = SHA1+salt (40) + MD5+salt (32)*

```
A66A4A34A78AEC1A7058C8FA3BB3B0F1CC537DD0 -> SHA1
42F0F3F909F87D0706DCF139AB37F86E -> MD5
```
- salt and hash concatenating
```
sansforensics@siftworkstation -> /c/FS
$ printf "%x\n" -6140990771726895285
aac6d16df244374b

echo "42f0f3f909f87d0706dcf139ab37f86e:aac6d16df244374b" > hash

```
 - Here is [Hashcat Cheatsheet](https://github.com/frizb/Hashcat-Cheatsheet) 
```
hashcat64.exe -m 10 -a 3 ..\..\hash -1 ?l?u?d INS{?1?1?1?1?1} -d 3
```
But my pc can't crack :(

Thanks   
-> http://arishitz.net/writeup-secr3tmgr-forensic-insomnihack-2017/
