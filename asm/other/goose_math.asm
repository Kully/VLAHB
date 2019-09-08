GOTO MAIN

// void MAIN()
// {
//   var a = 10
//   var b = 5
//   var c = STD_MATH_ADD(a, b)
//   var d = STD_MATH_SUB(a, b)
//   var e = STD_MATH_MUL(a, b)
//   var f = STD_MATH_DIV(a, b)
//   var g = STD_MATH_LONG_WINDED(a, b)
// }
MAIN:
    LD R[0] 10

    LD R[1] 5

    CALL STD_MATH_ADD
    LD R[2] R[4100]

    CALL STD_MATH_SUB
    LD R[3] R[4100]

    CALL STD_MATH_MUL
    LD R[4] R[4100]

    CALL STD_MATH_DIV
    LD R[5] R[4100]

    CALL STD_MATH_LONG_WINDED
    LD R[6] R[4100]

    EXIT