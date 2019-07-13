// ******************************************
// THE GAME OF LIFE
// originally written by John Conway in 1970
// ******************************************
// spare slots: 42501+
// [---functions---][UVYZ][----VRAM----][---VRAM2---][42501-----192000]

// A12394876:
// 	GOTO A12394876

LD R[0] 1

0X00020002
// 0X00000002

0XFFFFFFFF
0XFFFFFFFA




// LD R[0] R[1] MARIO 44

// LD R[42502] 5

// LD R[0] 1
// LD R[1] 1
// CMP R[42502] 2
// LD R[0] 0
// CMP R[42502] 3
// LD R[1] 0
// CALL LOGIC_OR

// LD R[0] R[4100]
// CALL LOGIC_NOT
// EXIT


// LD R[0] 0
// LD R[1] 0
// GTE R[42502] 2
// LD R[0] 1
// LTE R[42502] 3
// LD R[1] 1
// CALL LOGIC_OR
// EXIT


CALL RESET_POINTERS_THE_GAME_OF_LIFE

LD R[4101] 0  //XFFFFFFFF

// N == 2 doesnt work
LD R[42502] 8 // N
CALL TRANSITION_LOGIC_GAME_OF_LIFE

EXIT




// ******************
// THE GAME OF LIFE *
// ******************

// *** reset varaibles
CALL RESET_POINTERS_THE_GAME_OF_LIFE

// *** load VRAM with seed data
LD R[13781] 0XFFFFFFFF
LD R[13941] 0XFFFFFFFF
LD R[14101] 0XFFFFFFFF

LD R[13783] 0XFFFFFFFF
LD R[13943] 0XFFFFFFFF
LD R[14103] 0XFFFFFFFF

BLIT

// *** main loop
CALL MAIN_LOOP_THE_GAME_OF_LIFE
EXIT




MAIN_LOOP_THE_GAME_OF_LIFE:
	// generate x,y from VRAM index

	// R[4096] -> x
	// R[4097] -> y
	
	LD R[0] R[4099]
	CALL X_FROM_VRAM_INDEX
	LD R[4096] R[4100]  // U -> x

	LD R[0] R[4099]
	CALL Y_FROM_VRAM_INDEX
	LD R[4097] R[4100]  // V -> y


	// *** find N 

	// LD R[0] R[4096] // x
	// LD R[1] R[4097] // y
	// CALL COUNT_LIVE_NEIGHBOURS_THE_GAME_OF_LIFE
	// LD R[42502] R[4100]  // store N in R[42502]

	// store N in R[42502]
	LD R[42502] 3


	// *** transition logic

	LD R[0] R[4099]  // VRAM idx
	CALL RETURN_1_IF_GREATER_THAN_ZER0_ELSE_0
	LD R[Y] R[4100]  // CURRENT state -> VRAM2


	LD R[0] R[4099]
	CALL TRANSITION_LOGIC_GAME_OF_LIFE  // UPDATED cell state -> VRAM2

	// multiply 0XFFFFFFFF by RAM[VRAM2]

	// increment VRAM_idx and VRAM2_idx
	ADD R[4098] 1  // VRAM2 idx++
	ADD R[4099] 1  // VRAM idx++

	GTE R[4099] 23301  // last idx of VRAM...
		GOTO MAIN_LOOP_THE_GAME_OF_LIFE

	
	BLIT
	// reset variables: (x,y) -> (0,0)
	CALL RESET_POINTERS_THE_GAME_OF_LIFE
	GOTO MAIN_LOOP_THE_GAME_OF_LIFE







// ***************
// other functions
// ***************


RESET_POINTERS_THE_GAME_OF_LIFE:
	LD R[4096] 0  // U -> x=0
	LD R[4097] 0  // V -> y=0

	LD R[4098] 160
	MUL R[4098] 120
	ADD R[4098] 4101  // Y -> VRAM2 idx

	LD R[4099] 4101 // Z -> VRAM idx

	RETURN


SEED1_THE_GAME_OF_LIFE:
	LD R[4101:4200] 0XFF0000FF
	RETURN


SEED2_THE_GAME_OF_LIFE:
	RETURN

	
SEED3_THE_GAME_OF_LIFE:
	RETURN


// R[0]: Index of RAM
INDEX_IN_DISPLAY_SCOPE:
	LD R[4100] 0

	GTE R[0] 4101  // vram start: 4101
	RETURN
	LTE R[0] 23301 // vram end:   4101 + (120*160)
	RETURN

	// 4101 <= R[0] <= 23301 passes
	LD R[4100] 1
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
	LD R[4100] 0
	RETURN


TRANSITION_LOGIC_GAME_OF_LIFE:
	// ************************************
	// transition logic
	//
	// R[Y] -> UPDATED state of cell in R[Y]
	//
	// R[42502] -> N
	// R[Y] -> cell state in VRAM2
	//
	// GAME RULES
	// if alive and (N<2 or N>3), cell dead
	// if dead and N == 3, cell alive
	// ************************************

	// return (N<2 or N>3) boolean

	// LD R[0] 0
	// LD R[1] 0
	// GTE R[42502] 2
	// LD R[0] 1
	// LTE R[42502] 3
	// LD R[1] 1
	// CALL LOGIC_OR


	LD R[0] 1
	LD R[1] 1
	CMP R[42502] 2
	LD R[0] 0
	CMP R[42502] 3
	LD R[1] 0
	CALL LOGIC_OR

	LD R[0] R[4100]
	CALL LOGIC_NOT




	LD R[0] R[4100]  // (N<2 or N>3)
	LD R[4099] 1
	LD R[Z] R[Y]  // cell alive

	// R[0]: (N < 2 or N > 3)
	// R[1]: (cell_state {0,1})
	CALL LOGIC_AND

	CMP R[4100] 0
	LD R[Y] 0
	CMP R[Y] 0
	RETURN  // leave if cell is alive
	CMP R[42502] 3
	RETURN
	LD R[Y] 1  // revive cell if N == 3

	RETURN


COUNT_LIVE_NEIGHBOURS_THE_GAME_OF_LIFE:
	// store count here:R[12]
	// LD R[65002] 0
	LD R[12] 0
	PUSH

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
	
	// ADD R[65002] R[4100]
	POP
	ADD R[12] R[4100]
	PUSH

	// **
	// N2
	// **

	// move to next N
	ADD R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]
	PUSH


	// **
	// N3
	// **

	// move to next N
	ADD R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]
	PUSH


	// **
	// N4
	// **

	// move to next N
	ADD R[4097] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]
	PUSH

	// **
	// N5
	// **

	// move to next N
	ADD R[4097] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]
	PUSH

	// **
	// N6
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]
	PUSH

	// **
	// N7
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO


	POP
	ADD R[12] R[4100]
	PUSH


	// **
	// N8
	// **

	// move to next N
	SUB R[4096] 1

	LD R[0] R[4096]
	LD R[1] R[4097]
	CALL IS_VALUE_AT_XY_NOT_ZERO

	POP
	ADD R[12] R[4100]


	// load count in return slot
	LD R[4100] R[12]
	RETURN

