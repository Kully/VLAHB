// **********
// * TETRIS *
// **********

//  0000 -  4095: functions + misc
//  4096 -  4099: pointers U,V,Y,Z
//  4100 - 27140: VRAM
// 27140 - 65535: Heap

// What are in the slots?
// ======================
// 30001: X pos of piece when spawning at top
// 30002: Y pos of piece when spawning at top

// *** active piece info
// 30003: pc of active piece
// 30004: width of active piece (pixels)
// 30005: height of active piece in (pixels)
// 30006: what rotation index active piece is on
// 30007: total number of rotation sprite
// 30008: --
// 30009: pc of active rotation piece sprite
// 30010: width of active rotation piece sprite
// 30011: height of active rotation piece sprite
// 30012: --
// 30013: --
// 30014: --
// 30015: playfield: left X pos
// 30016: playfield: right X pos


// 65000: holds gravity speed
// 65535: counter for gravity <- MAX VALUE


// O
// ---------
// 30100: pc
// 30101: W
// 30102: H
LD R[30100] SPRITE_TETRIS_TETROMINO_O_ROT0
LD R[30101] 16
LD R[30102] 16


// S
// ---------
// rot0
// 30103: pc
// 30104: W
// 30105: H
LD R[30103] SPRITE_TETRIS_TETROMINO_S_ROT0
LD R[30104] 24
LD R[30105] 16

// rot1
// 30106: pc
// 30107: W
// 30108: H
LD R[30106] SPRITE_TETRIS_TETROMINO_S_ROT1
LD R[30107] 16
LD R[30108] 24


// Z
// ---------
// rot0
// 30109: pc
// 30110: W
// 30111: H
LD R[30109] SPRITE_TETRIS_TETROMINO_Z_ROT0
LD R[30110] 24
LD R[30111] 16

// rot1
// 30112: pc
// 30113: W
// 30114: H
LD R[30112] SPRITE_TETRIS_TETROMINO_Z_ROT1
LD R[30113] 16
LD R[30114] 24


// T
// ---------
// rot0
// 30115: pc
// 30116: W
// 30117: H
LD R[30115] SPRITE_TETRIS_TETROMINO_T_ROT0
LD R[30116] 24
LD R[30117] 16

// rot1
// 30118: pc
// 30119: W
// 30120: H
LD R[30118] SPRITE_TETRIS_TETROMINO_T_ROT1
LD R[30119] 16
LD R[30120] 24

// rot2
// 30121: pc
// 30122: W
// 30123: H
LD R[30121] SPRITE_TETRIS_TETROMINO_T_ROT2
LD R[30122] 24
LD R[30123] 16

// rot3
// 30124: pc
// 30125: W
// 30126: H
LD R[30124] SPRITE_TETRIS_TETROMINO_T_ROT3
LD R[30125] 16
LD R[30126] 24


// I
// ---------
// rot0
// 30127: pc
// 30128: W
// 30129: H
LD R[30127] SPRITE_TETRIS_TETROMINO_I_ROT0
LD R[30128] 32
LD R[30129] 8

// rot1
// 30130: pc
// 30131: W
// 30132: H
LD R[30130] SPRITE_TETRIS_TETROMINO_I_ROT1
LD R[30131] 8
LD R[30132] 32


// L
// ---------
// rot0
// 30133: pc
// 30134: W
// 30135: H
LD R[30133] SPRITE_TETRIS_TETROMINO_L_ROT0
LD R[30134] 24
LD R[30135] 16

// rot1
// 30136: pc
// 30137: W
// 30138: H
LD R[30136] SPRITE_TETRIS_TETROMINO_L_ROT1
LD R[30137] 16
LD R[30138] 24

// rot2
// 30139: pc
// 30140: W
// 30141: H
LD R[30139] SPRITE_TETRIS_TETROMINO_L_ROT2
LD R[30140] 24
LD R[30141] 16

