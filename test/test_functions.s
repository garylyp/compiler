    .data   
LC0:
    .asciz      "%d"                @ 0
    .asciz      "%d\n"              @ 3
    .asciz      "%s\n"              @ 7
    .asciz      ""                  @ 11
    .asciz      "\0\0\0\0\0\0\0\0"  @ 12
    .asciz      "\n"                @ 21
    .asciz      "\nFactorial of:"   @ 23
    .asciz      " equal to:"        @ 38
    .asciz      "Square of d larger than sum of squares"@ 49

    .text   
    .global     main
    .type       main, %function
main:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    mov        a1, #1              @ [VarAssign] a = 1
    mov        a2, #2              @ [VarAssign] b = 2
    mov        a3, #3              @ [VarAssign] i = 3
    mov        a4, #4              @ [VarAssign] d = 4
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #5
    bl         malloc
    mov        v2, a1              @ [VarAssign] _e0 = new Compute ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, v2              @ [VarAssign] help = _e0
    mov        v4, a2              @ mov value from a2 to v4
    mov        a2, v1              @ mov value from v1 to a2
    mov        v1, a3              @ mov value from a3 to v1
    mov        a3, v4              @ mov value from v4 to a3
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_2
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v2, a1              @ [VarAssign] _e1 = Compute_2(help,a,b)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, v1              @ mov value from v1 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e2 = Compute_0(help,i)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    add        a2, v2, v1          @ [VarAssign] _e3 = _e1 + _e2
    mov        v1, a2              @ [VarAssign] t1 = _e3
    mov        a2, a4              @ mov value from a4 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a4, a1              @ [VarAssign] _e4 = Compute_0(help,d)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    mov        a2, a4              @ [VarAssign] t2 = _e4
    cmp        a2, v1              @ if ( t2 > t1 ) goto .L0
    bgt        .L0
    b          .L1
.L0:
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 49
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    b          .L2
.L1:
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 49
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
.L2:
    mov        a1, v1              @ mov value from v1 to a1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #4              @ [Call] _a2 = 4
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_3
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e5 = Compute_3(help,4)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, v1              @ [VarAssign] t1 = _e5
    mov        v1, a1              @ mov value from a1 to v1
    mov        v2, a2              @ mov value from a2 to v2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 23
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 3        @ [println] "%d\n" format specifier
    mov        a2, #4
    bl         printf
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    ldr        a1, =LC0 + 7        @ [println] "%s\n" format specifier
    ldr        a2, =LC0 + 38
    bl         printf
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
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

Compute_0:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    mul        a1, a2, a2          @ [VarAssign] _e0 = a * a
    mov        a1, a1              @ return _e0
    b          .Compute_0_exit
.Compute_0_exit:
    ldmfd      sp!, {fp,pc}

Compute_1:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    add        a1, a2, a3          @ [VarAssign] _e0 = a + b
    mov        a1, a1              @ return _e0
    b          .Compute_1_exit
.Compute_1_exit:
    ldmfd      sp!, {fp,pc}

Compute_2:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    ldr        a4, [a1, #0]        @ [VarAssign] _e0 = this.computedsquares
    cmp        a4, #0              @ if ( _e0 ) goto .L3
    bgt        .L3
    b          .L4
.L3:
    ldr        a4, [a1, #1]        @ [VarAssign] _e1 = this.chachedvalue
    mov        a1, a4              @ return _e1
    b          .Compute_2_exit
.L4:
    mov        a4, #1              @ [VarAssign] _e2 = true
    mov        v3, a4              @ [FieldAssign] v3 = _e2
    str        v3, [a1, #0]        @ [FieldAssign] this.computedsquares = v3 (temp reg)
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a4, a1              @ [VarAssign] _e3 = Compute_0(this,a)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    mov        v1, a2              @ mov value from a2 to v1
    mov        a2, a3              @ mov value from a3 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a3, a1              @ [VarAssign] _e4 = Compute_0(this,b)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a2              @ mov value from a2 to v2
    mov        a2, a4              @ mov value from a4 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_1
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a4, a1              @ [VarAssign] _e5 = Compute_1(this,_e3,_e4)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    mov        a1, a4              @ return _e5
    b          .Compute_2_exit
.Compute_2_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

Compute_3:
    stmfd      sp!, {fp,lr,v1}
    add        fp, sp, #24
    cmp        a2, #1              @ if ( num < 1 ) goto .L5
    blt        .L5
    b          .L6
.L5:
    mov        a3, #1              @ [VarAssign] num_aux = 1
    mov        a1, a3              @ return num_aux
    b          .Compute_3_exit
.L6:
    mov        v3, #1
    sub        a3, a2, v3          @ [VarAssign] _e0 = num - 1
    mov        v1, a2              @ mov value from a2 to v1
    mov        a2, a3              @ mov value from a3 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Compute_3
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a3, a1              @ [VarAssign] _e1 = Compute_3(this,_e0)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mul        a2, v1, a3          @ [VarAssign] _e2 = num * _e1
    mov        a3, a2              @ [VarAssign] num_aux = _e2
    mov        a1, a3              @ return num_aux
    b          .Compute_3_exit
.Compute_3_exit:
    ldmfd      sp!, {fp,pc,v1}

