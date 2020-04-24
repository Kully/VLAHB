#!/bin/bash

python3 assembler.py conway.vasm -s
gcc -O3 -march=native -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin
