## x86 Assembly 101

**System call in Assembly**

    eax = sys call;
    ebx = first arg;
    ecx = second arg;
    edx = third arg;

**Quick Sys call table**
https://syscalls.kernelgrok.com/
http://shell-storm.org/shellcode/files/syscalls.html


**Interrupt**

    int 0x80

**Sections**

    .data = initialized global variables
    .bss = unintialized global variables
    .text = instruction codes
**Compiling asm to object**

    nasm -f elf32 -o filename.o filename.asm
**Linking with executable**

    ld -m elf_i386 -o filename filename.o
    
**Checking exit status**
`echo $?`

**Exercises**

 - Exit program to understand system call 
 ```mov eax,1 -> set exit sys call number (1) to eax register
  mov ebx,2 -> set first arguments to ebx register
  int 0x80 -> call interrupt```


 - Hello World program to understand output,global variables
 - A program to understand comparison , unconditional jump , conditional jump
 - A program to understand loop
 - A program to understand data movement with address 
 - A program to understand stack usage
 - A program to understand stack usage 2
 - A program to understand function call
 - A program to understand function proluge, return address and stack
 - A program to understand C library function call via assembly
 - A program to understand assembly to header file and call via C
 
 [ [Exercises from davy wybiral](https://github.com/code-tutorials/assembly-intro) ] 
