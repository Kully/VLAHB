// // draw a line from (x0,y0) to (x1,y1)
// LD R[0] 40  // x0
// LD R[1] 110 // x1
// LD R[2] 50  // y0
// LD R[3] 30  // y1

// GOTO RAM_111:

// RAM_111:
// 	// find abs(|y0-y1|)
// 	CALL STD_MATH_ABS_DIFF
// 	EXIT

// 	RETURN
// 	// find abs(|x0-x1|)