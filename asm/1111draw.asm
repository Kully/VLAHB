// ***********
// U := R[4096]
// V := R[4097]
// Y := R[4098]
// Z := R[4099]

// -> means "assign to" :)

// I am storing my colors starting from slot 120,000
// (there are 128,000 slots in RAM we can use)
// they can be stored anywhere, but I want them out of the
// way from VRAM

// SCREEN WIDTH := 160
// ***********


CALL LOAD_VALUES
CALL DRAW_ROWS
EXIT

LOAD_VALUES:
	LD R[4096] 4100  // U -> VRAM start_index
	LD R[4097] 4260  // V -> VRAM start_index + DISPLAY_WIDTH
	LD R[4099] 4100  // Z -> VRAM start

	// load colors
	LD R[120000] 0XFF0000FF  // load random slot RED
	LD R[120001] 0X00FF00FF  // load random slot GREEN
	LD R[120002] 0X0000FFFF  // load random slot BLUE

	LD R[4098] 120000  // Y -> slot that stores colors
	RETURN

DRAW_ROWS:
	LD R[U:V] R[Y]  // color current row
	BLIT  // update screen
	
	// ******************
	// CALL GET_DISPLAY_WIDTH_IN_PIXELS
	// ADD R[4096] R[4099]
	// ******************

	// bump U and V by DISPLAY_WIDTH
	ADD R[4096] 160
	ADD R[4097] 160
	

	// LD R[Z] R[Y]  // fill Z pixel with Y value

	GOTO DRAW_ROWS

EXIT