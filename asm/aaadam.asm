// fun rgba program

// slot 1: 4100
// slot N:  43200

// red == ff0000ff == 4278190335
// green == 00ff00ff == 16711935

// LD R[1] 3
// LD R[1:6] 3
LD R[0:3] 7

LD R[5:7] R[1:3]
EXIT
