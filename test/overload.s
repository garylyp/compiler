    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "cbty"              @ 21
    .asciz      "cker"              @ 26
    .asciz      "ckercbty"          @ 31
    .asciz      "peche"             @ 40

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
    mov        a1, #4
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v1, a2              @ [VarAssign] c = _e0
    mov        a1, v1              @ mov value from v1 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #1              @ [Call] _a2 = 1
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, #1              @ [VarAssign] _e1 = true
    mov        a2, #0              @ [VarAssign] _e1 = false
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
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #4
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e2 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, v1              @ mov value from v1 to a1
    mov        a3, a2              @ mov value from a2 to a3
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #5              @ [Call] _a2 = 5
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Clone_2
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e3 = Clone_2(c,5,_e2)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, v1              @ [VarAssign] s = _e3
    mov        a2, v2              @ mov value from v2 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
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
    mov        a1, #4
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Clone ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a2              @ [FieldAssign] v2 = _e0
    str        v2, [v1, #0]        @ [FieldAssign] this.other = v2 (temp reg)
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
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
    mov        v2, a3              @ [FieldAssign] v2 = c
    str        v2, [a1, #0]        @ [FieldAssign] this.other = v2 (temp reg)
    ldr        v1, =LC0 + 21       @ [VarAssign] s = "cbty"
.L0:
    cmp        a2, #0              @ if ( x >= 0 ) goto .L1
    bge        .L1
    b          .L2
.L1:
    ldr        v1, =LC0 + 40       @ [VarAssign] s = "peche"
    mov        v2, #1
    sub        v1, a2, v2          @ [VarAssign] _e0 = x - 1
    mov        a2, v1              @ [VarAssign] x = _e0
    ldr        v1, =LC0 + 31       @ [VarAssign] s = "ckercbty"
    b          .L0
.L2:
    ldr        v1, =LC0 + 26       @ [VarAssign] s = "cker"
    mov        a1, v1              @ return s
    b          .Clone_2_exit
.Clone_2_exit:
    ldmfd      sp!, {fp,pc,v1}

