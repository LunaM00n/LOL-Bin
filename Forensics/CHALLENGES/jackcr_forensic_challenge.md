## Jackr's Forensic Challenge - Memory Analysis

**Questions**

    What is the C2:
    
    What tools were placed on the machine:
    
    What type of backdoor:
    
    What was stolen:
    
    What was the name of the file that held the stolen data:
    
    What process id was the backdoor running in:
    
    What was the name of the dropper:
    
    What is the name of the backdoor:

သူ့ေမးခြန္းေတြက ကုိယ္ေတြအတြက္ Outline ေပးထားတဲ့သေဘာပဲျဖစ္ပါတယ္။ what is the C2 ဆိုေတာ့ C&C Server တစ္ခုရွိတယ္ဆိုတဲ့သေဘာပါပဲ။ ဒါကိုက်ေနာ္တို့က memory ကို Analysis လုပ္ျပီးရွာရမယ့္သေဘာေပါ့။

Challenge file ျဖစ္တဲ့ memdump.bin file ကို Image ဟာ ဘာ Profile လဲဆိုတာသိရေအာင္ အရင္ဆံုးလုပ္ရမယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/luna/Downloads/volatility_2.6_lin64_standalone/mem/memdump.bin)
                      PAE type : PAE
                           DTB : 0x311000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2012-11-17 18:49:50 UTC+0000
     Image local date and time : 2012-11-17 13:49:50 -0500
```
WinXPSP2x86 ကိုေတာ့ suggest လုပ္ထားတာေတြ့ရမယ္၊ ဒီေတာ့ C2 Server ကိုသိရဖို့အတြက္ Connection ေတြကိုသိဖို့လိုတယ္မဟုတ္လား။ ဒါေျကာင့္ volatility ကိုသံုးျပီး connection ေတြကိုျကည့္ရမယ္။

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin connscan
Volatility Foundation Volatility Framework 2.6
Offset(P)  Local Address             Remote Address            Pid
---------- ------------------------- ------------------------- ---
0x021eb3c0 192.168.56.103:1084       192.168.56.10:389         320
0x021ecaa8 192.168.56.103:1076       58.64.132.141:80          1072
0x0224e8e8 192.168.56.103:1081       192.168.56.10:445         1184
0x023a12f8 192.168.56.103:1079       58.64.132.141:80          1072
```
192 က local network ျဖစ္တာေျကာင့္ 58.64.132.141 က C2 Server ကိုသြားထားတဲ့ Connection လို့ယူဆရမယ္

ေနာက္ထပ္ေမးခြန္းတစ္ခုကေတာ့ ဘယ္ Tool ကို machine ေပာ္ထားခဲ့လဲဆိုတာျဖစ္တယ္ ။ ဒီေတာ့ C2 server ကို connect လုပ္တားတဲ့ ဟာမွာ process id ပါတယ္။ သေဘာကေတာ့ အဲ့ဒီ process က C2 Server ကိုခ်ိတ္ေအာင္လုပ္တဲ့အတြက္ အဲ့ဒီ process id ကို spawn လုပ္ထားတဲ့ service or software ကို သံသယဝင္ထားလို့ရတာေပါ့ ။ ဒါေျကာင့္ process list ကိုတစ္ခ်က္ျကည့္ျကည့္မယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x823c89c8 System                    4      0     54      254 ------      0                                                              
0x8219d020 smss.exe                368      4      3       19 ------      0 2012-11-17 18:30:27 UTC+0000                                 
0x8228e020 csrss.exe               616    368     12      364      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x822acc78 winlogon.exe            640    368     20      611      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x82065020 services.exe            684    640     16      249      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x821a4020 lsass.exe               696    640     24      395      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x8215d230 VBoxService.exe         856    684      8      106      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x8206c020 svchost.exe             900    684     18      167      0      0 2012-11-17 18:30:28 UTC+0000                                 
0x8216f558 svchost.exe             988    684      9      222      0      0 2012-11-17 18:30:29 UTC+0000                                 
0x8217d7e8 svchost.exe            1072    684     76     1406      0      0 2012-11-17 18:30:29 UTC+0000                                 
0x8203eda0 svchost.exe            1124    684      6       75      0      0 2012-11-17 18:30:29 UTC+0000                                 
0x822cf020 svchost.exe            1184    684     14      245      0      0 2012-11-17 18:30:29 UTC+0000                                 
0x820298b0 spoolsv.exe            1380    684     10      104      0      0 2012-11-17 18:30:29 UTC+0000                                 
0x821a8a78 alg.exe                1924    684      5      103      0      0 2012-11-17 18:30:37 UTC+0000                                 
0x822dba20 explorer.exe            320    248     15      474      0      0 2012-11-17 18:30:47 UTC+0000                                 
0x821d6da0 VBoxTray.exe           1024    320      7       57      0      0 2012-11-17 18:30:48 UTC+0000                                 
0x821d13c0 wuauclt.exe            1880   1072      3      133      0      0 2012-11-17 18:31:39 UTC+0000                                 
0x8202c538 cmd.exe                1324   1072      0 --------      0      0 2012-11-17 18:33:30 UTC+0000   2012-11-17 18:47:24 UTC+0000  
0x82155da0 PsExec.exe             1772   1324      1       44      0      0 2012-11-17 18:45:40 UTC+0000                                 
0x822d07e8 cmd.exe                1212    320      1       33      0      0 2012-11-17 18:49:01 UTC+0000                                 
0x82028ad8 mdd.exe                1584   1212      1       24      0      0 2012-11-17 18:49:50 UTC+0000                                 
```
Result ကိုျကည့္ျခင္းအားျဖင့္ 1072 ဆိုတဲ့ Process id က svchost.exe ဆိုတာေတြ့ရမယ္။ ေနာက္တစ္ခုက ppid = parent process id အျဖစ္ေရာက္ေနတဲ့ wuaclt.exe ရယ္ ကိုလဲေတြ့ရမယ္။ ဒီလိုဆို အဲ့ဒီ process ေတြကိုပါထပ္ဖြင့္ထားတဲ့သေဘာလို့ သတ္မွတ္ထားလိုက္မယ္

svchost က launcer တစ္ခုျဖစ္ျပီးေတာ့ service ေတြ dll ေတြကို run ဖို့အသံုးျပုတာျဖစ္ေတာ့ သူေျကာင့္လို့ေတာ့ေျပာလို့မရပါဘူး။ ဒါေျကာင့္ 1072 က ဘယ္ dll ေတြကို run သလဲဆိုတာကိုသိေအာင္လုပ္ရပါမယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin dlllist -p 1072
Volatility Foundation Volatility Framework 2.6
************************************************************************
svchost.exe pid:   1072
Command line : C:\WINDOWS\System32\svchost.exe -k netsvcs
Service Pack 3

Base             Size  LoadCount Path
---------- ---------- ---------- ----
0x01000000     0x6000     0xffff C:\WINDOWS\System32\svchost.exe
0x7c900000    0xaf000     0xffff C:\WINDOWS\system32\ntdll.dll
0x7c800000    0xf6000     0xffff C:\WINDOWS\system32\kernel32.dll
0x77dd0000    0x9b000     0xffff C:\WINDOWS\system32\ADVAPI32.dll
0x77e70000    0x92000     0xffff C:\WINDOWS\system32\RPCRT4.dll
0x77fe0000    0x11000     0xffff C:\WINDOWS\system32\Secur32.dll
0x5cb70000    0x26000        0x1 C:\WINDOWS\System32\ShimEng.dll
0x6f880000   0x1ca000        0x1 C:\WINDOWS\AppPatch\AcGenral.DLL
0x7e410000    0x91000      0x3e3 C:\WINDOWS\system32\USER32.dll
0x77f10000    0x49000      0x228 C:\WINDOWS\system32\GDI32.dll
0x76b40000    0x2d000       0x20 C:\WINDOWS\System32\WINMM.dll
0x774e0000   0x13d000       0xe5 C:\WINDOWS\system32\ole32.dll
0x77c10000    0x58000      0x415 C:\WINDOWS\system32\msvcrt.dll
0x77120000    0x8b000       0x94 C:\WINDOWS\system32\OLEAUT32.dll
0x77be0000    0x15000        0x1 C:\WINDOWS\System32\MSACM32.dll
0x77c00000     0x8000       0x20 C:\WINDOWS\system32\VERSION.dll
0x7c9c0000   0x817000       0x13 C:\WINDOWS\system32\SHELL32.dll
0x77f60000    0x76000       0x6b C:\WINDOWS\system32\SHLWAPI.dll
0x769c0000    0xb4000       0x17 C:\WINDOWS\system32\USERENV.dll
0x5ad70000    0x38000        0x4 C:\WINDOWS\System32\UxTheme.dll
0x76390000    0x1d000        0x3 C:\WINDOWS\system32\IMM32.DLL
0x773d0000   0x103000        0x9 C:\WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll
0x5d090000    0x9a000        0x9 C:\WINDOWS\system32\comctl32.dll
0x77690000    0x21000        0x1 C:\WINDOWS\System32\NTMARTA.DLL
0x71bf0000    0x13000       0x15 C:\WINDOWS\System32\SAMLIB.dll
0x76f60000    0x2c000       0x23 C:\WINDOWS\system32\WLDAP32.dll
0x00630000   0x2c5000        0x2 C:\WINDOWS\System32\xpsp2res.dll
0x776e0000    0x23000        0x3 c:\windows\system32\shsvcs.dll
0x76360000    0x10000       0x19 C:\WINDOWS\System32\WINSTA.dll
0x5b860000    0x55000       0x8d C:\WINDOWS\System32\NETAPI32.dll
0x7d4b0000    0x22000        0x5 c:\windows\system32\dhcpcsvc.dll
0x76f20000    0x27000       0x15 c:\windows\system32\DNSAPI.dll
0x71ab0000    0x17000       0x88 c:\windows\system32\WS2_32.dll
0x71aa0000     0x8000       0x53 c:\windows\system32\WS2HELP.dll
0x76d60000    0x19000       0x15 c:\windows\system32\iphlpapi.dll
0x68000000    0x36000        0x1 C:\WINDOWS\System32\rsaenh.dll
0x7db10000    0x8c000        0x2 c:\windows\system32\wzcsvc.dll
0x76e80000     0xe000       0x5e c:\windows\system32\rtutils.dll
0x76d30000     0x4000        0x4 c:\windows\system32\WMI.dll
0x77a80000    0x95000       0x34 c:\windows\system32\CRYPT32.dll
0x77b20000    0x12000       0x2c c:\windows\system32\MSASN1.dll
0x72810000     0xb000        0x3 c:\windows\system32\EapolQec.dll
0x76b20000    0x11000       0x29 c:\windows\system32\ATL.DLL
0x726c0000    0x16000        0x5 c:\windows\system32\QUtil.dll
0x76080000    0x65000       0x23 c:\windows\system32\MSVCP60.dll
0x478c0000     0xa000        0xc c:\windows\system32\dot3api.dll
0x76f50000     0x8000       0x15 c:\windows\system32\WTSAPI32.dll
0x606b0000   0x10d000        0x4 c:\windows\system32\ESENT.dll
0x76fd0000    0x7f000        0x5 C:\WINDOWS\System32\CLBCATQ.DLL
0x77050000    0xc5000       0x11 C:\WINDOWS\System32\COMRes.dll
0x76b70000    0x27000        0x7 C:\WINDOWS\System32\rastls.dll
0x754d0000    0x80000        0x8 C:\WINDOWS\System32\CRYPTUI.dll
0x63000000    0xe6000        0xa C:\WINDOWS\system32\WININET.dll
0x01490000     0x9000        0xa C:\WINDOWS\system32\Normaliz.dll
0x1a400000   0x132000        0xa C:\WINDOWS\system32\urlmon.dll
0x5dca0000   0x1e8000       0x14 C:\WINDOWS\system32\iertutil.dll
0x76c30000    0x2e000        0xc C:\WINDOWS\System32\WINTRUST.dll
0x76c90000    0x28000        0xc C:\WINDOWS\system32\IMAGEHLP.dll
0x76d40000    0x18000        0xd C:\WINDOWS\System32\MPRAPI.dll
0x77cc0000    0x32000        0xe C:\WINDOWS\System32\ACTIVEDS.dll
0x76e10000    0x25000        0xf C:\WINDOWS\System32\adsldpc.dll
0x77920000    0xf3000       0x1a C:\WINDOWS\System32\SETUPAPI.dll
0x76ee0000    0x3c000       0x16 C:\WINDOWS\System32\RASAPI32.dll
0x76e90000    0x12000       0x1d C:\WINDOWS\System32\rasman.dll
0x76eb0000    0x2f000       0x1a C:\WINDOWS\System32\TAPI32.dll
0x767f0000    0x27000        0x7 C:\WINDOWS\System32\SCHANNEL.dll
0x723d0000    0x1c000        0x7 C:\WINDOWS\System32\WinSCard.dll
0x76bf0000     0xb000        0xf C:\WINDOWS\System32\PSAPI.DLL
0x76bd0000    0x16000        0x6 C:\WINDOWS\System32\raschap.dll
0x77c70000    0x24000        0x1 C:\WINDOWS\system32\msv1_0.dll
0x77300000    0x33000        0x1 c:\windows\system32\schedsvc.dll
0x767a0000    0x13000        0x8 c:\windows\system32\NTDSAPI.dll
0x74f50000     0x5000        0x1 C:\WINDOWS\System32\MSIDLE.DLL
0x708b0000     0xd000        0x1 c:\windows\system32\audiosrv.dll
0x76e40000    0x23000        0x1 c:\windows\system32\wkssvc.dll
0x76ce0000    0x12000        0x1 c:\windows\system32\cryptsvc.dll
0x77b90000    0x32000        0x1 c:\windows\system32\certcli.dll
0x74f90000     0x9000        0x1 c:\windows\system32\dmserver.dll
0x74f80000     0x9000        0x1 c:\windows\system32\ersvc.dll
0x77710000    0x42000        0x3 c:\windows\system32\es.dll
0x74f40000     0xc000        0x1 c:\windows\pchealth\helpctr\binaries\pchsvc.dll
0x75090000    0x1a000        0x1 c:\windows\system32\srvsvc.dll
0x77d00000    0x33000        0x1 c:\windows\system32\netman.dll
0x76400000   0x1a5000        0x5 c:\windows\system32\netshell.dll
0x76c00000    0x2e000        0x5 c:\windows\system32\credui.dll
0x736d0000     0x6000        0x5 c:\windows\system32\dot3dlg.dll
0x01d80000    0x28000        0x5 c:\windows\system32\OneX.DLL
0x745b0000    0x22000        0x5 c:\windows\system32\eappcfg.dll
0x015d0000     0xe000        0x5 c:\windows\system32\eappprxy.dll
0x73030000    0x10000        0x1 c:\windows\system32\WZCSAPI.DLL
0x73d20000     0x8000        0x1 c:\windows\system32\seclogon.dll
0x722d0000     0xd000        0x4 c:\windows\system32\sens.dll
0x662b0000    0x58000        0x6 C:\WINDOWS\System32\HNETCFG.DLL
0x751a0000    0x2e000        0x1 c:\windows\system32\srsvc.dll
0x74ad0000     0x8000        0x1 c:\windows\system32\POWRPROF.dll
0x75070000    0x19000        0x1 c:\windows\system32\trkwks.dll
0x767c0000    0x2c000        0x3 c:\windows\system32\w32time.dll
0x59490000    0x28000        0x1 c:\windows\system32\wbem\wmisvc.dll
0x753e0000    0x6d000        0x1 C:\WINDOWS\system32\VSSAPI.DLL
0x50000000     0x5000        0x1 c:\windows\system32\wuauserv.dll
0x50040000   0x119000        0x1 C:\WINDOWS\system32\wuaueng.dll
0x65000000    0x2e000        0x1 C:\WINDOWS\System32\ADVPACK.dll
0x75150000    0x13000        0x1 C:\WINDOWS\System32\Cabinet.dll
0x600a0000     0xb000        0x1 C:\WINDOWS\System32\mspatcha.dll
0x76bb0000     0x5000        0x1 C:\WINDOWS\System32\sfc.dll
0x76c60000    0x2a000        0x2 C:\WINDOWS\System32\sfc_os.dll
0x76780000     0x9000        0x1 C:\WINDOWS\System32\SHFOLDER.dll
0x4d4f0000    0x59000        0x2 C:\WINDOWS\System32\WINHTTP.dll
0x73000000    0x26000        0x1 C:\WINDOWS\System32\WINSPOOL.DRV
0x71a50000    0x3f000        0x8 C:\WINDOWS\system32\mswsock.dll
0x71a90000     0x8000        0x1 C:\WINDOWS\System32\wshtcpip.dll
0x4c0a0000    0x17000        0x1 c:\windows\system32\wscsvc.dll
0x7d1e0000   0x2bc000        0x1 c:\windows\system32\msi.dll
0x76fb0000     0x8000        0x1 C:\WINDOWS\System32\winrnr.dll
0x76da0000    0x16000        0x1 c:\windows\system32\browser.dll
0x7e720000    0xb0000        0x1 C:\WINDOWS\System32\SXS.DLL
0x76620000   0x13c000        0x3 C:\WINDOWS\system32\comsvcs.dll
0x75130000    0x14000        0x3 C:\WINDOWS\system32\colbact.DLL
0x750f0000    0x13000        0x3 C:\WINDOWS\system32\MTXCLU.DLL
0x71ad0000     0x9000        0x3 C:\WINDOWS\system32\WSOCK32.dll
0x76d10000    0x12000        0x5 C:\WINDOWS\System32\CLUSAPI.DLL
0x750b0000    0x12000        0x1 C:\WINDOWS\System32\RESUTILS.DLL
0x750d0000    0x19000        0x1 C:\WINDOWS\System32\mtxoci.dll
0x66460000    0x55000        0x1 c:\windows\system32\ipnathlp.dll
0x776c0000    0x12000        0x2 c:\windows\system32\AUTHZ.dll
0x76fc0000     0x6000        0x1 C:\WINDOWS\System32\rasadhlp.dll
0x75290000    0x37000        0xf C:\WINDOWS\System32\wbem\wbemcomn.dll
0x762c0000    0x85000        0x1 C:\WINDOWS\System32\Wbem\wbemcore.dll
0x75310000    0x3f000        0x4 C:\WINDOWS\System32\Wbem\esscli.dll
0x75690000    0x76000        0x8 C:\WINDOWS\System32\Wbem\FastProx.dll
0x75020000    0x1b000        0x1 C:\WINDOWS\System32\wbem\wmiutils.dll
0x75200000    0x2f000        0x1 C:\WINDOWS\System32\wbem\repdrvfs.dll
0x597f0000    0x6d000        0x1 C:\WINDOWS\System32\wbem\wmiprvsd.dll
0x5f770000     0xc000        0x2 C:\WINDOWS\system32\NCObjAPI.DLL
0x75390000    0x46000        0x1 C:\WINDOWS\System32\wbem\wbemess.dll
0x755f0000    0x9a000        0x3 C:\WINDOWS\System32\netcfgx.dll
0x76de0000    0x24000        0x1 C:\WINDOWS\System32\upnp.dll
0x74f00000     0xc000        0x1 C:\WINDOWS\System32\SSDPAPI.dll
0x768d0000    0xa4000        0x1 C:\WINDOWS\System32\RASDLG.dll
0x77b40000    0x22000        0x1 C:\WINDOWS\system32\Apphelp.dll
0x50640000     0xc000        0x1 C:\WINDOWS\system32\wups.dll
0x5f740000     0xe000        0x1 C:\WINDOWS\System32\wbem\ncprov.dll
0x733e0000    0x40000        0x1 c:\windows\system32\tapisrv.dll
0x7df30000    0x32000        0x3 c:\windows\system32\rasmans.dll
0x74370000     0xb000        0x3 c:\windows\system32\WINIPSEC.DLL
0x75880000    0x11000        0x2 C:\WINDOWS\System32\rastapi.dll
0x57cc0000    0x36000        0x1 C:\WINDOWS\System32\unimdm.tsp
0x72000000     0x7000        0x1 C:\WINDOWS\System32\uniplat.dll
0x57d40000     0xb000        0x1 C:\WINDOWS\System32\kmddsp.tsp
0x57d20000    0x10000        0x1 C:\WINDOWS\System32\ndptsp.tsp
0x57d50000     0x8000        0x1 C:\WINDOWS\System32\ipconf.tsp
0x57d70000    0x46000        0x1 C:\WINDOWS\System32\h323.tsp
0x57d60000     0xa000        0x1 C:\WINDOWS\System32\hidphone.tsp
0x688f0000     0x9000        0x1 C:\WINDOWS\System32\HID.DLL
0x72240000    0x37000        0x2 C:\WINDOWS\System32\rasppp.dll
0x724b0000     0x6000        0x2 C:\WINDOWS\System32\ntlsapi.dll
0x71cf0000    0x4c000        0x1 C:\WINDOWS\system32\kerberos.dll
0x76790000     0xc000        0x1 C:\WINDOWS\System32\cryptdll.dll
0x72ae0000    0x13000        0x2 C:\WINDOWS\System32\RASQEC.DLL
0x10000000    0x1c000        0x1 c:\windows\system32\6to4ex.dll
0x73b80000    0x12000        0x1 c:\windows\system32\AVICAP32.dll
0x75a70000    0x21000        0x2 c:\windows\system32\MSVFW32.dll
0x73d30000    0x17000        0x1 C:\WINDOWS\System32\wbem\wbemcons.dll
```

