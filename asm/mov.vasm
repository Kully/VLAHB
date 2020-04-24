// **********************
// mov is turing complete
// **********************
// - make sure DEBUG=1 in vm.c to see registers


// Ex. 1: branching
//
// if (i == j)
//    load R[4] with 1
// else
//    load R[4] with 1

LD R[4096] 2   // store i
LD R[4097] 2   // store j
LD R[4098] 4   // store k

LD R[U] 0      // mov [R_i], 0
LD R[V] 1      // mov [R_j], 1
LD R[Y] R[U]   // mov R_k, [R_i]
EXIT