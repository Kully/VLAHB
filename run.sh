#!/bin/bash

filename="array.asm"

# -O turns printing off
python3 asm.py $filename
python3 vm.py # -O
