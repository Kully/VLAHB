// CALL STD_GET_LAST_VRAM_INDEX
// EXIT

// store sprite X and Y values
// LD R[220] 20  // X
// LD R[221] 50  // Y 


GAME_LOOP_1:
    INPUT R[0]  // INPUT

    // put bits into seperate slots
    SHT R[0] R[28000] 0  // UP
    SHT R[0] R[28001] 1  // RIGHT
    SHT R[0] R[28002] 2  // DOWN
    SHT R[0] R[28003] 3  // RIGHT
    SHT R[0] R[28004] 4  // H
    SHT R[0] R[28005] 5  // J
    SHT R[0] R[28006] 6  // K
    SHT R[0] R[28007] 7  // ESC

    // player controller
    // CMP R[28000] 0
    // CALL STD_SCREEN_FILL_GREEN
    // CMP R[28001] 0
    // CALL STD_SCREEN_FILL_BLUE
    // CMP R[28002] 0
    // CALL STD_SCREEN_FILL_RED
    // CMP R[28003] 0
    // CALL STD_SCREEN_FILL_ORANGE
    // CMP R[28004] 0
    // CALL STD_SCREEN_FILL_GREY
    CMP R[28007] 0  // ESC exits the VM
    EXIT
    CMP R[28006] 0  // END exits the VM
    EXIT

    // CLEAR 0XFF0000FF
    CALL STD_SCREEN_FILL_RED
    BLIT

    // clock tick
    WAIT

    // go to start of loop
    GOTO GAME_LOOP_1


WAIT_N_SECONDS:
    LD R[29000] 0
    WAIT_N_SECONDS_INNER_LOOP:
        ADD R[29000] 1
        CMP R[29000] 1500000
        GOTO WAIT_N_SECONDS_INNER_LOOP
    RETURN







// MAIN_MAIN_LOOP:
//  CALL WAIT_N_SECONDS
//  CALL STD_SCREEN_FILL_RED
    
//  CALL WAIT_N_SECONDS
//  CALL STD_SCREEN_FILL_RED

//  GOTO MAIN_MAIN_LOOP


// GAME_LOOP_1:
//     INPUT
//     MOVE MARIO
//     PLACE MARIO ARRAY IN VRAM
//     CLEAR SCREEN
//     BLIT
//     GOTO LOOP
// EXIT
