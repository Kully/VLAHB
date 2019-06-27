# VLAHB
**V**irtual Machine <br>
**L**anguage <br>
**A**ssembler <br>
**H**exadecimal <br>
**B**inary <br>

## What?
A virtual machine written in Python with original compiler and processor design with display using Pygame.

## Why?

1. An opportunity to learn and write algorithms in a primative programming language.
2. Build cool assembly programs.
3. The love and curiosity of learning.

## Instructions
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

`GOTO 4`<br>
Set PC (program counter) to line 4.

`LD R[0] 4`<br>
Load RAM[0] with value 4.

`LD R[0] R[2]`<br>
Load RAM[0] with value of RAM[2].

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

`CMP A B`<br>
If A == B, skip next line of assembly code.

`LT A B`<br>
If A $\lt$ B, skip next line of assembly code.

`LTE A B`<br>
If A $\leq$ B, skip next line of assembly code.

`GT A B`<br>
If A $\gt$ B, skip next line of assembly code.

`GTE A B`<br>
If A $\geq$ B, skip next line of assembly code.

`CALL FUNCTION`<br>
Push PC to the Stack and set PC to where label `FUNCTION` is.

`RETURN`<br>
Pop the number from the Stack and set PC to that value.

`EXIT`<br>
Exit virtual machine.


What makes coding in ASM effective (as well as fun) is using the built in pointers. We have assigned the variables `U,V,Y,Z` to point to the values stored at specific slots in RAM. In particular:

```
U := R[4096]
V := R[4097]
Y := R[4098]
Z := R[4099]
```


## Opcodes

| HEX  | Opcode         |
| ---- |----------------|
| 0001   | GOTO  |
| 0002   | DIRECT LOAD |
| 0003   | DIRECT ADD |
| 0003   | DIRECT ADD |
| 0004   | DIRECT SUBTRACT |
| 0005   | DIRECT MULTIPLY |
| 0006   | DIRECT DIVIDE |
| 0007   | REGISTER TO REGISTER LOAD  |
| 0008   | REGISTER TO REGISTER ADD  |
| 0009   | REGISTER TO REGISTER SUBTRACT  |
| 000a   | REGISTER TO REGISTER MULTIPLY  |
| 000b   | REGISTER TO REGISTER DIVIDE  |
| 000c   | COMPARE REGISTER TO DIRECT  |
| 000d   | COMPARE REGISTER TO REGISTER  |
| 000f   | RETURN  |
| 0010   | STRICT LESS THAN REGISTER TO DIRECT  |
| 0011   | STRICT LESS THAN REGISTER TO REGISTER  |
| 0012   | LESS THAN OR EQUAL REGISTER TO DIRECT  |
| 0013   | LESS THAN OR EQUAL REGISTER TO REGISTER  |
| 0014   | STRICT GREATER THAN REGISTER TO DIRECT  |
| 0015   | STRICT GREATER THAN REGISTER TO REGISTER  |
| 0016   | GREATER THAN OR EQUAL REGISTER TO DIRECT  |
| 0017   | GREATER THAN OR EQUAL REGISTER TO REGISTER  |
| 0018   | BLIT  |
| 0019   | DIRECT SQRT  |
| 001a   | REGISTER TO REGISTER SQRT  |
| 001b   | DIRECT SIN  |
| 001c   | REGISTER TO REGISTER SIN  |
| 001d   | DIRECT COS  |
| 001e   | REGISTER TO REGISTER COS  |
| ffff | EXIT  |


## Technical Details/Slot Dedication

- `RAM` is a pythonic list
- a "slot in RAM" is a location in RAM that can be identified with an index eg. RAM[i]
- RAM is 512KB in size which means RAM has `128000` slots
- all numerical values in any `.asm` file should be interpretted by humans as integers. Having said this, you can only direct load hex values eg. `LD R[4100] 0XFF0000FF`

The indices in the table below are of the form `x-y` which correspond to the standard list indexing of Python. This means the values of RAM with the range of indices `x-y` are `RAM[x], RAM[x+1], ... , RAM[y]`.

| Indices in RAM  | Dedication |
| ------------- |----------------|
| 0-4095  | Function Inputs*  |
| 4096-4099  | Pointers for Indices (U,V,Y,Z resp)  |
| 4100    | Return slot for function outputs |
| 4101-43201 | Indices for VRAM** |

* Functions takes a maximum of 16 inputs from R[0-15]
** Liable to change if screen display changes (currently 160X120)
