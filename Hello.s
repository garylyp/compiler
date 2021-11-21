	.arch armv5t
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 6
	.eabi_attribute 34, 0
	.eabi_attribute 18, 4
	.file	"Hello.c"
	.text
	.align	2
	.global	init
	.syntax unified
	.arm
	.fpu softvfp
	.type	init, %function
init:
	@ args = 0, pretend = 0, frame = 8
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
	sub	sp, sp, #12
	str	r0, [fp, #-8]
	str	r1, [fp, #-12]
	ldr	r3, [fp, #-12]
	sub	r2, r3, #1
	ldr	r3, [fp, #-8]
	str	r2, [r3]
	ldr	r3, [fp, #-12]
	lsl	r2, r3, #1
	ldr	r3, [fp, #-8]
	str	r2, [r3, #4]
	nop
	add	sp, fp, #0
	@ sp needed
	ldr	fp, [sp], #4
	bx	lr
	.size	init, .-init
	.align	2
	.global	foo
	.syntax unified
	.arm
	.fpu softvfp
	.type	foo, %function
foo:
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
	sub	sp, sp, #20
	str	r0, [fp, #-16]
	ldr	r3, [fp, #-16]
	ldr	r3, [r3]
	ldr	r2, [fp, #-16]
	ldr	r2, [r2, #4]
	mul	r3, r2, r3
	str	r3, [fp, #-8]
	ldr	r3, [fp, #-8]
	mov	r0, r3
	add	sp, fp, #0
	@ sp needed
	ldr	fp, [sp], #4
	bx	lr
	.size	foo, .-foo
	.section	.rodata
	.align	2
.LC0:
	.ascii	"%d\012\000"
	.align	2
.LC1:
	.word	__stack_chk_guard
	.text
	.align	2
	.global	main
	.syntax unified
	.arm
	.fpu softvfp
	.type	main, %function
main:
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	push	{fp, lr}
	add	fp, sp, #4
	sub	sp, sp, #16
	ldr	r3, .L7
	ldr	r3, [r3]
	str	r3, [fp, #-8]
	mov	r3,#0
	sub	r3, fp, #16
	mov	r1, #9
	mov	r0, r3
	bl	init
	sub	r3, fp, #16
	mov	r0, r3
	bl	foo
	mov	r3, r0
	mov	r1, r3
	ldr	r0, .L7+4
	bl	printf
	mov	r3, #0
	ldr	r2, .L7
	ldr	r1, [r2]
	ldr	r2, [fp, #-8]
	eors	r1, r2, r1
	mov	r2, #0
	beq	.L6
	bl	__stack_chk_fail
.L6:
	mov	r0, r3
	sub	sp, fp, #4
	@ sp needed
	pop	{fp, pc}
.L8:
	.align	2
.L7:
	.word	.LC1
	.word	.LC0
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",%progbits
