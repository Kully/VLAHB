// The idea is that each time one of these tests fails
// R[0] goes up by 1.
//
// Therefore we get a count of the total number of
// failures of the tests
//
//

// eventually move these out of the 0-16 RAM index range

LD R[0] 0  // number of test failures
LD R[1] 2  // number of tests

// load values
LD R[8004] 4
LD R[8005] 5
LD R[8006] 6

//
// TESTS
//

// less than <

LT R[8005] 6
ADD R[0] 1
LT R[8005] R[8006]
ADD R[0] 1

// test <=
// test >
// test >=

EXIT









