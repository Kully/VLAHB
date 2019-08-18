#!/bin/bash

# filename="***ball_bouncing_off_walls"
filename="array"

# -O turns printing off
python3 asm.py $filename.asm
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address vm.c -lSDL2 -lm && ./a.out bin/file.bin
