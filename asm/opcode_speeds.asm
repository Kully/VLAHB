// test every opcode
// INCOMPLETE

LD R[1] 50
LD R[0] R[1]
ADD R[0] 4
ADD R[0] R[4]

CALL OPCODE_TEST_LABEL
EXIT

OPCODE_TEST_LABEL:
	ADD R[65000] 1
	CMP R[65000] 5
	GOTO OPCODE_TEST_LABEL
	RETURN