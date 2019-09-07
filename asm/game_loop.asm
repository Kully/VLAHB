// store sprite X and Y values
LD R[220] 20  // X
LD R[221] 50  // Y 


GAME_LOOP_1:
    INPUT R[0]  // INPUT

    // put bits into seperate slots
    SHT R[0] R[24000] 0  // W
    SHT R[0] R[24001] 1  // A
    SHT R[0] R[24002] 2  // S
    SHT R[0] R[24003] 3  // D
    SHT R[0] R[24004] 4  // H
    SHT R[0] R[24005] 5  // J
    SHT R[0] R[24006] 6  // K
    SHT R[0] R[24007] 7  // L

    // EXIT
    // LD R[24003] 1

    // move mario right if you press W
    CMP R[24004] 0
    EXIT

    CLEAR
    BLIT

    // clock tick
    // CALL WAIT_N_SECONDS

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
