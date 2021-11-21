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
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    mov        a2, #1
    mov        a4, #2
    add        a1, a2, a4          @ [VarAssign] _e0 = 1 + 2
    mov        a4, #3
    add        a2, a1, a4          @ [VarAssign] _e1 = _e0 + 3
    mov        a4, #4
    add        a1, a2, a4          @ [VarAssign] _e2 = _e1 + 4
    mov        a4, #5
    add        a2, a1, a4          @ [VarAssign] _e3 = _e2 + 5
    mov        a4, #6
    add        a1, a2, a4          @ [VarAssign] _e4 = _e3 + 6
    mov        a4, #7
    add        a2, a1, a4          @ [VarAssign] _e5 = _e4 + 7
    mov        a4, #8
    add        a1, a2, a4          @ [VarAssign] _e6 = _e5 + 8
    mov        a4, #9
    add        a2, a1, a4          @ [VarAssign] _e7 = _e6 + 9
    mov        a4, #10
    add        a1, a2, a4          @ [VarAssign] _e8 = _e7 + 10
    mov        a4, #11
    add        a2, a1, a4          @ [VarAssign] _e9 = _e8 + 11
    mov        a4, #12
    add        a1, a2, a4          @ [VarAssign] _e10 = _e9 + 12
    mov        a4, #13
    add        a2, a1, a4          @ [VarAssign] _e11 = _e10 + 13
    mov        a4, #14
    add        a1, a2, a4          @ [VarAssign] _e12 = _e11 + 14
    mov        a4, #15
    add        a2, a1, a4          @ [VarAssign] _e13 = _e12 + 15
    mov        a4, #16
    add        a1, a2, a4          @ [VarAssign] _e14 = _e13 + 16
    mov        a4, #17
    add        a2, a1, a4          @ [VarAssign] _e15 = _e14 + 17
    mov        a4, #18
    add        a1, a2, a4          @ [VarAssign] _e16 = _e15 + 18
    mov        a4, #19
    add        a2, a1, a4          @ [VarAssign] _e17 = _e16 + 19
    mov        a4, #20
    add        a1, a2, a4          @ [VarAssign] _e18 = _e17 + 20
    mov        a2, a1              @ [VarAssign] a = _e18
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
.main_exit:
    ldmfd      sp!, {fp,pc}

