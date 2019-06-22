// fun rgba program

// slot 1: 4100
// slot N:  43200

// red == ff0000ff == 4278190335
// green == 00ff00ff == 16711935


ADAM_DRAWS:

	LD R[4100:9300] 16711935
	BLIT

	GOTO ADAM_DRAWS


EXIT
