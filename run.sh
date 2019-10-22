#!/bin/bash
# conway.asm

python3 asm.py conway.asm -s
gcc -Og -g -Wall -Wextra -Wpedantic bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin
