; test that CMP works
LD R[0] = 0
LD R[2] = 5
ADD R[0] 1
CMP R[0] R[2]
GOTO 4
EXIT