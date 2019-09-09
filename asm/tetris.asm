// **********
// * TETRIS *
// **********


// ======
//  INIT 
// ======

LD R[0] ROTATE_ACTIVE_PIECE:
EXIT


// set active piece variables and define constants for it
LD R[30000] 100  // init X pos
LD R[30001] 0  // init Y pos
LD R[30002] 3  // width from GIMP
LD R[30003] 2  // height from GIMP
// automate these!!
LD R[30004] 24  // width in pixels
LD R[30005] 16  // height in pixels

// slots that store if key is held
LD R[40000] 0  // UP    held
LD R[40001] 0  // LEFT  held
LD R[40002] 0  // DOWN  held
LD R[40003] 0  // RIGHT held
LD R[40004] 0  // Z     held
LD R[40005] 0  // X     held

// R[U]: pointer to active piece function, say

// R[50000:] - boundary information

GOTO TETRIS_MAIN_LOOP


TETRIS_MAIN_LOOP:
    
	// STORE BUTTON BITS IN REGISTERS

    INPUT R[0]
    SHT R[0] R[28000] 0  // UP
    SHT R[0] R[28001] 1  // LEFT
    SHT R[0] R[28002] 2  // DOWN
    SHT R[0] R[28003] 3  // RIGHT
    SHT R[0] R[28004] 4  // Z
    SHT R[0] R[28005] 5  // X
    SHT R[0] R[28006] 6  // END
    SHT R[0] R[28007] 7  // ESC

    // EXIT VM if ESC or END key is pressed
    CMP R[28006] 0
    EXIT
    CMP R[28007] 0
    EXIT

    // move piece - X direction
    CMP R[28001] 0
    SUB R[30000] 1  // move piece left
    CMP R[28003] 0
    ADD R[30000] 1  // move piece right

    // rotate piece - Z
    // CMP R[28004] 0
    // CALL ROTATE_ACTIVE_PIECE

    
    CALL STD_SCREEN_FILL_BLACK  // clear screen

    // *********************
    // PLACE SPRITES IN VRAM
    // *********************
    // Note: move values in high slots to slots < 255
    // so that opcode can work correctly

    LD R[0] 0
    LD R[1] 0
    LD TETRIS_GAMEBOY_BACKGROUND R[0] R[1] 160 144

    LD R[240] R[30000]
    LD R[241] R[30001]
    LD SPRITE_TETRIS_TETROMINO_S_ROT0_X8 R[240] R[241] 24 16

    BLIT  // draw to screen
    WAIT  // wait 17 ms

    // increment counter
    ADD R[65535] 1
    LTE R[65535] 1
    CALL FIRE_LOGIC_EVERY_N_FRAMES

    GOTO TETRIS_MAIN_LOOP

EXIT




// ======
//  UTIL
// ======

FIRE_LOGIC_EVERY_N_FRAMES:
    // -----------------------------------------------
    // this function resets a counter that goes up by
    // count per frame (17ms) and then resets it to 0
    // once it hits some number N (see the function in
    // the main loop). Triggers logic too
    // -----------------------------------------------
    LD R[65535] 0  // reset counter at R[65535] to 0

    // store (pieceHeight + pieceYpos) in R[45678]
    LD R[45678] R[30001] // load piece Y pos
    ADD R[45678] R[30005] // add piece height in px

    // check if bottom of piece is lower than bottom of screen
    LT R[45678] 144
    LD R[30001] 0 // if >= 160, place piece on board
    ADD R[30001] 1  // move active tetromino down 1 pixel

    RETURN


ROTATE_ACTIVE_PIECE:
    RETURN
