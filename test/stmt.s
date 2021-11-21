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
    mov        a1, #10             @ [VarAssign] x = 10
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #9
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] c = _e0
    mov        a4, v1              @ [FieldAssign] a4 = x
    str        a4, [a1, #0]        @ [FieldAssign] c.val = a4 (temp reg)
    mov        a2, #1              @ [VarAssign] _e1 = true
    mov        a2, #0              @ [VarAssign] _e1 = false
    mov        a4, a2              @ [FieldAssign] a4 = _e1
    str        a4, [a1, #8]        @ [FieldAssign] c.bl = a4 (temp reg)
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e2 = Clone_0(c)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a4, a1              @ [FieldAssign] a4 = c
    str        a4, [a2, #4]        @ [FieldAssign] _e2.parent = a4 (temp reg)
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e3 = Clone_0(c)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] c = _e3
    mov        a2, #1              @ [VarAssign] _e4 = true
    mov        a2, #0              @ [VarAssign] _e4 = false
    mov        a4, a2              @ [FieldAssign] a4 = _e4
    str        a4, [a1, #8]        @ [FieldAssign] c.bl = a4 (temp reg)
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e5 = Clone_0(c)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a1              @ mov value from a1 to v2
    mov        a1, a2              @ mov value from a2 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e6 = Clone_0(_e5)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ mov value from a2 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a2, a1              @ [VarAssign] _e7 = Clone_0(_e6)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a2              @ [VarAssign] c = _e7
    ldr        a2, [v2, #0]        @ [VarAssign] _e8 = c.val
    mov        v1, a2              @ [VarAssign] x = _e8
.L0:
    cmp        v1, #0              @ if ( x > 0 ) goto .L1
    bgt        .L1
    b          .L2
.L1:
    mov        a4, #1
    sub        a2, v1, a4          @ [VarAssign] _e9 = x - 1
    mov        v1, a2              @ [VarAssign] x = _e9
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
    mov        v1, a2              @ mov value from a2 to v1
    mov        a2, v2              @ mov value from v2 to a2
    mov        v2, v1              @ mov value from v1 to v2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_1
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    b          .L0
.L2:
    b          .main_exit
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
    mov        a1, #9
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] c = _e0
    ldr        a2, [v1, #0]        @ [VarAssign] _e1 = this.val
    mov        a4, a2              @ [FieldAssign] a4 = _e1
    str        a4, [a1, #0]        @ [FieldAssign] c.val = a4 (temp reg)
    mov        a4, v1              @ [FieldAssign] a4 = this
    str        a4, [a1, #4]        @ [FieldAssign] c.parent = a4 (temp reg)
    ldr        a2, [v1, #8]        @ [VarAssign] _e2 = this.bl
    mov        a4, a2              @ [FieldAssign] a4 = _e2
    str        a4, [a1, #8]        @ [FieldAssign] c.bl = a4 (temp reg)
    mov        a1, a1              @ return c
    b          .Clone_0_exit
.Clone_0_exit:
    ldmfd      sp!, {fp,pc,v1}

Clone_1:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    b          .Clone_1_exit
.Clone_1_exit:
    ldmfd      sp!, {fp,pc}

