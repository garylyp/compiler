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
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 0        @ [readln] %d format specifier
    ldr        a2, =LC0 + 12       @ [readln] write address
    bl         scanf
    ldr        a2, =LC0 + 12       @ [readln] write address
    ldr        a2, [a2]            @ [readln] save scanned integer
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v1, a2              @ mov value from a2 to v1
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
    neg        a2, v1              @ [VarAssign] _e0 = -x
    neg        a1, v1              @ [VarAssign] _e1 = -x
    mul        a3, a2, a1          @ [VarAssign] _e2 = _e0 * _e1
    mov        v3, #4
    mul        a1, v1, v3          @ [VarAssign] _e3 = x * 4
    add        a2, a3, a1          @ [VarAssign] _e4 = _e2 + _e3
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #8
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e5 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] c = _e5
    mov        v3, #2              @ [FieldAssign] v3 = 2
    str        v3, [a1, #0]        @ [FieldAssign] c.a = v3 (temp reg)
    mov        v3, #4
    mov        v4, #4
    mul        a2, v3, v4          @ [VarAssign] _e6 = 4 * 4
    mov        v1, a2              @ [VarAssign] x = _e6
    ldr        a2, [a1, #0]        @ [VarAssign] _e7 = c.a
    mov        v1, a2              @ [VarAssign] x = _e7
    mov        v2, a1              @ mov value from a1 to v2
    mov        a2, v1              @ mov value from v1 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v3, #17
    mov        v4, #5
    mul        a1, v3, v4          @ [VarAssign] _e8 = 17 * 5
    mov        v3, a1              @ [FieldAssign] v3 = _e8
    str        v3, [v2, #4]        @ [FieldAssign] c.b = v3 (temp reg)
    ldr        a1, [v2, #4]        @ [VarAssign] _e9 = c.b
    neg        v2, a1              @ [VarAssign] _e10 = -_e9
    mov        a2, v2              @ [VarAssign] x = _e10
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    b          .main_exit
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

