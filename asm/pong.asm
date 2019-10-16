// ****
// PONG
// ****
PONG_MAIN:

    // global variables
    LD R[30000] 4    // LPattle X
    LD R[30001] 80   // LPattle Y
    LD R[30002] 154  // RPattle X
    LD R[30003] 80   // RPattle Y
    LD R[30004] 0    // LScore
    LD R[30005] 0    // RScore
    LD R[30006] 0    // General Counter

    LD R[30011] 4  // min Y height
    LD R[30012] 124 // max Y height

    LD R[30015] 4  // width of ball in px
    LD R[30016] 2  // paddle speed 

    // load pcs of sprites to RAM
    LD R[30020] SPRITE_FONT_0
    LD R[30021] SPRITE_FONT_1
    LD R[30022] SPRITE_FONT_2
    LD R[30023] SPRITE_FONT_3
    LD R[30024] SPRITE_FONT_4
    LD R[30025] SPRITE_FONT_5
    LD R[30026] SPRITE_FONT_6
    LD R[30027] SPRITE_FONT_7
    LD R[30028] SPRITE_FONT_8
    LD R[30029] SPRITE_FONT_9

    LD R[30030] PONG_SPRITE_BALL

    // counters for physics
    LD R[30040] 0  // counter A
    LD R[30041] 0  // counter B

    LD R[30050] 0  // leftHeldDown
    
    // background color
    LD R[30060] 0X000000FF

    CALL PONG_RESET_BALL
    GOTO PONG_GAME_LOOP

    PONG_GAME_LOOP:
        INPUT R[0]
        SHT R[0] R[28000] 0  // UP
        SHT R[0] R[28001] 1  // LEFT
        SHT R[0] R[28002] 2  // DOWN
        SHT R[0] R[28003] 3  // RIGHT
        SHT R[0] R[28004] 4  // Z
        SHT R[0] R[28005] 5  // X
        SHT R[0] R[28006] 6  // END <- decide what to do with this
        SHT R[0] R[28007] 7  // ESC

        // exit if ESC pressed
        CMP R[28007] 0
            EXIT

        // check if score is over 9
        LTE R[30004] 9
        GOTO PONG_PLAYER_WINS_SCREEN
        LTE R[30005] 9
        GOTO PONG_PLAYER_WINS_SCREEN


        // handle L-Pattle Movement
        CMP R[28004] 0  // Z
        CALL PONG_MOVE_LPADDLE_UP
        CMP R[28005] 0  // X
        CALL PONG_MOVE_LPADDLE_DOWN

        // handle R-Pattle Movement
        CMP R[28000] 0  // UP
        CALL PONG_MOVE_RPADDLE_UP
        CMP R[28002] 0  // DOWN
        CALL PONG_MOVE_RPADDLE_DOWN


        // ========================
        // move ball left and right
        // ========================

        // R[0] -> left boundary
        LD R[0] R[30000]
        ADD R[0] R[30015]
        GT R[30007] R[0]
        CALL PONG_BALL_AT_LEFT_SCREEN

        // R[1] -> right boundary
        LD R[1] R[30002]
        SUB R[1] 4
        LT R[30007] R[1]
        CALL PONG_BALL_AT_RIGHT_SCREEN

        CALL PONG_MOVE_BALL_LEFT_OR_RIGHT


        // =====================
        // move ball up and down
        // =====================

        GTE R[30008] 4
        LD R[30014] 1
        LTE R[30008] 140
        LD R[30014] 0

        CALL PONG_MOVE_BALL_UP_OR_DOWN


        // ====
        // VRAM
        // ====

        CALL PONG_COLOR_SCREEN_GREY

        // =============
        // draw L-Pattle
        // =============

        LD R[4096] R[30030]
        LD R[41] R[30000]   // X
        LD R[42] R[30001]   // Y
        LD R[43] 4          // WIDTH
        LD R[44] 4          // HEIGHT
        
        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]


        // =============
        // draw R-Pattle
        // =============

        LD R[41] R[30002]   // X
        LD R[42] R[30003]   // Y
        LD R[43] 4          // WIDTH
        LD R[44] 4          // HEIGHT

        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]
        ADD R[42] 4
        LD R[U] R[41] R[42] R[43] R[44]


        // =========
        // draw ball
        // =========

        LD R[41] R[30007]  // X
        LD R[42] R[30008]  // Y
        LD R[43] 4         // WIDTH
        LD R[44] 4         // HEIGHT
        LD R[U] R[41] R[42] R[43] R[44]

        // ===========
        // draw LScore
        // ===========

        LD R[0] 2 // X
        LD R[1] 2  // Y
        LD R[2] 5  // W
        LD R[3] 5  // H

        LD R[4099] 30020
        ADD R[4099] R[30004]
        LD R[4096] R[Z]
        LD R[U] R[0] R[1] R[2] R[3]


        // ===========
        // draw RScore
        // ===========

        LD R[0] 153  // X
        LD R[2] 5    // W
        LD R[3] 5    // H

        LD R[4099] 30020
        ADD R[4099] R[30005]
        LD R[4096] R[Z]
        LD R[U] R[0] R[1] R[2] R[3]


        // "PONG!!!"
        LD R[0] 65
        LD R[4096] SPRITE_FONT_P
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_O
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_N
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_G
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_EXCLAMATION
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 3
        LD R[4096] SPRITE_FONT_EXCLAMATION
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 3
        LD R[4096] SPRITE_FONT_EXCLAMATION
        LD R[U] R[0] R[1] R[2] R[3]

        WAIT  // wait 17 ms
        BLIT  // draw to screen
        GOTO PONG_GAME_LOOP



    // ****************
    // helper functions
    // ****************

    // left paddle
    PONG_MOVE_LPADDLE_UP:
    	GTE R[30001] R[30011]
    	RETURN
    	SUB R[30001] R[30016]
    	RETURN

    PONG_MOVE_LPADDLE_DOWN:
    	LTE R[30001] R[30012]
    	RETURN
    	ADD R[30001] R[30016]
    	RETURN

    // right paddle
    PONG_MOVE_RPADDLE_UP:
        GTE R[30003] R[30011]
        RETURN
        SUB R[30003] R[30016]
        RETURN

    PONG_MOVE_RPADDLE_DOWN:
        LTE R[30003] R[30012]
        RETURN
        ADD R[30003] R[30016]
        RETURN


    PONG_RESET_BALL:
        LD R[30007] 78  // Ball X
        LD R[30008] 52  // Ball Y
        LD R[30009] 1  // Ball Velocity X
        LD R[30010] 1   // Ball Velocity Y

        RAND R[30013]  // Ball X-Velo Sign (0-> -ve, 1-> +ve)
        RAND R[30014]  // Ball Y-Velo Sign (0-> -ve, 1-> +ve)
    	RETURN


    INCREASE_L_SCORE:
        ADD R[30004] 1
        RETURN 

    INCREASE_R_SCORE:
        ADD R[30005] 1
        RETURN

    RESET_L_AND_R_SCORES:
        LD R[30004] 0
        LD R[30005] 0
        RETURN


    PONG_MOVE_BALL_LEFT_OR_RIGHT:
        CMP R[30013] 0
        GOTO __PONG_MOVE_BALL_RIGHT
        GOTO __PONG_MOVE_BALL_LEFT

        __PONG_MOVE_BALL_LEFT:
            SUB R[30007] R[30009]
            RETURN

        __PONG_MOVE_BALL_RIGHT:
            ADD R[30007] R[30009]
            RETURN


    PONG_MOVE_BALL_UP_OR_DOWN:
        CMP R[30014] 0
        GOTO __PONG_MOVE_BALL_DOWN
        GOTO __PONG_MOVE_BALL_UP

        __PONG_MOVE_BALL_UP:
            SUB R[30008] R[30010]
            RETURN

        __PONG_MOVE_BALL_DOWN:
            ADD R[30008] R[30010]
            RETURN


    // left side logic
    PONG_BALL_AT_LEFT_SCREEN:
        CALL PONG_IS_BALL_IN_L_PADDLE
        
        CMP R[4100] 1
        GOTO __PONG_BALL_GOES_IN_L_GOAL
        GOTO __PONG_SWITCH_DIR_GO_RIGHT


        __PONG_SWITCH_DIR_GO_RIGHT:
            LD R[30013] 1
            CALL __PONG_MOVE_BALL_RIGHT
            RETURN

        __PONG_BALL_GOES_IN_L_GOAL:
            CALL WAIT_1_SECOND
            CALL PONG_RESET_BALL
            CALL INCREASE_R_SCORE
            RETURN


    PONG_IS_BALL_IN_L_PADDLE:
        LD R[4100] 0

        // R[42] -> L-Pattle y0
        // R[43] -> L-Pattle y1
        // R[44] -> ball y-4
        // R[45] -> ball y+4
        LD R[42] R[30001]
        LD R[43] R[42]
        ADD R[43] 12

        LD R[44] R[30008]
        SUB R[44] 4
        LD R[45] R[44]
        ADD R[45] 4

        // extend hitbox of pattle
        SUB R[42] 2
        ADD R[43] 2

        // check if ball touching L-Pattle
        GTE R[45] R[42]
            RETURN
        LTE R[44] R[43]
            RETURN

        LD R[4100] 1
        RETURN


    // right side logic
    PONG_BALL_AT_RIGHT_SCREEN:
        CALL PONG_IS_BALL_IN_R_PADDLE
        
        CMP R[4100] 1
        GOTO __PONG_BALL_GOES_IN_R_GOAL
        GOTO __PONG_SWITCH_DIR_GO_LEFT


        __PONG_SWITCH_DIR_GO_LEFT:
            LD R[30013] 0
            CALL __PONG_MOVE_BALL_LEFT
            RETURN

        __PONG_BALL_GOES_IN_R_GOAL:
            CALL WAIT_1_SECOND
            CALL PONG_RESET_BALL
            CALL INCREASE_L_SCORE
            RETURN


    PONG_IS_BALL_IN_R_PADDLE:
        LD R[4100] 0

        // R[42] -> R-Pattle y0
        // R[43] -> R-Pattle y1
        // R[44] -> ball y-4
        // R[45] -> ball y+4
        LD R[42] R[30003]
        LD R[43] R[42]
        ADD R[43] 12

        LD R[44] R[30008]
        SUB R[44] 4
        LD R[45] R[44]
        ADD R[45] 4

        // extend hitbox of pattle
        SUB R[42] 2
        ADD R[43] 2

        // check if ball touching R-Pattle
        GTE R[45] R[42]
            RETURN
        LTE R[44] R[43]
            RETURN

        LD R[4100] 1
        RETURN


    PONG_PLAYER_WINS_SCREEN:

        CALL PONG_COLOR_SCREEN_GREY

        // decide who wins
        LTE R[30004] 9
        LD R[4099] SPRITE_FONT_1
        LTE R[30005] 9
        LD R[4099] SPRITE_FONT_2

        // "PLAYER 1 WINS" or "PLAYER 2 WINS"
        LD R[0] 46
        LD R[1] 60
        LD R[2] 5
        LD R[3] 5
        LD R[4096] SPRITE_FONT_P
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_L
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_A
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_Y
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_E
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_R
        LD R[U] R[0] R[1] R[2] R[3]

        ADD R[0] 8
        LD R[4096] R[4099]
        LD R[U] R[0] R[1] R[2] R[3]

        ADD R[0] 8
        LD R[4096] SPRITE_FONT_W
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_I
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_N
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_S
        LD R[U] R[0] R[1] R[2] R[3]
        ADD R[0] 6
        LD R[4096] SPRITE_FONT_EXCLAMATION
        LD R[U] R[0] R[1] R[2] R[3]

        BLIT

        LD R[30006] 0  // for general counter loop
        LD R[30061] 86  // cursor Y position

        _LOOP_THROUGH_GENERAL_COUNTER:
            INPUT R[9]
            SHT R[9] R[28000] 0  // UP
            SHT R[9] R[28001] 1  // LEFT
            SHT R[9] R[28002] 2  // DOWN
            SHT R[9] R[28003] 3  // RIGHT
            SHT R[9] R[28004] 4  // Z
            SHT R[9] R[28005] 5  // X
            SHT R[9] R[28006] 6  // ENTER
            SHT R[9] R[28007] 7  // ESC

            // exit if ESC pressed
            CMP R[28007] 0
                EXIT

            // "RESTART?"
            LD R[0] 46  // set X
            LD R[1] 70 // set Y
            LD R[4096] SPRITE_FONT_R
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_E
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_S
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_T
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_A
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_R
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_T
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_QUESTION_MARK
            LD R[U] R[0] R[1] R[2] R[3]

            LD R[0] 55
            LD R[1] 70

            // "YES"
            ADD R[0] 5  // reset X
            ADD R[1] 8  // new Y line
            LD R[4096] SPRITE_FONT_Y
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_E
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_S
            LD R[U] R[0] R[1] R[2] R[3]

            // "NO"
            LD R[0] 60  // reset X
            ADD R[1] 8  // new Y line
            LD R[4096] SPRITE_FONT_N
            LD R[U] R[0] R[1] R[2] R[3]
            ADD R[0] 6
            LD R[4096] SPRITE_FONT_O
            LD R[U] R[0] R[1] R[2] R[3]


            // LD R[1] 78 // or YES
            // LD R[1] 86 // or NO


            CALL DECIDE_WHERE_CURSOR_POINTS

            // ">"
            LD R[0] 53
            LD R[1] R[30061] // set cursor Y val
            LD R[4096] PONG_CURSOR
            LD R[2] 5
            LD R[3] 5
            LD R[U] R[0] R[1] R[2] R[3]

            // if x or y pressed, start game again
            CMP R[28004] 0
            GOTO PONG_MAIN
            CMP R[28005] 0
            GOTO PONG_MAIN

            BLIT
            WAIT

            GOTO _LOOP_THROUGH_GENERAL_COUNTER

            EXIT

    DECIDE_WHERE_CURSOR_POINTS:
        CMP R[28000] 1
        GOTO __CURSOR_POINTS_AT_YES
        GOTO __CURSOR_POINTS_AT_NO

        __CURSOR_POINTS_AT_YES:
            LD R[30061] 86
            RETURN

        __CURSOR_POINTS_AT_NO:
            LD R[30061] 78
            RETURN


    PONG_COLOR_SCREEN_GREY:
        CALL STD_GET_LAST_VRAM_INDEX
        LD R[4097] R[4100]
        LD R[65000] R[30060]
        LD R[4099] 65000
        LD R[4096] 4101
        LD R[U:V] R[Z]
        RETURN


