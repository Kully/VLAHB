#!/bin/bash

filename="array"

# -O turns printing off
python3 asm.py $filename.asm
gcc -O3 bin.c && ./a.out hex/file.hex bin/file.bin
gcc -O3 vm.c -lSDL2 && ./a.out bin/file.bin

# NOTE: maybe use a switch to enable this vm?
#python3 vm.py -O
