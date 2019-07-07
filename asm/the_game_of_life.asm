// ******************************************
// THE GAME OF LIFE
// originally written by John Conway in 1970
// ******************************************


// |N|=3
LD R[4101] 0XFFFFFFFF
LD R[4102] 0XFFFFFFFF
LD R[4103] 0XFFFFFFFF

LD R[4096] 1
LD R[4097] 0
CALL COUNT_ALIVE_NEIGHBOURS_THE_GAME_OF_LIFE
EXIT


CALL INIT_TGOL
CALL MAIN_THE_GAME_OF_LIFE

EXIT



INIT_TGOL:
	LD R[4096] 0  // U -> x index
	LD R[4097] 0  // V -> y index
	RETURN


// initial states
INIT_STATE0_THE_GAME_OF_LIFE:

INIT_STATE1_THE_GAME_OF_LIFE:

INIT_STATE2_THE_GAME_OF_LIFE:


// main
MAIN_THE_GAME_OF_LIFE:

	// ****************
	// update all cells
	// ****************

	// put (x,y) index in R[65000]
	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL VRAM_INDEX_FROM_X_Y
	LD R[65000] R[4100]


	CALL COUNT_ALIVE_NEIGHBOURS_THE_GAME_OF_LIFE





	// *************
	// update screen
	// *************
	BLIT

	// increment x and y
	// LT R[4096] 120


	GOTO MAIN_THE_GAME_OF_LIFE


// R[0] Index of RAM
INDEX_IN_DISPLAY_SCOPE:
	LD R[4100] 0 // false

	GTE R[0] 4101  // vram start: 4101
	RETURN
	LTE R[0] 23301 // vram end:   4101 + (120*160)
	RETURN

	// 4101 <= R[0] <= 23301 true
	LD R[4100] 1
	RETURN


COUNT_ALIVE_NEIGHBOURS_THE_GAME_OF_LIFE:
	// store count here:R[65002]
	LD R[65002] 0

	// Each Cell has 8 neighbours (N1 - N8)

	// 1 | 2 | 3
	// ---------
	// 8 | C | 4
	// ---------
	// 7 | 6 | 5

	// out of bounds check


	// **
	// N1
	// **

	// move to next N
	// and boundary check
	SUB R[4096] 1
	SUB R[4097] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]

	// **
	// N2
	// **

	// move to next N
	ADD R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]


	// **
	// N3
	// **

	// move to next N
	ADD R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]


	// **
	// N4
	// **

	// move to next N
	ADD R[4097] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]

	// **
	// N5
	// **

	// move to next N
	ADD R[4097] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]

	// **
	// N6
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]

	// **
	// N7
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]


	// **
	// N8
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO
	ADD R[65002] R[4100]


	// load count in return slot
	LD R[4100] R[65002]
	RETURN



// R[0]: X
// R[1]: Y
IS_VALUE_AT_XY_NOT_ZERO:
	CALL VRAM_INDEX_FROM_X_Y

	LD R[4099] R[4100]  // Z -> index
	LD R[4100] 0
	CMP R[Z] 0 // N is dead?
	LD R[4100] 1  // increase count
	RETURN


