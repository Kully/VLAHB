TV_NOISE_SIMULATION_MAIN:
    // ***
    // TV NOISE SIMULATION
    // ==================
    //
    // place random pixels on
    // the screen to simulate
    // tv noise/static.
    // ***

    LD R[80] 0XCACACAFF  // load color of noise

    GOTO TV_NOISE_SIM_MAIN

    TV_NOISE_SIM_MAIN:
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

        // pointers setups
        LD R[4096] 4101
        LD R[4099] 69
        _TV_NOISE_SIM_LOAD_PIXELS_ON_SCREEN:
            LD R[69] R[80]  // color
            RAND R[70]
            MUL R[69] R[70]
            LD R[U] R[Z]

            ADD R[4096] 1
            GTE R[4096] 27140
            GOTO _TV_NOISE_SIM_LOAD_PIXELS_ON_SCREEN

        BLIT  // draw to screen
        WAIT  // wait 17 ms

        GOTO TV_NOISE_SIM_MAIN

    EXIT