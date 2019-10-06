#!/bin/bash

filename="tetris"

# remove -fsanitize=address to run much faster
python3 asm.py $filename.asm -s
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address vm.c -lSDL2 -lm && ./a.out bin/file.bin
