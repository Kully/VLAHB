#!/bin/bash

python3 asm.py pong.asm -s
gcc -O3 -march=native -Wall -Wextra -Wpedantic bin.c && ./a.out hex/file.hex bin/file.bin
gcc -O3 -march=native -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin
