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

STD_CLEAR:
	LD R[4096] 4100
	LD R[4097] 23300
	LD R[U:V] 0X000000FF
	BLIT
	RETURN


STD_SCREEN_FILL_GREY:
	LD R[23333] 0X404040FF
	LD R[4099] 23333

	LD R[4096] 4101
	LD R[4097] 43201
	LD R[U:V] R[Z]
	BLIT
	RETURN

STD_SCREEN_FILL_BLACK:
	// put last vram index in slot 4097
	CALL STD_GET_LAST_VRAM_INDEX
	LD R[4097] R[4100]

	LD R[9996] 0X000000FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[U:V] 0X000000FF

	BLIT
	RETURN


STD_SCREEN_FILL_RED:
	// put last vram index in slot 4097
	CALL STD_GET_LAST_VRAM_INDEX
	LD R[4097] R[4100]

	LD R[9996] 0XFF0000FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[4097] 23301
	LD R[U:V] R[Z]
	RETURN


STD_SCREEN_FILL_GREEN:
	// put last vram index in slot 4097
	CALL STD_GET_LAST_VRAM_INDEX
	LD R[4097] R[4100]


	LD R[9996] 0X00FF00FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[U:V] R[Z]
	RETURN


STD_SCREEN_FILL_BLUE:
	// put last vram index in slot 4097
	CALL STD_GET_LAST_VRAM_INDEX
	LD R[4097] R[4100]

	LD R[9996] 0X0000FFFF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[U:V] R[Z]
	RETURN

STD_SCREEN_FILL_ORANGE:
	CALL STD_GET_LAST_VRAM_INDEX
	LD R[4097] R[4100]

	LD R[9996] 0XFF5733FF
	LD R[4099] 9996

	LD R[4096] 4101
	LD R[U:V] R[Z]
	RETURN


STD_GET_DISPLAY_WIDTH_IN_PIXELS:
	LD R[4100] 160
	RETURN


// UPDATE DISPLAY HEIGHT TO 144 for gameboy res
STD_GET_DISPLAY_HEIGHT_IN_PIXELS:
	LD R[4100] 120
	RETURN

// R[0] -> X
// R[1] -> Y
STD_VRAM_INDEX_FROM_X_Y:
	LD R[4100] 160  // STD_GET_DISPLAY_WIDTH_IN_PIXELS
	MUL R[4100] R[1]
	ADD R[4100] R[0]
	ADD R[4100] 4101  // should be LD
	RETURN

STD_X_FROM_VRAM_INDEX:
	SUB R[0] 4101 // sub VRAM start_idx
	LD R[1] 160
	CALL STD_MATH_DIV_REMAINDER
	RETURN

STD_Y_FROM_VRAM_INDEX:
	SUB R[0] 4101 // sub VRAM start_idx
	LD R[1] 160
	CALL STD_MATH_FLOOR_DIV
	RETURN

STD_GET_LAST_VRAM_INDEX:
	CALL STD_GET_DISPLAY_WIDTH_IN_PIXELS
	LD R[4099] R[4100]
	CALL STD_GET_DISPLAY_HEIGHT_IN_PIXELS
	MUL R[4100] R[4099]
	ADD R[4100] 4101
	RETURN

STD_DRAW_INFINITE_LINE_FROM_TOP_LEFT:
	// load indices in U,V
	LD R[4096] 4100
	LD R[4097] 4260

	// store x=0 and y=0 far from VLAHB
	LD R[63000] 0
	LD R[63001] 0

		STD_MAIN_DRAW_INFINITE_LINE_FROM_TOP_LEFT:
		// load (x,y) in U
		LD R[0] R[63000]
		LD R[1] R[63001]
		CALL STD_VRAM_INDEX_FROM_X_Y
		LD R[4096] R[4100]

		LD R[U] 0XAC80FFFF
		BLIT

		// increment x and y
		ADD R[63000] 1
		ADD R[63001] 1

		GOTO STD_MAIN_DRAW_INFINITE_LINE_FROM_TOP_LEFT


