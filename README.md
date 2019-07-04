# VLAHB
**V**irtual Machine <br>
**L**anguage <br>
**A**ssembler <br>
**H**exadecimal <br>
**B**inary <br>

A Virtual Machine, Assembler, and Compiler written in Python

Some features...

- original processor design
- peep hole optimizer with unrolling loops
- statically linked
- screen display

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

## ASM - Syntax (remove this section)

`GOTO,CALL,RETURN,PUSH,POP,LD,ADD,SUB,MUL,DIV,BLIT,CLEAR,CMP,LT,LTE,GT,GTE,SIN,COS,SQRT,EXIT`

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


## Syntax - make sure to keep switching up the

A few notes first

#### About Indexing
Do not confuse the syntax `R[0:4]` with Python syntax. In VLAHB, this code snippet is refering to the values of RAM from `RAM[0]` to `RAM[4]`. In Python, the 4 index is not inclusive in the indexing but here it is.


#### About Labels
Labels are what make VLAHB function well. Standard to a lot of other assembly languages, a label is declared in code with a line that starts with a capital word that ends with a colon.

```asm

MY_LABEL:
	// code goes here
	// ...

FOO_123:
	// more code here

```

These are two examples of valid labels. These labels are not written into the `file.hex` that gets generated to be read by the virtual machine `vm.py`, but rather is used in the preprocessing before the `file.hex` is created. `asm.py` attaches a line number to each label on the backend which is _actually_ the line number of the most immediate code line (not a comment) below the label.

This way, by calling `GOTO MY_LABEL` the program knows to jump to code that comes immediately after `MY_LABEL:`. This is the precursor to functions.

#### About VLAHB Pointers
What makes coding in ASM effective (as well as fun) is using the built in pointers. We have assigned the variables `U,V,Y,Z` to point to the values stored at specific slots in RAM. In particular:

`U := R[4096]`
`V := R[4097]`
`Y := R[4098]`
`Z := R[4099]`


This means that you can programmatically change an index. As an example:

`LD R[Z] R[V]`<br>

which roughly means

`LD R[R[4099]] R[R[4097]]`<br>

These variables only work with respect to the `LD` operation and some of the uses are currently limited.

#### About VRAM

A portion of `RAM` is dedicated to the screen output. In particular, RAM[4101:19200] is for the screen output and each slot of RAM in this range holds 4btyes which is interpretted as an rgba value eg `0XFF0000FF` is red


| hex    | description                             |   assembly example     |
|--------|-----------------------------------------|------------------------|
| 0001   | GOTO: set PC to where LABEL is defined                | GOTO LABEL         |       
| 0002   | load 4278190335 at R[0] | LD R[4101] 0XFF0000FF           |       
| 0003   | add 2 to R[0]                              | ADD R[0] 2            |
| 0004   | subtract 2 from R[0]                         | SUB R[0] 2          |       
| 0005   | multiply R[0] by 2                         | MUL R[0] 2         |       
| 0006   | divide R[0] by 2                           |  DIV R[0] 2         |       
| 0007   | load R[3] into R[1]              | LD R[1] R[3]          |       
| 0008   | add R[3] to R[1]                | ADD R[1] R[3]          |       
| 0009   | subtract R[3] from R[1]           | SUB R[1] R[3]          |       
| 000a   | multiply R[1] by R[3]           | MUL R[1] R[3]          |       
| 000b   | divide R[1] by R[3]             | DIV R[1] R[3]          |       
| 000c   | skip a line if R[4] == 42  |   CMP R[4] 42        | 
| 000d   | skip a line if R[1] == R[2]  | CMP R[1] R[2]          |       
| 000f   | GOTO+POP                         | RETURN                 |       
| 0010   | skip a line if R[2] < 3  | LT R[2] 3          |       
| 0011   | skip a line if R[2] < R[3]  | LT R[2] R[3]          |       
| 0012   | skip a line if R[2] U+02264 3  | LTE R[2] 3          |       
| 0013   | skip a line if R[2] U+02264 R[3]  | LTE R[2] R[3]          |       
| 0014   | skip a line if R[2] > 3  | GT R[2] 3          |       
| 0015   | skip a line if R[2] > R[3]  | GT R[2] R[3]          |       
| 0016   | skip a line if R[2] >= 3  | GTE R[2] 3          |       
| 0017   | skip a line if R[2] >= R[3]  | GTE R[2] R[3]          |       
| 0018   | update display  | BLIT     |       
| 0019   | load square root of 16 into R[5]  | SQRT R[5] 16         |       
| 001a   | load square root of R[16] into R[5]  | SQRT R[5] R[16]          |       
| 001b   | load sine(16) into R[5]  | SIN R[5] 16         |       
| 001c   | load sine(R[16]) into R[5]  | SIN R[5] R[16]          |       
| 001d   | load cos(16) into R[5]  | COS R[5] 16         |       
| 001e   | load cos(R[16]) into R[5]   |   COS R[5] R[16]        |       
| 001f   | load RAM[0] to R[4] with 6                           | LD R[0:4] 6       |       
| 0020   | load RAM[0] to R[4] with R[6]                        | LD R[0:4] R[6]          |       
| 0021   | load RAM[0:4] with R[13:17]                          | LD R[0:4] R[13:17]          |
| 0022   | load floor(R[7]) in R[7]   | FLOOR R[7]  |
| 0023   | load ceil(R[7]) in R[7]   | CEIL R[7]  |
| 0024   | load random bit $\in$ {0,1} in R[7]   | RAND R[7]  |
| 0100   | LD R[R[4096]] R[R[4097]]                             | LD R[U] R[V]   |       
| 0101   | LD R[R[4096]:R[4097]] R[R[4098]]                     | LD R[U:V] R[Y]          |       
| 0102   | LD R[R[4096]:R[4097]] R[R[4099]:R[4098]]    | LD R[U:V] R[Z:Y]        |       
| 0103   | LD R[R[4096]:R[4097]] R[5]                   | LD R[U:V] R[5]         |       
| 0104   | LD R[R[4096]] R[3]                     | LD R[U] R[3]          |       
| 0105   | LD R[R[4096]] 42                      | LD R[U] 42      |
| fff0   | POP value from the stack and assign to PC   | POP  |
| fff1   | PUSH PC value to stack | PUSH  |
| fff2   | load VRAM slots with 0 | CLEAR | 
| ffff   | quit program      | EXIT         |       


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
| 4101-19200 | Indices for VRAM** |

* Functions takes a maximum of 16 inputs from R[0-15]
** Liable to change if screen display changes (currently 160X120)
