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
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
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
    mov        v4, #4
    str        v4, [sp, #-20]      @ [Call] Place additional args on stk
    mov        v4, #5
    str        v4, [sp, #-24]      @ [Call] Place additional args on stk
    mov        v4, #6
    str        v4, [sp, #-28]      @ [Call] Place additional args on stk
    mov        v4, #7
    str        v4, [sp, #-32]      @ [Call] Place additional args on stk
    sub        sp, #32             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #32             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e1 = Clone_0(_e0,1,2,3,4,5,6,7)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
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
    b          .main_exit
.main_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_0:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #40
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        v4, [fp,#-16]
    str        v4, [sp, #-20]      @ [Call] Place additional args on stk
    ldr        v4, [fp,#-20]
    str        v4, [sp, #-24]      @ [Call] Place additional args on stk
    ldr        v4, [fp,#-24]
    str        v4, [sp, #-28]      @ [Call] Place additional args on stk
    ldr        v4, [fp,#-28]
    str        v4, [sp, #-32]      @ [Call] Place additional args on stk
    sub        sp, #32             @ [Call] Shift sp to top of stack
    bl         Clone_1
    add        sp, #32             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e0 = Clone_1(this,a,b,c,d,e,f,g)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v4, v1              @ [FieldAssign] v4 = _e0
    str        v4, [a1, #0]        @ [FieldAssign] this.a1 = v4 (temp reg)
    ldr        v1, [a1, #0]        @ [VarAssign] _e1 = this.a1
    mov        a1, v1              @ return _e1
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_1:
    stmfd      sp!, {fp,lr,v1,v2,v3,v4,v5}
    add        fp, sp, #56
    mov        v1, #1
    cmp        v1, #1              @ if ( 1 == 1 ) goto .L0
    beq        .L0
    b          .L1
.L0:
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v1, a2              @ mov value from a2 to v1
    mov        a2, a3              @ mov value from a3 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a2              @ mov value from a2 to v2
    mov        a2, a4              @ mov value from a4 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v3, a2              @ mov value from a2 to v3
    ldr        a2, [fp,#-16]       @ ld value from _m4 to _a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v4, a2              @ mov value from a2 to v4
    ldr        a2, [fp,#-20]       @ ld value from _m5 to _a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v5, a2              @ mov value from a2 to v5
    ldr        a2, [fp,#-24]       @ ld value from _m6 to _a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    ldr        a2, [fp,#-28]       @ ld value from _m7 to _a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ return g
    b          .Clone_1_exit
.L1:
    mov        a2, #-1             @ [VarAssign] _e0 = -1
    mov        a1, a2              @ return _e0
    b          .Clone_1_exit
.Clone_1_exit:
    ldmfd      sp!, {fp,pc,v1,v2,v3,v4,v5}

