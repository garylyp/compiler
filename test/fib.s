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
    mov        a1, #0              @ [VarAssign] i = 0
.L0:
    cmp        a1, #10             @ if ( i < 10 ) goto .L1
    blt        .L1
    b          .L2
.L1:
    mov        v1, a1              @ mov value from a1 to v1
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a1, #8
    bl         malloc
    mov        a2, a1              @ [VarAssign] _e0 = new Fib ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ mov value from a2 to a1
    mov        a2, v1              @ mov value from v1 to a2
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Fib_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        v1, a1              @ [VarAssign] _e1 = Fib_0(_e0,i)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        v2, a2              @ mov value from a2 to v2
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
    mov        v3, #1
    add        a1, v2, v3          @ [VarAssign] _e2 = i + 1
    mov        v2, a1              @ [VarAssign] i = _e2
    b          .L0
.L2:
.main_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

Fib_0:
    stmfd      sp!, {fp,lr,v1,v2}
    add        fp, sp, #28
    cmp        a2, #0              @ if ( x < 0 ) goto .L3
    blt        .L3
    b          .L4
.L3:
    mov        a3, #-1             @ [VarAssign] _e0 = -1
    mov        a1, a3              @ return _e0
    b          .Fib_0_exit
.L4:
    mov        v3, #0              @ [FieldAssign] v3 = 0
    str        v3, [a1, #0]        @ [FieldAssign] this.a = v3 (temp reg)
    mov        v3, #1              @ [FieldAssign] v3 = 1
    str        v3, [a1, #4]        @ [FieldAssign] this.b = v3 (temp reg)
.L5:
    cmp        a2, #0              @ if ( x > 0 ) goto .L6
    bgt        .L6
    b          .L7
.L6:
    ldr        a3, [a1, #4]        @ [VarAssign] _e1 = this.b
    mov        a4, a3              @ [VarAssign] temp = _e1
    ldr        a3, [a1, #0]        @ [VarAssign] _e2 = this.a
    ldr        v1, [a1, #4]        @ [VarAssign] _e3 = this.b
    add        v2, a3, v1          @ [VarAssign] _e4 = _e2 + _e3
    mov        v3, v2              @ [FieldAssign] v3 = _e4
    str        v3, [a1, #4]        @ [FieldAssign] this.b = v3 (temp reg)
    mov        v3, a4              @ [FieldAssign] v3 = temp
    str        v3, [a1, #0]        @ [FieldAssign] this.a = v3 (temp reg)
    mov        v3, #1
    sub        a4, a2, v3          @ [VarAssign] _e5 = x - 1
    mov        a2, a4              @ [VarAssign] x = _e5
    b          .L5
.L7:
    ldr        a2, [a1, #0]        @ [VarAssign] _e6 = this.a
    mov        a1, a2              @ return _e6
    b          .Fib_0_exit
.Fib_0_exit:
    ldmfd      sp!, {fp,pc,v1,v2}