// rot3
// 30142: pc
// 30143: W
// 30144: H
LD R[30142] SPRITE_TETRIS_TETROMINO_L_ROT3
LD R[30143] 16
LD R[30144] 24



// J
// ---------
// rot0
// 30145: pc
// 30146: W
// 30147: H
LD R[30145] SPRITE_TETRIS_TETROMINO_J_ROT0
LD R[30146] 24
LD R[30147] 16

// rot1
// 30148: pc
// 30149: W
// 30150: H
LD R[30148] SPRITE_TETRIS_TETROMINO_J_ROT1
LD R[30149] 16
LD R[30150] 24

// rot2
// 30151: pc
// 30152: W
// 30153: H
LD R[30151] SPRITE_TETRIS_TETROMINO_J_ROT2
LD R[30152] 24
LD R[30153] 16

// rot3
// 30154: pc
// 30155: W
// 30156: H
LD R[30154] SPRITE_TETRIS_TETROMINO_J_ROT3
LD R[30155] 16
LD R[30156] 24

// =========
// CONSTANTS
// =========

// playfield dimensions - (a tetris cell (4 per pixel) is 8X8px)
LD R[30015] 16 // playfield: left X pos
LD R[30016] 96 // playfield: right X pos

// slots that store if key is held
LD R[28020] 0  // UP    Pushed
LD R[28021] 0  // LEFT  Pushed
LD R[28022] 0  // DOWN  Pushed
LD R[28023] 0  // RIGHT Pushed
LD R[28024] 0  // Z     Pushed
LD R[28025] 0  // X     Pushed

// pos of piece for spawn
LD R[30001] 48  // X pos of piece when spawning at top
LD R[30002]  0  // Y pos of new piece when spawning at top

LD R[65000] 12  // gravity speed - number of frames to move piece down 8px


CALL UPDATE_ACTIVE_PIECE_SLOTS
CALL TETRIS_MAIN_LOOP

