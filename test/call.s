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
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #8
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] c = _e0
    mov        v5, #0              @ [FieldAssign] v5 = 0
    str        v5, [a1, #0]        @ [FieldAssign] c.id = v5 (temp reg)
    mov        v5, #5              @ [FieldAssign] v5 = 5
    str        v5, [a1, #4]        @ [FieldAssign] c.val = v5 (temp reg)
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #8
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e1 = new Pair ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] p = _e1
    mov        v5, v1              @ [FieldAssign] v5 = c
    str        v5, [a1, #0]        @ [FieldAssign] p.c1 = v5 (temp reg)
    mov        v2, a1              @ mov value from a1 to v2
    mov        a1, v1              @ mov value from v1 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #4              @ [Call] _a2 = 4
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e2 = Clone_0(c,4)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v5, v1              @ [FieldAssign] v5 = _e2
    str        v5, [v2, #4]        @ [FieldAssign] p.c2 = v5 (temp reg)
    ldr        v1, [v2, #4]        @ [VarAssign] _e3 = p.c2
    mov        a1, v1              @ mov value from v1 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #4              @ [Call] _a2 = 4
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e4 = Clone_0(_e3,4)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, v2              @ mov value from v2 to a1
    mov        a2, v1              @ mov value from v1 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Pair_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e5 = Pair_0(p,_e4)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, v1              @ [VarAssign] i = _e5
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
    ldmfd      sp!, {fp,pc,v1,v2}

Clone_0:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #8
    bl         malloc
    mov        a3, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a3              @ [VarAssign] c = _e0
    ldr        a3, [v1, #0]        @ [VarAssign] _e1 = this.id
    add        a4, a3, a2          @ [VarAssign] _e2 = _e1 + powdiff
    mov        v5, a4              @ [FieldAssign] v5 = _e2
    str        v5, [a1, #0]        @ [FieldAssign] c.id = v5 (temp reg)
    mov        v5, #5              @ [FieldAssign] v5 = 5
    str        v5, [a1, #4]        @ [FieldAssign] c.val = v5 (temp reg)
    mov        a1, a1              @ return c
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_1:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
    ldr        a3, [a2, #0]        @ [VarAssign] _e0 = c.id
    ldr        a4, [a1, #0]        @ [VarAssign] _e1 = this.id
    sub        v1, a3, a4          @ [VarAssign] _e2 = _e0 - _e1
    mov        a1, v1              @ return _e2
    b          .Clone_1_exit
.Clone_1_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_2:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    ldr        a2, [a1, #0]        @ [VarAssign] _e0 = this.id
    mov        a3, a2              @ [VarAssign] n = _e0
    ldr        a2, [a1, #4]        @ [VarAssign] _e1 = this.val
    mov        a4, a2              @ [VarAssign] res = _e1
.L0:
    cmp        a3, #0              @ if ( n > 0 ) goto .L1
    bgt        .L1
    b          .L2
.L1:
    mov        v5, #10
    mul        a2, a4, v5          @ [VarAssign] _e2 = res * 10
    mov        a4, a2              @ [VarAssign] res = _e2
    mov        v5, #1
    sub        a2, a3, v5          @ [VarAssign] _e3 = n - 1
    mov        a3, a2              @ [VarAssign] n = _e3
    b          .L0
.L2:
    mov        a1, a4              @ return res
    b          .Clone_2_exit
.Clone_2_exit:
    ldmfd      sp!, {fp,pc}

Pair_0:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    ldr        a3, [a1, #0]        @ [VarAssign] _e0 = this.c1
    mov        v1, a1              @ mov value from a1 to v1
    mov        a1, a3              @ mov value from a3 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_2
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a3, a1              @ [VarAssign] _e1 = Clone_2(_e0)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    ldr        a1, [v1, #4]        @ [VarAssign] _e2 = this.c2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_2
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a4, a1              @ [VarAssign] _e3 = Clone_2(_e2)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    add        a1, a3, a4          @ [VarAssign] _e4 = _e1 + _e3
    mov        v2, a1              @ mov value from a1 to v2
    mov        a1, a2              @ mov value from a2 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_2
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e5 = Clone_2(c3)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    add        a4, v2, a2          @ [VarAssign] _e6 = _e4 + _e5
    mov        a1, a4              @ return _e6
    b          .Pair_0_exit
.Pair_0_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

