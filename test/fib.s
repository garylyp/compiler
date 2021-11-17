    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    mov        a1, #0
.L0:
    cmp        a1, #10
    blt        .L1
    b          .L2
.L1:
    mov        v1, a1
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    mov        a1, #8
    bl         malloc
    mov        a2, a1
    ldr        a1, [fp,#0]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        a1, a2
    mov        a2, v1
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    sub        sp, #16
    bl         Fib_0
    add        sp, #16
    mov        v1, a1
    ldr        a1, [fp,#0]
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        v2, a2
    mov        a2, v1
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    ldr        a1, =LC0 + 3
    bl         printf
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        v4, #1
    add        a1, v2, v4
    mov        v2, a1
    b          .L0
.L2:
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

Fib_0:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    cmp        a2, #0
    blt        .L3
    b          .L4
.L3:
    mov        a3, #-1
    mov        a1, a3
    b          .Fib_0_exit
.L4:
    mov        v4, #0
    str        v4, [a1, #0]
    mov        v4, #1
    str        v4, [a1, #4]
.L5:
    cmp        a2, #0
    bgt        .L6
    b          .L7
.L6:
    ldr        a3, [a1, #4]
    mov        a4, a3
    ldr        a3, [a1, #0]
    ldr        v1, [a1, #4]
    add        v2, a3, v1
    mov        v4, v2
    str        v4, [a1, #4]
    mov        v4, a4
    str        v4, [a1, #0]
    mov        v4, #1
    sub        a4, a2, v4
    mov        a2, a4
    b          .L5
.L7:
    ldr        a2, [a1, #0]
    mov        a1, a2
    b          .Fib_0_exit
.Fib_0_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

