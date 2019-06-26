// Add these to ASM lang

// [ ] LD R[U] 42
// [ ] LD R[U] R[42]

// [ ] LD R[U:V] 42
// [X] LD R[U:V] R[42]


LD R[65000] 0XFF0000FF

LD R[4096] 4100
LD R[4097] 4261

ASDF:
	LD R[U:V] R[65000]
	ADD R[4096] 160
	ADD R[4097] 160
	BLIT
	GOTO ASDF




EXIT