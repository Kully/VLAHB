CLEAR 0X5907A3FF

// short loop
SHOGHIG_LOOP:
ADD R[0] 1
CMP R[0] 10000
GOTO SHOGHIG_LOOP
EXIT

// let's try to do alpha of 0
CLEAR 0XFF0000FF
LD SPRITE_SMB_MARIO_SMALL_STAND_RIGHT_ALPHA0 0 0 32 32
BLIT
// EXIT

AJASKJDHGAKSJDHGASKJHDGAKJHSDGJKASDGKJAHSD:
	GOTO AJASKJDHGAKSJDHGASKJHDGAKJHSDGJKASDGKJAHSD


CALL SCREEN_FILL_GREY
MARIO_SNES_FLYING_GIF_LOOP:
	LD SPRITE_SNES_CAPE_MARIO_RIGHT_0 2 17 28 28
	BLIT
	// target -> 100ms
	LD R[0] 0
	TIME_SLEEP0:
		ADD R[0] 1
		GT R[0] 60
		GOTO TIME_SLEEP0


	LD SPRITE_SNES_CAPE_MARIO_RIGHT_1 2 17 28 28
	BLIT

	// target -> 400ms
	LD R[0] 0
	TIME_SLEEP1:
		ADD R[0] 1
		GT R[0] 240
		GOTO TIME_SLEEP1


	LD SPRITE_SNES_CAPE_MARIO_RIGHT_2 2 17 28 28
	BLIT

	// target -> 100ms
	LD R[0] 0
	TIME_SLEEP2:
		ADD R[0] 1
		GT R[0] 60
		GOTO TIME_SLEEP2

	LD SPRITE_SNES_CAPE_MARIO_RIGHT_3 2 17 28 28
	BLIT

	// target -> 100ms
	LD R[0] 0
	TIME_SLEEP3:
		ADD R[0] 1
		GT R[0] 60
		GOTO TIME_SLEEP3

	GOTO MARIO_SNES_FLYING_GIF_LOOP
