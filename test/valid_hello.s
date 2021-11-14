    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "Hello world!"      @ 21

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr}
    ldr        a1, =LC0 + 0
    ldr        a2, =LC0 + 12
    bl         scanf
    ldr        a2, =LC0 + 12
    ldr        a2, [a2]
    ldr        a1, =LC0 + 7
    ldr        a2, =LC0 + 21
    bl         printf
.main_exit:
    ldmfd      sp!, {fp,pc}

