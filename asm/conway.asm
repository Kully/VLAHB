CONWAY_MAIN:
    // ***********************
    // CONWAY'S GAME OF LIFE
    // ***********************

    // ============
    // init program
    // ============

    // VRAM2 -> R[30000:53040]

    LD R[28000] 0  // x
    LD R[28001] 0  // y
    LD R[28002] 0  // number of neighbours for (x,y)
    LD R[28003] 0  // index of vram for (x,y)
    LD R[28004] 0  // next state of (x,y)

    LD R[28005] 0  // x == 0
    LD R[28006] 0  // y == 0
    LD R[28007] 0  // x == 159
    LD R[28008] 0  // y == 143

    LD R[28009] 0  // len of neighbour path
    LD R[28010] 0  // pos in path
    LD R[28011] 0  // pixelInVRAM
    LD R[28012] 0  // counter for number of generations

    // load initial state
    CALL CONWAY_INIT_STATE_INFINITE_GROWTH_2
    // CALL CONWAY_INIT_STATE_2
    
    BLIT

    CONWAY_GAME_LOOP:
        INPUT R[0]
        SHT R[0] R[29000] 6  // END
        SHT R[0] R[29001] 7  // ESC

        // exit if ESC or END
        CMP R[29000] 0
            EXIT
        CMP R[29001] 0
            EXIT

        LD R[28000] 0
        LD R[28001] 0
        _CONWAY_LOOP_THROUGH_EACH_PIXEL:
            // do stuff here for (x,y)

            LD R[0] R[28000]
            LD R[1] R[28001]
            CALL STD_VRAM_INDEX_FROM_X_Y
            LD R[28003] R[4100]

            CALL _CONWAY_FIND_NUM_OF_ALIVE_NEIGHBOURS

            // determine next-gen state of (x,y)
            CALL _CONWAY_WILL_PIXEL_BE_ALIVE_NEXT_ROUND

            // move next next-gen state of pixel to VRAM2
            MUL R[4100] 0XFFFFFFFF
            LD R[4099] R[28003]
            ADD R[4099] 25899
            LD R[Z] R[4100]

            // loop
            ADD R[28000] 1
            CMP R[28000] 160  // 159?
            GOTO _CONWAY_LOOP_THROUGH_EACH_PIXEL
            LD R[28000] 0
            ADD R[28001] 1
            CMP R[28001] 144  // 143?
            GOTO _CONWAY_LOOP_THROUGH_EACH_PIXEL

        CALL CONWAY_COLOR_SCREEN_BLACK

        // transfer vram2 to vram
        LD R[4096] 4101
        LD R[4097] 27141
        LD R[4098] 30000
        LD R[4099] 53040
        LD R[U:V] R[Y:Z]
        
        // clear VRAM2
        CALL CONWAY_CLEAR_VRAM2

        BLIT

        ADD R[28012] 1  // +1 to generation counter

        GOTO CONWAY_GAME_LOOP

    // ==============
    // initial states
    // ==============

    CONWAY_INIT_STATE_1:
        LD R[4096] 4150
        LD R[U] 0XFFFFFFFF
        
        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF
        
        ADD R[4096] 159
        LD R[U] 0XFFFFFFFF

        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF

        ADD R[4096] 8
        LD R[U] 0XFFFFFFFF
        RETURN

    CONWAY_INIT_STATE_2:
        LD R[4096] 4101
        _CONWAY_INIT_STATE_2:
            ADD R[4096] 1
            RAND R[0]
            MUL R[0] 0XFFFFFFFF
            LD R[U] R[0]
            CMP R[4096] 27141
            GOTO _CONWAY_INIT_STATE_2
        RETURN

    CONWAY_INIT_STATE_BEACON:
        LD R[12181] 0XFFFFFFFF
        LD R[12182] 0XFFFFFFFF

        LD R[12341] 0XFFFFFFFF
        LD R[12342] 0XFFFFFFFF

        LD R[12503] 0XFFFFFFFF
        LD R[12504] 0XFFFFFFFF

        LD R[12663] 0XFFFFFFFF
        LD R[12664] 0XFFFFFFFF
        RETURN

    CONWAY_INIT_STATE_BLINKER:
        LD R[12181] 0XFFFFFFFF
        LD R[12182] 0XFFFFFFFF
        LD R[12183] 0XFFFFFFFF
        RETURN

    CONWAY_INIT_STATE_INFINITE_GROWTH_2:
        // [#][#][#][ ][#]
        // [#][ ][ ][ ][ ]
        // [ ][ ][ ][#][#]
        // [ ][#][#][ ][#]
        // [#][ ][#][ ][#]
        LD R[4096] 16976
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 2
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 156
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 163
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF

        ADD R[4096] 157
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 1
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 2
        LD R[U] 0XFFFFFFFF
        ADD R[4096] 160
        LD R[U] 0XFFFFFFFF
        SUB R[4096] 2
        LD R[U] 0XFFFFFFFF
        SUB R[4096] 2
        LD R[U] 0XFFFFFFFF

        RETURN

    // ==============
    // util functions
    // ==============

    _CONWAY_FIND_NUM_OF_ALIVE_NEIGHBOURS:
        // R[28003] <- vram_idx_of_(x,y)
        //   this will shift to the other
        //   other pixels around it.
        //
        // 6 7 8
        // 5 * 1
        // 4 3 2

        LD R[28002] 0  // reset alive neighbours -> 0

        // 6
        SUB R[28003] 161  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 7
        ADD R[28003] 1  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 8
        ADD R[28003] 1  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 5
        ADD R[28003] 158  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 1
        ADD R[28003] 2  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 4
        ADD R[28003] 158  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 3
        ADD R[28003] 1  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // 2
        ADD R[28003] 1  // move (x,y) index
        CALL _CONWAY_IS_PIXEL_IN_VRAM
        CMP R[28011] 0
        CALL IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT

        // reset pixel back to original value
        SUB R[28003] 161

        RETURN

    _CONWAY_WILL_PIXEL_BE_ALIVE_NEXT_ROUND:
        // 1   0,1             ->  0  # Lonely
        // 1   4,5,6,7,8       ->  0  # Overcrowded
        // 1   2,3             ->  1  # Lives
        // 0   3               ->  1  # It takes three to give birth!
        // 0   0,1,2,4,5,6,7,8 ->  0  # Barren

        LD R[4096] R[28003]
        CMP R[U] 0  // CMP R[28003] 0
        GOTO _PIXEL_NEXT_STATE_IF_CURRENT_PIXEL_IS_ALIVE
        GOTO _PIXEL_NEXT_STATE_IF_CURRENT_PIXEL_IS_DEAD

        _PIXEL_NEXT_STATE_IF_CURRENT_PIXEL_IS_DEAD:
            LD R[4100] 0  // return "DEAD"

            CMP R[28002] 3
            RETURN
            LD R[4100] 1  // "ALIVE"
            RETURN

        _PIXEL_NEXT_STATE_IF_CURRENT_PIXEL_IS_ALIVE:
            LD R[4100] 0  // return "DEAD"

            GTE R[28002] 2
            RETURN
            LTE R[28002] 3
            RETURN
            LD R[4100] 1  // "ALIVE"
            RETURN

    IF_PIXEL_ALIVE_INCREASE_NEIGHBOUR_COUNT:
        LD R[4098] R[28003]
        CMP R[Y] 0
        ADD R[28002] 1
        RETURN

    _CONWAY_IS_PIXEL_IN_VRAM:
        LD R[28011] 1  // pixelInVRAM (BOOL)
        GTE R[28003] 4101
        LD R[28011] 0
        LTE R[28003] 27141
        LD R[28011] 0
        RETURN

    CONWAY_COLOR_SCREEN_BLACK:
        CALL STD_GET_LAST_VRAM_INDEX
        LD R[4097] R[4100]
        LD R[65000] 0
        LD R[4099] 65000
        LD R[4096] 4101
        LD R[U:V] R[Z]
        RETURN

    CONWAY_CLEAR_VRAM2:
        LD R[4097] 53040
        LD R[65000] 0XFF0000FF
        LD R[4099] 65000
        LD R[4096] 30000
        LD R[U:V] R[Z]
        RETURN
