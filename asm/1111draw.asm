// GOTO FLASHING_LIGHTS
// GOTO NEON_SIREN
GOTO KILL_BILL

KILL_BILL:
	LD R[R[4098]] 4101
	LD R[R[4099]] 4200
	LD R[45124] 0XFF0000FF  // red

	// LD R[4101:Z] R[45124]
	LD R[4101:R[4099]] R[45124]
	BLIT
	CALL BLACK_SCREEN_CLEAR

	GOTO KILL_BILL


FLASHING_LIGHTS:
	// load slots with color values
	LD R[45120] 0X12d3cfff
	LD R[45121] 0X67eacaff
	LD R[45122] 0Xb0f4e6ff
	LD R[45123] 0XFCF9ECFF
	LD R[45123] 0XFCF9ECFF
	LD R[45124] 0XFF0000FF  // red

	LD R[U] 4101 // vram starts
	CALL GET_DISPLAY_WIDTH_IN_PIXELS
	LD R[V] R[4100]
	ADD R[V] 4101

	// draw line 1
	LD R[U:V] R[45124]
	LD R[U:V] R[45124]
	LD R[U:V] R[45124]
	LD R[U:V] R[45124]
	BLIT

	CALL BLACK_SCREEN_CLEAR

	GOTO FLASHING_LIGHTS
EXIT


NEON_SIREN:
	LD R[45123] 0XFCF9ECFF

	LD R[9000:10000] R[45123]

	BLIT

	LD R[46000] 4  // start a counter up to 255

// TODO: allow tab spacing for labels

    // 
    NEON_SIREN_LOOP:
        // lower the opacity of the image by 1
		ADD R[46000] 1
		SUB R[45123] 150
		LD R[9000:10000] R[45123]
		BLIT
		CMP R[46000] 2
		GOTO NEON_SIREN_LOOP
		EXIT

	GOTO NEON_SIREN




EXIT