ဒီေနရာမွာ တိုင္နည္းနည္းပတ္တာပဲ။ dl့l file ေတြထဲမွာ သံသယရွိဖို့ဆိုတာက ဒီလိုမ်ိုးေတြကိုလုပ္ေနက်လူမွသာ အေတြ့အျကံုအရ ခန့္မွန္းခ်က္ေပးလို့ရမယ္၊ က်ေနာ့္အေနနဲ့ေတာ့ အျကံတစ္ခုခုထုတ္မွရမယ္

Popular DLL ေတြကိုဖယ္ထားလိုက္ရင္ေတာ့ နည္းနည္းအဆင္ေျပမယ္လို့ထင္ပါတယ္
https://fileextensiondll.net/populardlls.html
https://www.win7dll.info/
http://www.dlldownloader.com/top-dll-files/

ဒီနည္းနဲ့မွမဟုတ္ရင္ေတာ့ တစ္ခုခ်င္းစီလိုက္ျကည့္ရမွာျဖစ္ပါတယ္

c:\windows\system32\6to4ex.dll

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin dlldump -p 1072 --dump-dir dump/
Volatility Foundation Volatility Framework 2.6
Process(V) Name                 Module Base Module Name          Result
---------- -------------------- ----------- -------------------- ------
0x8217d7e8 svchost.exe          0x001000000 svchost.exe          OK: module.1072.237d7e8.1000000.dll
0x8217d7e8 svchost.exe          0x07c900000 ntdll.dll            OK: module.1072.237d7e8.7c900000.dll
0x8217d7e8 svchost.exe          0x077b90000 certcli.dll          OK: module.1072.237d7e8.77b90000.dll
0x8217d7e8 svchost.exe          0x076d30000 WMI.dll              OK: module.1072.237d7e8.76d30000.dll
0x8217d7e8 svchost.exe          0x077f60000 SHLWAPI.dll          OK: module.1072.237d7e8.77f60000.dll
0x8217d7e8 svchost.exe          0x073b80000 AVICAP32.dll         OK: module.1072.237d7e8.73b80000.dll
0x8217d7e8 svchost.exe          0x050000000 wuauserv.dll         OK: module.1072.237d7e8.50000000.dll
0x8217d7e8 svchost.exe          0x077fe0000 Secur32.dll          OK: module.1072.237d7e8.77fe0000.dll
0x8217d7e8 svchost.exe          0x0755f0000 netcfgx.dll          OK: module.1072.237d7e8.755f0000.dll
0x8217d7e8 svchost.exe          0x077c00000 VERSION.dll          OK: module.1072.237d7e8.77c00000.dll
0x8217d7e8 svchost.exe          0x068000000 rsaenh.dll           OK: module.1072.237d7e8.68000000.dll
0x8217d7e8 svchost.exe          0x0773d0000 comctl32.dll         OK: module.1072.237d7e8.773d0000.dll
0x8217d7e8 svchost.exe          0x071a50000 mswsock.dll          OK: module.1072.237d7e8.71a50000.dll
0x8217d7e8 svchost.exe          0x071ad0000 WSOCK32.dll          OK: module.1072.237d7e8.71ad0000.dll
0x8217d7e8 svchost.exe          0x0733e0000 tapisrv.dll          OK: module.1072.237d7e8.733e0000.dll
0x8217d7e8 svchost.exe          0x072000000 uniplat.dll          OK: module.1072.237d7e8.72000000.dll
0x8217d7e8 svchost.exe          0x075290000 wbemcomn.dll         OK: module.1072.237d7e8.75290000.dll
0x8217d7e8 svchost.exe          0x076eb0000 TAPI32.dll           OK: module.1072.237d7e8.76eb0000.dll
0x8217d7e8 svchost.exe          0x074ad0000 POWRPROF.dll         OK: module.1072.237d7e8.74ad0000.dll
0x8217d7e8 svchost.exe          0x077d00000 netman.dll           OK: module.1072.237d7e8.77d00000.dll
0x8217d7e8 svchost.exe          0x073000000 WINSPOOL.DRV         OK: module.1072.237d7e8.73000000.dll
0x8217d7e8 svchost.exe          0x075310000 esscli.dll           OK: module.1072.237d7e8.75310000.dll
0x8217d7e8 svchost.exe          0x077920000 SETUPAPI.dll         OK: module.1072.237d7e8.77920000.dll
0x8217d7e8 svchost.exe          0x07df30000 rasmans.dll          OK: module.1072.237d7e8.7df30000.dll
0x8217d7e8 svchost.exe          0x05f770000 NCObjAPI.DLL         OK: module.1072.237d7e8.5f770000.dll
0x8217d7e8 svchost.exe          0x001d80000 OneX.DLL             OK: module.1072.237d7e8.1d80000.dll
0x8217d7e8 svchost.exe          0x076390000 IMM32.DLL            OK: module.1072.237d7e8.76390000.dll
0x8217d7e8 svchost.exe          0x076fb0000 winrnr.dll           OK: module.1072.237d7e8.76fb0000.dll
0x8217d7e8 svchost.exe          0x077c10000 msvcrt.dll           OK: module.1072.237d7e8.77c10000.dll
0x8217d7e8 svchost.exe          0x076bd0000 raschap.dll          OK: module.1072.237d7e8.76bd0000.dll
0x8217d7e8 svchost.exe          0x07d1e0000 msi.dll              OK: module.1072.237d7e8.7d1e0000.dll
0x8217d7e8 svchost.exe          0x0767f0000 SCHANNEL.dll         OK: module.1072.237d7e8.767f0000.dll
0x8217d7e8 svchost.exe          0x07e410000 USER32.dll           OK: module.1072.237d7e8.7e410000.dll
0x8217d7e8 svchost.exe          0x076e10000 adsldpc.dll          OK: module.1072.237d7e8.76e10000.dll
0x8217d7e8 svchost.exe          0x073030000 WZCSAPI.DLL          OK: module.1072.237d7e8.73030000.dll
0x8217d7e8 svchost.exe          0x050640000 wups.dll             OK: module.1072.237d7e8.50640000.dll
0x8217d7e8 svchost.exe          0x057d60000 hidphone.tsp         OK: module.1072.237d7e8.57d60000.dll
0x8217d7e8 svchost.exe          0x076e80000 rtutils.dll          OK: module.1072.237d7e8.76e80000.dll
0x8217d7e8 svchost.exe          0x001490000 Normaliz.dll         OK: module.1072.237d7e8.1490000.dll
0x8217d7e8 svchost.exe          0x071aa0000 WS2HELP.dll          OK: module.1072.237d7e8.71aa0000.dll
0x8217d7e8 svchost.exe          0x0750b0000 RESUTILS.DLL         OK: module.1072.237d7e8.750b0000.dll
0x8217d7e8 svchost.exe          0x0726c0000 QUtil.dll            OK: module.1072.237d7e8.726c0000.dll
0x8217d7e8 svchost.exe          0x0688f0000 HID.DLL              OK: module.1072.237d7e8.688f0000.dll
0x8217d7e8 svchost.exe          0x074f00000 SSDPAPI.dll          OK: module.1072.237d7e8.74f00000.dll
0x8217d7e8 svchost.exe          0x075390000 wbemess.dll          OK: module.1072.237d7e8.75390000.dll
0x8217d7e8 svchost.exe          0x076b20000 ATL.DLL              OK: module.1072.237d7e8.76b20000.dll
0x8217d7e8 svchost.exe          0x075130000 colbact.DLL          OK: module.1072.237d7e8.75130000.dll
0x8217d7e8 svchost.exe          0x05f740000 ncprov.dll           OK: module.1072.237d7e8.5f740000.dll
0x8217d7e8 svchost.exe          0x057d50000 ipconf.tsp           OK: module.1072.237d7e8.57d50000.dll
0x8217d7e8 svchost.exe          0x076360000 WINSTA.dll           OK: module.1072.237d7e8.76360000.dll
0x8217d7e8 svchost.exe          0x074f80000 ersvc.dll            OK: module.1072.237d7e8.74f80000.dll
0x8217d7e8 svchost.exe          0x077b40000 Apphelp.dll          OK: module.1072.237d7e8.77b40000.dll
0x8217d7e8 svchost.exe          0x0767c0000 w32time.dll          OK: module.1072.237d7e8.767c0000.dll
0x8217d7e8 svchost.exe          0x0753e0000 VSSAPI.DLL           OK: module.1072.237d7e8.753e0000.dll
0x8217d7e8 svchost.exe          0x063000000 WININET.dll          OK: module.1072.237d7e8.63000000.dll
0x8217d7e8 svchost.exe          0x0767a0000 NTDSAPI.dll          OK: module.1072.237d7e8.767a0000.dll
0x8217d7e8 svchost.exe          0x066460000 ipnathlp.dll         OK: module.1072.237d7e8.66460000.dll
0x8217d7e8 svchost.exe          0x075a70000 MSVFW32.dll          OK: module.1072.237d7e8.75a70000.dll
0x8217d7e8 svchost.exe          0x076080000 MSVCP60.dll          OK: module.1072.237d7e8.76080000.dll
0x8217d7e8 svchost.exe          0x077690000 NTMARTA.DLL          OK: module.1072.237d7e8.77690000.dll
0x8217d7e8 svchost.exe          0x05dca0000 iertutil.dll         OK: module.1072.237d7e8.5dca0000.dll
0x8217d7e8 svchost.exe          0x04c0a0000 wscsvc.dll           OK: module.1072.237d7e8.4c0a0000.dll
0x8217d7e8 svchost.exe          0x0662b0000 HNETCFG.DLL          OK: module.1072.237d7e8.662b0000.dll
0x8217d7e8 svchost.exe          0x0478c0000 dot3api.dll          OK: module.1072.237d7e8.478c0000.dll
0x8217d7e8 svchost.exe          0x0774e0000 ole32.dll            OK: module.1072.237d7e8.774e0000.dll
0x8217d7e8 svchost.exe          0x075690000 FastProx.dll         OK: module.1072.237d7e8.75690000.dll
0x8217d7e8 svchost.exe          0x077710000 es.dll               OK: module.1072.237d7e8.77710000.dll
0x8217d7e8 svchost.exe          0x073d20000 seclogon.dll         OK: module.1072.237d7e8.73d20000.dll
0x8217d7e8 svchost.exe          0x074f50000 MSIDLE.DLL           OK: module.1072.237d7e8.74f50000.dll
0x8217d7e8 svchost.exe          0x05cb70000 ShimEng.dll          OK: module.1072.237d7e8.5cb70000.dll
0x8217d7e8 svchost.exe          0x076790000 cryptdll.dll         OK: module.1072.237d7e8.76790000.dll
0x8217d7e8 svchost.exe          0x076da0000 browser.dll          OK: module.1072.237d7e8.76da0000.dll
0x8217d7e8 svchost.exe          0x0769c0000 USERENV.dll          OK: module.1072.237d7e8.769c0000.dll
0x8217d7e8 svchost.exe          0x076fd0000 CLBCATQ.DLL          OK: module.1072.237d7e8.76fd0000.dll
0x8217d7e8 svchost.exe          0x071bf0000 SAMLIB.dll           OK: module.1072.237d7e8.71bf0000.dll
0x8217d7e8 svchost.exe          0x075200000 repdrvfs.dll         OK: module.1072.237d7e8.75200000.dll
0x8217d7e8 svchost.exe          0x072810000 EapolQec.dll         OK: module.1072.237d7e8.72810000.dll
0x8217d7e8 svchost.exe          0x000630000 xpsp2res.dll         OK: module.1072.237d7e8.630000.dll
0x8217d7e8 svchost.exe          0x0776c0000 AUTHZ.dll            OK: module.1072.237d7e8.776c0000.dll
0x8217d7e8 svchost.exe          0x077050000 COMRes.dll           OK: module.1072.237d7e8.77050000.dll
0x8217d7e8 svchost.exe          0x077c70000 msv1_0.dll           OK: module.1072.237d7e8.77c70000.dll
0x8217d7e8 svchost.exe          0x076400000 netshell.dll         OK: module.1072.237d7e8.76400000.dll
0x8217d7e8 svchost.exe          0x07d4b0000 dhcpcsvc.dll         OK: module.1072.237d7e8.7d4b0000.dll
0x8217d7e8 svchost.exe          0x0750d0000 mtxoci.dll           OK: module.1072.237d7e8.750d0000.dll
0x8217d7e8 svchost.exe          0x075090000 srvsvc.dll           OK: module.1072.237d7e8.75090000.dll
0x8217d7e8 svchost.exe          0x0776e0000 shsvcs.dll           OK: module.1072.237d7e8.776e0000.dll
0x8217d7e8 svchost.exe          0x071cf0000 kerberos.dll         OK: module.1072.237d7e8.71cf0000.dll
0x8217d7e8 svchost.exe          0x077300000 schedsvc.dll         OK: module.1072.237d7e8.77300000.dll
0x8217d7e8 svchost.exe          0x076f20000 DNSAPI.dll           OK: module.1072.237d7e8.76f20000.dll
0x8217d7e8 svchost.exe          0x076b40000 WINMM.dll            OK: module.1072.237d7e8.76b40000.dll
0x8217d7e8 svchost.exe          0x075150000 Cabinet.dll          OK: module.1072.237d7e8.75150000.dll
0x8217d7e8 svchost.exe          0x057d70000 h323.tsp             OK: module.1072.237d7e8.57d70000.dll
0x8217d7e8 svchost.exe          0x0745b0000 eappcfg.dll          OK: module.1072.237d7e8.745b0000.dll
0x8217d7e8 svchost.exe          0x01a400000 urlmon.dll           OK: module.1072.237d7e8.1a400000.dll
0x8217d7e8 svchost.exe          0x074f40000 pchsvc.dll           OK: module.1072.237d7e8.74f40000.dll
0x8217d7e8 svchost.exe          0x075020000 wmiutils.dll         OK: module.1072.237d7e8.75020000.dll
0x8217d7e8 svchost.exe          0x05b860000 NETAPI32.dll         OK: module.1072.237d7e8.5b860000.dll
0x8217d7e8 svchost.exe          0x077e70000 RPCRT4.dll           OK: module.1072.237d7e8.77e70000.dll
0x8217d7e8 svchost.exe          0x071a90000 wshtcpip.dll         OK: module.1072.237d7e8.71a90000.dll
0x8217d7e8 svchost.exe          0x0600a0000 mspatcha.dll         OK: module.1072.237d7e8.600a0000.dll
0x8217d7e8 svchost.exe          0x0606b0000 ESENT.dll            OK: module.1072.237d7e8.606b0000.dll
0x8217d7e8 svchost.exe          0x077cc0000 ACTIVEDS.dll         OK: module.1072.237d7e8.77cc0000.dll
0x8217d7e8 svchost.exe          0x0722d0000 sens.dll             OK: module.1072.237d7e8.722d0000.dll
0x8217d7e8 svchost.exe          0x07db10000 wzcsvc.dll           OK: module.1072.237d7e8.7db10000.dll
0x8217d7e8 svchost.exe          0x077120000 OLEAUT32.dll         OK: module.1072.237d7e8.77120000.dll
0x8217d7e8 svchost.exe          0x076d40000 MPRAPI.dll           OK: module.1072.237d7e8.76d40000.dll
0x8217d7e8 svchost.exe          0x057d40000 kmddsp.tsp           OK: module.1072.237d7e8.57d40000.dll
0x8217d7e8 svchost.exe          0x073d30000 wbemcons.dll         OK: module.1072.237d7e8.73d30000.dll
0x8217d7e8 svchost.exe          0x076f50000 WTSAPI32.dll         OK: module.1072.237d7e8.76f50000.dll
0x8217d7e8 svchost.exe          0x0751a0000 srsvc.dll            OK: module.1072.237d7e8.751a0000.dll
0x8217d7e8 svchost.exe          0x0723d0000 WinSCard.dll         OK: module.1072.237d7e8.723d0000.dll
0x8217d7e8 svchost.exe          0x0597f0000 wmiprvsd.dll         OK: module.1072.237d7e8.597f0000.dll
0x8217d7e8 svchost.exe          0x065000000 ADVPACK.dll          OK: module.1072.237d7e8.65000000.dll
0x8217d7e8 svchost.exe          0x076b70000 rastls.dll           OK: module.1072.237d7e8.76b70000.dll
0x8217d7e8 svchost.exe          0x077dd0000 ADVAPI32.dll         OK: module.1072.237d7e8.77dd0000.dll
0x8217d7e8 svchost.exe          0x076e40000 wkssvc.dll           OK: module.1072.237d7e8.76e40000.dll
0x8217d7e8 svchost.exe          0x075070000 trkwks.dll           OK: module.1072.237d7e8.75070000.dll
0x8217d7e8 svchost.exe          0x076c90000 IMAGEHLP.dll         OK: module.1072.237d7e8.76c90000.dll
0x8217d7e8 svchost.exe          0x0708b0000 audiosrv.dll         OK: module.1072.237d7e8.708b0000.dll
0x8217d7e8 svchost.exe          0x010000000 6to4ex.dll           OK: module.1072.237d7e8.10000000.dll
0x8217d7e8 svchost.exe          0x0754d0000 CRYPTUI.dll          OK: module.1072.237d7e8.754d0000.dll
0x8217d7e8 svchost.exe          0x05d090000 comctl32.dll         OK: module.1072.237d7e8.5d090000.dll
0x8217d7e8 svchost.exe          0x072ae0000 RASQEC.DLL           OK: module.1072.237d7e8.72ae0000.dll
0x8217d7e8 svchost.exe          0x0750f0000 MTXCLU.DLL           OK: module.1072.237d7e8.750f0000.dll
0x8217d7e8 svchost.exe          0x076d10000 CLUSAPI.DLL          OK: module.1072.237d7e8.76d10000.dll
0x8217d7e8 svchost.exe          0x057cc0000 unimdm.tsp           OK: module.1072.237d7e8.57cc0000.dll
0x8217d7e8 svchost.exe          0x076780000 SHFOLDER.dll         OK: module.1072.237d7e8.76780000.dll
0x8217d7e8 svchost.exe          0x076fc0000 rasadhlp.dll         OK: module.1072.237d7e8.76fc0000.dll
0x8217d7e8 svchost.exe          0x0724b0000 ntlsapi.dll          OK: module.1072.237d7e8.724b0000.dll
0x8217d7e8 svchost.exe          0x0015d0000 eappprxy.dll         OK: module.1072.237d7e8.15d0000.dll
0x8217d7e8 svchost.exe          0x076f60000 WLDAP32.dll          OK: module.1072.237d7e8.76f60000.dll
0x8217d7e8 svchost.exe          0x07c800000 kernel32.dll         OK: module.1072.237d7e8.7c800000.dll
0x8217d7e8 svchost.exe          0x057d20000 ndptsp.tsp           OK: module.1072.237d7e8.57d20000.dll
0x8217d7e8 svchost.exe          0x077be0000 MSACM32.dll          OK: module.1072.237d7e8.77be0000.dll
0x8217d7e8 svchost.exe          0x050040000 wuaueng.dll          OK: module.1072.237d7e8.50040000.dll
0x8217d7e8 svchost.exe          0x076c60000 sfc_os.dll           OK: module.1072.237d7e8.76c60000.dll
0x8217d7e8 svchost.exe          0x06f880000 AcGenral.DLL         OK: module.1072.237d7e8.6f880000.dll
0x8217d7e8 svchost.exe          0x076bf0000 PSAPI.DLL            OK: module.1072.237d7e8.76bf0000.dll
0x8217d7e8 svchost.exe          0x071ab0000 WS2_32.dll           OK: module.1072.237d7e8.71ab0000.dll
0x8217d7e8 svchost.exe          0x075880000 rastapi.dll          OK: module.1072.237d7e8.75880000.dll
0x8217d7e8 svchost.exe          0x0736d0000 dot3dlg.dll          OK: module.1072.237d7e8.736d0000.dll
0x8217d7e8 svchost.exe          0x076ce0000 cryptsvc.dll         OK: module.1072.237d7e8.76ce0000.dll
0x8217d7e8 svchost.exe          0x059490000 wmisvc.dll           OK: module.1072.237d7e8.59490000.dll
0x8217d7e8 svchost.exe          0x077f10000 GDI32.dll            OK: module.1072.237d7e8.77f10000.dll
0x8217d7e8 svchost.exe          0x076d60000 iphlpapi.dll         OK: module.1072.237d7e8.76d60000.dll
0x8217d7e8 svchost.exe          0x074370000 WINIPSEC.DLL         OK: module.1072.237d7e8.74370000.dll
0x8217d7e8 svchost.exe          0x074f90000 dmserver.dll         OK: module.1072.237d7e8.74f90000.dll
0x8217d7e8 svchost.exe          0x076bb0000 sfc.dll              OK: module.1072.237d7e8.76bb0000.dll
0x8217d7e8 svchost.exe          0x076e90000 rasman.dll           OK: module.1072.237d7e8.76e90000.dll
0x8217d7e8 svchost.exe          0x076de0000 upnp.dll             OK: module.1072.237d7e8.76de0000.dll
0x8217d7e8 svchost.exe          0x05ad70000 UxTheme.dll          OK: module.1072.237d7e8.5ad70000.dll
0x8217d7e8 svchost.exe          0x076620000 comsvcs.dll          OK: module.1072.237d7e8.76620000.dll
0x8217d7e8 svchost.exe          0x076c30000 WINTRUST.dll         OK: module.1072.237d7e8.76c30000.dll
0x8217d7e8 svchost.exe          0x072240000 rasppp.dll           OK: module.1072.237d7e8.72240000.dll
0x8217d7e8 svchost.exe          0x07e720000 SXS.DLL              OK: module.1072.237d7e8.7e720000.dll
0x8217d7e8 svchost.exe          0x077a80000 CRYPT32.dll          OK: module.1072.237d7e8.77a80000.dll
0x8217d7e8 svchost.exe          0x07c9c0000 SHELL32.dll          OK: module.1072.237d7e8.7c9c0000.dll
0x8217d7e8 svchost.exe          0x0762c0000 wbemcore.dll         OK: module.1072.237d7e8.762c0000.dll
0x8217d7e8 svchost.exe          0x0768d0000 RASDLG.dll           OK: module.1072.237d7e8.768d0000.dll
0x8217d7e8 svchost.exe          0x076ee0000 RASAPI32.dll         OK: module.1072.237d7e8.76ee0000.dll
0x8217d7e8 svchost.exe          0x076c00000 credui.dll           OK: module.1072.237d7e8.76c00000.dll
0x8217d7e8 svchost.exe          0x04d4f0000 WINHTTP.dll          OK: module.1072.237d7e8.4d4f0000.dll
0x8217d7e8 svchost.exe          0x077b20000 MSASN1.dll           OK: module.1072.237d7e8.77b20000.dll
```

သံသယရွိတဲ့ DLL ကို Reverse Engineering လုပ္ရမွာျဖစ္ပါတယ္၊ Strings command နဲ့ပဲရပါတယ္၊ တကယ္ heavy လုပ္ရမယ္ဆိုရင္ေတာ့ ေနာက္တစ္ပိုင္းေပါ့

```
!This program cannot be run in DOS mode.
Rich8
oC5H
.text
`.rdata
@.data
.rsrc
@.reloc
SUV3
SSSS
j RP
V@j QR
_^][
GD]_[Y
SUVW
_^]2
k@Ph
_^]2
CE][
SUVWj
_^]3
D$ y
u	_^3
[_^]
[_^]
^][Y
.PQV
^][Y
 SUVW
_^]2
_^]2
_^]2
T$$R
_^]2
_^][
L$(j
D$< 
_^][
L$$Pj
L$8Pj
_^][
t$$P
_^][
L$(j
D$,P
L$(QU
_^][
_^][
Phxz
SUVW
D$ h
L$$j\Q
D$ RP
L$ h
j#Rj
_^][
RQPj
PVQSS
_^][
L$@PQ
SUVW
j#Rj
RPhda
_^][
_^]3
_]^[
tSSWU
_[^]
SUVW
_^][d
I@QP
?\uK
8\uC
tJ<\u8
SUVW
|$lj.
_^]2
_^]2
D$lRPj
_^]2
T$lh
D$lh
L$lh
D$lRP
D$(D
D$0ta
D$(RPj
_^][
L$(h
|$0h
L$4QRRRRRU
L$0GQ
<AtG<BtC
D$$RPU
jBVU
L$L$
L$ QR
_^]2
|$<.tK
D$<PVhd`
{	AU
^_][
^_][
\u!V
D$,W
D$(u
|$\.
D$\PWVh
L$ U
D$ ;
T$0RP
L$,Q
_^]d
_^jk
_^][
_^][
{ PW
T$$j
_^][
_^][
_^][d
SVW3
tLh 
_^][
T$ h
QRSh
L$0Ph
L$0Q
L$0Ph
L$0Q
t$`W
Iu	_^[
QRPPPPPPVP
D$Lta
|$`j/W
D$@D
D$Hta
T$dQRP
T$dR
D$dh
tVVP
D$ D
D$(ta
T$ QRj
_^][
t$(Wj
SUVW
_^]2
T$@QR
_^]2
_^]2
_^]2
_^]2
L$$j
Qh R
_^][
SUVWj
PWVS
_^][Y
0_^[
t$ WSPVR
D$,P
L$ P
< uX
;!u'
(SVW3
QSSSSSSSSj
QSUV
_^][Y
T$$h
tOVWS
PWVS
+^][
SVW3
Qh|d
Qhtd
Qhdd
RhPd
RhDd
Ph,d
SVW3
QSh?
QVRS
D$TSUVW
F$t%
VhP}
_^][d
QSUV
F$t%
_^][d
tfjdj
t5jdj
QSVW
IGQW
JGRW
_^][
QSUVW
_^][Y
_^][
_^]j
wQt1-
_][^
t\SV
t6WS
SUWV
_][^
DSUV
L$d3
^`PQ
F(RPQ
VDUUW
NDSUPQ
FhURUPQ
FLRP
VHQR
F(RPU
N4UQ
^][d
_^[d
l$(VW3
D$0j
FxQRP
~0;~,}
_^][
_^]3
FHUj
U&OR
^4Uj
_^]2
QSUVW
_^][Y
NLRPj
QSUVW
D$ Pj
VDPQRUSP
FLQP
FLh 
NPRPUSj
_^][Y
QWRVj
_^][
:;9t_
SUVW
L$(3
T$$j
D$xh
D$<D
T$|Qj
^][d
T$$h
RPVQ
T$$h
QSUV
_^][Y
L$(W
T$ Fj:V
T$(Fj:V
_^][
PQRV
|$ +
L$ Q
][_^
L$@jdQV
T$,h
D$ WP
D$$f
D$ h
_^][Y
_^][Y
T$$j
_^][Y
8MZuC
L$(P
l$(C%
l$,;
_^]3
SUVW
SQPj
T$,QRW
;j8s9
L$4SQ
C;j8r
_^][
D$$SVh 
QRWV
L$8h
QRPV
|$(u
Vtdhp
T$8h
L$4Qj
D$ R
L$ P
T$,QR
L$(P
T$ Q
L$ RQPj
L$hP
T$4P
T$xQR
L$hP
L$4Qj
|$,W
HAPQ
D$$3
l$H~+
D$$E;
FVj@
L$@_^][d
QSVW
_^[Y
D$$(
L$$Qj
D$@P
jBVU
t$@A
jBSU
VPj(
T$,Vj
D$ Q
L$ Rh
SUVWj
~$UW
_^][
_^]3
t-Vh
QVVj
u	_^
SUVW
u	_^
u	_^
SUV3
WUUU
|$ u
_^]2
UUPW
_^]2
D$(h
|$$MZu'
D$,RPQ
L$@jdQV
,SUVW
_^][
_^]2
_^]2
RSh,
Pj,h-
_^]2
Rj,h
QPPVhp
_^][
_^][
F,_^[
l$,t
M263
D$ IV32
D$$MP42
D$(cvid
Phvidc
vidc
FDtB
VLRQh
FDQU
NLPQh
^[_]d
t)Wj
T$<VW
D$DS
\$DV
N(PQ
~(9~$u
_^][
_^][
_^][
_^][
|$08
W(9W$u
\$ ;
D$(;
_^][
_^][
tZ9H tU9H$tP
n ux
_^]3
F|UV
_^]3
_^]3
_^]3
V(PR
N(PQ
V(QR
B<Wf
_^][
U0SQR
Fdf+Fh
Nlw^
~@B3
SUVW
T$ v
D$(8D*
D$ ;
_^][
QSUV
nXtX
f+F\
VlH3
NlBI
FlAH
^][Y
_^]3
G(RP
G0_^
W(VR
G(Sj
W(QR
G(VP
D$8S
\$8U
C0V;
L$Ds
D$$R
L$,P
T$4Q
D$<RP
D$<Q
L$DR
T$LPQR
 s,3
T$D;
T$Ds
|$HPWS
T$Ds
D$ u"
T$Ds
L$ +
t$Hj
N(PQ
D$4s
L$ ;
L$DRQ
L$0R
D$D	
T$(PQR
N(PQ
T$DPVS
L$Ds
L$LQP
_^][
_^][
_^][
_^][
D$HQ
_^][
_^][
T$LRWS
_^][
L$D+
T$LRP
_^][
_^][
L$L+
_^][
F(RP
_^][
L$LQV
_^][
F(RP
_^][
V(QR
T$HVS
_^][
_^][
L$LQVS
K4PVS
_^][
_^][
_^][
L$H+
_^][
N(PQ
F(RP
N(WQ
|$ WUSV
@APQV
_^][
D$$f
T$ RV
_^][
_^][
D$$SUV
L$03
t$ f
D$0tb
D$0H
_^][
]_^[Y
HPQV
JRPV
_^][
T$ }
]_^[
l$ 3
l$ f
l$ f
l$ f
t$ W
WVQR3
D$,s
D$(3
L$$r
D$$#
D$(3
L$$r
D$$#
D$(3
L$$r
D$$#
D$(3
L$$r
D$$#
T$,RWV
;N,u
T$,RWV
T$,RWV
_^][
_^][
L$,QWV
_^][
T$,RWV
_^][
_^][
_^][
_^][
|$ j
L$ RUPj
W(SR
^]_[Y
W(SR
^]_[Y
9t$Tu
:_^]3
98u	A
T$,v
T+3x%A
t$Dy
t$DB
L$,;
T$,+
L$H;
D$1+
T$0+
;D$<s!
;D$<r
|$8M#
L$,B;
t$D3
\$,UV
C(Wj
L$4R
T$,PQh
L$8R
T$(P
D$0Qh|2
C(WP
_^][Y
K(WQ
_^][Y
K(WQ
_^][Y
K(WQ
_^][Y
S(WR
_^][Y
S(WR
_^][Y
K<UWQ
K<UVQ
L$(SU
t$0#
t$4#
L$,+
l$(+
l$(+
GFMu
GFIu
GFIu
GFIu
\$8+
{4_^]3
\$8+
{4_^]
\$8+
{4_^]
t	WVS
NWVS
u7WPS
u&WVS
_^[]
#9vb[9v
aE~?gF~e
B~@}B~
A~+wB~
B~k!C~
B~i#C~Q
A~,}B~/
 deflate 1.1.4 Copyright 1995-2002 Jean-loup Gailly 
								
 inflate 1.1.4 Copyright 1995-2002 Mark Adler 
CreateEventA
CloseHandle
TerminateThread
WaitForSingleObject
SetEvent
ResumeThread
CreateThread
InitializeCriticalSection
DeleteCriticalSection
VirtualFree
LeaveCriticalSection
EnterCriticalSection
VirtualAlloc
ResetEvent
lstrcpyA
InterlockedExchange
CancelIo
Sleep
lstrlenA
GetPrivateProfileSectionNamesA
lstrcatA
GetWindowsDirectoryA
FreeLibrary
GetProcAddress
LoadLibraryA
MultiByteToWideChar
WideCharToMultiByte
lstrcmpA
GetPrivateProfileStringA
GetVersionExA
DeleteFileA
GetLastError
CreateDirectoryA
GetFileAttributesA
CreateProcessA
GetDriveTypeA
GetDiskFreeSpaceExA
GetVolumeInformationA
GetLogicalDriveStringsA
FindClose
LocalFree
FindNextFileA
LocalReAlloc
FindFirstFileA
LocalAlloc
RemoveDirectoryA
GetFileSize
CreateFileA
ReadFile
SetFilePointer
WriteFile
MoveFileA
GetModuleFileNameA
SetLastError
GetSystemDirectoryA
GetCurrentProcess
CreateRemoteThread
WriteProcessMemory
VirtualAllocEx
OpenProcess
MoveFileExA
GetTickCount
GetLocalTime
HeapFree
GetProcessHeap
MapViewOfFile
CreateFileMappingA
HeapAlloc
UnmapViewOfFile
GlobalFree
GlobalUnlock
GlobalLock
GlobalAlloc
GlobalSize
GetStartupInfoA
CreatePipe
DisconnectNamedPipe
TerminateProcess
PeekNamedPipe
WaitForMultipleObjects
SizeofResource
LoadResource
FindResourceA
DeviceIoControl
LoadLibraryExA
GetModuleHandleA
SetFileAttributesA
ReleaseMutex
OpenEventA
SetErrorMode
CreateMutexA
SetUnhandledExceptionFilter
FreeConsole
LocalSize
Process32Next
Process32First
CreateToolhelp32Snapshot
lstrcmpiA
GetCurrentThreadId
KERNEL32.dll
DispatchMessageA
TranslateMessage
GetMessageA
wsprintfA
CharNextA
GetWindowTextA
GetActiveWindow
GetKeyNameTextA
CallNextHookEx
SetWindowsHookExA
UnhookWindowsHookEx
LoadCursorA
DestroyCursor
BlockInput
SystemParametersInfoA
SendMessageA
keybd_event
MapVirtualKeyA
SetCapture
WindowFromPoint
SetCursorPos
mouse_event
CloseClipboard
SetClipboardData
EmptyClipboard
OpenClipboard
GetClipboardData
GetSystemMetrics
SetRect
GetDC
GetDesktopWindow
ReleaseDC
GetCursorInfo
GetCursorPos
SetProcessWindowStation
OpenWindowStationA
GetProcessWindowStation
ExitWindowsEx
GetWindowThreadProcessId
IsWindowVisible
EnumWindows
CloseDesktop
SetThreadDesktop
OpenInputDesktop
GetUserObjectInformationA
GetThreadDesktop
OpenDesktopA
PostMessageA
CreateWindowExA
CloseWindow
IsWindow
USER32.dll
SelectObject
CreateDIBSection
CreateCompatibleDC
DeleteObject
DeleteDC
BitBlt
GetDIBits
CreateCompatibleBitmap
GDI32.dll
IsValidSid
LookupAccountNameA
LsaClose
LsaRetrievePrivateData
LsaOpenPolicy
LsaFreeMemory
RegCloseKey
RegQueryValueA
RegOpenKeyExA
CloseServiceHandle
DeleteService
ControlService
QueryServiceStatus
OpenServiceA
OpenSCManagerA
RegSetValueExA
RegCreateKeyA
RegQueryValueExA
RegOpenKeyA
CloseEventLog
ClearEventLogA
OpenEventLogA
AdjustTokenPrivileges
LookupPrivilegeValueA
OpenProcessToken
FreeSid
SetSecurityDescriptorDacl
AddAccessAllowedAce
InitializeAcl
GetLengthSid
AllocateAndInitializeSid
InitializeSecurityDescriptor
RegEnumValueA
RegEnumKeyExA
RegDeleteValueA
RegDeleteKeyA
RegCreateKeyExA
StartServiceA
RegisterServiceCtrlHandlerA
SetServiceStatus
LookupAccountSidA
GetTokenInformation
ADVAPI32.dll
SHGetSpecialFolderPathA
SHGetFileInfoA
SHELL32.dll
SHDeleteKeyA
SHLWAPI.dll
??2@YAPAXI@Z
??3@YAXPAX@Z
__CxxFrameHandler
memmove
ceil
_ftol
strstr
_CxxThrowException
strchr
malloc
free
_except_handler3
strrchr
strncpy
strncat
realloc
atoi
wcstombs
_beginthreadex
calloc
MSVCRT.dll
??1type_info@@UAE@XZ
_initterm
_adjust_fdiv
waveOutClose
waveOutUnprepareHeader
waveOutReset
waveInClose
waveInUnprepareHeader
waveInReset
waveInStop
waveOutWrite
waveInStart
waveInAddBuffer
waveInPrepareHeader
waveInOpen
waveInGetNumDevs
waveOutPrepareHeader
waveOutOpen
waveOutGetNumDevs
WINMM.dll
WSAIoctl
WS2_32.dll
?_Tidy@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@AAEX_N@Z
?_C@?1??_Nullstr@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@CAPBDXZ@4DB
??1?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ
?assign@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAEAAV12@PBDI@Z
?_Grow@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@AAE_NI_N@Z
?_Refcnt@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@AAEAAEPBD@Z
?_Eos@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@AAEXI@Z
?_Split@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@AAEXXZ
?_Xran@std@@YAXXZ
?npos@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@2IB
MSVCP60.dll
ImmReleaseContext
ImmGetCompositionStringA
ImmGetContext
IMM32.dll
InternetCloseHandle
InternetReadFile
InternetOpenUrlA
InternetOpenA
WININET.dll
capGetDriverDescriptionA
capCreateCaptureWindowA
ICSeqCompressFrame
ICSeqCompressFrameStart
ICSendMessage
ICOpen
ICClose
ICCompressorFree
ICSeqCompressFrameEnd
AVICAP32.dll
MSVFW32.dll
GetModuleFileNameExA
EnumProcessModules
PSAPI.DLL
WTSFreeMemory
WTSQuerySessionInformationA
WTSAPI32.dll
_strnicmp
_strcmpi
nC5H
svchost.dll
ResetSSDT
ServiceMain
.PAX
.PAD
bad Allocate
bad buffer
%s\%s
Microsoft\Network\Connections\pbk\rasphone.pbk
\Application Data\Microsoft\Network\Connections\pbk\rasphone.pbk
Documents and Settings\
ConvertSidToStringSidA
advapi32.dll
L$_RasDefaultCredentials#0
RasDialParams!%s#0
Device
PhoneNumber
DialParamsUID
WinSta0\Default
%s\shell\open\command
%s\*.*
%s%s%s
%s%s*.*
SYSTEM\CurrentControlSet\Services\%s
InstallModule
RegSetValueEx(start)
Type
SYSTEM\CurrentControlSet\Services\
RegQueryValueEx(Type)
\syslog.dat
Gh0st Update
Applications\iexplore.exe\shell\open\command
System
Security
Application
Host
SeDebugPrivilege
CloseHandle
Sleep
kernel32.dll
SHDeleteKeyA
shlwapi.dll
CloseServiceHandle
DeleteService
StartServiceA
ControlService
QueryServiceStatus
OpenServiceA
OpenSCManagerA
winlogon.exe
%d.bak
ex.dll
[%02d/%02d/%d %02d:%02d:%02d] (%s)
_kaspersky
REG_BINARY
%-24s %-15s 
REG_MULTI_SZ
%-24s %-15s 0x%x(%d) 
REG_DWORD
%-24s %-15s %s 
REG_EXPAND_SZ
REG_SZ
[%s]
\cmd.exe
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
AAAA
Mozilla/4.0 (compatible)
https://
http://
~MHz
HARDWARE\DESCRIPTION\System\CentralProcessor\0
KeServiceDescriptorTable
ntdll.dll
NtQuerySystemInformation
\\.\RESSDTDOS
Global\Gh0st %d
winsta0
AAAAAA
SeShutdownPrivilege
explorer.exe
Winlogon
CVideoCap
#32770
1.1.4
need dictionary
incorrect data check
incorrect header check
invalid window size
unknown compression method
invalid bit length repeat
too many length or distance symbols
invalid stored block lengths
invalid block type
incompatible version
buffer error
insufficient memory
data error
stream error
file error
stream end
invalid distance code
invalid literal/length code
incomplete dynamic bit lengths tree
oversubscribed dynamic bit lengths tree
incomplete literal/length tree
oversubscribed literal/length tree
empty distance tree with lengths
incomplete distance tree
oversubscribed distance tree
.?AVtype_info@@
!This program cannot be run in DOS mode.
Rich
.text
h.rdata
H.data
INIT
.reloc
_WWR
SVW`3
PPj"WPV
_^[]
Y_^[
RSDSJ+
e:\gh0st\server\sys\i386\RESSDT.pdb
IofCompleteRequest
IoDeleteDevice
IoDeleteSymbolicLink
KeServiceDescriptorTable
ProbeForWrite
ProbeForRead
_except_handler3
IoCreateSymbolicLink
IoCreateDevice
RtlInitUnicodeString
KeTickCount
ntoskrnl.exe
6$636<6A6L6]6
```
Most Frequent word ကိုရွာျကည့္ေသးတယ္ အဆင္မေျပဘူး
```6T7X7tr -c '[:alnum:]' '[\n*]' < test.txt | sort | uniq -c | sort -nr | head  -10```

Global\Gh0st %d ကိုေတြ့ရင္ေတာ့ Gh0st ဆိုတာကိုသိနိုင္တယ္

What was stolen ဆိုတာအတြက္ ဘာေတြ run ထားလဲဆိုတာသိေအာင္လုပ္ရပါမယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin consoles
Volatility Foundation Volatility Framework 2.6
**************************************************
ConsoleProcess: csrss.exe Pid: 616
Console: 0x4f2398 CommandHistorySize: 50
HistoryBufferCount: 4 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\System32\svchost.exe
Title: C:\WINDOWS\System32\svchost.exe - PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
AttachedProcess: PsExec.exe Pid: 1772 Handle: 0x598
----
CommandHistory: 0x10f8898 Application: PsExec.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x598
```
ဒီ Command ကိုျကည့္ျပီးေတာ့ က်ေနာ္တို့သိနိုင္တာက psexec ကိုသံုးျပီး command ရိုက္သြားတယ္ဆိုတာပါ။ ဒါေျကာင့္ psexec နဲ့ပတ္သတ္တာေတြကို memory ထဲမွာလိုက္ရွာျကည့္မယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ strings mem/memdump.bin | egrep -n20 -i -a "psexec"
16454-Vad 
16455-Irp (
16456-VadS
16457-Vadl
16458-Io  
16459-Ntfn
16460-Ntfi
16461-FSfm
16462-Ntfr
16463-Ntfn
16464-VadS
16465-Ntfr
16466-NtFs
16467-ReTa
16468-Vadl
16469-CcSc
16470-Ntfn
16471-Vad 
16472-Vad 
16473-Irp `
16474:PsExec.exe
16475-Cm  
16476-CPnp
16477-NtFs
16478-Vad 
16479-CcSc
16480-Wmip
16481-Ntfi
16482-NtFs
16483-MmCa
16484-MmCa@8
16485-FSfm
16486-Vad 
16487-CcSc
16488-VadS
16489-Hal 
16490-MmCi8
16491-Vad  o
16492-TCPC
16493-Ntfn`
16494-Nbtl
--
393480-PreShiftInfo0
393481-dbl2
393482-dbl3nk 
393483-dbl4
393484-dbl53
393485-dbl6
393486-Title
393487-dbl74
393488-dbl8
393489-PostShift0_
393490-PreShift0reShift
393491-dbl2
393492-dbl30
393493-hbin
393494-Shell Extensions
393495-Blocked
393496-Cached
393497-{FF393560-C2A7-11CF-BFF4-444553540000} {062E1261-A60E-11D0-82C2-00C04FD5AE38} 0x401
393498-"C:\Program Files\Windows Media Player\wmplayer.exe"
393499-C:\Program Files\Windows Media Player\wmplayer.exe
393500:PsExec
393501-h	}Z
393502-]	zX	zX
393503-~\	zX
393504-tR	}Z
393505-~\	wU
393506-k	|U
393507-_$~[$~[$~[#}Z#zX wU
393508-nL#wU(|Z'{Y$xV&wV'xW,
393509-^&|Z%yW"xV%yW#yW!uS
393510-mL"qP$sR%tS$sR"qP oN
393511-iI!lL$oO&qQ'rR
393512-fF"nN
393513-eF fG
393514-]>"hI fG
393515-dE fG fG"gL%jO&kP$iN eJ
393516-cH eJ#hM&kP#hM
393517-cH fH
393518-eF!gH fG
393519-eF fG"hI$jK#iJ
393520-yZ ~_
--
676199-38B5
676200-__InstanceOperationEvent
676201-ou((
676202-.iuH
676203-.iuH
676204-iu(P
676205-eld`
676206-h01u
676207-D' u@
676208-D73323810DAB2D362482D85928C165A\CR_A44D1BF95F0A41768D5546A4044C1625\C_35EC67A815B3C0868ACC23C410EA83D2
676209-D' u
676210-DEB2
676211-|/iu
676212-dhTl
676213- Volume in drive C has no label.
676214- Volume Serial Number is 3CD4-8C81
676215- Directory of C:\WINDOWS\system32\xircom
676216-11/17/2012  01:35 PM    <DIR>          .
676217-11/17/2012  01:35 PM    <DIR>          ..
676218-11/17/2012  01:35 PM           303,104 gsecdump.exe
676219:11/17/2012  01:35 PM           381,816 PsExec.exe
676220-               2 File(s)        684,920 bytes
676221-               2 Dir(s)   5,849,026,560 bytes free
676222-C:\WINDOWS\system32\xircom>
676223-__SystemClass
676224-__IndicationRelated
676225-abstract
676226-__IndicationRelated
676227-__SystemClass
676228-__EventFilter
676229-CreatorSID
676230-uint8
676231-EventAccess
676232-string
676233-EventNamespace
676234-string
676235-Name
676236-string
676237-Query
676238-string
676239-QueryLanguage
--
769616-ObSq
769617-LNKFILE
769618-Ntfo\
769619-ObSq
769620-CMVIH~
769621-Gla4
769622-Gh05
769623-{93F2F68C-1D1B-11D3-A30E-00C04F79ABD1}l
769624-Gla@h
769625-CMVa
769626-.ASMrentId
769627-{DC971EE5-44EB-4FE4-AE2E-B91490411BFC}
769628-CMVI
769629-CMVa
769630-EnableConsoleTracingP=
769631-ObSq
769632-AuDA
769633-AudC
769634-ObSq
769635-CMVI`
769636:PSEXEC.EXE
769637-ObNmP
769638-A672-0
769639-CMVaP
769640-CMVa
769641-Description
769642-FSim
769643-IoNm\
769644-92-116680F0CEDA}}
769645-AudLH
769646-ObSq
769647-CMVI
769648-ObHd
769649-MmSm
769650-CMDa
769651-CMVa
769652-Ntfc	
769653-CMDa
769654-{C3480414-
769655-.SBR2}0
769656-CMVI
--
809032-CMVIX
809033-CMVa
809034-DeDeviceDesc
809035-20yk
809036-CMDa
809037-CMDa
809038-Service
809039-CMDa
809040-CMVa
809041-PreferExecuteOnMismatch
809042-AtmA
809043-CMDa
809044-DisplayString
809045-CMVI
809046-NtFsPG
809047-ObSq
809048-AudD\
809049-ObSqH`
809050-CMVa
809051-.%Tl
809052:PSEXECl
809053-Ustm
809054-SrSC<
809055-Usqm
809056-MmSm
809057-Gh05
809058-&)&&
809059-=@//
809060-CMVI
809061-CMVa
809062-cFormatTags
809063-CMVa
809064-cFormatTags
809065-CMVa
809066-cFormatTags
809067-AUDIOCOMPRESSIONMANAGER
809068-Gfnt
809069-Ph(`
809070-IpDnsSuffix
809071-IpDnsFlags
809072-IpWins2
--
1009484-Identifier
1009485-AtmA0M
1009486-CMDa
1009487-sLongDate
1009488-NtFI
1009489-Gla8
1009490-Ntf0
1009491-CMVa
1009492-CMVa
1009493-Class
1009494-CMVa
1009495-DeviceDescA
1009496-SeAcP
1009497-RxFc(
1009498-#2222
1009499-CMDa
1009500-uiDlllumnHi
1009501-,-6412	
1009502-MmSt
1009503-NtFsI'
1009504:PsExec v1.98 - Execute processes r
1009505-ObSq
1009506-CMVa
1009507-*ImagePathB
1009508-Gfnt 
1009509-SeAc
1009510-CMVa
1009511-Type
1009512-ObSq
1009513-CMVa
1009514-yPSupportedNameSpaces
1009515-Pp  
1009516-NtFA@w
1009517-CMVa
1009518-Count
1009519-CMVI
1009520-Gfnt*
1009521-j\hH
1009522-PWWW
1009523-9HTt
1009524-9HTt
--
1347836-SendMessageW
1347837-ShowWindow
1347838-GetWindowLongW
1347839-SetDlgItemTextW
1347840-CheckDlgButton
1347841-SendDlgItemMessageW
1347842-GetParent
1347843-IsDlgButtonChecked
1347844-WinHelpW
1347845-GetWindow
1347846-PostMessageW
1347847-RSDS$
1347848-setupapi.pdb
1347849-dhTl
1347850- Volume in drive C has no label.
1347851- Volume Serial Number is 3CD4-8C81
1347852- Directory of C:\WINDOWS\system32\xircom
1347853-11/17/2012  01:35 PM    <DIR>          .
1347854-11/17/2012  01:35 PM    <DIR>          ..
1347855-11/17/2012  01:35 PM           303,104 gsecdump.exe
1347856:11/17/2012  01:35 PM           381,816 PsExec.exe
1347857-               2 File(s)        684,920 bytes
1347858-               2 Dir(s)   5,849,026,560 bytes free
1347859-C:\WINDOWS\system32\xircom>
1347860-Qpgn
1347861-/h<P+
1347862-'h<P
1347863-*Tp3.;P
1347864-*Sp3.
1347865-'vi;
1347866-A~9|B~
1347867-B~nCB~
1347868-B~6xB~4
1347869-A~r C~}mE~
1347870-UnRegisterTypeLib
1347871-ATL:%8.8X
1347872-Can not run Unicode version of ATL.DLL on Windows 95.
1347873-Please install the correct version.
1347874-@Qm6t
1347875-vInterlockedCompareExchange
1347876-InterlockedPopEntrySList
--
1452171-ObSq
1452172-LNKFILE
1452173-Ntfo\
1452174-ObSq
1452175-CMVIH~
1452176-Gla4
1452177-Gh05
1452178-{93F2F68C-1D1B-11D3-A30E-00C04F79ABD1}l
1452179-Gla@h
1452180-CMVa
1452181-.ASMrentId
1452182-{DC971EE5-44EB-4FE4-AE2E-B91490411BFC}
1452183-CMVI
1452184-CMVa
1452185-EnableConsoleTracingP=
1452186-ObSq
1452187-AuDA
1452188-AudC
1452189-ObSq
1452190-CMVI`
1452191:PSEXEC.EXE
1452192-ObNmP
1452193-A672-0
1452194-CMVaP
1452195-CMVa
1452196-Description
1452197-FSim
1452198-IoNm\
1452199-92-116680F0CEDA}}
1452200-AudLH
1452201-ObSq
1452202-CMVI
1452203-ObHd
1452204-MmSm
1452205-CMDa
1452206-CMVa
1452207-Ntfc	
1452208-CMDa
1452209-{C3480414-
1452210-.SBR2}0
1452211-CMVI
--
1504687-CMVIX
1504688-CMVa
1504689-DeDeviceDesc
1504690-20yk
1504691-CMDa
1504692-CMDa
1504693-Service
1504694-CMDa
1504695-CMVa
1504696-PreferExecuteOnMismatch
1504697-AtmA
1504698-CMDa
1504699-DisplayString
1504700-CMVI
1504701-NtFsPG
1504702-ObSq
1504703-AudD\
1504704-ObSqH`
1504705-CMVa
1504706-.%Tl
1504707:PSEXECl
1504708-Ustm
1504709-SrSC<
1504710-Usqm
1504711-MmSm
1504712-Gh05
1504713-&)&&
1504714-=@//
1504715-CMVI
1504716-CMVa
1504717-cFormatTags
1504718-CMVa
1504719-cFormatTags
1504720-CMVa
1504721-cFormatTags
1504722-AUDIOCOMPRESSIONMANAGER
1504723-Gfnt
1504724-1uPh
1504725-01uj
1504726-C;^H|
1504727-1uPh
--
1581398-NotInsertableD
1581399-{8C3ADF99-CCFE-11d2-AD10-00C04F72DD47}h4
1581400-tAppID
1581401-LocalServer32
1581402-ft_0&
1581403-{8C4EB103-516F-11D1-A6DF-006097C4E476}
1581404-er Name            Remark
1581405--------------------------------------------------------------------------------
1581406-\\2K3DC                                                                        
1581407-\\GH0ST1                                                                       
1581408-The command completed successfully.
1581409-C:\WINDOWS\system32\xircom>:
1581410-59Yh
1581411-8D*`3
1581412- Volume in drive C has no label.
1581413- Volume Serial Number is 3CD4-8C81
1581414- Directory of C:\WINDOWS\system32\xircom
1581415-11/17/2012  01:35 PM    <DIR>          .
1581416-11/17/2012  01:35 PM    <DIR>          ..
1581417-11/17/2012  01:35 PM           303,104 gsecdump.exe
1581418:11/17/2012  01:35 PM           381,816 PsExec.exe
1581419-               2 File(s)        684,920 bytes
1581420-               2 Dir(s)   5,849,026,560 bytes free
1581421-C:\WINDOWS\system32\xircom>
1581422- DxK-
1581423-eMmz
1581424- Volume in drive C has no label.
1581425- Volume Serial Number is 3CD4-8C81
1581426- Directory of C:\WINDOWS\system32\xircom
1581427-11/17/2012  01:37 PM    <DIR>          .
1581428-11/17/2012  01:37 PM    <DIR>          ..
1581429-11/17/2012  01:37 PM             4,947 berry.gif
1581430-11/17/2012  01:35 PM           303,104 gsecdump.exe
1581431:11/17/2012  01:35 PM           381,816 PsExec.exe
1581432-               3 File(s)        689,867 bytes
1581433-               2 Dir(s)   5,849,042,944 bytes free
1581434-C:\WINDOWS\system32\xircom>n
1581435-=!mg
1581436--46W
1581437-(/}p m
1581438-t5dS
1581439-l5wI
1581440-Xw){
1581441-HJ-*
1581442-edH/NMN)
1581443-2,`a
1581444-C:\WINDOWS\system32>V
1581445-+:u	
1581446-KD!t
1581447-ilX(
1581448-             6,656 routetab.dll
1581449-08/29/2002  07:00 AM            22,016 rpcns4.dll
1581450-04/14/2008  05:42 AM           584,704 rpcrt4.dll
1581451-04/14/2008  05:42 AM           399,360 rpcss.dll
--
1729401-Identifier
1729402-AtmA0M
1729403-CMDa
1729404-sLongDate
1729405-NtFI
1729406-Gla8
1729407-Ntf0
1729408-CMVa
1729409-CMVa
1729410-Class
1729411-CMVa
1729412-DeviceDescA
1729413-SeAcP
1729414-RxFc(
1729415-#2222
1729416-CMDa
1729417-uiDlllumnHi
1729418-,-6412	
1729419-MmSt
1729420-NtFsI'
1729421:PsExec v1.98 - Execute processes r
1729422-ObSq
1729423-CMVa
1729424-*ImagePathB
1729425-Gfnt 
1729426-SeAc
1729427-CMVa
1729428-Type
1729429-ObSq
1729430-CMVa
1729431-yPSupportedNameSpaces
1729432-Pp  
1729433-NtFA@w
1729434-CMVa
1729435-Count
1729436-CMVI
1729437-Gfnt*
1729438-Ph\b
1729439-_[^]
1729440-HtCHt1Ht
1729441-t*Ht
--
1903448-OS=Windows_NT
1903449-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1903450-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1903451-PROCESSOR_ARCHITECTURE=x86
1903452-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1903453-PROCESSOR_LEVEL=6
1903454-PROCESSOR_REVISION=2a07
1903455-ProgramFiles=C:\Program Files
1903456-PROMPT=$P$G
1903457-SystemDrive=C:
1903458-SystemRoot=C:\WINDOWS
1903459-TEMP=C:\WINDOWS\TEMP
1903460-TMP=C:\WINDOWS\TEMP
1903461-USERPROFILE=C:\Documents and Settings\NetworkService
1903462-windir=C:\WINDOWS
1903463-                          
1903464-                        
1903465-        
1903466-abcdefghijklmnopqrstuvwxyz
1903467-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1903468:PsExec.exe
1903469-\\w2k3dc
1903470-cmd /c ipconfig
1903471-\accepteula
1903472-ALLUSERSPROFILE=C:\Documents and Settings\All Users
1903473-CommonProgramFiles=C:\Program Files\Common Files
1903474-COMPUTERNAME=GH0ST1
1903475-ComSpec=C:\WINDOWS\system32\cmd.exe
1903476-FP_NO_HOST_CHECK=NO
1903477-NUMBER_OF_PROCESSORS=1
1903478-OS=Windows_NT
1903479-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1903480-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1903481-PROCESSOR_ARCHITECTURE=x86
1903482-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1903483-PROCESSOR_LEVEL=6
1903484-PROCESSOR_REVISION=2a07
1903485-ProgramFiles=C:\Program Files
1903486-PROMPT=$P$G
1903487-SystemDrive=C:
1903488-SystemRoot=C:\WINDOWS
--
1908387-SamIFree_SAMPR_ENUMERATION_BUFFER
1908388-SamIFree_SAMPR_GET_GROUPS_BUFFER
1908389-SamIFree_SAMPR_GET_MEMBERS_BUFFER
1908390-SamIFree_SAMPR_GROUP_INFO_BUFFER
1908391-SamIFree_SAMPR_PSID_ARRAY
1908392-SamIFree_SAMPR_RETURNED_USTRING_ARRAY
1908393-SamIFree_SAMPR_SR_SECURITY_DESCRIPTOR
1908394-SamIFree_SAMPR_ULONG_ARRAY
1908395-SamIFree_SAMPR_USER_INFO_BUFFER
1908396-SamIFree_UserInternal6Information
1908397-SamIGCLookupNames
1908398-SamIGCLookupSids
1908399-SamIGetAliasMembership
1908400-SamIGetBootKeyInformation
1908401-SamIGetDefaultAdministratorName
1908402-SamIGetFixedAttributes
1908403-SamIGetInterdomainTrustAccountPasswordsForUpgrade
1908404-SamIGetPrivateData
1908405-equires Windows NT/2000/XP/2003.
1908406-Use PsKill to terminate the remotely running program.
1908407:The version of the PsExec service running on the remote system is not compabible with this version of PsExec.
1908408:execute, not PsExec.
1908409:Error codes returned by PsExec are specific to the applications you
1908410-the password is transmitted in clear text to the remote system.
1908411-to network resources or to run in a different account. Note that
1908412-in the Domain\User syntax if the remote process requires access
1908413-resources (because it is impersonating). Specify a valid user name
1908414-account on the remote system, but will not have access to network
1908415-If you omit a user name the process will run in the context of your
1908416-key, and typing Ctrl-C terminates the remote process.
1908417-Input is only passed to the remote system when you press the enter
1908418:quotation marks e.g. psexec \\marklap "c:\long name app.exe".
1908419-You can enclose applications that have spaces in their name with
1908420-                absolute paths on the target system).
1908421-     arguments  Arguments to pass (note that file paths must be
1908422-     program    Name of application to execute.
1908423-                in the file.
1908424:     @file      PsExec will execute the command on each of the computers listed
1908425-                command on all computers in the current domain.
1908426:                and if you specify a wildcard (\\*), PsExec runs the
1908427:                name PsExec runs the application on the local system, 
1908428-                computer or computers specified. If you omit the computer
1908429:     computer   Direct PsExec to run the application on the remote
1908430-                -background to run at low memory and I/O priority on Vista.
1908431-                -realtime to run the process at a different priority. Use
1908432-     -priority	Specifies -low, -belownormal, -abovenormal, -high or
1908433-     -x         Display the UI on the Winlogon secure desktop (local system
1908434-                only).
1908435-                remote computer).
1908436-     -w         Set the working directory of the process (relative to
1908437-     -v         Copy the specified file only if it has a higher version number
1908438-                or is new
1908439-v&Pj@
1908440-RWWP
1908441-ch(	
1908442-HtXHt
1908443-tGh,
1908444-VVj'V
1908445-QQW3
1908446-ct[!}
1908447-QQW3
1908448-ctO!}
1908449- SVW
--
1909036-th\J
1909037-thlJ
1909038-th|J
1909039-thLJ
1909040-GZ u
1909041-u Wj(
1909042-SVW3
1909043-H$N;
1909044-q CKMc
1909045-dhTl
1909046- f{X
1909047-Serv
1909048-Global\Ready1:  ESENT Performance Data Schema Version 40
1909049-{sk`
1909050-Vsk`
1909051-                          
1909052-                        
1909053-        
1909054-abcdefghijklmnopqrstuvwxyz
1909055-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1909056:]C:\WINDOWS\system32\xircom\PsExec.exe
1909057-                          
1909058-                        
1909059-        
1909060-abcdefghijklmnopqrstuvwxyz
1909061-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1909062-)IYh
1909063-PSWSSSh|)IY
1909064-uEjJh0)IYj
1909065-(IYPj
1909066-PSh?
1909067-SSSh
1909068-(IYh
1909069-u2jLh0(IYj
1909070-PSh?
1909071-SSSh
1909072-'IYh
1909073-'IYj
1909074-Shp'IY
1909075-Ph@7IY
1909076-Ph<'IY
--
1910393-Thawte Consulting1(0&
1910394-Certification Services Division1$0"
1910395-Thawte Personal Freemail CA1+0)
1910396-personal-freemail@thawte.com0
1910397-%u(t:B,c'
1910398-]nz|
1910399-l`q\
1910400-_#&	
1910401-RegisterApp
1910402-RtfToForeign32
1910403-ForeignToRtf32
1910404-IsFormatCorrect32
1910405-InitConverter32
1910406-WORDPAD
1910407-CEmbeddedItem
1910408-7IY%
1910409-RCRD(
1910410-EFGHIJKLMNOPQRSTUVWABCDEFGHI
1910411-ABCDEFGHIJKLMNOPQRSTUVWABCDEFGHI
1910412-FE2X
1910413:PsExec v1.98 - Execute processes remotely
1910414-Copyright (C) 2001-2010 Mark Russinovich
1910415-Sysinternals - www.sysinternals.com
1910416-H96v
1910417-86vLC6vDC6v8C6v
1910418-p)'r
1910419-p)'rt
1910420-t)'r
1910421-x)'rt
1910422-|)'r
1910423-5h)'rh
1910424-5d)'rh0a$r
1910425-5`)'rhHa$rh
1910426-5|)'r
1910427-5x)'rh
1910428-5t)'rh
1910429-5p)'rh
1910430-`$rh
1910431-\#'rSVW3
1910432-l)'r
1910433-a$rh
--
1911256-dutch-belgian
1911257-chinese-traditional
1911258-chinese-singapore
1911259-chinese-simplified
1911260-chinese-hongkong
1911261-chinese
1911262-canadian
1911263-belgian
1911264-australian
1911265-american-english
1911266-american english
1911267-american
1911268-Norwegian-Nynorsk
1911269-('8PW
1911270-700PP
1911271-`h`hhh
1911272-xppwpp
1911273-SunMonTueWedThuFriSat
1911274-JanFebMarAprMayJunJulAugSepOctNovDec
1911275-RSDS
1911276:c:\src\Pstools\psexec\EXE\Release\psexec.pdb
1911277-YYv 
1911278-A9F4Q
1911279-9_0u
1911280-9_,u	9_4
1911281-SSVW
1911282-SSVW
1911283-machine
1911284-force
1911285-command
1911286-write
1911287-notify
1911288-password
1911289-login
1911290-default
1911291-WSPStartupEx
1911292-MSAFD: SAN provider %ls (%ls) has a duplicate entry in 'TCP on SAN' key
1911293-SAN Provider %ls is not installed in winsock catalog!!!
1911294-Provider id %ld conflicts with provider id %ld for address %s
1911295-qudp
1911296-255.255.255.255
--
1913676-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1913677-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1913678-PROCESSOR_ARCHITECTURE=x86
1913679-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1913680-PROCESSOR_LEVEL=6
1913681-PROCESSOR_REVISION=2a07
1913682-ProgramFiles=C:\Program Files
1913683-SystemDrive=C:
1913684-SystemRoot=C:\WINDOWS
1913685-TEMP=C:\WINDOWS\TEMP
1913686-TMP=C:\WINDOWS\TEMP
1913687-USERPROFILE=C:\WINDOWS\system32\config\systemprofile
1913688-windir=C:\WINDOWS
1913689-%windir%\tracing
1913690-%windir%\tracing
1913691-Microsoft Sans Serif
1913692-Microsoft Sans Serif
1913693-Regular
1913694-Microsoft Sans Serif Regular
1913695-Service-0x0-3e7$\Default
1913696:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
1913697-G~ ?
1913698-G~H?
1913699-G~p?
1913700-G~PA
1913701-VVj	
1913702-9= .
1913703-chh"
1913704-chP"
1913705-ch4"
1913706-CertFreeCertificateChain
1913707-CertFindChainInStore
1913708-CryptUninstallDefaultContext
1913709-CryptInstallDefaultContext
1913710-crypt32
1913711-SslFreeCertificate
1913712-SslCrackCertificate
1913713-schannel
1913714-N<Wt
1913715-%s:%d
1913716-QQVW3
--
1917124-VERSION.dll
1917125-SETUPAPI.dll
1917126-SHLWAPI.dll
1917127-malloc
1917128-_XcptFilter
1917129-_^[]
1917130-_^[]
1917131-_^[]
1917132-u	!>
1917133-_^[]
1917134-u19E
1917135-wY^u
1917136-SVWu
1917137-_^[]
1917138-_^[]
1917139-, les garanties implicites de qualit
1917140- marchande, d'ad
1917141-quation 
1917142- un usage particulier et d'absence de contrefa
1917143-on sont exclues.
1917144:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
1917145- !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
1917146-f9^(tS
1917147-uA8]
1917148-6h,?
1917149-YYSV
1917150-3SVh!
1917151-}hl>
1917152-PhL>
1917153-uAh(>
1917154-9>v=S
1917155-8;>r
1917156-[_^]
1917157-PVWj
1917158-u<h 
1917159-QSVW
1917160-Vh`B
1917161-VhDA
1917162-YYt	
1917163-}_^[
1917164-SVh|
--
2067879->0!0	
2067880-1S0Q0,
2067881->0!0	
2067882-w!K0b
2067883-1T0R
2067884-1S0Q0,
2067885->0!0	
2067886-n%6i
2067887-1T0R
2067888- oZ  oZ  oZ( oZ( oZ0 oZ0 oZ8 oZ8 oZ@ oZ@ oZH oZH oZP oZP oZX oZX oZ` oZ` oZh oZh oZp oZp oZx oZx oZ
2067889-!oZ !oZ !oZ(!oZ(!oZ0!oZ0!oZ8!oZ8!oZ@!oZ@!oZH!oZH!oZP!oZP!oZX!oZX!oZ`!oZ`!oZh!oZh!oZp!oZp!oZx!oZx!oZ
2067890-"oZ "oZ "oZ("oZ("oZ0"oZ0"oZ8"oZ8"oZ@"oZ@"oZH"oZH"oZP"oZP"oZX"oZX"oZ`"oZ`"oZh"oZh"oZp"oZp"oZx"oZx"oZ
2067891-#oZ #oZ #oZ(#oZ(#oZ0#oZ0#oZ8#oZ8#oZ
2067892-dhTl
2067893- Volume in drive C has no label.
2067894- Volume Serial Number is 3CD4-8C81
2067895- Directory of C:\WINDOWS\system32\xircom
2067896-11/17/2012  01:35 PM    <DIR>          .
2067897-11/17/2012  01:35 PM    <DIR>          ..
2067898-11/17/2012  01:35 PM           303,104 gsecdump.exe
2067899:11/17/2012  01:35 PM           381,816 PsExec.exe
2067900-               2 File(s)        684,920 bytes
2067901-               2 Dir(s)   5,849,026,560 bytes free
2067902-C:\WINDOWS\system32\xircom>
2067903-`w@"
2067904-MEOW
2067905-!Nwp!Nw
2067906-X!Nwh
2067907-D!Nwh
2067908-4!Nw$!Nw<
2067909-uhD 
2067910-uVVVVh
2067911-Pt/j
2067912-QSVW3
2067913-WVh(,
2067914-VPPVh
2067915-uVVj
2067916-u>9}
2067917-St5WWWW
2067918-uWj@Y
2067919-Y_^[
--
2287849-dutch-belgian
2287850-chinese-traditional
2287851-chinese-singapore
2287852-chinese-simplified
2287853-chinese-hongkong
2287854-chinese
2287855-canadian
2287856-belgian
2287857-australian
2287858-american-english
2287859-american english
2287860-american
2287861-Norwegian-Nynorsk
2287862-('8PW
2287863-700PP
2287864-`h`hhh
2287865-xppwpp
2287866-SunMonTueWedThuFriSat
2287867-JanFebMarAprMayJunJulAugSepOctNovDec
2287868-RSDS
2287869:c:\src\Pstools\psexec\EXE\Release\psexec.pdb
2287870-A~@}B~
2287871-^E~Y
2287872-B~,}B~
2287873-}B~/
2287874-A~nCB~I
2287875-B~NJB~
2287876-B~4eF~6
2287877-_^[]
2287878-<tj(
2287879-[S<tdS<t
2287880-Y_^[
2287881-uOV3
2287882-<tf=
2287883-=tuDh
2287884-=th(
2287885-=th 
2287886-=tYY3
2287887-> rEWj
2287888-PSBASE.dll
2287889-FPasswordChangeNotify
--
2303576->_^[]
2303577-};FHt!V
2303578-YYtOj
2303579-;_^[]
2303580-t:Ht(Ht
2303581-F(SWP
2303582-}@Pj@
2303583-@Pj@
2303584-@Pj@
2303585-YY_^[
2303586-3h(W
2303587-ShhX
2303588-Sh0X
2303589-YYu"
2303590-PhhY
2303591-Ph$Z
2303592-td9}
2303593-F0Ph
2303594-9~0uK9~ t
2303595-9~$uAh
2303596:]C:\WINDOWS\system32\xircom\PsExec.exe
2303597-                          
2303598-                        
2303599-        
2303600-abcdefghijklmnopqrstuvwxyz
2303601-ABCDEFGHIJKLMNOPQRSTUVWXYZ
2303602-MEOW
2303603-QS[\
2303604-PESP
2303605-ncacn_np
2303606-\PIPE\lsass
2303607-\PIPE\lsass
2303608-\\GH0ST1
2303609-LMEMP
2303610-PESP~
2303611-ncalrpc
2303612-dhcpcsvc
2303613-dhcpcsvc
2303614-PESPz
2303615-ncalrpc
2303616-wzcsvc
--
2309623-OS=Windows_NT
2309624-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
2309625-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
2309626-PROCESSOR_ARCHITECTURE=x86
2309627-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
2309628-PROCESSOR_LEVEL=6
2309629-PROCESSOR_REVISION=2a07
2309630-ProgramFiles=C:\Program Files
2309631-PROMPT=$P$G
2309632-SystemDrive=C:
2309633-SystemRoot=C:\WINDOWS
2309634-TEMP=C:\WINDOWS\TEMP
2309635-TMP=C:\WINDOWS\TEMP
2309636-USERPROFILE=C:\Documents and Settings\NetworkService
2309637-windir=C:\WINDOWS
2309638-                          
2309639-                        
2309640-        
2309641-abcdefghijklmnopqrstuvwxyz
2309642-ABCDEFGHIJKLMNOPQRSTUVWXYZ
2309643:PsExec.exe
2309644-\\w2k3dc
2309645-cmd /c ipconfig
2309646-\accepteula
2309647-ALLUSERSPROFILE=C:\Documents and Settings\All Users
2309648-CommonProgramFiles=C:\Program Files\Common Files
2309649-COMPUTERNAME=GH0ST1
2309650-ComSpec=C:\WINDOWS\system32\cmd.exe
2309651-FP_NO_HOST_CHECK=NO
2309652-NUMBER_OF_PROCESSORS=1
2309653-OS=Windows_NT
2309654-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
2309655-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
2309656-PROCESSOR_ARCHITECTURE=x86
2309657-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
2309658-PROCESSOR_LEVEL=6
2309659-PROCESSOR_REVISION=2a07
2309660-ProgramFiles=C:\Program Files
2309661-PROMPT=$P$G
2309662-SystemDrive=C:
2309663-SystemRoot=C:\WINDOWS
--
2311252-F(+F$
2311253-C~ofF~
2311254-7C~L
2311255-7C~L
2311256-7C~L
2311257-7C~L
2311258-7C~/
2311259-7C~/
2311260-7C~L
2311261-bE~'
2311262-@)A~
2311263-T!A~
2311264-@1C~
2311265-0C~J8C~t
2311266-windows.hlp
2311267-2A~h2A~
2311268-TF~DUF~SVF~fUF~~VF~
2311269-VF~P
2311270-equires Windows NT/2000/XP/2003.
2311271-Use PsKill to terminate the remotely running program.
2311272:The version of the PsExec service running on the remote system is not compabible with this version of PsExec.
2311273:execute, not PsExec.
2311274:Error codes returned by PsExec are specific to the applications you
2311275-the password is transmitted in clear text to the remote system.
2311276-to network resources or to run in a different account. Note that
2311277-in the Domain\User syntax if the remote process requires access
2311278-resources (because it is impersonating). Specify a valid user name
2311279-account on the remote system, but will not have access to network
2311280-If you omit a user name the process will run in the context of your
2311281-key, and typing Ctrl-C terminates the remote process.
2311282-Input is only passed to the remote system when you press the enter
2311283:quotation marks e.g. psexec \\marklap "c:\long name app.exe".
2311284-You can enclose applications that have spaces in their name with
2311285-                absolute paths on the target system).
2311286-     arguments  Arguments to pass (note that file paths must be
2311287-     program    Name of application to execute.
2311288-                in the file.
2311289:     @file      PsExec will execute the command on each of the computers listed
2311290-                command on all computers in the current domain.
2311291:                and if you specify a wildcard (\\*), PsExec runs the
2311292:                name PsExec runs the application on the local system, 
2311293-                computer or computers specified. If you omit the computer
2311294:     computer   Direct PsExec to run the application on the remote
2311295-                -background to run at low memory and I/O priority on Vista.
2311296-                -realtime to run the process at a different priority. Use
2311297-     -priority	Specifies -low, -belownormal, -abovenormal, -high or
2311298-     -x         Display the UI on the Winlogon secure desktop (local system
2311299-                only).
2311300-                remote computer).
2311301-     -w         Set the working directory of the process (relative to
2311302-     -v         Copy the specified file only if it has a higher version number
2311303-                or is newf=%d, pConn=0x%x
2311304-No referred entry found
2311305-Found referred Entry. 0x%08x
2311306-CreateConnection:Dialasneeded is set
2311307-CreateConnection: dial in progress. hconn=0x%x, ref=%d, pConn=0x%x
2311308-CreateConnection: another dial is in progress. The process initiating  this dial is not longer alive . hconn=0x%x, ref=%d, pConn=0x%x
2311309-CreateConnection: Entry Already connected. hconn=0x%x, ref=%d, pConn=0x%x
2311310-CreateConnection: entry=%s, pbk=%s
2311311-SetDevConfig: port %d is unavailable
2311312-GetDevConfig: port %d is unavailable
2311313-GetConnectionStats: No Connected/Open Port found for 0x%08x
2311314-GetLinkStats: conn=0x%08x, SubEntry=%d is not connected/open
--
2311524-IpxcpRouterStarted: Entered
2311525-IpxcpRouterStopped: Entered
2311526-IpxcpBind: Entered
2311527-NetworkNumberHandler: SND REQ with net 0x%x
2311528-NetworkNumberHandler: RCV NAK with net 0x%x
2311529-NetworkNumberHandler: rcv req in re-negociation
2311530-NetworkNumberHandler: SND NAK to force request for net 0x%x
2311531-NodeNumberHandler: SND REQ with local node %.2x%.2x%.2x%.2x%.2x%.2x
2311532-NodeNumberHandler: RCV NAK accepted. New local node %.2x%.2x%.2x%.2x%.2x%.2x
2311533-NodeNumberHandler: RCV REQ with remote node %.2x%.2x%.2x%.2x%.2x%.2x, accepted
2311534-NodeNumberHandler: RCV REQ with non unique remote client node, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311535-NodeNumberHandler: RCV REQ with remote client node different, ACCEPT it
2311536-NodeNumberHandler: RCV REQ with remote client node but we force a specific node, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311537-NodeNumberHandler: RCV REQ with remote node 0x0, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311538-NodeNumberHandler: rcv req i
2311539-Microsoft Sans Serif
2311540-Microsoft Sans Serif
2311541-Regular
2311542-Microsoft Sans Serif Regular
2311543-Service-0x0-3e7$\Default
2311544:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
2311545-G~ ?
2311546-G~H?
2311547-G~p?
2311548-G~PA
2311549-_uY9
2311550-_uY9
2311551-fuSWjAY3
2311552-_uVh
2311553-u5hh
2311554-_SSW
2311555-t(hH
2311556-j j h
2311557-_uWh
2311558-_^[u
2311559-FL^t
2311560-NL;AHu
2311561-_uWj
2311562-_uWj
2311563-KH;AHu
2311564-VVVVVhiB
--
2315228-t!hX
2315229-YYVj
2315230-IY_^]
2315231-VVhh
2315232-t4h\
2315233-VVhh
2315234-u<!E
2315235-IYh`
2315236-IYP3
2315237-IYCS
2315238-YYhx
2315239-YY^[
2315240-IYh`
2315241-IYPh
2315242-IYh`
2315243-M, les garanties implicites de qualit
2315244- marchande, d'ad
2315245-quation 
2315246- un usage particulier et d'absence de contrefa
2315247-on sont exclues.
2315248:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
2315249- !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
2315250-t:f9]
2315251-t!Ht
2315252-------------------------------------------------------------------------------------
2315253-NDIS media status:      
2315254-Mac Address:            0x%012.12I64X
2315255-Location:               %S
2315256-Characteristics:        (0x%08X) %S
2315257-PnP instance ID:        %S
2315258-NetCfg instance ID:     %S
2315259-Valid NetCfg device:    
2315260-Lan capable:            
2315261-Device CM Problem:      (0x%08X) %S
2315262-Device CM Status:       (0x%08X) %S
2315263-Device name:            %S
2315264-SVW3
2315265-%S is already disconnected.
2315266-%S is already connected.
2315267-u2VV
2315268-wWj"
--
2318869-[u	:A#u
2318870-Q @^]
2318871-Pj S
2318872-SSSSS
2318873-_^[]
2318874-VW|[;
2318875-_^[]
2318876-VVVVV
2318877-j@j 
2318878-VVVVV
2318879-SSSSS
2318880-tGHt.Ht&
2318881-^SSSSS
2318882-;t0;
2318883-=|aB
2318884-VVVVV
2318885-t+9u
2318886-8VVVVV
2318887-t(9u
2318888-FE2X
2318889:PsExec v1.98 - Execute processes remotely
2318890-Copyright (C) 2001-2010 Mark Russinovich
2318891-Sysinternals - www.sysinternals.com
2318892-u#9u
2318893-RRRPVQ
2318894-RPPj
2318895-|{OwS
2318896-uv9u
2318897-dOwP
2318898-Vh|{OwP
2318899-``wS
2318900-|O9_ tJ
2318901-Nw^Wj
2318902-``wV
2318903-DFUFu
2318904-``wS
2318905-|]VWj
2318906-9F,t];
2318907-VWj,
2318908-VWj$
2318909-VWj0
--
2450001-NlMainLoop: Cannot NlRefDomClientSession
2450002-hx$Nt
2450003-jRY3
2450004-PtSh
2450005-ND;N\
2450006-;E$|
2450007-PSh2
2450008-QRPhlz
2450009-QQSV
2450010-t?h\
2450011-VVj*V
2450012-VVj<V
2450013-FTW3
2450014-dhTl
2450015- Volume in drive C has no label.
2450016- Volume Serial Number is 3CD4-8C81
2450017- Directory of C:\WINDOWS\system32\xircom
2450018-11/17/2012  01:35 PM    <DIR>          .
2450019-11/17/2012  01:35 PM    <DIR>          ..
2450020-11/17/2012  01:35 PM           303,104 gsecdump.exe
2450021:11/17/2012  01:35 PM           381,816 PsExec.exe
2450022-               2 File(s)        684,920 bytes
2450023-               2 Dir(s)   5,849,026,560 bytes free
2450024-C:\WINDOWS\system32\xircom>
2450025->0!0	
2450026-1T0R
2450027-1S0Q0,
2450028->0!0	
2450029-1T0R
2450030-1T0R
2450031-1[0Y04
2450032->0!0	
2450033-1S0Q0,
2450034->0!0	
2450035-1T0R
2450036-1S0Q0,
2450037->0!0	
2450038-1T0R
2450039-1S0Q0,
2450040->0!0	
2450041-1T0Rluna@lol:~/Downloads/volatility_2.6_lin64_standalone$ strings mem/memdump.bin | egrep -n20 -i -a "psexec"
16454-Vad 
16455-Irp (
16456-VadS
16457-Vadl
16458-Io  
16459-Ntfn
16460-Ntfi
16461-FSfm
16462-Ntfr
16463-Ntfn
16464-VadS
16465-Ntfr
16466-NtFs
16467-ReTa
16468-Vadl
16469-CcSc
16470-Ntfn
16471-Vad 
16472-Vad 
16473-Irp `
16474:PsExec.exe
16475-Cm  
16476-CPnp
16477-NtFs
16478-Vad 
16479-CcSc
16480-Wmip
16481-Ntfi
16482-NtFs
16483-MmCa
16484-MmCa@8
16485-FSfm
16486-Vad 
16487-CcSc
16488-VadS
16489-Hal 
16490-MmCi8
16491-Vad  o
16492-TCPC
16493-Ntfn`
16494-Nbtl
--
393480-PreShiftInfo0
393481-dbl2
393482-dbl3nk 
393483-dbl4
393484-dbl53
393485-dbl6
393486-Title
393487-dbl74
393488-dbl8
393489-PostShift0_
393490-PreShift0reShift
393491-dbl2
393492-dbl30
393493-hbin
393494-Shell Extensions
393495-Blocked
393496-Cached
393497-{FF393560-C2A7-11CF-BFF4-444553540000} {062E1261-A60E-11D0-82C2-00C04FD5AE38} 0x401
393498-"C:\Program Files\Windows Media Player\wmplayer.exe"
393499-C:\Program Files\Windows Media Player\wmplayer.exe
393500:PsExec
393501-h	}Z
393502-]	zX	zX
393503-~\	zX
393504-tR	}Z
393505-~\	wU
393506-k	|U
393507-_$~[$~[$~[#}Z#zX wU
393508-nL#wU(|Z'{Y$xV&wV'xW,
393509-^&|Z%yW"xV%yW#yW!uS
393510-mL"qP$sR%tS$sR"qP oN
393511-iI!lL$oO&qQ'rR
393512-fF"nN
393513-eF fG
393514-]>"hI fG
393515-dE fG fG"gL%jO&kP$iN eJ
393516-cH eJ#hM&kP#hM
393517-cH fH
393518-eF!gH fG
393519-eF fG"hI$jK#iJ
393520-yZ ~_
--
676199-38B5
676200-__InstanceOperationEvent
676201-ou((
676202-.iuH
676203-.iuH
676204-iu(P
676205-eld`
676206-h01u
676207-D' u@
676208-D73323810DAB2D362482D85928C165A\CR_A44D1BF95F0A41768D5546A4044C1625\C_35EC67A815B3C0868ACC23C410EA83D2
676209-D' u
676210-DEB2
676211-|/iu
676212-dhTl
676213- Volume in drive C has no label.
676214- Volume Serial Number is 3CD4-8C81
676215- Directory of C:\WINDOWS\system32\xircom
676216-11/17/2012  01:35 PM    <DIR>          .
676217-11/17/2012  01:35 PM    <DIR>          ..
676218-11/17/2012  01:35 PM           303,104 gsecdump.exe
676219:11/17/2012  01:35 PM           381,816 PsExec.exe
676220-               2 File(s)        684,920 bytes
676221-               2 Dir(s)   5,849,026,560 bytes free
676222-C:\WINDOWS\system32\xircom>
676223-__SystemClass
676224-__IndicationRelated
676225-abstract
676226-__IndicationRelated
676227-__SystemClass
676228-__EventFilter
676229-CreatorSID
676230-uint8
676231-EventAccess
676232-string
676233-EventNamespace
676234-string
676235-Name
676236-string
676237-Query
676238-string
676239-QueryLanguage
--
769616-ObSq
769617-LNKFILE
769618-Ntfo\
769619-ObSq
769620-CMVIH~
769621-Gla4
769622-Gh05
769623-{93F2F68C-1D1B-11D3-A30E-00C04F79ABD1}l
769624-Gla@h
769625-CMVa
769626-.ASMrentId
769627-{DC971EE5-44EB-4FE4-AE2E-B91490411BFC}
769628-CMVI
769629-CMVa
769630-EnableConsoleTracingP=
769631-ObSq
769632-AuDA
769633-AudC
769634-ObSq
769635-CMVI`
769636:PSEXEC.EXE
769637-ObNmP
769638-A672-0
769639-CMVaP
769640-CMVa
769641-Description
769642-FSim
769643-IoNm\
769644-92-116680F0CEDA}}
769645-AudLH
769646-ObSq
769647-CMVI
769648-ObHd
769649-MmSm
769650-CMDa
769651-CMVa
769652-Ntfc	
769653-CMDa
769654-{C3480414-
769655-.SBR2}0
769656-CMVI
--
809032-CMVIX
809033-CMVa
809034-DeDeviceDesc
809035-20yk
809036-CMDa
809037-CMDa
809038-Service
809039-CMDa
809040-CMVa
809041-PreferExecuteOnMismatch
809042-AtmA
809043-CMDa
809044-DisplayString
809045-CMVI
809046-NtFsPG
809047-ObSq
809048-AudD\
809049-ObSqH`
809050-CMVa
809051-.%Tl
809052:PSEXECl
809053-Ustm
809054-SrSC<
809055-Usqm
809056-MmSm
809057-Gh05
809058-&)&&
809059-=@//
809060-CMVI
809061-CMVa
809062-cFormatTags
809063-CMVa
809064-cFormatTags
809065-CMVa
809066-cFormatTags
809067-AUDIOCOMPRESSIONMANAGER
809068-Gfnt
809069-Ph(`
809070-IpDnsSuffix
809071-IpDnsFlags
809072-IpWins2
--
1009484-Identifier
1009485-AtmA0M
1009486-CMDa
1009487-sLongDate
1009488-NtFI
1009489-Gla8
1009490-Ntf0
1009491-CMVa
1009492-CMVa
1009493-Class
1009494-CMVa
1009495-DeviceDescA
1009496-SeAcP
1009497-RxFc(
1009498-#2222
1009499-CMDa
1009500-uiDlllumnHi
1009501-,-6412	
1009502-MmSt
1009503-NtFsI'
1009504:PsExec v1.98 - Execute processes r
1009505-ObSq
1009506-CMVa
1009507-*ImagePathB
1009508-Gfnt 
1009509-SeAc
1009510-CMVa
1009511-Type
1009512-ObSq
1009513-CMVa
1009514-yPSupportedNameSpaces
1009515-Pp  
1009516-NtFA@w
1009517-CMVa
1009518-Count
1009519-CMVI
1009520-Gfnt*
1009521-j\hH
1009522-PWWW
1009523-9HTt
1009524-9HTt
--
1347836-SendMessageW
1347837-ShowWindow
1347838-GetWindowLongW
1347839-SetDlgItemTextW
1347840-CheckDlgButton
1347841-SendDlgItemMessageW
1347842-GetParent
1347843-IsDlgButtonChecked
1347844-WinHelpW
1347845-GetWindow
1347846-PostMessageW
1347847-RSDS$
1347848-setupapi.pdb
1347849-dhTl
1347850- Volume in drive C has no label.
1347851- Volume Serial Number is 3CD4-8C81
1347852- Directory of C:\WINDOWS\system32\xircom
1347853-11/17/2012  01:35 PM    <DIR>          .
1347854-11/17/2012  01:35 PM    <DIR>          ..
1347855-11/17/2012  01:35 PM           303,104 gsecdump.exe
1347856:11/17/2012  01:35 PM           381,816 PsExec.exe
1347857-               2 File(s)        684,920 bytes
1347858-               2 Dir(s)   5,849,026,560 bytes free
1347859-C:\WINDOWS\system32\xircom>
1347860-Qpgn
1347861-/h<P+
1347862-'h<P
1347863-*Tp3.;P
1347864-*Sp3.
1347865-'vi;
1347866-A~9|B~
1347867-B~nCB~
1347868-B~6xB~4
1347869-A~r C~}mE~
1347870-UnRegisterTypeLib
1347871-ATL:%8.8X
1347872-Can not run Unicode version of ATL.DLL on Windows 95.
1347873-Please install the correct version.
1347874-@Qm6t
1347875-vInterlockedCompareExchange
1347876-InterlockedPopEntrySList
--
1452171-ObSq
1452172-LNKFILE
1452173-Ntfo\
1452174-ObSq
1452175-CMVIH~
1452176-Gla4
1452177-Gh05
1452178-{93F2F68C-1D1B-11D3-A30E-00C04F79ABD1}l
1452179-Gla@h
1452180-CMVa
1452181-.ASMrentId
1452182-{DC971EE5-44EB-4FE4-AE2E-B91490411BFC}
1452183-CMVI
1452184-CMVa
1452185-EnableConsoleTracingP=
1452186-ObSq
1452187-AuDA
1452188-AudC
1452189-ObSq
1452190-CMVI`
1452191:PSEXEC.EXE
1452192-ObNmP
1452193-A672-0
1452194-CMVaP
1452195-CMVa
1452196-Description
1452197-FSim
1452198-IoNm\
1452199-92-116680F0CEDA}}
1452200-AudLH
1452201-ObSq
1452202-CMVI
1452203-ObHd
1452204-MmSm
1452205-CMDa
1452206-CMVa
1452207-Ntfc	
1452208-CMDa
1452209-{C3480414-
1452210-.SBR2}0
1452211-CMVI
--
1504687-CMVIX
1504688-CMVa
1504689-DeDeviceDesc
1504690-20yk
1504691-CMDa
1504692-CMDa
1504693-Service
1504694-CMDa
1504695-CMVa
1504696-PreferExecuteOnMismatch
1504697-AtmA
1504698-CMDa
1504699-DisplayString
1504700-CMVI
1504701-NtFsPG
1504702-ObSq
1504703-AudD\
1504704-ObSqH`
1504705-CMVa
1504706-.%Tl
1504707:PSEXECl
1504708-Ustm
1504709-SrSC<
1504710-Usqm
1504711-MmSm
1504712-Gh05
1504713-&)&&
1504714-=@//
1504715-CMVI
1504716-CMVa
1504717-cFormatTags
1504718-CMVa
1504719-cFormatTags
1504720-CMVa
1504721-cFormatTags
1504722-AUDIOCOMPRESSIONMANAGER
1504723-Gfnt
1504724-1uPh
1504725-01uj
1504726-C;^H|
1504727-1uPh
--
1581398-NotInsertableD
1581399-{8C3ADF99-CCFE-11d2-AD10-00C04F72DD47}h4
1581400-tAppID
1581401-LocalServer32
1581402-ft_0&
1581403-{8C4EB103-516F-11D1-A6DF-006097C4E476}
1581404-er Name            Remark
1581405--------------------------------------------------------------------------------
1581406-\\2K3DC                                                                        
1581407-\\GH0ST1                                                                       
1581408-The command completed successfully.
1581409-C:\WINDOWS\system32\xircom>:
1581410-59Yh
1581411-8D*`3
1581412- Volume in drive C has no label.
1581413- Volume Serial Number is 3CD4-8C81
1581414- Directory of C:\WINDOWS\system32\xircom
1581415-11/17/2012  01:35 PM    <DIR>          .
1581416-11/17/2012  01:35 PM    <DIR>          ..
1581417-11/17/2012  01:35 PM           303,104 gsecdump.exe
1581418:11/17/2012  01:35 PM           381,816 PsExec.exe
1581419-               2 File(s)        684,920 bytes
1581420-               2 Dir(s)   5,849,026,560 bytes free
1581421-C:\WINDOWS\system32\xircom>
1581422- DxK-
1581423-eMmz
1581424- Volume in drive C has no label.
1581425- Volume Serial Number is 3CD4-8C81
1581426- Directory of C:\WINDOWS\system32\xircom
1581427-11/17/2012  01:37 PM    <DIR>          .
1581428-11/17/2012  01:37 PM    <DIR>          ..
1581429-11/17/2012  01:37 PM             4,947 berry.gif
1581430-11/17/2012  01:35 PM           303,104 gsecdump.exe
1581431:11/17/2012  01:35 PM           381,816 PsExec.exe
1581432-               3 File(s)        689,867 bytes
1581433-               2 Dir(s)   5,849,042,944 bytes free
1581434-C:\WINDOWS\system32\xircom>n
1581435-=!mg
1581436--46W
1581437-(/}p m
1581438-t5dS
1581439-l5wI
1581440-Xw){
1581441-HJ-*
1581442-edH/NMN)
1581443-2,`a
1581444-C:\WINDOWS\system32>V
1581445-+:u	
1581446-KD!t
1581447-ilX(
1581448-             6,656 routetab.dll
1581449-08/29/2002  07:00 AM            22,016 rpcns4.dll
1581450-04/14/2008  05:42 AM           584,704 rpcrt4.dll
1581451-04/14/2008  05:42 AM           399,360 rpcss.dll
--
1729401-Identifier
1729402-AtmA0M
1729403-CMDa
1729404-sLongDate
1729405-NtFI
1729406-Gla8
1729407-Ntf0
1729408-CMVa
1729409-CMVa
1729410-Class
1729411-CMVa
1729412-DeviceDescA
1729413-SeAcP
1729414-RxFc(
1729415-#2222
1729416-CMDa
1729417-uiDlllumnHi
1729418-,-6412	
1729419-MmSt
1729420-NtFsI'
1729421:PsExec v1.98 - Execute processes r
1729422-ObSq
1729423-CMVa
1729424-*ImagePathB
1729425-Gfnt 
1729426-SeAc
1729427-CMVa
1729428-Type
1729429-ObSq
1729430-CMVa
1729431-yPSupportedNameSpaces
1729432-Pp  
1729433-NtFA@w
1729434-CMVa
1729435-Count
1729436-CMVI
1729437-Gfnt*
1729438-Ph\b
1729439-_[^]
1729440-HtCHt1Ht
1729441-t*Ht
--
1903448-OS=Windows_NT
1903449-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1903450-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1903451-PROCESSOR_ARCHITECTURE=x86
1903452-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1903453-PROCESSOR_LEVEL=6
1903454-PROCESSOR_REVISION=2a07
1903455-ProgramFiles=C:\Program Files
1903456-PROMPT=$P$G
1903457-SystemDrive=C:
1903458-SystemRoot=C:\WINDOWS
1903459-TEMP=C:\WINDOWS\TEMP
1903460-TMP=C:\WINDOWS\TEMP
1903461-USERPROFILE=C:\Documents and Settings\NetworkService
1903462-windir=C:\WINDOWS
1903463-                          
1903464-                        
1903465-        
1903466-abcdefghijklmnopqrstuvwxyz
1903467-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1903468:PsExec.exe
1903469-\\w2k3dc
1903470-cmd /c ipconfig
1903471-\accepteula
1903472-ALLUSERSPROFILE=C:\Documents and Settings\All Users
1903473-CommonProgramFiles=C:\Program Files\Common Files
1903474-COMPUTERNAME=GH0ST1
1903475-ComSpec=C:\WINDOWS\system32\cmd.exe
1903476-FP_NO_HOST_CHECK=NO
1903477-NUMBER_OF_PROCESSORS=1
1903478-OS=Windows_NT
1903479-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1903480-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1903481-PROCESSOR_ARCHITECTURE=x86
1903482-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1903483-PROCESSOR_LEVEL=6
1903484-PROCESSOR_REVISION=2a07
1903485-ProgramFiles=C:\Program Files
1903486-PROMPT=$P$G
1903487-SystemDrive=C:
1903488-SystemRoot=C:\WINDOWS
--
1908387-SamIFree_SAMPR_ENUMERATION_BUFFER
1908388-SamIFree_SAMPR_GET_GROUPS_BUFFER
1908389-SamIFree_SAMPR_GET_MEMBERS_BUFFER
1908390-SamIFree_SAMPR_GROUP_INFO_BUFFER
1908391-SamIFree_SAMPR_PSID_ARRAY
1908392-SamIFree_SAMPR_RETURNED_USTRING_ARRAY
1908393-SamIFree_SAMPR_SR_SECURITY_DESCRIPTOR
1908394-SamIFree_SAMPR_ULONG_ARRAY
1908395-SamIFree_SAMPR_USER_INFO_BUFFER
1908396-SamIFree_UserInternal6Information
1908397-SamIGCLookupNames
1908398-SamIGCLookupSids
1908399-SamIGetAliasMembership
1908400-SamIGetBootKeyInformation
1908401-SamIGetDefaultAdministratorName
1908402-SamIGetFixedAttributes
1908403-SamIGetInterdomainTrustAccountPasswordsForUpgrade
1908404-SamIGetPrivateData
1908405-equires Windows NT/2000/XP/2003.
1908406-Use PsKill to terminate the remotely running program.
1908407:The version of the PsExec service running on the remote system is not compabible with this version of PsExec.
1908408:execute, not PsExec.
1908409:Error codes returned by PsExec are specific to the applications you
1908410-the password is transmitted in clear text to the remote system.
1908411-to network resources or to run in a different account. Note that
1908412-in the Domain\User syntax if the remote process requires access
1908413-resources (because it is impersonating). Specify a valid user name
1908414-account on the remote system, but will not have access to network
1908415-If you omit a user name the process will run in the context of your
1908416-key, and typing Ctrl-C terminates the remote process.
1908417-Input is only passed to the remote system when you press the enter
1908418:quotation marks e.g. psexec \\marklap "c:\long name app.exe".
1908419-You can enclose applications that have spaces in their name with
1908420-                absolute paths on the target system).
1908421-     arguments  Arguments to pass (note that file paths must be
1908422-     program    Name of application to execute.
1908423-                in the file.
1908424:     @file      PsExec will execute the command on each of the computers listed
1908425-                command on all computers in the current domain.
1908426:                and if you specify a wildcard (\\*), PsExec runs the
1908427:                name PsExec runs the application on the local system, 
1908428-                computer or computers specified. If you omit the computer
1908429:     computer   Direct PsExec to run the application on the remote
1908430-                -background to run at low memory and I/O priority on Vista.
1908431-                -realtime to run the process at a different priority. Use
1908432-     -priority	Specifies -low, -belownormal, -abovenormal, -high or
1908433-     -x         Display the UI on the Winlogon secure desktop (local system
1908434-                only).
1908435-                remote computer).
1908436-     -w         Set the working directory of the process (relative to
1908437-     -v         Copy the specified file only if it has a higher version number
1908438-                or is new
1908439-v&Pj@
1908440-RWWP
1908441-ch(	
1908442-HtXHt
1908443-tGh,
1908444-VVj'V
1908445-QQW3
1908446-ct[!}
1908447-QQW3
1908448-ctO!}
1908449- SVW
--
1909036-th\J
1909037-thlJ
1909038-th|J
1909039-thLJ
1909040-GZ u
1909041-u Wj(
1909042-SVW3
1909043-H$N;
1909044-q CKMc
1909045-dhTl
1909046- f{X
1909047-Serv
1909048-Global\Ready1:  ESENT Performance Data Schema Version 40
1909049-{sk`
1909050-Vsk`
1909051-                          
1909052-                        
1909053-        
1909054-abcdefghijklmnopqrstuvwxyz
1909055-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1909056:]C:\WINDOWS\system32\xircom\PsExec.exe
1909057-                          
1909058-                        
1909059-        
1909060-abcdefghijklmnopqrstuvwxyz
1909061-ABCDEFGHIJKLMNOPQRSTUVWXYZ
1909062-)IYh
1909063-PSWSSSh|)IY
1909064-uEjJh0)IYj
1909065-(IYPj
1909066-PSh?
1909067-SSSh
1909068-(IYh
1909069-u2jLh0(IYj
1909070-PSh?
1909071-SSSh
1909072-'IYh
1909073-'IYj
1909074-Shp'IY
1909075-Ph@7IY
1909076-Ph<'IY
--
1910393-Thawte Consulting1(0&
1910394-Certification Services Division1$0"
1910395-Thawte Personal Freemail CA1+0)
1910396-personal-freemail@thawte.com0
1910397-%u(t:B,c'
1910398-]nz|
1910399-l`q\
1910400-_#&	
1910401-RegisterApp
1910402-RtfToForeign32
1910403-ForeignToRtf32
1910404-IsFormatCorrect32
1910405-InitConverter32
1910406-WORDPAD
1910407-CEmbeddedItem
1910408-7IY%
1910409-RCRD(
1910410-EFGHIJKLMNOPQRSTUVWABCDEFGHI
1910411-ABCDEFGHIJKLMNOPQRSTUVWABCDEFGHI
1910412-FE2X
1910413:PsExec v1.98 - Execute processes remotely
1910414-Copyright (C) 2001-2010 Mark Russinovich
1910415-Sysinternals - www.sysinternals.com
1910416-H96v
1910417-86vLC6vDC6v8C6v
1910418-p)'r
1910419-p)'rt
1910420-t)'r
1910421-x)'rt
1910422-|)'r
1910423-5h)'rh
1910424-5d)'rh0a$r
1910425-5`)'rhHa$rh
1910426-5|)'r
1910427-5x)'rh
1910428-5t)'rh
1910429-5p)'rh
1910430-`$rh
1910431-\#'rSVW3
1910432-l)'r
1910433-a$rh
--
1911256-dutch-belgian
1911257-chinese-traditional
1911258-chinese-singapore
1911259-chinese-simplified
1911260-chinese-hongkong
1911261-chinese
1911262-canadian
1911263-belgian
1911264-australian
1911265-american-english
1911266-american english
1911267-american
1911268-Norwegian-Nynorsk
1911269-('8PW
1911270-700PP
1911271-`h`hhh
1911272-xppwpp
1911273-SunMonTueWedThuFriSat
1911274-JanFebMarAprMayJunJulAugSepOctNovDec
1911275-RSDS
1911276:c:\src\Pstools\psexec\EXE\Release\psexec.pdb
1911277-YYv 
1911278-A9F4Q
1911279-9_0u
1911280-9_,u	9_4
1911281-SSVW
1911282-SSVW
1911283-machine
1911284-force
1911285-command
1911286-write
1911287-notify
1911288-password
1911289-login
1911290-default
1911291-WSPStartupEx
1911292-MSAFD: SAN provider %ls (%ls) has a duplicate entry in 'TCP on SAN' key
1911293-SAN Provider %ls is not installed in winsock catalog!!!
1911294-Provider id %ld conflicts with provider id %ld for address %s
1911295-qudp
1911296-255.255.255.255
--
1913676-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
1913677-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
1913678-PROCESSOR_ARCHITECTURE=x86
1913679-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
1913680-PROCESSOR_LEVEL=6
1913681-PROCESSOR_REVISION=2a07
1913682-ProgramFiles=C:\Program Files
1913683-SystemDrive=C:
1913684-SystemRoot=C:\WINDOWS
1913685-TEMP=C:\WINDOWS\TEMP
1913686-TMP=C:\WINDOWS\TEMP
1913687-USERPROFILE=C:\WINDOWS\system32\config\systemprofile
1913688-windir=C:\WINDOWS
1913689-%windir%\tracing
1913690-%windir%\tracing
1913691-Microsoft Sans Serif
1913692-Microsoft Sans Serif
1913693-Regular
1913694-Microsoft Sans Serif Regular
1913695-Service-0x0-3e7$\Default
1913696:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
1913697-G~ ?
1913698-G~H?
1913699-G~p?
1913700-G~PA
1913701-VVj	
1913702-9= .
1913703-chh"
1913704-chP"
1913705-ch4"
1913706-CertFreeCertificateChain
1913707-CertFindChainInStore
1913708-CryptUninstallDefaultContext
1913709-CryptInstallDefaultContext
1913710-crypt32
1913711-SslFreeCertificate
1913712-SslCrackCertificate
1913713-schannel
1913714-N<Wt
1913715-%s:%d
1913716-QQVW3
--
1917124-VERSION.dll
1917125-SETUPAPI.dll
1917126-SHLWAPI.dll
1917127-malloc
1917128-_XcptFilter
1917129-_^[]
1917130-_^[]
1917131-_^[]
1917132-u	!>
1917133-_^[]
1917134-u19E
1917135-wY^u
1917136-SVWu
1917137-_^[]
1917138-_^[]
1917139-, les garanties implicites de qualit
1917140- marchande, d'ad
1917141-quation 
1917142- un usage particulier et d'absence de contrefa
1917143-on sont exclues.
1917144:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
1917145- !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
1917146-f9^(tS
1917147-uA8]
1917148-6h,?
1917149-YYSV
1917150-3SVh!
1917151-}hl>
1917152-PhL>
1917153-uAh(>
1917154-9>v=S
1917155-8;>r
1917156-[_^]
1917157-PVWj
1917158-u<h 
1917159-QSVW
1917160-Vh`B
1917161-VhDA
1917162-YYt	
1917163-}_^[
1917164-SVh|
--
2067879->0!0	
2067880-1S0Q0,
2067881->0!0	
2067882-w!K0b
2067883-1T0R
2067884-1S0Q0,
2067885->0!0	
2067886-n%6i
2067887-1T0R
2067888- oZ  oZ  oZ( oZ( oZ0 oZ0 oZ8 oZ8 oZ@ oZ@ oZH oZH oZP oZP oZX oZX oZ` oZ` oZh oZh oZp oZp oZx oZx oZ
2067889-!oZ !oZ !oZ(!oZ(!oZ0!oZ0!oZ8!oZ8!oZ@!oZ@!oZH!oZH!oZP!oZP!oZX!oZX!oZ`!oZ`!oZh!oZh!oZp!oZp!oZx!oZx!oZ
2067890-"oZ "oZ "oZ("oZ("oZ0"oZ0"oZ8"oZ8"oZ@"oZ@"oZH"oZH"oZP"oZP"oZX"oZX"oZ`"oZ`"oZh"oZh"oZp"oZp"oZx"oZx"oZ
2067891-#oZ #oZ #oZ(#oZ(#oZ0#oZ0#oZ8#oZ8#oZ
2067892-dhTl
2067893- Volume in drive C has no label.
2067894- Volume Serial Number is 3CD4-8C81
2067895- Directory of C:\WINDOWS\system32\xircom
2067896-11/17/2012  01:35 PM    <DIR>          .
2067897-11/17/2012  01:35 PM    <DIR>          ..
2067898-11/17/2012  01:35 PM           303,104 gsecdump.exe
2067899:11/17/2012  01:35 PM           381,816 PsExec.exe
2067900-               2 File(s)        684,920 bytes
2067901-               2 Dir(s)   5,849,026,560 bytes free
2067902-C:\WINDOWS\system32\xircom>
2067903-`w@"
2067904-MEOW
2067905-!Nwp!Nw
2067906-X!Nwh
2067907-D!Nwh
2067908-4!Nw$!Nw<
2067909-uhD 
2067910-uVVVVh
2067911-Pt/j
2067912-QSVW3
2067913-WVh(,
2067914-VPPVh
2067915-uVVj
2067916-u>9}
2067917-St5WWWW
2067918-uWj@Y
2067919-Y_^[
--
2287849-dutch-belgian
2287850-chinese-traditional
2287851-chinese-singapore
2287852-chinese-simplified
2287853-chinese-hongkong
2287854-chinese
2287855-canadian
2287856-belgian
2287857-australian
2287858-american-english
2287859-american english
2287860-american
2287861-Norwegian-Nynorsk
2287862-('8PW
2287863-700PP
2287864-`h`hhh
2287865-xppwpp
2287866-SunMonTueWedThuFriSat
2287867-JanFebMarAprMayJunJulAugSepOctNovDec
2287868-RSDS
2287869:c:\src\Pstools\psexec\EXE\Release\psexec.pdb
2287870-A~@}B~
2287871-^E~Y
2287872-B~,}B~
2287873-}B~/
2287874-A~nCB~I
2287875-B~NJB~
2287876-B~4eF~6
2287877-_^[]
2287878-<tj(
2287879-[S<tdS<t
2287880-Y_^[
2287881-uOV3
2287882-<tf=
2287883-=tuDh
2287884-=th(
2287885-=th 
2287886-=tYY3
2287887-> rEWj
2287888-PSBASE.dll
2287889-FPasswordChangeNotify
--
2303576->_^[]
2303577-};FHt!V
2303578-YYtOj
2303579-;_^[]
2303580-t:Ht(Ht
2303581-F(SWP
2303582-}@Pj@
2303583-@Pj@
2303584-@Pj@
2303585-YY_^[
2303586-3h(W
2303587-ShhX
2303588-Sh0X
2303589-YYu"
2303590-PhhY
2303591-Ph$Z
2303592-td9}
2303593-F0Ph
2303594-9~0uK9~ t
2303595-9~$uAh
2303596:]C:\WINDOWS\system32\xircom\PsExec.exe
2303597-                          
2303598-                        
2303599-        
2303600-abcdefghijklmnopqrstuvwxyz
2303601-ABCDEFGHIJKLMNOPQRSTUVWXYZ
2303602-MEOW
2303603-QS[\
2303604-PESP
2303605-ncacn_np
2303606-\PIPE\lsass
2303607-\PIPE\lsass
2303608-\\GH0ST1
2303609-LMEMP
2303610-PESP~
2303611-ncalrpc
2303612-dhcpcsvc
2303613-dhcpcsvc
2303614-PESPz
2303615-ncalrpc
2303616-wzcsvc
--
2309623-OS=Windows_NT
2309624-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
2309625-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
2309626-PROCESSOR_ARCHITECTURE=x86
2309627-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
2309628-PROCESSOR_LEVEL=6
2309629-PROCESSOR_REVISION=2a07
2309630-ProgramFiles=C:\Program Files
2309631-PROMPT=$P$G
2309632-SystemDrive=C:
2309633-SystemRoot=C:\WINDOWS
2309634-TEMP=C:\WINDOWS\TEMP
2309635-TMP=C:\WINDOWS\TEMP
2309636-USERPROFILE=C:\Documents and Settings\NetworkService
2309637-windir=C:\WINDOWS
2309638-                          
2309639-                        
2309640-        
2309641-abcdefghijklmnopqrstuvwxyz
2309642-ABCDEFGHIJKLMNOPQRSTUVWXYZ
2309643:PsExec.exe
2309644-\\w2k3dc
2309645-cmd /c ipconfig
2309646-\accepteula
2309647-ALLUSERSPROFILE=C:\Documents and Settings\All Users
2309648-CommonProgramFiles=C:\Program Files\Common Files
2309649-COMPUTERNAME=GH0ST1
2309650-ComSpec=C:\WINDOWS\system32\cmd.exe
2309651-FP_NO_HOST_CHECK=NO
2309652-NUMBER_OF_PROCESSORS=1
2309653-OS=Windows_NT
2309654-Path=C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
2309655-PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
2309656-PROCESSOR_ARCHITECTURE=x86
2309657-PROCESSOR_IDENTIFIER=x86 Family 6 Model 42 Stepping 7, GenuineIntel
2309658-PROCESSOR_LEVEL=6
2309659-PROCESSOR_REVISION=2a07
2309660-ProgramFiles=C:\Program Files
2309661-PROMPT=$P$G
2309662-SystemDrive=C:
2309663-SystemRoot=C:\WINDOWS
--
2311252-F(+F$
2311253-C~ofF~
2311254-7C~L
2311255-7C~L
2311256-7C~L
2311257-7C~L
2311258-7C~/
2311259-7C~/
2311260-7C~L
2311261-bE~'
2311262-@)A~
2311263-T!A~
2311264-@1C~
2311265-0C~J8C~t
2311266-windows.hlp
2311267-2A~h2A~
2311268-TF~DUF~SVF~fUF~~VF~
2311269-VF~P
2311270-equires Windows NT/2000/XP/2003.
2311271-Use PsKill to terminate the remotely running program.
2311272:The version of the PsExec service running on the remote system is not compabible with this version of PsExec.
2311273:execute, not PsExec.
2311274:Error codes returned by PsExec are specific to the applications you
2311275-the password is transmitted in clear text to the remote system.
2311276-to network resources or to run in a different account. Note that
2311277-in the Domain\User syntax if the remote process requires access
2311278-resources (because it is impersonating). Specify a valid user name
2311279-account on the remote system, but will not have access to network
2311280-If you omit a user name the process will run in the context of your
2311281-key, and typing Ctrl-C terminates the remote process.
2311282-Input is only passed to the remote system when you press the enter
2311283:quotation marks e.g. psexec \\marklap "c:\long name app.exe".
2311284-You can enclose applications that have spaces in their name with
2311285-                absolute paths on the target system).
2311286-     arguments  Arguments to pass (note that file paths must be
2311287-     program    Name of application to execute.
2311288-                in the file.
2311289:     @file      PsExec will execute the command on each of the computers listed
2311290-                command on all computers in the current domain.
2311291:                and if you specify a wildcard (\\*), PsExec runs the
2311292:                name PsExec runs the application on the local system, 
2311293-                computer or computers specified. If you omit the computer
2311294:     computer   Direct PsExec to run the application on the remote
2311295-                -background to run at low memory and I/O priority on Vista.
2311296-                -realtime to run the process at a different priority. Use
2311297-     -priority	Specifies -low, -belownormal, -abovenormal, -high or
2311298-     -x         Display the UI on the Winlogon secure desktop (local system
2311299-                only).
2311300-                remote computer).
2311301-     -w         Set the working directory of the process (relative to
2311302-     -v         Copy the specified file only if it has a higher version number
2311303-                or is newf=%d, pConn=0x%x
2311304-No referred entry found
2311305-Found referred Entry. 0x%08x
2311306-CreateConnection:Dialasneeded is set
2311307-CreateConnection: dial in progress. hconn=0x%x, ref=%d, pConn=0x%x
2311308-CreateConnection: another dial is in progress. The process initiating  this dial is not longer alive . hconn=0x%x, ref=%d, pConn=0x%x
2311309-CreateConnection: Entry Already connected. hconn=0x%x, ref=%d, pConn=0x%x
2311310-CreateConnection: entry=%s, pbk=%s
2311311-SetDevConfig: port %d is unavailable
2311312-GetDevConfig: port %d is unavailable
2311313-GetConnectionStats: No Connected/Open Port found for 0x%08x
2311314-GetLinkStats: conn=0x%08x, SubEntry=%d is not connected/open
--
2311524-IpxcpRouterStarted: Entered
2311525-IpxcpRouterStopped: Entered
2311526-IpxcpBind: Entered
2311527-NetworkNumberHandler: SND REQ with net 0x%x
2311528-NetworkNumberHandler: RCV NAK with net 0x%x
2311529-NetworkNumberHandler: rcv req in re-negociation
2311530-NetworkNumberHandler: SND NAK to force request for net 0x%x
2311531-NodeNumberHandler: SND REQ with local node %.2x%.2x%.2x%.2x%.2x%.2x
2311532-NodeNumberHandler: RCV NAK accepted. New local node %.2x%.2x%.2x%.2x%.2x%.2x
2311533-NodeNumberHandler: RCV REQ with remote node %.2x%.2x%.2x%.2x%.2x%.2x, accepted
2311534-NodeNumberHandler: RCV REQ with non unique remote client node, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311535-NodeNumberHandler: RCV REQ with remote client node different, ACCEPT it
2311536-NodeNumberHandler: RCV REQ with remote client node but we force a specific node, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311537-NodeNumberHandler: RCV REQ with remote node 0x0, snd NAK with remote node %.2x%.2x%.2x%.2x%.2x%.2x
2311538-NodeNumberHandler: rcv req i
2311539-Microsoft Sans Serif
2311540-Microsoft Sans Serif
2311541-Regular
2311542-Microsoft Sans Serif Regular
2311543-Service-0x0-3e7$\Default
2311544:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
2311545-G~ ?
2311546-G~H?
2311547-G~p?
2311548-G~PA
2311549-_uY9
2311550-_uY9
2311551-fuSWjAY3
2311552-_uVh
2311553-u5hh
2311554-_SSW
2311555-t(hH
2311556-j j h
2311557-_uWh
2311558-_^[u
2311559-FL^t
2311560-NL;AHu
2311561-_uWj
2311562-_uWj
2311563-KH;AHu
2311564-VVVVVhiB
--
2315228-t!hX
2315229-YYVj
2315230-IY_^]
2315231-VVhh
2315232-t4h\
2315233-VVhh
2315234-u<!E
2315235-IYh`
2315236-IYP3
2315237-IYCS
2315238-YYhx
2315239-YY^[
2315240-IYh`
2315241-IYPh
2315242-IYh`
2315243-M, les garanties implicites de qualit
2315244- marchande, d'ad
2315245-quation 
2315246- un usage particulier et d'absence de contrefa
2315247-on sont exclues.
2315248:PsExec.exe \\w2k3dc "cmd /c ipconfig"  \accepteula
2315249- !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
2315250-t:f9]
2315251-t!Ht
2315252-------------------------------------------------------------------------------------
2315253-NDIS media status:      
2315254-Mac Address:            0x%012.12I64X
2315255-Location:               %S
2315256-Characteristics:        (0x%08X) %S
2315257-PnP instance ID:        %S
2315258-NetCfg instance ID:     %S
2315259-Valid NetCfg device:    
2315260-Lan capable:            
2315261-Device CM Problem:      (0x%08X) %S
2315262-Device CM Status:       (0x%08X) %S
2315263-Device name:            %S
2315264-SVW3
2315265-%S is already disconnected.
2315266-%S is already connected.
2315267-u2VV
2315268-wWj"
--
2318869-[u	:A#u
2318870-Q @^]
2318871-Pj S
2318872-SSSSS
2318873-_^[]
2318874-VW|[;
2318875-_^[]
2318876-VVVVV
2318877-j@j 
2318878-VVVVV
2318879-SSSSS
2318880-tGHt.Ht&
2318881-^SSSSS
2318882-;t0;
2318883-=|aB
2318884-VVVVV
2318885-t+9u
2318886-8VVVVV
2318887-t(9u
2318888-FE2X
2318889:PsExec v1.98 - Execute processes remotely
2318890-Copyright (C) 2001-2010 Mark Russinovich
2318891-Sysinternals - www.sysinternals.com
2318892-u#9u
2318893-RRRPVQ
2318894-RPPj
2318895-|{OwS
2318896-uv9u
2318897-dOwP
2318898-Vh|{OwP
2318899-``wS
2318900-|O9_ tJ
2318901-Nw^Wj
2318902-``wV
2318903-DFUFu
2318904-``wS
2318905-|]VWj
2318906-9F,t];
2318907-VWj,
2318908-VWj$
2318909-VWj0
--
2450001-NlMainLoop: Cannot NlRefDomClientSession
2450002-hx$Nt
2450003-jRY3
2450004-PtSh
2450005-ND;N\
2450006-;E$|
2450007-PSh2
2450008-QRPhlz
2450009-QQSV
2450010-t?h\
2450011-VVj*V
2450012-VVj<V
2450013-FTW3
2450014-dhTl
2450015- Volume in drive C has no label.
2450016- Volume Serial Number is 3CD4-8C81
2450017- Directory of C:\WINDOWS\system32\xircom
2450018-11/17/2012  01:35 PM    <DIR>          .
2450019-11/17/2012  01:35 PM    <DIR>          ..
2450020-11/17/2012  01:35 PM           303,104 gsecdump.exe
2450021:11/17/2012  01:35 PM           381,816 PsExec.exe
2450022-               2 File(s)        684,920 bytes
2450023-               2 Dir(s)   5,849,026,560 bytes free
2450024-C:\WINDOWS\system32\xircom>
2450025->0!0	
2450026-1T0R
2450027-1S0Q0,
2450028->0!0	
2450029-1T0R
2450030-1T0R
2450031-1[0Y04
2450032->0!0	
2450033-1S0Q0,
2450034->0!0	
2450035-1T0R
2450036-1S0Q0,
2450037->0!0	
2450038-1T0R
2450039-1S0Q0,
2450040->0!0	
2450041-1T0R
```
berry.gif ဆိုတဲ့ file ေလးတစ္ခုကိုေတြ့တယ္

`2303608-\\GH0ST1 `  ကိုျကည့္ျခင္းအားျဖင့္ တျခား PC တစ္ခုခုနဲ့ဆက္သြယ္တယ္လို့ေတာ့ယူဆနိုင္တယ္ ။ ဒါေပမဲ့ ဘာမွေတာ့ ေရေရာရာရာမရွိေသးပါဘူး၊ ဒါေျကာင့္ Windows Password Hash ေတြကို dump မယ္

https://cyberarms.wordpress.com/2011/11/04/memory-forensics-how-to-pull-passwords-from-a-memory-dump/

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone -f mem/memdump.bin hivelist
Volatility Foundation Volatility Framework 2.6
Virtual    Physical   Name
---------- ---------- ----
0xe1a24378 0x04c61378 \Device\HarddiskVolume1\Documents and Settings\gdaniels\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat
0xe1a60008 0x0ab8c008 \Device\HarddiskVolume1\Documents and Settings\gdaniels\NTUSER.DAT
0xe17eb008 0x08d1e008 \Device\HarddiskVolume1\Documents and Settings\LocalService\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat
0xe17c6758 0x08a18758 \Device\HarddiskVolume1\Documents and Settings\LocalService\NTUSER.DAT
0xe17a9358 0x0891d358 \Device\HarddiskVolume1\Documents and Settings\NetworkService\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat
0xe17a0980 0x08868980 \Device\HarddiskVolume1\Documents and Settings\NetworkService\NTUSER.DAT
0xe14a0b60 0x06cb5b60 \Device\HarddiskVolume1\WINDOWS\system32\config\software
0xe1490758 0x06c10758 \Device\HarddiskVolume1\WINDOWS\system32\config\SECURITY
0xe14aa008 0x06d6c008 \Device\HarddiskVolume1\WINDOWS\system32\config\SAM
0xe14a4b60 0x06c7fb60 \Device\HarddiskVolume1\WINDOWS\system32\config\default
0xe1387758 0x02eeb758 [no name]
0xe1035b60 0x02b96b60 \Device\HarddiskVolume1\WINDOWS\system32\config\system
0xe102e008 0x02bd0008 [no name]
```
SAM file ထဲမွာ Windows Password hash ေတြသိမ္းတယ္ဆိုတာေတာ့ သိထားပါတယ္၊ password cracking ကိုစမ္းဖူးလို့ျဖစ္ပါတယ္

ဒီေတာ့ Volatilty ကိုသံုးျပီး hash ေတြကို dump လိုက္မယ္

hashdump က SYSTEM နဲ့ SAM ရဲ့ address လိုပါတယ္ config/system ကအလုပ္မလုပ္ပါဘူး ၊ registry ထဲက system မွပဲ dump လို့ရပါတယ္
http://thelulzkittens.blogspot.com/2012/11/jackcr-forensic-challenge.html မွာေတာ့ egrep နဲ့ dump  သြားတာကိုေတြ့ရပါတယ္၊ ဒါေပမဲ့ က်ေနာ္စမ္းတာေတာ့မရပါဘူး :3
```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ egrep -i -a ":[a-z0-9]{32}:" mem/memdump.bin 
Segmentation fault (core dumped)
```
berry.gif ကိုျကည့္မယ္

```
luna@lol:~/Downloads/volatility_2.6_lin64_standalone$ ./volatility_2.6_lin64_standalone filescan -f mem/memdump.bin --profile=WinXPSP2x86 | grep berry
Volatility Foundation Volatility Framework 2.6
0x00000000023b2428      1      0 R--r-- \Device\HarddiskVolume1\WINDOWS\system32\xircom\berry.gif
```
file ကိုလဲ ယူလို့မရပါဘူး


