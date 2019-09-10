// **********
// * TETRIS *
// **********

//  0000 - 4095: functions + misc
//  4096 - 4099: pointers U,V,Y,Z
//  4100 -27140: VRAM

// CONSTANTS
// 30000: X pos of piece when spawning at top
// 30001: Y pos of piece when spawning at top

// *** active piece
// 30003: pc of active piece
// 30004: width of active piece (pixels)
// 30005: height of active piece in (pixels)


// O
// ---------
// 30100: pc
// 30101: W
// 30102: H
LD R[30100] SPRITE_TETRIS_TETROMINO_O
LD R[30101] 16
LD R[30102] 16


// S
// ---------
// rot0
// 30103: pc
// 30104: W
// 30105: H

// rot1
// 30106: pc
// 30107: W
// 30108: H



// Z
// ---------
// rot0
// 30109: pc
// 30110: W
// 30111: H

// rot1
// 30112: pc
// 30113: W
// 30114: H



// T
// ---------
// rot0
// 30115: pc
// 30116: W
// 30117: H

// rot1
// 30118: pc
// 30119: W
// 30120: H

// rot2
// 30121: pc
// 30122: W
// 30123: H

// rot3
// 30124: pc
// 30125: W
// 30126: H



// I
// ---------
// rot0
// 30127: pc
// 30128: W
// 30129: H

// rot1
// 30130: pc
// 30131: W
// 30132: H



// L
// ---------
// rot0
// 30133: pc
// 30134: W
// 30135: H

// rot1
// 30136: pc
// 30137: W
// 30138: H

// rot2
// 30139: pc
// 30140: W
// 30141: H

// rot3
// 30142: pc
// 30143: W
// 30144: H



// J
// ---------
// rot0
// 30145: pc
// 30146: W
// 30147: H

// rot1
// 30148: pc
// 30149: W
// 30150: H

// rot2
// 30151: pc
// 30152: W
// 30153: H

// rot3
// 30154: pc
// 30155: W
// 30156: H


// COUNTERS

// 65534: value to help keep piece moving only once per keypress
// 65535: counter for gravity <- MAX VALUE



// ======
//  INIT 
// ======

// constants

// playfield dimensions - 10 tetris cells wide 80px wide
LD R[50000] 16 // playfield: left X pos
LD R[50001] 96 // playfield: right X pos

// slots that store if key is held
LD R[40000] 0  // UP    held
LD R[40001] 0  // LEFT  held
LD R[40002] 0  // DOWN  held
LD R[40003] 0  // RIGHT held
LD R[40004] 0  // Z     held
LD R[40005] 0  // X     held

// pos of piece when spawning
LD R[30000] 48  // X pos of piece when spawning at top
LD R[30001]  0  // Y pos of new piece when spawning at top


CALL LOAD_NEW_TETRIS_PIECE_AT_TOP_OF_PLAYFIELD

GOTO TETRIS_MAIN_LOOP
TETRIS_MAIN_LOOP:

	// load inputs

    INPUT R[0]
    SHT R[0] R[28000] 0  // UP
    SHT R[0] R[28001] 1  // LEFT
    SHT R[0] R[28002] 2  // DOWN
    SHT R[0] R[28003] 3  // RIGHT
    SHT R[0] R[28004] 4  // Z
    SHT R[0] R[28005] 5  // X
    SHT R[0] R[28006] 6  // END
    SHT R[0] R[28007] 7  // ESC

    // exit vm if ESC/END is pressed
    CMP R[28006] 0
        EXIT
    CMP R[28007] 0
        EXIT

    // (holding left)OR(holding right)
    LD R[0] R[28001]
    LD R[1] R[28003]
    CALL STD_LOGIC_OR

    // enter left/right logic
    CMP R[4100] 0
    CALL HANDLE_X_POS_OF_TETRIS_PIECE

    // move active piece faster is DOWN
    // CMP R[28002] 0
    //     ADD R[30001] 3

    // rotate piece - Z
    CMP R[28004] 0
        CALL ROTATE_ACTIVE_PIECE

    CALL STD_SCREEN_FILL_BLACK  // clear screen

    // *********************
    // LOAD SPRITES IN VRAM
    // *********************
    // transfer X and Y values of sprites to slots R[:255]
    // opcodes work. Need to fit in 8 bits

    // sprite
    LD R[240] R[30000]
    LD R[241] R[30001]
    LD SPRITE_TETRIS_TETROMINO_O R[240] R[241] 16 16

    BLIT  // draw to screen
    WAIT  // wait 17 ms

    // increment counter
    ADD R[65535] 1
    LTE R[65535] 20
        CALL FIRE_LOGIC_EVERY_N_FRAMES

    GOTO TETRIS_MAIN_LOOP

EXIT




// ======
//  UTIL
// ======

// -----------------------------------------------
// this function resets a counter that goes up by
// count per frame (17ms) and then resets it to 0
// once it hits some number N (see the function in
// the main loop). Triggers logic too
// -----------------------------------------------
FIRE_LOGIC_EVERY_N_FRAMES:
    LD R[65535] 0  // reset counter at R[65535] to 0

    // store (pieceHeight + pieceYpos) in R[45678]
    LD R[45678] R[30001] // load piece Y pos
    ADD R[45678] R[30005] // add piece height in px

    // check if bottom of piece is lower than bottom of screen
    LT R[45678] 144
        LD R[30001] 0
    ADD R[30001] 8  // move active tetromino down 8 pixels

    RETURN



// -----------------------------------------------
// called if LEFT or RIGHT is down
// -----------------------------------------------
HANDLE_X_POS_OF_TETRIS_PIECE:
    // counter
    // LD R[65534] 0XFFFFFFFF

    // LD R[0] 0XFFFFFFFF
    // LT R[0] 0XFFFFFFFF
    // LD R[2] 1

    // 28001

    CMP R[28001] 0
        SUB R[30000] 8  // move piece LEFT
    CMP R[28003] 0
        ADD R[30000] 8  // move piece RIGHT

    // if piece is placed left of playfield, push back in
    GTE R[30000] R[50000]
        CALL _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_LEFT

    // if piece is placed right of playfield, push back in
    LD R[0] R[30004]
    ADD R[0] R[30000]  // R[0] contains Xpos + width
    LTE R[0] R[50001]
        CALL _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_RIGHT

    RETURN  // exit function

    _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_LEFT:
        LD R[30000] R[50000]
        RETURN

    _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_RIGHT:
        LD R[30000] R[50001]
        SUB R[30000] R[30004]
        RETURN


ROTATE_ACTIVE_PIECE:
    RETURN



LOAD_NEW_TETRIS_PIECE_AT_TOP_OF_PLAYFIELD:

    CALL DECIDE_RANDOM_PIECE_AND_RETURN_INDEX_TO_PC
    
    LD R[4096] 30003  // U
    LD R[4097] 30006  // V

    LD R[4098] R[4100]  // Y
    LD R[4099] R[4100]  // Z
    ADD R[4099] 3

    LD R[U:V] R[Y:Z]

    RETURN


DECIDE_RANDOM_PIECE_AND_RETURN_INDEX_TO_PC:
    // decide random piece

    // from random number between 0-6,
    // return the index to pc of piece
    // CMP R[0] 0
    // CMP R[0] 1
    // CMP R[0] 2
    // CMP R[0] 3
    // CMP R[0] 4
    // CMP R[0] 5
    // CMP R[0] 6


    LD R[4100] 30100  // replace later

    RETURN

