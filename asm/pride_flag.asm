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
	LD R[4097] 4261  // V -> VRAM start_index + DISPLAY_WIDTH

	// load colors in RAM slots
	LD R[65000] 0XE70000FF  // load RED
	LD R[65001] 0XFF8C00FF  // load ORANGE
	LD R[65002] 0XFFEF00FF  // load YELLOW
	LD R[65003] 0X00811FFF  // load GREEN
	LD R[65004] 0X0044FFFF  // load BLUE
	LD R[65005] 0X760089FF  // load PURPLE

	LD R[4098] 65000  // Y -> slot that stores colors

	LD R[9999] 0  // counter for color change

	RETURN

DRAW_ROWS:
	ADD R[9999] 1

	CALL DECIDE_COLOR

	LD R[U:V] R[Y]  // color current row
	BLIT

	// bump U and V by DISPLAY_WIDTH
	ADD R[4096] 160
	ADD R[4097] 160

	GOTO DRAW_ROWS


DECIDE_COLOR:
	LT R[9999] 10
	LD R[4098] 65001

	LT R[9999] 20
	LD R[4098] 65002

	LT R[9999] 30
	LD R[4098] 65003

	LT R[9999] 40
	LD R[4098] 65004

	LT R[9999] 50
	LD R[4098] 65005

	RETURN


EXIT