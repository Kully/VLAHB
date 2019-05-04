; Here I use RAM slot 512 as the return register.
; We should agree on a proper return register.

GOTO MAIN

; var MATH_ADD(var a, var b)
; {
;     a += b
;     return a
; }
MATH_ADD:
    ADD R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATH_SUB(var a, var b)
; {
;     a -= b
;     return a
; }
MATH_SUB:
    SUB R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATH_MUL(var a, var b)
; {
;     a *= b
;     return a
; }
MATH_MUL:
    MUL R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATH_DIV(var a, var b)
; {
;     a /= b
;     return a
; }
MATH_DIV:
    DIV R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATH_LONG_WINDED(var a, var b)
; {
;     b = MATH_ADD(a, b)
;     b = MATH_ADD(a, b)
;     b = MATH_ADD(a, b)
;     b = MATH_ADD(a, b)
;     return b;
; }
MATH_LONG_WINDED:
    CALL MATH_ADD
    LD R[1] R[512] ; 15
    CALL MATH_ADD
    LD R[1] R[512] ; 25
    CALL MATH_ADD
    LD R[1] R[512] ; 35
    CALL MATH_ADD
    RETURN ; 45

; void MAIN()
; {
;   var a = 10
;   var b = 5
;   var c = MATH_ADD(a, b)
;   var d = MATH_SUB(a, b)
;   var e = MATH_MUL(a, b)
;   var f = MATH_DIV(a, b)
;   var g = MATH_LONG_WINDED(a, b)
; }
MAIN:
    LD R[0] 10

    LD R[1] 5

    CALL MATH_ADD
    LD R[2] R[512]

    CALL MATH_SUB
    LD R[3] R[512]

    CALL MATH_MUL
    LD R[4] R[512]

    CALL MATH_DIV
    LD R[5] R[512]

    CALL MATH_LONG_WINDED
    LD R[6] R[512]

    EXIT
