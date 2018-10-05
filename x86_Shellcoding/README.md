## x86 Shellcoding 101
**Hello World Shellcode** 
(Note)
*We already have hello world program in x86_ASM/lesson2

    root@local:~/Desktop/Shellcode# ./lesson2
    Hello World
**Diassembling with Objdump**

    root@local:~/Desktop/Shellcode# objdump -d lesson2
    
    lesson2:     file format elf32-i386
    
    
    Disassembly of section .text:
    
    08049000 <_start>:
     8049000:       b8 04 00 00 00          mov    $0x4,%eax
     8049005:       bb 01 00 00 00          mov    $0x1,%ebx
     804900a:       b9 00 a0 04 08          mov    $0x804a000,%ecx
     804900f:       ba 0d 00 00 00          mov    $0xd,%edx
     8049014:       cd 80                   int    $0x80
     8049016:       b8 01 00 00 00          mov    $0x1,%eax
     804901b:       bb 00 00 00 00          mov    $0x0,%ebx
     8049020:       cd 80                   int    $0x80
     (Note) 
     * objdump will print as AT&T Syntax
**Creating Shellcode from OP code**

    root@local:~/Desktop/Shellcode# objdump -d lesson2 | grep "^ " \
    >  | cut -d$'\t' -f 2 | tr '\n' ' ' | sed -e 's/ *$//' \
    >  | sed -e 's/ \+/\\x/g' | awk '{print "\\x"$0}'
    \xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00\xb9\x00\xa0\x04\x08\xba\x0d\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xbb\x00\x00\x00\x00\xcd\x80
    (Note)
    * \x00 - Null bytes will terminate our shellcode

**Removing Null bytes 0x00**

    xor eax,eax
    xor ebx,ebx
    xor ecx,ecx
    xor edx,edx 
    (Note)
    * xor ->if same vaule , set 0
    mov al,1
    (Note)
    * al -> 16 bits register for eax , this mean we will only use 16 bits
Disassembly Result    

    root@local:~/Desktop/Shellcode# objdump -d sc_0
    
    sc_0:     file format elf32-i386
    
    
    Disassembly of section .text:
    
    08049000 <_start>:
     8049000:       31 c0                   xor    %eax,%eax
     8049002:       31 db                   xor    %ebx,%ebx
     8049004:       31 c9                   xor    %ecx,%ecx
     8049006:       31 d2                   xor    %edx,%edx
     8049008:       b0 04                   mov    $0x4,%al
     804900a:       b3 01                   mov    $0x1,%bl
     804900c:       b9 00 a0 04 08          mov    $0x804a000,%ecx
     8049011:       b2 0b                   mov    $0xb,%dl
     8049013:       cd 80                   int    $0x80
     8049015:       b0 01                   mov    $0x1,%al
     8049017:       31 db                   xor    %ebx,%ebx
     8049019:       cd 80                   int    $0x80

**Refernce Problem**
`$0x804a000 `
(Note)
*When we inject this shellcode , we can't access this address that containted "Hello World".
*We need to push our string to the stack and mov into ecx again

**Using stack**
"LOL Scode"
(Note)
*We will use 8 bytes string to easy push

Hexdump 

    root@local:~/Desktop/Shellcode# python -c "print 'LOL Scode'" | hexdump -C -v
    00000000  4c 4f 4c 20 53 63 6f 64  65 0a                    |LOL Scode.|
    0000000a

Endianess

    4c 4f 4c 20 -> 20 4c 4f 4c
    63 6f 64  65 -> 65 64 6f 63
    (Note)
    * I deleted 53 (S)  , because it was 9 bytes :3 . Sry !

 new instruction

     push 0x65646f63
     push 0x204c4f4c
     mov ecx,esp
     mov dl,0x8
     (Note)
     *We need to reverse push , Stack is LIFO strucutre
 New disassembly
 

    root@local:~/Desktop/Shellcode# objdump -d sc_1
    
    sc_1:     file format elf32-i386
    
    
    Disassembly of section .text:
    
    08049000 <_start>:
     8049000:       31 c0                   xor    %eax,%eax
     8049002:       31 db                   xor    %ebx,%ebx
     8049004:       31 c9                   xor    %ecx,%ecx
     8049006:       31 d2                   xor    %edx,%edx
     8049008:       b0 04                   mov    $0x4,%al
     804900a:       b3 01                   mov    $0x1,%bl
     804900c:       68 63 6f 64 65          push   $0x65646f63
     8049011:       68 4c 4f 4c 20          push   $0x204c4f4c
     8049016:       89 e1                   mov    %esp,%ecx
     8049018:       b2 08                   mov    $0x8,%dl
     804901a:       cd 80                   int    $0x80
     804901c:       b0 01                   mov    $0x1,%al
     804901e:       31 db                   xor    %ebx,%ebx
     8049020:       cd 80                   int    $0x80

 Create Shellcode from disassembly

     root@local:~/Desktop/Shellcode# objdump -d sc_1 | grep "^ " | cut -d$'\t' -f 2 | tr '\n' ' ' | sed -e 's/ *$//' | sed -e 's/ \+/\\x/g'| awk '{print "\\x"$0}'
    \x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\x04\xb3\x01\x68\x63\x6f\x64\x65\x68\x4c\x4f\x4c\x20\x89\xe1\xb2\x08\xcd\x80\xb0\x01\x31\xdb\xcd\x80

**Testing Shellcode**

    #include <stdio.h>
    #include <string.h>
    
    char *shellcode="\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\x04\xb3\x01\x68\x63\x6f\x64\x65\x68\x4c\x4f\x4c\x20\x89\xe1\xb2\x08\xcd\x80\xb0\x01\x31\xdb\xcd\x80";
    
    int main(void)
    {
            ( *( void(*)() ) shellcode)();
    }
compile this c and run 

    root@local:~/Desktop/Shellcode# gcc shelltest.c -m32 -z execstack -o shelltest
    root@local:~/Desktop/Shellcode# ./shelltest
    LOL code


[ [Exercise](https://exploit.courses/#/challenge/3) from Yukiterm ]
