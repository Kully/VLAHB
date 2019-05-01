# VLAHB
**V**irtual Machine, **L**anguage, **A**ssembler, **H**exadecimal, **B**inary

# Instructions
1. Edit/Write a `.asm` file
2. Open `Makefile` to make sure all variables are correct
3. Run `make` in root directory

## Assembly Syntax
The best way to understand the syntax is through example.

Tips:
- RAM is a list
- all numerical values in your `file.asm` are integers
  eg. 4 != 0x04

`GOTO 4`<br>
Set PC (program counter) to line 4

`LD R[0] 4`<br>
Load RAM[0] with value 4

`LD R[0] R[2]`<br>
Load RAM[0] with value of RAM[2]

`ADD R[2] 8`<br>
Add 8 to RAM[2]

`ADD R[2] R[6]`<br>
Add value of R[6] to RAM[2]

`SUB R[0] 3`<br>
Subtract 3 from RAM[0]

`MUL R[0] 2`<br>
Multiply RAM[0] by 2

`DIV R[0] 2`<br>
Divide RAM[0] by 2

`CMP R[0] R[1]`<br>
Compare RAM[0] with RAM[1].

`CMP R[0] 42`<br>
Compare RAM[0] with value 42.

```bash
if they match:
    skip next line in `.asm` (PC += 2)
else:
    go to next line
```





Example Program: "Clock"
```

```




## Op Codes for Hex

```
1    == GOTO
2    == DIRECT LOAD
3    == DIRECT ADD
4    == DIRECT SUBTRACT
5    == DIRECT MULTIPLY
6    == DIRECT DIVIDE
7    == REGISTER TO REGISTER LOAD
8    == REGISTER TO REGISTER ADD
9    == REGISTER TO REGISTER SUBTRACT
a    == REGISTER TO REGISTER MULTIPLY
b    == REGISTER TO REGISTER DIVIDE
c    == COMPARE REGISTER TO VALUE
d    == COMPARE REGISTER TO REGISTER
ffff == EXIT
```
