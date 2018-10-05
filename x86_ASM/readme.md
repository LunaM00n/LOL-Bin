
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

 1.Exit program to understand system call 

    mov eax,1 -> set exit sys call number (1) to eax register
    mov ebx,2 -> set first arguments to ebx register
    int 0x80 -> call interrupt


2.Hello World program to understand output,global variables

    msg db "Hello, world!",  0x0a -> defining global db and assign Hello , world! to this variable
    len equ $ - msg -> caculate the length of msg variable and assign to len
    mov eax,4 -> set write sys call number (4) to eax
    mov ebx,1 -> set file descriptor as first argument
    mov ecx,msg -> set message as second argument
    mov edx,len -> set length as third argument
    int 0x80 -> call interrupt 

3.A program to understand comparison , unconditional jump , conditional jump


    _start
    mov ecx,99 - set 99 to eax
    mov ebx,42 - set 42 to ebx
    mov eax,1 - set exit system call to eax
    cmp ecx,100 - compare ecx (99) and 100
    jl skip - if less than jump to skip
    
    skip
    int 0x80 - sys call interrupt

4.A program to understand loop

    _start
    mov ebx,1 -> set 1 to ebx
    mov ecx,6 -> set 6 to ecx ( ecx is counter register)
    
    label
    add ebx,ebx -> same with ebx + ebx
    dec ecx -> same with ecx--
    cmp ecx,0 -> compare ecx and 0
    jg label -> Jump to label if greater than 0
    mov eax,1
    int 0x80
    (Note)
    * ecx will decrease to 0 because of compare with 0
    * first round ebx=2 , ecx=5 
    * second round ebx=4 , ecx=4
    * third round ebx=8 , ecx=3
    * fourth round ebx=16 , ecx=2
    * fifth round ebx=32 , ecx=1
    * sixth round ebx=64 , ecx=0
    * When ecx is not greater than 0 , prgram call exit interrupt 

5.A program to understand data movement with [address] 

    addr db "yellow" - > define "yellow" in global variable addr
    mov [addr],byte 'H' -> move 'H' to the first byte of addr 
    mov [addr+5],byte '!' -> move '!' to the sixth byte of addr
    (Note)
    * after moving some byte ,write and exit

 6.A program to understand stack usage

    sub esp,4 - > esp - 4 means take 4 bytes from the stack
    mov [esp],byte 'H' -> set H to top of the stack ESP
    mov [esp+1],byte 'e' -> set e to esp+1
    mov [esp+2],byte 'y' -> set y to esp+2
    mov [esp+3],byte '!' -> set ! to esp+3
    (Note)
    * call system write and exit

7.A program to understand function call

    _start:
    call func -> when call func , push eip to the stack
    mov eax,1 -> set sys call exit to eax
    int 0x80 -> call interrupt
    
    func:
    mov ebx,42 -> set 42 to ebx
    ret -> set address at the top of the stack as eip
    (Note)
    * when func called , push next instruction to the stack 
    * when ret , top of the stack will be next instruction
    * it will return to mov eax,1 

8.A program to understand function proluge on the stack

    func
    push ebp -> saved current ebp at the top of the stack
    mov ebp,esp -> move esp address to ebp
    sub esp,2 -> take 2 bytes from the esp
    ....
    mov esp,ebp -> move ebp address to esp
    pop ebp -> popping saved ebp to current ebp
    ret
    (Note)
    * the function proluge is take 2 bytes for func
    * when function is finished instructions , taken 2 bytes space on the stack where destroyed (same with leave) , and then put saved ebp to the current ebp 

 9.A program to understand push on the stack and return value

     _start
     push 21 -> push 21 to the top of the stack
     call times2 -> call times function
     mov ebx,eax -> mov eax's value to ebx
     mov eax,1
     int 0x80
    
    times2
    push ebp -> saved ebp
    mov ebp,esp -> move esp to ebp
    mov eax,[ebp+8] -> move 21 to eax
    add eax,eax -> 21+21 =42
    mov esp,ebp -> move ebp to esp
    pop ebp -> popped saved ebp to ebp
    ret -> set next instruction pointer on the top of the stack
    (Note)
    * we pushed 21 to the stack and call times2
    * times 2 make function proluge and 21 is exists at [ebp+8]
    * mov 21 to eax and peform 21+21 , now eax will be 42 
    * and the stack frame is destroy and return to main function
    * eax stil 42 and mov this value to ebx 
    * when exit , exit status will be 42 because ebx=42
 
 [ [Exercises from davy wybiral](https://github.com/code-tutorials/assembly-intro) ] 

