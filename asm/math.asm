; Here I use RAM slot 512 as the return register.
; We should agree on a proper return register.

GOTO MAIN

; var MATHADD(var a, var b)
; {
;     a += b
;     return a
; }
MATHADD:
    ADD R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATHSUB(var a, var b)
; {
;     a -= b
;     return a
; }
MATHSUB:
    SUB R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATHMUL(var a, var b)
; {
;     a *= b
;     return a
; }
MATHMUL:
    MUL R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATHDIV(var a, var b)
; {
;     a /= b
;     return a
; }
MATHDIV:
    DIV R[0] R[1]
    LD R[512] R[0]
    RETURN

; var MATHLONGWINDED(var a, var b)
; {
;     b = MATHADD(a, b)
;     b = MATHADD(a, b)
;     b = MATHADD(a, b)
;     b = MATHADD(a, b)
;     return b;
; }
MATHLONGWINDED:
    CALL MATHADD
    LD R[1] R[512] ; 15
    CALL MATHADD
    LD R[1] R[512] ; 25
    CALL MATHADD
    LD R[1] R[512] ; 35
    CALL MATHADD
    RETURN ; 45

; void MAIN()
; {
;   var a = 10
;   var b = 5
;   var c = MATHADD(a, b)
;   var d = MATHSUB(a, b)
;   var e = MATHMUL(a, b)
;   var f = MATHDIV(a, b)
;   var g = MATHLONGWINDED(a, b)
; }
MAIN:
    LD R[0] 10

    LD R[1] 5

    CALL MATHADD
    LD R[2] R[512]

    CALL MATHSUB
    LD R[3] R[512]

    CALL MATHMUL
    LD R[4] R[512]

    CALL MATHDIV
    LD R[5] R[512]

    CALL MATHLONGWINDED
    LD R[6] R[512]

    EXIT