TETRIS_MAIN_LOOP:

    // *************
	// Load Inputs *
    // *************

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

    // ***********************
    // Update Buttons Pushed *
    // ***********************

    // ZPushed
    CMP R[28004] 0  // if R[28004] = 1, R[28024] += 1
    ADD R[28024] 1
    CMP R[28004] 1  // if R[28004] = 0, R[28024] = 0
    LD R[28024] 0

    // LEFTPushed
    CMP R[28001] 0
    ADD R[28021] 1
    CMP R[28001] 1
    LD R[28021] 0

    // RIGHTPushed
    CMP R[28003] 0
    ADD R[28023] 1
    CMP R[28003] 1
    LD R[28023] 0


    // LEFT Down
    CMP R[28021] 1
    GOTO __SKIP_LEFT_DOWN__
    CALL HANDLE_X_POS_OF_TETRIS_PIECE
    __SKIP_LEFT_DOWN__:
    // RIGHT Down
    CMP R[28023] 1
    GOTO __SKIP_RIGHT_DOWN__
    CALL HANDLE_X_POS_OF_TETRIS_PIECE
    __SKIP_RIGHT_DOWN__:


    // rotate piece - Z
    CMP R[28024] 1  // if ZPushed
    GOTO __SKIP_ROTATE__
    CALL TETRIS_ROTATE_ACTIVE_PIECE
    __SKIP_ROTATE__:

    // ********************
    // Move Bytes to VRAM *
    // ********************

    CALL STD_SCREEN_FILL_BLACK  // clear screen

    // load background
    LD R[0] 0
    LD R[1] 0
    LD SPRITE_TETRIS_BKGD_STRIP_16_144 R[0] R[1] 16 144
    LD R[0] 96
    LD SPRITE_TETRIS_BKGD_STRIP_16_144 R[0] R[1] 16 144
    ADD R[0] 16
    LD SPRITE_TETRIS_BKGD_STRIP_16_144 R[0] R[1] 16 144
    ADD R[0] 16
    LD SPRITE_TETRIS_BKGD_STRIP_16_144 R[0] R[1] 16 144
    ADD R[0] 16
    LD SPRITE_TETRIS_BKGD_STRIP_16_144 R[0] R[1] 16 144


    // load saved playfield into vram
    LD R[0] R[4096]
    LD R[1] R[4097]
    LD R[2] R[4098]
    LD R[3] R[4099]

    LD R[4096] 40000 
    LD R[4097] 40080
    LD R[4098] 4117
    LD R[4099] 4197
    LOAD_SAVED_PLAYFIELD_TO_VRAM:
        LD R[Y:Z] R[U:V]
        ADD R[4096] 160
        ADD R[4097] 160
        ADD R[4098] 160
        ADD R[4099] 160
        ADD R[39999] 1

        GTE R[39999] 144  // counts up
        GOTO LOAD_SAVED_PLAYFIELD_TO_VRAM
    LD R[39999] 0 // reset timer
    LD R[4096] R[0]
    LD R[4097] R[1]
    LD R[4098] R[2]
    LD R[4099] R[3]


    // load active tetris sprite
    LD R[4099] R[30009]
    LD R[0] R[30001]
    LD R[1] R[30002]
    LD R[2] R[30010]
    LD R[3] R[30011]
    LD R[Z] R[0] R[1] R[2] R[3]

    // load score
    // LD R[0] 125 // X
    // LD R[1] 22  // Y
    // LD SPRITE_FONT_3 R[0] R[1] 5 5
    // ADD R[0] 6
    // LD SPRITE_FONT_3 R[0] R[1] 5 5


    BLIT  // draw to screen
    WAIT  // wait 17 ms

    // increment counter
    ADD R[65535] 1
    LTE R[65535] R[65000]
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
    LD R[45678] R[30002] // load piece Y pos
    ADD R[45678] R[30011] // add piece height in px

    // check if bottom of piece is lower than bottom of screen
    LT R[45678] 144
    CALL _PIECE_TOUCHING_OR_PAST_FLOOR
    ADD R[30002] 8  // move active tetromino down 8 pixels

    RETURN

    _PIECE_TOUCHING_OR_PAST_FLOOR:
        LD R[30002] 0  // Y -> 0
        LD R[64666] 1
        CALL UPDATE_ACTIVE_PIECE_SLOTS
        LD R[30001] 48 // reset X-value for new piece
        RETURN



// -----------------------------------------------
// called if LEFT/RIGHT key is held down
// -----------------------------------------------
HANDLE_X_POS_OF_TETRIS_PIECE:
    CMP R[28001] 0
        SUB R[30001] 8  // move piece LEFT
    CMP R[28003] 0
        ADD R[30001] 8  // move piece RIGHT

    // if piece is placed left of playfield, push back in
    GTE R[30001] R[30015]
        CALL _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_LEFT

    // if piece is placed right of playfield, push back in
    LD R[0] R[30010]
    ADD R[0] R[30001]  // R[0] contains Xpos + width
    LTE R[0] R[30016]
        CALL _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_RIGHT

    RETURN  // leave

    // contained helper functions
    _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_LEFT:
        LD R[30001] R[30015]
        RETURN

    _PUSH_TETRIS_PIECE_INTO_BOUNDS_FROM_RIGHT:
        LD R[30001] R[30016]
        SUB R[30001] R[30010]
        RETURN



TETRIS_ROTATE_ACTIVE_PIECE:
    // R[30003]: pc of sprite (rot0)
    // R[30006]: index of rotation
    // R[30007]: total number of rotation sprite
    // R[30009-30011]: pc,w,h of current sprite rotation

    // increment rotation index
    LT R[30006] R[30007]
    LD R[30006] 0
    ADD R[30006] 1


    // calculate pc,w,h for rotation sprite
    LD R[0] R[4098]

    // R[30009] -> R[30003] + (3* (R[30006]-1) )
    LD R[1] R[30006]
    SUB R[1] 1
    MUL R[1] 3
    ADD R[1] R[0]

    // R[1] contains i where ram[ram[i]] = pc of new sprite

    // new pc -> R[30009]
    LD R[4099] R[1]
    LD R[4096] 30009
    LD R[U] R[Z]


    // width -> R[30010]
    ADD R[4096] 1
    ADD R[4099] 1
    LD R[U] R[Z]

    ADD R[4096] 1
    ADD R[4099] 1
    LD R[U] R[Z]
    
    RETURN


