all:
	gcc -O3 vm.c -lSDL2 -lm -o vm
	gcc -O3 lang.c -o lang
	gcc -O3 bin.c -o binner
