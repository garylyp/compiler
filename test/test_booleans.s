    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "false"             @ 21
    .asciz      "true"              @ 27

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr,v1,v2,v3}
    add        fp, sp, #32
    mov        a1, #4              @ [VarAssign] a = 4
    mov        a2, #5              @ [VarAssign] b = 5
    mov        a3, #1              @ [VarAssign] _e0 = true
    mov        a4, a3              @ [VarAssign] b1 = _e0
    mov        a3, #1              @ [VarAssign] _e1 = true
    mov        a3, #0              @ [VarAssign] _e1 = false
    mov        v1, a3              @ [VarAssign] b2 = _e1
    mov        a3, #1              @ [VarAssign] _e2 = true
    mov        v2, #1              @ [VarAssign] _e3 = true
    cmp        a4, #0              @ if ( b1 ) goto .L0
    bgt        .L0
    b          .L1
.L0:
    cmp        v1, #0              @ if ( b2 ) goto .L2
    bgt        .L2
.L1:
    mov        v3, #0              @ [VarAssign] _e3 = false
.L2:
    cmp        v2, #0              @ if ( _e3 ) goto .L4
    bgt        .L4
    cmp        a2, #0              @ if ( b2 ) goto .L4
    bgt        .L4
    mov        a1, #1              @ [VarAssign] _e4 = true
    cmp        v3, #0              @ if ( b1 ) goto .L3
    bgt        .L3
    cmp        v3, #0              @ if ( b2 ) goto .L3
    bgt        .L3
    mov        v3, #0              @ [VarAssign] _e4 = false
.L3:
    cmp        a1, #0              @ if ( _e4 ) goto .L4
    bgt        .L4
    mov        a1, #0              @ [VarAssign] _e2 = false
.L4:
    mov        v2, a3              @ [VarAssign] b3 = _e2
    mov        v1, #1              @ [VarAssign] _e5 = true
    mov        a4, #1              @ [VarAssign] _e6 = true
    cmp        a1, a2              @ if ( a < b ) goto .L5
    blt        .L5
    mov        a2, #0              @ [VarAssign] _e6 = false
.L5:
    cmp        a4, #0              @ if ( _e6 ) goto .L6
    bgt        .L6
    b          .L7
.L6:
    cmp        v2, #0              @ if ( b3 ) goto .L8
    bgt        .L8
.L7:
    mov        a2, #0              @ [VarAssign] _e5 = false
.L8:
    mov        a4, v1              @ [VarAssign] b1 = _e5
    mov        a4, #1              @ [VarAssign] _e7 = true
    cmp        a1, a2              @ if ( a < b ) goto .L9
    blt        .L9
    mov        a2, #0              @ [VarAssign] _e7 = false
.L9:
    cmp        a4, #0              @ if ( _e7 ) goto .L10
    bgt        .L10
    b          .L12
.L10:
    cmp        v2, #0              @ if ( b3 ) goto .L11
    bgt        .L11
    b          .L12
.L11:
    mov        v1, a1              @ mov value from a1 to v1
    mov        v3, a2              @ mov value from a2 to v3
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 27
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    b          .L13
.L12:
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 21
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
.L13:
    cmp        v2, #0              @ if ( b3 ) goto .L15
    bgt        .L15
    mov        a2, #1              @ [VarAssign] _e8 = true
    cmp        a1, v3              @ if ( a > b ) goto .L14
    bgt        .L14
    mov        a2, #0              @ [VarAssign] _e8 = false
.L14:
    cmp        a2, #0              @ if ( _e8 ) goto .L15
    bgt        .L15
    b          .L16
.L15:
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 27
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    b          .L17
.L16:
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 21
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
.L17:
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2,v3}

Boolops_0:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    mov        v3, #6
    add        a1, v3, a2          @ [VarAssign] _e0 = 6 + x
    mov        a1, a1              @ return _e0
    b          .Boolops_0_exit
.Boolops_0_exit:
    ldmfd      sp!, {fp,pc}

