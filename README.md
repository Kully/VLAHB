# VLAHB
**V**irtual Machine, **L**anguage, **A**ssembler, **H**exadecimal, **B**inary

# Instructions
1. Edit/Write a `.asm` file
2. Open `Makefile` to make sure all variables are correct
3. Run `make` in root directory

## Assembly Syntax
The best way to understand the syntax is through example.

RAM is a list

`GOTO 4`<br>
Set PC (program counter) to line 4

`LD R[0] 4`
Load RAM[0] with value 4

`LD R[0] R[2]`
Load RAM[0] with value of RAM[2]

`ADD R[2] 8`
Add 8 to RAM[2]


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
