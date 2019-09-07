// CALL STD_GET_LAST_VRAM_INDEX
// EXIT

// store sprite X and Y values
// LD R[220] 20  // X
// LD R[221] 50  // Y 

// LD R[4100] 0X00FF00FF
// LD R[4096] 4101
// LD R[4097] 23299
// LD R[U:V] 0XFF0000FF
// LD R[23298] 0X00FF00FF
// BLIT


GAME_LOOP_1:
    INPUT R[0]  // INPUT

    // put bits into seperate slots
    SHT R[0] R[24000] 0  // UP
    SHT R[0] R[24001] 1  // RIGHT
    SHT R[0] R[24002] 2  // DOWN
    SHT R[0] R[24003] 3  // RIGHT
    SHT R[0] R[24004] 4  // H
    SHT R[0] R[24005] 5  // J
    SHT R[0] R[24006] 6  // K
    SHT R[0] R[24007] 7  // ESC

    CMP R[24000] 0
    CALL STD_SCREEN_FILL_GREEN
    CMP R[24001] 0
    CALL STD_SCREEN_FILL_BLUE
    CMP R[24007] 0  // ESC exits the VM
    EXIT

    // CLEAR
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
