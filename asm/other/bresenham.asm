LD R[0] 1          // X0
LD R[1] 5  		   // Y0
LD R[2] 7		   // X1
LD R[3] 2          // Y1
LD R[4] 0XAC80FFFF // color
PUSH

CALL DRAW_LINE
EXIT


// Draw line from (X0,Y0) to (X1,Y1)
// R[0] X0
// R[1] Y0
// R[2] X1
// R[3] Y1
// R[4] color
DRAW_LINE:
	// store (X0,Y0) in VRAM
	CALL STD_VRAM_INDEX_FROM_X_Y
	LD R[4096] R[4100]
	LD R[U] R[4]
	BLIT

	// store abs(X0-X1) in R[5]
	POP
	LD R[1] R[2]
	CALL STD_MATH_ABS_DIFF
	LD R[5] R[4100]

	POP

	// store abs(Y0-Y1) in R[6]
	LD R[0] R[3]
	CALL STD_MATH_ABS_DIFF
	LD R[6] R[4100]

	POP
	EXIT

	// Load Sign of sign(X1-X0) R[7]
	// 0 == neg
	// 1 == pos
	LD R[7] 1
	LTE R[2] R[0]
	SUB R[7] 1

	// Load Sign of sign(X1-X0) R[7]
	// 0 == neg
	// 1 == pos
	LD R[8] 1
	LTE R[3] R[1]
	SUB R[8] 1

	// determine min{abs(X0-X1), abs(Y0-Y1)}


	RETURN