UPDATE_ACTIVE_PIECE_SLOTS:
    LD R[4096] 20  // Left   (l)
    LD R[4097] 26  // Right  (r)

    CALL DECIDE_RANDOM_PIECE_AND_RETURN_INDEX_TO_PC

    // update the active piece stats (index to pc, width, height)
    LD R[4096] 30003  // U
    LD R[4097] 30006  // V

    LD R[4098] R[4100]  // Y
    LD R[4099] R[4100]  // Z
    ADD R[4099] 3
    LD R[U:V] R[Y:Z]

    // copy current pc,w,h info to r[30009-30011]
    // will use for rotation values 
    ADD R[4096] 6
    ADD R[4097] 6
    LD R[U:V] R[Y:Z]

    // update number of rotations for active piece 
    LT R[4100] 30100  // O
        LD R[30007] 1
    LT R[4100] 30103  // S
        LD R[30007] 2
    LT R[4100] 30109  // Z
        LD R[30007] 2
    LT R[4100] 30115  // T
        LD R[30007] 4
    LT R[4100] 30127  // I
        LD R[30007] 2
    LT R[4100] 30133  // L
        LD R[30007] 4
    LT R[4100] 30145  // J
        LD R[30007] 4

    LD R[30006] 1  // start at rotation 1

    // load playfield to slots R[40000-...]
    LD R[150] R[4096]
    LD R[151] R[4097]
    LD R[152] R[4098]
    LD R[153] R[4099]

    LD R[4096] 40000 
    LD R[4097] 40080
    LD R[4098] 4117
    LD R[4099] 4197
    LOAD_VRAM_PLAYFIELD_TO_HEAP:
        LD R[U:V] R[Y:Z]
        ADD R[4096] 160
        ADD R[4097] 160
        ADD R[4098] 160
        ADD R[4099] 160
        ADD R[39999] 1

        GTE R[39999] 144  // counts up
        GOTO LOAD_VRAM_PLAYFIELD_TO_HEAP
    LD R[39999] 0  // reset loop counter
    LD R[4096] R[150]
    LD R[4097] R[151]
    LD R[4098] R[152]
    LD R[4099] R[153]


    RETURN



DECIDE_RANDOM_PIECE_AND_RETURN_INDEX_TO_PC:
    
    // reset first few slots
    LD R[0] 0
    LD R[1] 0
    LD R[2] 0
    LD R[3] 0
    LD R[4] 0
    LD R[5] 0
    LD R[6] 0
    LD R[7] 0

    // calc CEIL( (R[4097] - R[4096]) / 2)
    LD R[4] R[4097]
    SUB R[4] R[4096]
    PUSH
    LD R[0] R[4]
    LD R[1] 2
    CALL STD_MATH_CEIL_DIV
    POP
    LD R[4] R[4100]  // gets stored here in R[4]

    RAND R[5]  // load 0 or 1

    // chop off half of the ints
    CMP R[5] 0
    SUB R[4097] R[4]
    CMP R[5] 1
    ADD R[4096] R[4]

    LD R[7] R[4]
    ADD R[7] 1

    LTE R[7] 1
    GOTO DECIDE_RANDOM_PIECE_AND_RETURN_INDEX_TO_PC

    // load return address with the pc of selected piece
    LD R[4099] 4100

    LD R[20] 30100 // O
    LD R[21] 30103 // S
    LD R[22] 30109 // Z
    LD R[23] 30115 // T
    LD R[24] 30127 // I
    LD R[25] 30133 // L
    LD R[26] 30145 // J

    LD R[Z] R[V]
    RETURN
