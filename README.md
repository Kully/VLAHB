# from 0XFFFF to PONG

VLAHB (pron. _vee-lab_) is a passion project that was made with the aim of understanding how computers work at the lower level. Sure, anyone can boot up Python and write expressions that read like what the computer is doing after compiling, such as `x = 1 + 4` or `print("Hello World")`.

Read this guide to learn build PONG and [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) from the ground up. Don't worry about this blog sounding overly technically, I'm going to do my very best to use language that helps make the point I am trying to make and simulataneously avoid language and terms that make you want to smash your head into a computer screen with full force.

## 1. Computers are just bits

Look at your phone, the one that's parked next to you on the table. Now open it up and look at the back. What do you see? It's a bunch of green silicon with etches in it. In all green silicon boards that you find (in your microwave, TV, speakers, phone, Wakki Takki, digital clock) is a place where electricity, or electrons, flow in and out of other places. They chill in one corner for a bit, then move to another spot, and all this net movement of the electrons is the _actual_ reason why your phone works.

It's literally electricity that is moving from one place to another. That's it!








## How to Build
1. Ensure filename in `run.sh` is the name of a file in `/asm`
2. Run `$ ./run.sh`

## Technical Specs
- 16 bit virtual machine with 32-bit opcodes
- two-pass assembler
- 47 opcodes
- ~262 KB RAM
- 160X144 px resolution display
- statically-linked library



