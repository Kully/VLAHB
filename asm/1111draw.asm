// Display: 160 X 120
// Slots for Display: R[4100:43200]

// ******
// Colors
// ******

// 0XFF0000FF - Red
// 0X00FF00FF - Green
// 0X0000FFFF - Blue
// 0X000000FF - Black
// 0XFAFAFAFF - Light Grey
// 0X333333FF - Dark Grey

// colorhunt - easter colors
// *************************
// 0Xfcf9ecff - faded baige
// 0Xb0f4e6ff - cool blue
// 0X67eacaff - clean green
// 0X12d3cfff - ocean blue




BLACK_SCREEN_CLEAR:
	LD R[9996] 0X000000FF
	LD R[4100:43200] R[9996]
	BLIT
	RETURN


GET_DISPLAY_WIDTH_IN_PIXELS:
	LD R[4099] 160
	RETURN

GET_DISPLAY_HEIGHT_IN_PIXELS:
	LD R[4099] 120
	LD R[4099] 

// R[0:1] X, Y
VRAM_INDEX_FROM_X_Y:
	// CALL GET_DISPLAY_WIDTH_IN_PIXELS
	LD R[4099] 160
	MUL R[4099] R[1]
	ADD R[4099] R[0]
	ADD R[4099] 4100
	RETURN


DRAW_A_PICTURE:
	// load slots with color values
	LD R[43100] 0Xfcf9ecff
	LD R[43101] 0Xb0f4e6ff
	LD R[43101] 0X67eacaff
	LD R[43101] 0X12d3cfff




	// draw stuff
	LD R[0] 2
	LD R[1] 2
	CALL VRAM_INDEX_FROM_X_Y

	CALL BLACK_SCREEN_CLEAR

	GOTO DRAW_A_PICTURE



EXIT
