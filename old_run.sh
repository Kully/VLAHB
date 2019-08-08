#!/bin/bash

filename="test"

# -O turns printing off
python3 asm.py $filename.asm
python3 vm.py -O
