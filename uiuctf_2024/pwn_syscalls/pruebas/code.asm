section .text
global _start

_start:

    xor  rdx, rdx
    push rdx
    mov  rsi, 0x7478742e67616c66
    push rsi
    mov  rsi, rsp
    xor  rdi, rdi
    sub  rdi, 100
    mov  rax, 0x101
    syscall

    mov  rcx, 0x64
    mov  esi, eax
    xor  rdi, rdi
    inc  edi
    mov   al, 0x28
    syscall

    mov   al, 0x3c
    syscall

section .data
    filename db "flag.txt", 0