WAIT_1_SECOND:
    LD R[0] 0

    _WAIT_1_SECOND_LOOP:
        ADD R[0] 1
        CMP R[0] 0X3FFFFFF
        GOTO _WAIT_1_SECOND_LOOP
    RETURN


// 4 4
PONG_SPRITE_BALL:
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF
	0XABABABFF

// 5 5
PONG_CURSOR:
    0XAB1569FF
    0XAB1569FF
    0XAB1569FF
    0XFFFFFF00
    0XFFFFFF00

    0XFFFFFF00
    0XAB1569FF
    0XAB1569FF
    0XAB1569FF
    0XFFFFFF00

    0XFFFFFF00
    0XFFFFFF00
    0XAB1569FF
    0XAB1569FF
    0XAB1569FF

    0XFFFFFF00
    0XAB1569FF
    0XAB1569FF
    0XAB1569FF
    0XFFFFFF00

    0XAB1569FF
    0XAB1569FF
    0XAB1569FF
    0XFFFFFF00
    0XFFFFFF00

// 5 5
PONG_CURSOR_WHITE:
    0XABABABFF
    0XABABABFF
    0XABABABFF
    0XFFFFFF00
    0XFFFFFF00

    0XFFFFFF00
    0XABABABFF
    0XABABABFF
    0XABABABFF
    0XFFFFFF00

    0XFFFFFF00
    0XFFFFFF00
    0XABABABFF
    0XABABABFF
    0XABABABFF

    0XFFFFFF00
    0XABABABFF
    0XABABABFF
    0XABABABFF
    0XFFFFFF00

    0XABABABFF
    0XABABABFF
    0XABABABFF
    0XFFFFFF00
    0XFFFFFF00
