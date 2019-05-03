GOTO INIT

INIT:
	LD R[90] 0 ; n_0
	LD R[91] 1 ; n_1
	LD R[99] 0 ; counter
	GOTO ALGO

ALGO:
	ADD R[99] 1 ; add 1 to counter
	ADD R[0] R[90]
	ADD R[0] R[99]
	LD R[90] R[0]
	CMP R[99] 5
	GOTO ALGO
	EXIT
