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
    mov        a2, a1              @ [VarAssign] _e0 = new Fieldaccess ()
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a3, [fp,#-8]        @ ld a3 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a1, a2              @ [VarAssign] f = _e0
    str        a1, [fp,#0]         @ st a1 to stack before func call
    str        a2, [fp,#-4]        @ st a2 to stack before func call
    str        a3, [fp,#-8]        @ st a3 to stack before func call
    str        a4, [fp,#-12]       @ st a4 to stack before func call
    mov        a2, #5              @ [Call] _a2 = 5
    sub        sp, #16             @ [Call] Shift sp to top of stack
    bl         Fieldaccess_0
    add        sp, #16             @ [Call] Shift sp back to prev pos (top of frame)
    mov        a3, a1              @ [VarAssign] _e1 = Fieldaccess_0(f,5)
    ldr        a1, [fp,#0]         @ ld a1 original val from stack after func call
    ldr        a2, [fp,#-4]        @ ld a2 original val from stack after func call
    ldr        a4, [fp,#-12]       @ ld a4 original val from stack after func call
    mov        a2, a3              @ [VarAssign] b = _e1
    mov        v5, #7              @ [FieldAssign] v5 = 7
    str        v5, [a1, #0]        @ [FieldAssign] f.a = v5 (temp reg)
    ldr        a3, [a1, #0]        @ [VarAssign] _e2 = f.a
    add        a1, a3, a2          @ [VarAssign] _e3 = _e2 + b
    mov        v5, #2
    mul        a3, a1, v5          @ [VarAssign] _e4 = _e3 * 2
    mov        a1, a3              @ [VarAssign] temp = _e4
    mov        a2, a1              @ mov value from a1 to a2
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
    ldmfd      sp!, {fp,pc,v1}

Fieldaccess_0:
    stmfd      sp!, {fp,lr}
    add        fp, sp, #20
    mov        v5, #6
    add        a1, v5, a2          @ [VarAssign] _e0 = 6 + x
    mov        a1, a1              @ return _e0
    b          .Fieldaccess_0_exit
.Fieldaccess_0_exit:
    ldmfd      sp!, {fp,pc}

