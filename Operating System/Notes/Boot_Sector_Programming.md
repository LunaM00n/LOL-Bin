# Boot Sector Programming

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

Writing LOL

```
mov ah,0x0e
mov al,'L'
int 0x10
mov al,'O'
int 0x10
mov al,'L'
int 0x10

jmp $ ;jump to the current address

times 510-($-$$) db 0
dw 0xaa55

```
 - jmp $ -> is the same as forever looping ( $ = current address )  

### Memory Layout and Stack Usage

According to our very first firmware, we knew the following things.
 - BIOS loaded 512 bytes for Boot Sector
 - Code in the Boot Sector is loaded by BIOS at 0000:7c00
 - Machine Starts in Real Mode ( https://wiki.osdev.org/Real_Mode )
 
Memory Layout after Boot

```
Free
0xC0000 - BIOS ( 256 kb )
0xA0000 - Video Memory ( 128 kb )
0x9fc00 - Extended BIOS data area ( 639 kb )
Free
0x7c00 - Loaded Boot Sector ( 512 Bytes )
0x400 to 0x500 - BIOS Data Area ( 256 Bytes )
0x00 - Interrupt Vector Table ( 1kb )
```
'X' mark the Spot

```
mov ah,0x0e
mov al,the_secret
int 0x10
mov al,[the_secret]
int 0x10
mov bx,the_secret
add bx,0x7c00
mov al,[bx]
int 0x10

jmp $ ;jump forever

the_secret:
	db "X"

times 510-($-$$) db 0
dw 0xaa55

```
In above code , we created the function the_secret and define X in this function.As using BIOS print like in our very
first firmware , We can sport the address where 'X' is occupied.

If you run above code, You will see third attempt will show 'X'. So, We can easily know how BIOS print work only at 0x7c00 ( Boot Sector ) in Real Mode.In this case, We can use ORG `[ORG 0x7c00]` to correct loading of Boot Sector from BIOS.


Defining Strings
```
msg:
 db "Booting OS",0
```
At the end of the string, we have to provide 0 as Null-T
erminated string.

Using the Stack

```
mov ah,0x0e

mov bp,0x8000
mov sp,bp

push 'A'
push 'B'
push 'C'

pop bx
mov al,bl
int 0x10

pop bx
mov al,bl
int 0x10

mov al,[0x7ffe]
int 0x10

jmp $

times 510-($-$$) db 0
dw 0xaa55

```
 - we defined stack's base pointer (bp) to 0x8000 which is free data above from Boot Sector
 - we defined stack's pointer (sp) to 0x8000 which is same as base pointer (bp)
 - And then we put three characters A,B and C to the stack
 - Popped out the character to (bx) which is 16 bit , then moved this character from (bl) which is 8 bit to (al) and then print out.
 - In third attempt,we used memory address of 'A' Character to understand more.

### Control Structures

If we really finished with my x86 assembly exercises, it shouldn't be hard for this time.
But I'll recall our knowledges with tiny example.

Conditional Jump

```
mov ah,0x0e

mov cx,5
cmp cx,5
je equal
mov cx,3
jmp diff

equal:
	mov al,'Y'
	int 0x10

diff:
	mov al,'N'
	int 0x10

jmp $

times 510-($-$$) db 0
dw 0xaa55

```
 - je -> Jump if equal
 - jne -> Jump if no equal
 - jl -> Jump if less than
 - je -> Jump if greader than
 - jle -> Jump if less than or equal
 - jge -> Jump if greater than or equal
 
 Function Call
 
 ```
jmp first_print

first_print:
	mov ah,0x0e
	call second_print

second_print:
	mov al,'X'
	int 0x10
	ret

jmp $

times 510-($-$$) db 0
dw 0xaa55
 
 ```
 
 Include Files
 
 ```
 %include "my_print_funcion.asm"
 ```
 By using this include files , we can create a neat code for our OS.
 
### Writing Hello World

Simple One
```
; Hello World Porgram

[org 0x7c00]

xor ax,ax
cld

mov si,msg
call bios_print

msg db 'Hello World',13,10,0

bios_print:
	lodsb ; load string 
	or al,al ; zero=end of string
	jz done ; if equal zero
	mov ah,0x0e
	mov bh,0
	int 0x10
	jmp bios_print

done:
	ret


jmp $

times 510-($-$$) db 0
dw 0xaa55

```
Using Include for print function

```
;print_string.asm
print_string:
	pusha
	lodsb
	or al,al
	jz done
	mov ah,0x0e
	int 0x10
	jmp print_string

done:
	ret

```
and boot.asm 
```
; Hello World Porgram

[org 0x7c00]
mov si,msg
call print_string

%include "print_string.asm"

msg db 'Hello World',13,10,0


jmp $

times 510-($-$$) db 0
dw 0xaa55


```

### References
 - https://www.youtube.com/playlist?list=PLmlvkUN3-1MNKwINqdCDtTdNDjfBmWcZA - Writing an Operating System
 - https://www.youtube.com/playlist?list=PLr05M0l7e0fZLZxtxgxCDLwGrUoWV-UKN - OS Development by Nick Blundell
 - https://riptutorial.com/x86/example/23463/system-call-mechanisms
 - https://wiki.osdev.org/Tutorials
 - http://www.baldwin.cx/386htm/toc.htm
 - https://wiki.qemu.org/Documentation
 
 
