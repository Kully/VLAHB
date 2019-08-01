// ********************************
// Stack Overflow Underflow Tests *
// ********************************

// test #1
LD R[4099] 0XFFFFFFFF
MUL R[4099] 1
EXIT
// expect R[4099] == 0XFFFFFFFF

// test #2
LD R[4099] 1
MUL R[4099] 0XFFFFFFFF
EXIT
// expect R[4099] == 0XFFFFFFFF

// test #3 - overflow
LD R[4099] 0XFFFFFFFF
ADD R[4099] 1
EXIT
// expect R[4099] == 0

// test #4 - underflow
LD R[4099] 0
SUB R[4099] 1
EXIT
// expect R[4099] == 0XFFFFFFFF

EXIT
