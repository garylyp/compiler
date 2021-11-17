    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "Hello"             @ 21

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    mov        a1, #3
    mov        v1, a1
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    mov        a1, #4
    bl         malloc
    mov        a2, a1
    ldr        a1, [fp,#0]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        a1, a2
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    mov        a2, #1
    mov        a3, #2
    mov        a4, #3
    mov        v5, #4
    str        v5, [sp, #-20]
    mov        v5, v1
    str        v5, [sp, #-24]
    sub        sp, #24
    bl         Clone_0
    add        sp, #24
    mov        v2, a1
    ldr        a1, [fp,#0]
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        a2, v2
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    ldr        a1, =LC0 + 3
    bl         printf
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    b          .main_exit
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

Clone_0:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #28
    ldr        v5, =LC0 + 21
    str        v5, [a1, #0]
    mul        a1, a2, a3
    add        a3, a1, a4
    ldr        a1, [fp,#-20]
    neg        a4, a1
    ldr        a1, [fp,#-16]
    mul        a2, a1, a4
    sub        a1, a3, a2
    mov        a1, a1
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc}

