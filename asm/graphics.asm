// Display: 160 X 120
// Slots for Display: R[4101:43201]

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


BLACK_SCREEN_FILL:
	LD R[9996] 0X000000FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[4097] 43201
	LD R[U:V] R[Z]
	BLIT
	RETURN


RED_SCREEN_FILL:
	LD R[9996] 0XFF0000FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[4097] 43201
	LD R[U:V] R[Z]
	BLIT
	RETURN


GREEN_SCREEN_FILL:
	LD R[9996] 0X00FF00FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[4097] 43201
	LD R[U:V] R[Z]
	BLIT
	RETURN


BLUE_SCREEN_FILL:
	LD R[9996] 0X00FF00FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[4097] 43201
	LD R[U:V] R[Z]
	BLIT
	RETURN


GET_DISPLAY_WIDTH_IN_PIXELS:
	LD R[4100] 160
	RETURN


GET_DISPLAY_HEIGHT_IN_PIXELS:
	LD R[4100] 120
	RETURN


VRAM_INDEX_FROM_X_Y:
	LD R[4100] 160  // GET_DISPLAY_WIDTH_IN_PIXELS
	MUL R[4100] R[1]
	ADD R[4100] R[0]
	ADD R[4100] 4101
	RETURN


DRAW_INFINITE_LINE_FROM_TOP_LEFT:
	// load indices in U,V
	LD R[4096] 4100
	LD R[4097] 4260

	// store x=0 and y=0 far from VLAHB
	LD R[63000] 0
	LD R[63001] 0

		MAIN_DRAW_INFINITE_LINE_FROM_TOP_LEFT:
		// load (x,y) in U
		LD R[0] R[63000]
		LD R[1] R[63001]
		CALL VRAM_INDEX_FROM_X_Y
		LD R[4096] R[4100]

		LD R[U] 0XAC80FFFF
		BLIT

		// increment x and y
		ADD R[63000] 1
		ADD R[63001] 1

		GOTO MAIN_DRAW_INFINITE_LINE_FROM_TOP_LEFT

