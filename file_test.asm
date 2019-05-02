GOTO MAIN

FUNCTION:
    LD R[1] 2
    RETURN

MAIN:
    LD R[0] 1
    CALL FUNCTION
    LD R[2] 3

EXIT  ; the end of the program
