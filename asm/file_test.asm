GOTO FOO
; a comment
FUNCTION:
    LD R[1] 2
    RETURN

FOO:
    LD R[0] 1
    CALL FUNCTION ; push PC to stack
    LD R[2] 3

EXIT  ; the end of the program
