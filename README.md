# VLAHB
**V**irtual Machine <br>
**L**anguage <br>
**A**ssembler <br>
**H**exadecimal <br>
**B**inary <br>

# Why VLAHB?

1. An opportunity to learn more about how hardware works
2. Build cool asm programs
3. The love of learning

# Instructions
1. Choose a filename in the `Makefile` to match the `.asm` you want to run

```
filename = draw.asm  # name of file in /asm you want to run

run:
	python asm.py $(filename)
	python vm.py

clean:  # remove all hex files in /hex
	rm -f hex/*.hex

```

2. Run `make` in root directory (you must be here for linking to work properly)

3. Sit back and enjoy the magic of code! :tada: 

## ASM - Syntax
An easy way to understand any syntax is through example.

Notes:
- `RAM` is a pythonic list
- `VRAM` is also a pythonic list
- all numerical values in any `file.asm` are integers eg. 4 != 0x04

`GOTO 4`<br>
Set PC (program counter) to line 4.

`LD R[0] 4`<br>
Load RAM[0] with value 4.

`LD R[0] R[2]`<br>
Load RAM[0] with value of RAM[2].

`LD V[0] 255,0,0,255`<br>
Load VRAM[0] with the color red

`LD V[3] V[5]`<br>
Load VRAM[3] with the value of VRAM[5]

`ADD R[2] 8`<br>
Add 8 to RAM[2].

`ADD R[2] R[6]`<br>
Add value of R[6] to RAM[2].

`SUB R[0] 3`<br>
Subtract 3 from RAM[0].

`MUL R[0] 2`<br>
Multiply RAM[0] by 2.

`DIV R[0] 2`<br>
Divide RAM[0] by 2.

`CMP R[0] R[1]`<br>
Compare RAM[0] with RAM[1].

`CMP R[0] 42`<br>
Compare RAM[0] with value 42.

```bash
if (X == Y):
    skip next line in .asm (PC += 2)
```

`CALL FUNCTION`<br>
Push PC to the Stack and set PC to where label `FUNCTION` is.

`RETURN`<br>
Pop the number from the Stack and set PC to that value.

`EXIT`<br>
Exit virtual machine.


## Opcodes

| HEX  | Opcode         |
| ---- |----------------|
| 01   | GOTO  |
| 02   | DIRECT LOAD |
| 03   | DIRECT ADD |
| 03   | DIRECT ADD |
| 04   | DIRECT SUBTRACT |
| 05   | DIRECT MULTIPLY |
| 06   | DIRECT DIVIDE |
| 07   | REGISTER TO REGISTER LOAD  |
| 08   | REGISTER TO REGISTER ADD  |
| 09   | REGISTER TO REGISTER SUBTRACT  |
| 0a   | REGISTER TO REGISTER MULTIPLY  |
| 0b   | REGISTER TO REGISTER DIVIDE  |
| 0c   | COMPARE REGISTER TO DIRECT  |
| 0d   | COMPARE REGISTER TO REGISTER  |
| 0f   | RETURN  |
| 10   | STRICT LESS THAN REGISTER TO DIRECT  |
| 11   | STRICT LESS THAN REGISTER TO REGISTER  |
| 12   | LESS THAN OR EQUAL REGISTER TO DIRECT  |
| 13   | LESS THAN OR EQUAL REGISTER TO REGISTER  |
| 14   | STRICT GREATER THAN REGISTER TO DIRECT  |
| 15   | STRICT GREATER THAN REGISTER TO REGISTER  |
| 16   | GREATER THAN OR EQUAL REGISTER TO DIRECT  |
| 17   | GREATER THAN OR EQUAL REGISTER TO REGISTER  |
| 18   | VRAM DIRECT LOAD  |
| 19   | VRAM REGISTER TO REGISTER LOAD  |
| ffff | EXIT  |


## About the RAM Slots - WIP

- a "slot in RAM" is a location in RAM that can be identified with an index eg RAM[i]
- RAM is 512KB in size => RAM has `128000` slots

#### Slot Dedication

The indices in the table below are of the form `x-y` which correspond to the standard list indexing of Python. This means the values of RAM with the range of indices `x-y` are `RAM[x], RAM[x+1], ... , RAM[y]`.

| Indices in RAM  | Dedication |
| ------------- |----------------|
| 0-4095  | Function Inputs*  |
| 4099   | Return slot for function outputs |
| 4100-... | Indices for VRAM Colors |

* Functions takes a maximum of 16 inputs from R[0-15]
