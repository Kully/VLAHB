#!/bin/bash

python3 asm.py ball_bouncing.asm -s
gcc -Og -g -Wall -Wextra -Wpedantic bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin
