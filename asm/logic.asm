LOGIC_OR:
	LD R[4100] 1
	CMP R[0] 0
	RETURN
	CMP R[1] 0
	RETURN
	LD R[4100] 0
	RETURN


LOGIC_AND:
 	// count num of 1s in R[4]
	LD R[4100] 0

	CMP R[0] 0
	ADD R[4] 1

	CMP R[1] 0
	ADD R[4] 1

	CMP R[4] 2
	RETURN
	LD R[4100] 1
	LD R[4] 0  // reset R[4] to 0
	RETURN
