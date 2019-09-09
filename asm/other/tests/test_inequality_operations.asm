// tests for <, <=, >, >=
//           LT LTE GT GTE
//
// R[0] <- number of test failures
// R[1] <- number of tests

// TODO - eventually move these out of the 0-16 RAM index range

LD R[0] 0  // number of test failures
LD R[1] 12  // number of tests

// load values in RAM
LD R[8004] 4
LD R[8005] 5
LD R[8006] 6

// test: <
LT R[8005] 6
	ADD R[0] 1
LT R[8005] R[8006]
	ADD R[0] 1

// test: <=
LTE R[8005] 6
	ADD R[0] 1
LTE R[8005] R[8006]
	ADD R[0] 1
LTE R[8006] 6
	ADD R[0] 1
LTE R[8006] R[8006]
	ADD R[0] 1

// test: >
GT R[8006] 5
	ADD R[0] 1
GT R[8006] R[8005]
	ADD R[0] 1

// test: >=
GTE R[8006] 5
	ADD R[0] 1
GTE R[8006] R[8005]
	ADD R[0] 1
GTE R[8006] 6
	ADD R[0] 1
GTE R[8006] R[8006]
	ADD R[0] 1

EXIT
