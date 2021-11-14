    .data
L1:
    .asciz "Hello World!"     @ 12+1
    .asciz "Hello Universe\n" @ 15+1
    .asciz "%d\n"             @ 3+1
    .asciz "%d"               @ 2+1
    .asciz "\0\0\0\0\0\0\0\0"

    .text
    .global main
    .type main, %function
main:
    stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
    add fp,sp,#24
    sub sp,fp,#32
    ldr a1,=L1 + 13
    cmp a1, a2
    bl printf
    ldr a1,=L1 + 33
    ldr a2,=L1 + 36
    bl scanf
    ldr a1,=L1 + 29
    ldr a2,=L1 + 36
    ldr a2, [a2]
    bl printf


.L1exit:
    mov a4,#0
    mov a1,r3
    sub sp,fp,#24
    ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
