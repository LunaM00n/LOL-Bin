global _start

section .text
_start:
	mov ebx,1
	mov ecx,6
label:
	add ebx,ebx
	dec ecx
	cmp ecx,0
	jg label
	mov eax,1
	int 0x80
