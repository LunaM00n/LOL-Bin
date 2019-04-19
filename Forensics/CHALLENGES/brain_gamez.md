## Brainz_Game - Forensics Challenge

> This challenge is good to understand file analysis

Challenge file : [brain.jpg](https://github.com/LunaM00n/LOL-Bin/blob/master/Forensics/FILES/brain.jpg)

**File Information**

```
luna@lol:~/Downloads$ file brain.jpg 
brain.jpg: JPEG image data, JFIF standard 1.02, aspect ratio, density 1x1, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=5, description=TjB0X0YxYUdfQnVUX200WV9uMzNk, resolutionunit=1], baseline, precision 8, 635x444, frames 3
```

We can see base64 encoded data in description

```
luna@lol:~/Downloads$ echo "TjB0X0YxYUdfQnVUX200WV9uMzNk" | base64 -d
N0t_F1aG_BuT_m4Y_n33d
```
**Binwalk**

```
luna@lol:~/Downloads$ binwalk brain.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.02
30            0x1E            TIFF image data, big-endian, offset of first image directory: 8
28650         0x6FEA          Zip archive data, encrypted at least v2.0 to extract, compressed size: 172, uncompressed size: 203, name: flag.txt
28982         0x7136          End of Zip archive, footer length: 22
```

using binwalk, we can see file has another zip file with flag.txt

`binwalk -e brain.jpg` can extract and unzip using `unzip 6FEA.zip`

We can use `N0t_F1aG_BuT_m4Y_n33d` as zip password

```
luna@lol:~/Downloads/_brain.jpg.extracted$ cat flag.txt 
Condor, 

I found what you are looking for, but you know me better than that. You have to 
look deeper in order to find the goods. F*CK the system! Hack the planet.

-Kevin M.

P.S. Lay3rz_0f_Obfusc4t10n
```
this is notflag , but it may be another password 

**Steghide - Stegnography tool**

```
luna@lol:~/Downloads$ steghide extract -sf brain.jpg 
Enter passphrase: 
wrote extracted data to "realflag.txt".
```
ok realflag

```
luna@lol:~/Downloads$ cat realflag.txt 
Condor,

I know about your love for esoteric programming languages so I put the info you’re looking for below. 

-[------->+<]>-.+++++.----------.>-[--->+<]>-.[----->+<]>++.>--[-->+++++<]>.+[-->+<]>++++.---[----->+<]>-.[-->+<]>-----.---.-[----->+<]>--.---------------.-[----->+<]>+.+[++>-----<]>.[-->+++<]>-.[->++++<]>-.+[--->++<]>++.[->+++++<]>---.-[->++++++<]>.+++++[->++<]>.>-[----->+<]>.---[->++<]>-.-[----->+<]>.[++>-------<]>.-------.[--->+<]>+++.


Good luck with everything,
-Kevin M. l
```
OMG! what is esoteric programming? brainfuck because of filename

https://tio.run/ or any other online tools can help you

```HMCTF{Br41n_G4M3z_4r3_Fun}```





