// COLOR UTIL


// to encode rgba tuple to int
// eg. encode (255,0,255,255) to integer of ff00ffff

// R[0] 255 
// R[1] 0
// R[2] 0
// R[3] 255

// make sure the R[0:4] are not greater than 255
// play in R[4]

ENCODE_RGBA_TO_INT_FOO_BAR:
	LTE R[0] 255
	LD R[0] 255
	LTE R[1] 255
	LD R[1] 255
	LTE R[2] 255
	LD R[2] 255
	LTE R[3] 255
	LD R[3] 255

	// encoding math below
	LD R[1] 16
	CALL MATH_FLOOR_DIV
	LD R[4] R[4100]

	LD R[1] 16
	CALL MATH_DIV_REMAINDER
	LD R[5] R[4100]



	RETURN
