; Here I use RAM slot 512 as the return register.
; We should agree on a proper return register.

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

; x < y
; 0 if false
; 1 if true
; only works with ints
MATH_INT_LESS_THAN:
    LD R[512] 0
    LD R[2] R[0]
    LD R[3] R[1]
    DIV R[2] R[1]
    DIV R[3] R[0]
    SUB R[2] 1
    SUB R[3] 1
    CMP R[2] 4294967294
    LD R[512] 0
    RETURN

MATH_CEIL:
    GOTO MATH_CEIL

MATH_FLOOR:
    GOTO MATH_FLOOR