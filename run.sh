#!/bin/bash

filename="array"

# -O turns printing off
python3 asm.py $filename.asm
gcc -Og -g -fsanitize=address bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -fsanitize=address vm.c -lSDL2 && ./a.out bin/file.bin
