// Here I use RAM slot 512 as the return register.
// We should agree on a proper return register.

// var MATH_ADD(var a, var b)
// {
//     a += b
//     return a
// }
MATH_ADD:
    ADD R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var MATH_SUB(var a, var b)
// {
//     a -= b
//     return a
// }
MATH_SUB:
    SUB R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var MATH_MUL(var a, var b)
// {
//     a *= b
//     return a
// }
MATH_MUL:
    MUL R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var MATH_DIV(var a, var b)
// {
//     a /= b
//     return a
// }
MATH_DIV:
    DIV R[0] R[1]
    LD R[4100] R[0]
    RETURN

// var MATH_LONG_WINDED(var a, var b)
// {
//     b = MATH_ADD(a, b)
//     b = MATH_ADD(a, b)
//     b = MATH_ADD(a, b)
//     b = MATH_ADD(a, b)
//     return b//
// }
MATH_LONG_WINDED:
    CALL MATH_ADD
    LD R[1] R[4100] // 15
    CALL MATH_ADD
    LD R[1] R[4100] // 25
    CALL MATH_ADD
    LD R[1] R[4100] // 35
    CALL MATH_ADD
    RETURN // 45


MATH_FLOOR_DIV:
    // Python: R[0] // R[1]
    GTE R[0] R[1]
    RETURN
    ADD R[4100] 1
    SUB R[0] R[1]
    GOTO MATH_FLOOR_DIV


// not complete
MATH_MODULO:
    // Python: R[0] % R[1]
    GTE R[0] R[1]
    RETURN
    LD R[4100] R[0]
    SUB R[0] R[1]
    GOTO MATH_MODULO





