#!/bin/bash

filename="array"

# -O turns printing off
python3 asm.py $filename.asm
python3 vm.py  # -O
