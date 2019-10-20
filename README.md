# This Article will Give You Assembly Superpowers!

_Huge thanks to [glouw](https://github.com/glouw) for the idea of VLAHB and his support throughout the project._

VLAHB (pron. _vee-lab_) is a project that I created with the curiosity to understand and hands-on understand the low level of computers backing me, with the target to create a virtual machine and an assembly language that I could make games on.

Read this guide to learn how to write a virtual machine ("vm") that reads bytes, then a program that converts hexadecimal code to bytes that the vm reads, then an assembler that compiles assembly code to hexadecimal that compiles to bytes that the vm reads. I've included Pong and [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in the GitHub repo if you want to run those.

If you only care about running the project, go to the [How to Build](#how-to-build) section. Otherwise, keep reading for your own Assembly Superpowers! :tada:

---

#### Table of Contents

1. [Binary](#binary) <br>
2. [RAM](#RAM) <br>
3. [Hexadecimal](#Hexadecimal) <br>
4. [Assembly](#Assembly) <br>
5. [Let's Write a Simple Program](#lets-write-a-simple-program) <br>

> [How to Build](#how-to-build)<br>
[Further Reading](#Further-Reading)<br>

---

## Binary

_A little background..._

Look at your phone, the one that's parked next to you on the table. Now open it up and look at the back. What do you see? It's a bunch of green silicon with etches in it. In all green silicon boards that you find (in your microwave, TV, speakers, phone, Wakki Takki, digital clock) is a place where electricity, or electrons, flow in and out of other places. They chill in one corner for a bit, then move to another spot, and all this net movement of the electrons is the _actual_ reason why your phone works.

It's literally electricity that is moving from one place to another. That's it!

Now I'm sure you might be asking "But how do the 1s and 0s do stuff?" That is a question for another blog post, as the answer that question involves a lot of engineering knowledge that I don't fully understand. Let this be our only black box for the course, and let us move upwards.

A **bit** is a representation of a value that is either 0 or 1.<br>
A **byte** is the collection of 8 bits.

---

## RAM

Here's the deal with RAM. Your computer right now has dedicated "slots" or places where certain amounts of electricity can be stored in dynamically. When your Computer Specs say something like "8 GB of RAM", this is referring to the amount of physically space on the computer for these.

Imagine you have a bunch of buckets or slots that can contain numbers:

```c
[ ][ ][ ][ ][ ][ ][ ][ ]
```

This is what RAM is. Each slot can store a number between `$00000000` and `$FFFFFFFF` (roughly 4billion). By default, they are all 0

Disclaimer: we are _not_ going to touch the real slots that our computer uses and calls its RAM. Instead, we are going to write a Virtual Machine, or a virutal computer, to simulate what it would be like if we were able to directly target some RAM slots that we create:

<!-- Diagram of computer within a computer: rectangle within a rectangle -->


## Virtual Machine

_The brains of the operation_


So at this point we can forget electricity. We are going to use the C Programming Language to write a `vm.c` program that will create a list called ram. This is a snippet of `vm.c`

```c
uint32_t rom[ROM_SLOTS];       // rom
uint32_t ram[RAM_SLOTS];       // ram
int16_t sp;                    // stack pointer
int16_t stack[STACK_MAX_SIZE]; // stack
```



then the meat of the vm

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
```







## Hexadecimal

_Fancy Codes for Computers_

## Assembly:

_This is starting to get easier to read_


## Let's Write a Simple Program

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


## How to Build
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

then you're all set! :tada:


## Further Reading

In the spirit of intellectual humility, I can assuredly say that the further reading I've procurred below is just as applicable to me as it is to any other reader of the blog. Don't let the inclusion of this section imply an intellectual supirority from the author, who I strongly suspect is napping in the room next door.

- [ ] Check out [Crash Course YouTube Channel](https://www.youtube.com/user/crashcourse) for awesome educational videos on computers
- [ ] Jack Crenshaw's [Let's Build a Compiler](https://compilers.iecc.com/crenshaw/) guide
- [ ] If you want an intro to making NES games, checkout [Easy 6502](http://www.6502.org/tutorials/6502opcodes.html) which is a Javascript 6502 Assembler and Simulator
