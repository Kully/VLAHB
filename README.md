# This Article will Give You Assembly Superpowers!

(_Special thanks to [glouw](https://github.com/glouw) for the idea of VLAHB and his support throughout the project._)

**VLAHB** (pron. _vee-lab_) began as a passion project fueled with a genuine curiousity about the innerworkings of computers. I started the project back in early April 2019 with the goal to write a virtual machine, an assembler, an assembly language, and a way to transform my assembly code into machine-code that my virtual machine could run and understand. Many long nights and cups of coffee later, I can proudly say that VLAHB is finished.

In this post, I will present an overview of the basic principles that I learned, show some snippets of code along the way, and do my best to teach these ideas.

Checkout the [Github](https://github.com/Kully/VLAHB) page for the full project and to run on your own machine. With my language I wrote a bunch of small programs and a couple games: Pong and [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

---

#### Table of Contents

> 1. [The Basics](#the-basics) <br>
2. [Ram](#ram) <br>
3. [Virtual Machine](#virtual-machine) <br>
4. [What does Virtual Machine Read?](#what-does-virtual-machine-read) <br>
5. [Assembly](#assembly) <br>
6. [Let's Write a Simple Program](#lets-write-a-simple-program) <br>
7. [How to Build](#how-to-build)<br>
8. [Further Reading](#Further-Reading)<br>

---

## The Basics

_0s and 1s_

Look at your phone, the one that's parked next to you on the table. Now open it up and look at the back. What do you see? It's a bunch of green silicon with etches in it. In all green silicon boards that you find (in your microwave, TV, speakers, phone, Wakki Takki, digital clock) is a place where electricity, or electrons, flow in and out of other places. They chill in one corner for a bit, then move to another spot, and all this net movement of the electrons is the _actual_ reason why your phone works.

It's literally electricity that is moving from one place to another. That's it!

>>A **bit** is a representation of a value that is either 0 or 1.<br>
A **byte** is the collection of 8 bits.

Now I'm sure you might be asking "But how do the 1s and 0s do stuff?" That is a question for another blog post, as the answer to that question involves a lot of engineering knowledge that I don't fully grasp. With our first black box acknowledged, let us move forth with the post.

---

## RAM

_all computers have them_

Right now your computer right is using dedicated registers where electricity can be stored dynamically. If a computer has "8 GB of ram" according to its specs, this is telling you how much physically space on the circuit board is dedicated to this.

Imagine you have a bunch of containers or "slots" that can store numbers with a max size:

```c
[0][0][0][0][0][0][0][0]
```

This is what ram is: a bunch of slots Each slot can store a number between `$00000000` and `$FFFFFFFF` (0 to 4.29 billion). They all start with `0`s inside.

>> A hexideciaml number looks like 0XFF or 0X1A4A9<br>
Each symbol is from the set of values 0-9 and letters a-f

Disclaimer: we are _not_ touching the real slots that our computer uses and calls its ram. Instead our virtual machine will act like our computer and we will be simulating the ram slots with a list in C.

<!-- Diagram of computer within a computer: rectangle within a rectangle -->


## Virtual Machine

_How do we do stuff with our slots of ram?_

Our virtual machine is a C file. For setup, we set some initial variables and structures:

```c
uint32_t rom[ROM_SLOTS];       // rom
uint32_t ram[RAM_SLOTS];       // ram
int16_t sp;                    // stack pointer
int16_t stack[STACK_MAX_SIZE]; // stack
```

There are more in [vm.c](https://github.com/Kully/VLAHB/blob/master/vm.c) but the really important ones are `rom`, `ram`, `stack pointer` and the `stack`. We touch on these later, but notice that ram is in there.

Scroll through vm.c some more and we get to the brains of the program:

```c
switch(word0_second_half)
{
    case 0x0001:  // GOTO LABEL, GOTO k //
    {
        pc = word1;
        break;
    }
    case 0x0002:  // DIRECT LOAD //
    {
        ram[word0_first_half] = word1;
        break;
    }
    case 0x0003:  // DIRECT ADD //
    {
        ram[word0_first_half] += word1;
        break;
    }
    case 0x0004:  // DIRECT SUBTRACT //
    {
        ram[word0_first_half] -= word1;
        break;
    }
    case 0x0005:  // DIRECT MULTIPLY //
    {
        ram[word0_first_half] *= word1;
        break;
    }
    ... 
```

When the virtual machine is running, it is going to look for a file called `file.bin`. It is going to read this binary file line by line and do things based on what the binary says.

>> bin stands for binary, so file.bin is a file of 1s and 0s

Each case corresponds to an instruction in our vm. Depending on what the lines of bytes say in `file.bin`, the vm will do something different. These instructions are arbitrary. For `case 0X0001`, I could have chosen to summon a monster to eat `ram` and give birth to 2 more `rom`s. But I want to create a vm that operates _closely_ to how a real computer does.


## What does Virtual Machine Read?

Here is a snippet of the file that vm may reads

```
00040003
00000001
0001000c
00000000
00040003
00000001
0004000c
00000002
```

Okay, what does that all mean? When designing your own virtual machine, you can make it do *ANYTHING YOU WANT!* :smile: 

---

Let's say we want to load ram's 2nd slot with the number 5...then we write 2 lines of hex code:

```c
00010002
00000005
```

>This reads "load (opcode `0002`) slot `0001` with the value `00000005`"

```c
ram: [0][5][0][0][0][0]
```

Now let's say we want to add the number 2 to the same 2nd slot. We write

```c
00010003
00000002
```

>This reads "add (opcode `0003`) the value `00000002` to slot `0001` "

```c
ram: [0][5][0][0][0][0]
```

Now I'm not gonna spend anymore on these codes. If you are interested, you can read the vm.c in full. But what we get in the end is the ability to
- add
- sub
- multiply
- divide
- copy and paste sections of ram (similar to python )
- draw to the screen

```python
myList[0:4] = myList[4:8]
```

>> An "opcode" is a fancy name for the code that treated as an instruction by the virtual machine.


## VRAM

```bash
[0-4095][4096-4099][4100][4101-27141][27141-65535]
```



## Assembly:

_This is starting to get easier to read_

What if we didn't have to write `file.hex` files anymore. What if we could write more human readable code. Well, we can!

```c
LD R[1] 7 
```

asm.py converts this to

```c
00010002
00000007
```

which results in `7` getting loaded into slot `1` of ram

```c
[ ][7][ ][ ][ ][ ]
 ^  ^  ^  ^  ^  ^
 0  1  2  3  4  5
```


To read the full assembler file, [click here](https://github.com/Kully/VLAHB/blob/master/asm.py).


- Pointers!!! 4096-4099

## Let's Write a Simple Program

Here's a guide on how to write a program using our new assembly language.

```c
LD R[28000] 0  // x
LD R[28001] 0  // y
LD R[28002] 0  // number of neighbours for (x,y)
LD R[28003] 0  // index of vram for (x,y)
LD R[28004] 0  // next state of (x,y)

LD R[28005] 0  // x == 0
LD R[28006] 0  // y == 0
LD R[28007] 0  // x == 159
LD R[28008] 0  // y == 143
```


### How to Build
Ensure filename in `run.sh` is the name of a file in `/asm`

```bash
#!/bin/bash

filename="conway"

# remove -fsanitize=address to run much faster
python3 asm.py $filename.asm -s
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic -fsanitize=address vm.c -lSDL2 -lm && ./a.out bin/file.bin
```

then

```bash
$ ./run.sh
```

and you're all set! :tada:


### Further Reading

In the spirit of intellectual humility, I can assuredly say that the further reading I've procurred below is just as applicable to me as it is to any other reader of the blog. Don't let the inclusion of this section imply an intellectual supirority from the author, who I strongly suspect is napping in the room next door.

- [ ] Check out [Crash Course YouTube Channel](https://www.youtube.com/user/crashcourse) for awesome educational videos on computers
- [ ] Jack Crenshaw's [Let's Build a Compiler](https://compilers.iecc.com/crenshaw/) guide
- [ ] If you want an intro to making NES games, checkout [Easy 6502](http://www.6502.org/tutorials/6502opcodes.html) which is a Javascript 6502 Assembler and Simulator



<!-- to learn how to write an assembler that turns assembly code into to hexadecimal code, a program that takes hexadecimal code and turns it into raw bytes, and then a virtual machine ("vm") with opcodes and all, that can read your raw byte file and run the file. The entire -->