// COLOR UTIL


// to encode rgba tuple to int
// eg. encode (255,0,255,255) to integer of ff00ffff

// R[0] 255 
// R[1] 0
// R[2] 0
// R[3] 255

// make sure the R[0:4] are not greater than 255
// play in R[4]
ENCODE_RGBA_TO_INT:
	LTE R[0] 255
	LD R[0] 255
	LTE R[1] 255
	LD R[1] 255
	LTE R[2] 255
	LD R[2] 255
	LTE R[3] 255
	LD R[3] 255

	// do the encoding math here
	LD R[4100] 0

	DIV R[0] 16

	RETURN





