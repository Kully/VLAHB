// ******************************************
// THE GAME OF LIFE
// originally written by John Conway in 1970
// ******************************************

// if N < 2 or N > 3
LD R[42502] 6
LD R[0] 0
LD R[1] 0
GTE R[42502] 2
LD R[0] 1
LTE R[42502] 3
LD R[1] 1
CALL LOGIC_OR
EXIT




// spare slots: 42501+

// (x,y) = (2,7)
R[4096] = 2
R[4097] = 7


// Y -> index for cell state (VRAM2)
// R[4098] -> 120*160 + vram_idx
LD R[4098] 120
MUL R[4098] 160

LD R[0] R[4096]
LD R[1] R[4097]
CALL VRAM_INDEX_FROM_X_Y
ADD R[4098] R[4100]



// ***********
// compute |N|

// CALL COUNT_ALIVE_NEIGHBOURS_THE_GAME_OF_LIFE
// R[4100] -> 3, say

// LD R[42502] R[4100]

// ***********





// decide what to do with |N|
// R[42502] -> N

CALL RETURN_1_IF_GREATER_THAN_ZER0_ELSE_0
LD R[Y] R[4100]  // store 0 or 1 in R[ idx + 120*160 ]


// transition logic


// if N < 2 or N > 3 - // copied above!!!
// ...



// if R[Y] == 1:
// 	if N < 2 or N > 3:
// 		LD R[Y] 0

// elif R[Y] == 0:
// 	if N == 3:
// 		LD R[Y] 1


EXIT


// |N|=3
LD R[4101] 0XFFFFFFFF
LD R[4102] 0XFFFFFFFF
LD R[4103] 0XFFFFFFFF

LD R[4096] 1
LD R[4097] 0
CALL COUNT_ALIVE_NEIGHBOURS_THE_GAME_OF_LIFE
EXIT


// ***********
// STARTS HERE
// ***********

// init stuff
CALL INIT_THE_GAME_OF_LIFE
CALL SEED0_THE_GAME_OF_LIFE

// game loop
CALL MAIN_LOOP_THE_GAME_OF_LIFE

EXIT



INIT_THE_GAME_OF_LIFE:
	LD R[4096] 0  // U -> x index
	LD R[4097] 0  // V -> y index
	RETURN


// initial states
SEED0_THE_GAME_OF_LIFE:
	RETURN

SEED1_THE_GAME_OF_LIFE:
	RETURN
	

SEED2_THE_GAME_OF_LIFE:
	RETURN

// main
MAIN_LOOP_THE_GAME_OF_LIFE:

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


	GOTO MAIN_LOOP_THE_GAME_OF_LIFE



// **************
// util functions
// **************


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

RETURN_1_IF_GREATER_THAN_ZER0_ELSE_0:
	LD R[4100] 1
	GT R[0] 0
	SUB R[4100] 1
	RETURN
