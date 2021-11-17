    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "peche"             @ 21
    .asciz      "cker"              @ 27
    .asciz      "cbty"              @ 32
    .asciz      "ckercbty"          @ 37

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
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
    sub        sp, #16
    bl         Clone_0
    add        sp, #16
    ldr        a1, [fp,#0]
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        a2, #1
    mov        a2, #0
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    sub        sp, #16
    bl         Clone_1
    add        sp, #16
    ldr        a1, [fp,#0]
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
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
    mov        a1, v1
    mov        a3, a2
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    mov        a2, #5
    sub        sp, #16
    bl         Clone_2
    add        sp, #16
    mov        v1, a1
    ldr        a1, [fp,#0]
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
    mov        a2, v1
    str        a1, [fp,#0]
    str        a2, [fp,#-4]
    str        a3, [fp,#-8]
    str        a4, [fp,#-12]
    ldr        a1, =LC0 + 7
    bl         printf
    ldr        a2, [fp,#-4]
    ldr        a3, [fp,#-8]
    ldr        a4, [fp,#-12]
.main_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_0:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
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
    mov        v2, a2
    str        v2, [v1, #0]
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_1:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    b          .Clone_1_exit
.Clone_1_exit:
    ldmfd      sp!, {fp,pc}

Clone_2:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    mov        v2, a3
    str        v2, [a1, #0]
    ldr        a3, =LC0 + 32
.L0:
    cmp        a2, #0
    bge        .L1
    b          .L2
.L1:
    ldr        a3, =LC0 + 21
    mov        v2, #1
    sub        a3, a2, v2
    mov        a2, a3
    ldr        a3, =LC0 + 37
    b          .L0
.L2:
    ldr        a2, =LC0 + 27
    mov        a1, a2
    b          .Clone_2_exit
.Clone_2_exit:
    ldmfd      sp!, {fp,pc}