// R[0] -> X
// R[1] -> Y
// R[2] -> len of line
// R[3] -> COLOR
// TOOD: WIP
STD_DRAW_LINE_FROM_X_Y_DOWN:
	CALL STD_VRAM_INDEX_FROM_X_Y
	LD R[4096] R[4100]  // VRAM idx

	LD R[U] R[3]  // load
	SUB R[2] 1  // decr
	LTE R[2] 0  // compare
	GOTO STD_DRAW_LINE_FROM_X_Y_DOWN
	RETURN


// var STD_MATH_ADD(var a, var b)
// {
//     a += b
//     return a
// }
STD_MATH_ADD:
    ADD R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var STD_MATH_SUB(var a, var b)
// {
//     a -= b
//     return a
// }
STD_MATH_SUB:
    SUB R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var STD_MATH_MUL(var a, var b)
// {
//     a *= b
//     return a
// }
STD_MATH_MUL:
    MUL R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var STD_MATH_DIV(var a, var b)
// {
//     a /= b
//     return a
// }
STD_MATH_DIV:
    DIV R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var STD_MATH_LONG_WINDED(var a, var b)
// {
//     b = STD_MATH_ADD(a, b)
//     b = STD_MATH_ADD(a, b)
//     b = STD_MATH_ADD(a, b)
//     b = STD_MATH_ADD(a, b)
//     return b//
// }
STD_MATH_LONG_WINDED:
    CALL STD_MATH_ADD
    LD R[1] R[4100] // 15
    CALL STD_MATH_ADD
    LD R[1] R[4100] // 25
    CALL STD_MATH_ADD
    LD R[1] R[4100] // 35
    CALL STD_MATH_ADD
    RETURN // 45


// TODO: what should happen if you divide by 0?

// Python: R[0] // R[1]
STD_MATH_FLOOR_DIV:
    GTE R[0] R[1]
    RETURN
    ADD R[4100] 1
    SUB R[0] R[1]
    GOTO STD_MATH_FLOOR_DIV

// Python: R[0] mod R[1]
STD_MATH_DIV_REMAINDER:
    CALL STD_MATH_FLOOR_DIV
    LD R[3] R[1]
    MUL R[3] R[4100]
    
    LD R[4] R[0]
    SUB R[4] R[3]  // stack underflow
    
    LD R[4100] R[4]
    RETURN

// Python: R[0] // 16
STD_MATH_FLOOR_DIV_16:
    GTE R[0] 16
        RETURN
    ADD R[4100] 1
    SUB R[0] 16
    GOTO STD_MATH_FLOOR_DIV_16

// Python: R[0] % 16
STD_MATH_DIV_REMAINDER_16:
    CALL STD_MATH_FLOOR_DIV_16
    LD R[3] 16
    MUL R[3] R[4100]
    
    LD R[4] R[0]
    SUB R[4] R[3]  // stack underflow
    
    LD R[4100] R[4]
    RETURN

// R[0]: X
// R[1]: Y
// Returns abs(X-Y)
STD_MATH_ABS_DIFF:
    LTE R[0] R[1]
    GOTO MATH_ABS_DIFF_LTE_FALSE
    LD R[4100] R[1]
    SUB R[4100] R[0]
    RETURN

    MATH_ABS_DIFF_LTE_FALSE:
        LD R[4100] R[0]
        SUB R[4100] R[1]
        RETURN

    RETURN


STD_LOGIC_OR:
	LD R[4100] 1
	CMP R[0] 0
	RETURN
	CMP R[1] 0
	RETURN
	LD R[4100] 0
	RETURN


STD_LOGIC_AND:
 	// count num of 1s in R[4]
	LD R[4100] 0

	CMP R[0] 0
	ADD R[4] 1

	CMP R[1] 0
	ADD R[4] 1

	CMP R[4] 2
	RETURN
	LD R[4100] 1
	LD R[4] 0  // reset R[4] to 0
	RETURN

STD_LOGIC_NOT:
	CMP R[0] 0
	LD R[4100] 0
	LD R[4100] 1
	RETURN

