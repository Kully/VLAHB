// fast ticking clock

CLOCK_PROGRAM:
	ADD R[1] 1
	CMP R[1] 59
	GOTO CLOCK_PROGRAM
	LD R[1] 0 // reset minute to 0
	ADD R[0] 1
	CMP R[0] 23
	GOTO CLOCK_PROGRAM
	LD R[0] 0 // reset hour to 0
	GOTO CLOCK_PROGRAM
	EXIT