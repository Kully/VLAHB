// LD R[0] 11
// LD R[1] 23
// LD R[2] 33
// LD R[3] 33
// CALL LOVE_IS_HERE
// POP


LD R[0] 1          // X0
LD R[1] 5  		   // Y0
LD R[2] 7		   // X1
LD R[3] 2          // Y1
LD R[4] 0XAC80FFFF // color
PUSH

CALL DRAW_LINE
EXIT


// Draw line from (X0,Y0) to (X1,Y1)
DRAW_LINE:
	// store (X0,Y0) in VRAM
	CALL VRAM_INDEX_FROM_X_Y
	LD R[4096] R[4100]
	LD R[U] R[4]
	BLIT

	// store abs(X0-X1) in R[5]
	POP
	LD R[1] R[2]
	CALL MATH_ABS_DIFF
	LD R[5] R[4100]


	POP
	// retrieve first inputs
	EXIT


	// store abs(Y0-Y1) in R[6]
	LD R[0] R[3]
	CALL MATH_ABS_DIFF
	LD R[6] R[4100]

	// retrieve first inputs
	LD R[0] R[100]
	LD R[1] R[101]
	LD R[2] R[102]
	LD R[3] R[103]
	LD R[4] R[104]


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




DRAW_THREE_HORIZONTAL_LINES:
	LD R[0] 10
	LD R[1] 100
	LD R[2] 20
	LD R[3] 0XAC80FFFF
	CALL DRAW_HORIZONTAL_LINE

	LD R[0] 1
	LD R[1] 10
	LD R[2] 2
	LD R[3] 0XFF80FFFF
	CALL DRAW_HORIZONTAL_LINE

	LD R[0] 7
	LD R[1] 7
	LD R[2] 8
	LD R[3] 0X0000FFFF
	CALL DRAW_HORIZONTAL_LINE

	CALL SCREEN_FILL_BLACK


// Draws a line (X0,Y) to (X1, Y)
// args: X0, Y, X1, color R[0:3]
DRAW_HORIZONTAL_LINE:
	CALL VRAM_INDEX_FROM_X_Y
	LD R[4096] R[4100]

	// todo - only works when x1 > x0
	LD R[4097] R[4100]
	ADD R[4097] R[2]

	LD R[U:V] R[3]
	BLIT

	RETURN
