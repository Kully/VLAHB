// void MAIN()
// {
//   var a = 10
//   var b = 5
//   var c = MATH_ADD(a, b)
//   var d = MATH_SUB(a, b)
//   var e = MATH_MUL(a, b)
//   var f = MATH_DIV(a, b)
//   var g = MATH_LONG_WINDED(a, b)
// }
MAIN:
    LD R[0] 10

    LD R[1] 5

    CALL MATH_ADD
    LD R[2] R[4099]

    CALL MATH_SUB
    LD R[3] R[4099]

    CALL MATH_MUL
    LD R[4] R[4099]

    CALL MATH_DIV
    LD R[5] R[4099]

    CALL MATH_LONG_WINDED
    LD R[6] R[4099]

    EXIT