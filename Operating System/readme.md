# Operating System

Today, I'm going to learn Operating System and tiny development of operating system using Assembly, C Languages.

### Assembly

I have learned assembly language before.If you don't know anything about of assembly, you can learn my brief exercises.
https://github.com/LunaM00n/LOL-Bin/tree/master/x86_ASM

We may need some references for x86 assembly.So, We can use following reference from OS-Dev Wiki.
https://wiki.osdev.org/CPU_Registers_x86

### Very First Firmware

When we learned some basic of Assembly language, we can write "Hello World" program using assembly.
Remember, we used 0x80 interrupt in our assembly exercises and we can't use this system call interrupt for BIOS and
we need to use BIOS Interrupt for boot process now.

Example BIOS call
```
mov ah,<function>
mov al,<data>
int <interrupt>
```

We can use following BIOS interrupt list for reference.
https://en.wikipedia.org/wiki/BIOS_interrupt_call

Let's write our code.

```
;printing a character
mov ah,0x0e
mov al,'Z'
int 0x10

;Looping
hang:
 jmp hang
  ;padding and magic number
 times 510-($-$$) db 0
 db 0x55
 db 0xaa
```
0x0e -> write character function
0x10 -> video services interrupt
times 510-($-$$) db 0 -> when bios load it will fill 510 bytes with zero
0x55aa -> its magic number or boot signature.Older BIOS will identified the end of boot sector on disk

We have to compile our assembly code to disk image.

```
nasm boot.asm -f bin -o boot.bin
```

Running Binary in QEMU

```
qemu-system-i386 -fda boot.bin
```



### References
 - https://www.youtube.com/playlist?list=PLmlvkUN3-1MNKwINqdCDtTdNDjfBmWcZA - Writing an Operating System
 - https://www.youtube.com/playlist?list=PLr05M0l7e0fZLZxtxgxCDLwGrUoWV-UKN - OS Development by Nick Blundell
 - https://riptutorial.com/x86/example/23463/system-call-mechanisms
 - https://wiki.osdev.org/Tutorials
 - http://www.baldwin.cx/386htm/toc.htm
 - https://wiki.qemu.org/Documentation
 
 
