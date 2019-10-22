// >>>>>>>>>>>>
LD R[35000] 16
// >>>>>>>>>>>>

// subtracting amount
LD R[35001] 16
SUB R[35001] R[35000]

OK_GAME_LOOP:
	INPUT R[0]
    SHT R[0] R[28000] 0  // UP
    SHT R[0] R[28001] 1  // LEFT
    SHT R[0] R[28002] 2  // DOWN
    SHT R[0] R[28003] 3  // RIGHT
    SHT R[0] R[28004] 4  // Z
    SHT R[0] R[28005] 5  // X
    SHT R[0] R[28006] 6  // END
    SHT R[0] R[28007] 7  // ESC

    // exit if ESC pressed
    CMP R[28006] 0
        EXIT
    CMP R[28007] 0
        EXIT

    // left
    CMP R[28001] 0
    SUB R[35000] 1

    // right
    CMP R[28003] 0
    ADD R[35000] 1



	CALL STD_SCREEN_FILL_BLACK


    // transfer vars to smaller slots
    LD R[7] R[35000]
    LD R[8] R[35001]

    LD R[4096] SPRITE_TETRIS_BKGD_STRIP_16_144
    LD R[1] 0      // X
    LD R[2] 0      // Y
    LD R[3] R[7]   // W
    LD R[4] 144    // H
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // X
    SUB R[2] R[8]  // Y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // X
    SUB R[2] R[8]  // Y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // X
    SUB R[2] R[8]  // Y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // X
    SUB R[2] R[8]  // Y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // X
    SUB R[2] R[8]  // Y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // x
    SUB R[2] R[8]  // y
    LD R[U] R[1] R[2] R[3] R[4]

    ADD R[1] R[7]  // x
    SUB R[2] R[8]  // y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // x
    SUB R[2] R[8]  // y
    LD R[U] R[1] R[2] R[3] R[4]
    
    ADD R[1] R[7]  // x
    SUB R[2] R[8]  // y
    LD R[U] R[1] R[2] R[3] R[4]


    BLIT
    WAIT
	GOTO OK_GAME_LOOP

EXIT