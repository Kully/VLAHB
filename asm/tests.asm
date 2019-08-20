// test all non-screen-output opcodes

// direct opcodes
// LD R[0] 4   // 4
// ADD R[0] 2  // 6
// SUB R[0] 2  // 4
// MUL R[0] 2  // 8
// DIV R[0] 2  // 4

// LD R[9999] 4
// CMP R[0] 9999
// CMP R[0] R[9999]
// EXIT  // should not exit

// // register opcodes
// LD R[0] R[9999]
// ADD R[0] R[9999]
// SUB R[0] R[9999]
// MUL R[0] R[9999]
// DIV R[0] R[9999]
LD R[3] 42

LD R[0] 4
LD R[1] 5
LD R[2] 6

GTE R[2] R[0]
LD R[3] 69  // if false
EXIT
