// it takes ~65429 cycles for screen to update

CLEAR
GGGGGGGGFGFGFGF:
	ADD R[0] 1
	// GTE R[0] 21810
	GTE R[0] 20
	GOTO GGGGGGGGFGFGFGF
	EXIT
