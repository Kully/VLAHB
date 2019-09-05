// fill screen with red
LD R[4096] 4100
LD R[4097] 23300
LD R[U:V] 0X00FF00FF

LD SPRITE_SMB_MARIO_SMALL_STAND_RIGHT_ALPHA0 6 2 32 32
BLIT
AGHDAGSDGAHJSDKJHASGDKJAHSGDKJHASDASD:
	GOTO AGHDAGSDGAHJSDKJHASGDKJAHSGDKJHASDASD


// Y points to color
LD R[4098] 65000

// init variables
LD R[65000] 0X30FA00FF  // ball color
LD R[65001] 1  // ball X coord
LD R[65002] 1  // ball Y coord

// ball velocity
// 0 is +
// 1 is -
LD R[65003] 0  // X velo
LD R[65004] 1  // Y velo


BALL_BOUNCING_OFF_WALLS_MAIN:

	// ***************
	// collision logic
	// ***************

	// ** X - right wall
	LT R[65001] 158  // screen width - 1
	LD R[65003] 0
	// ** X - left wall
	GT R[65001] 2
	LD R[65003] 1

	// ** Y - bottom wall
	LT R[65002] 118  // screen height
	LD R[65004] 0
	// ** Y - top wall
	GT R[65002] 2
	LD R[65004] 1

	// ************************************
	// update ball coords based on velocity
	// ************************************
	// ** X
	GT R[65003] 0
	SUB R[65001] 2
	ADD R[65001] 1
	// ** Y
	GT R[65004] 0
	SUB R[65002] 2
	ADD R[65002] 1


	// ****************
	// fetch vram index
	// ****************
	LD R[0] R[65001]
	LD R[1] R[65002]
	CALL VRAM_INDEX_FROM_X_Y

	LD R[4099] R[4100] // Z -> vram_index

	// ****
	// draw
	// ****

	LD R[4096] 4100
	LD R[4097] 23300
	LD R[U:V] 0X000000FF

	LD R[Z] R[Y] // load color in display

	BLIT

	GOTO BALL_BOUNCING_OFF_WALLS_MAIN



EXIT