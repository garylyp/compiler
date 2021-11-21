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
    mov        v1, #3              @ [VarAssign] x = 3
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #4
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ mov value from a2 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #1              @ [Call] _a2 = 1
    mov        a3, #2              @ [Call] _a3 = 2
    mov        a4, #3              @ [Call] _a4 = 3
    mov        v3, #4
    str        v3, [sp, #-20]      @ [Call] Place additional args on stk
    mov        v3, v1
    str        v3, [sp, #-24]      @ [Call] Place additional args on stk
    sub        sp, #24             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #24             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v2, a1              @ [VarAssign] _e1 = Clone_0(_e0,1,2,3,4,x)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, v2              @ mov value from v2 to a2
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

Clone_0:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #28
    ldr        v1, =LC0 + 21       @ [FieldAssign] v1 = "Hello"
    str        v1, [a1, #0]        @ [FieldAssign] this.s = v1 (temp reg)
    mul        a1, a2, a3          @ [VarAssign] _e0 = a * b
    add        a3, a1, a4          @ [VarAssign] _e1 = _e0 + c
    ldr        a1, [fp,#-20]       @ ld value from _m5 to _a1
    neg        a4, a1              @ [VarAssign] _e2 = -e
    ldr        a2, [fp,#-16]       @ ld value from _m4 to _a2
    mul        a1, a2, a4          @ [VarAssign] _e3 = d * _e2
    sub        a2, a3, a1          @ [VarAssign] _e4 = _e1 - _e3
    mov        a1, a2              @ return _e4
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc}

