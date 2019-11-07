# VLAHB

Write your own games and programs with a _brand new_ assembly langauge in `VLAHB`! (pron. _"vee-lab"_)

####

__Specs__

- virtual machine, assembler, compiler
- 48 opcodes
- 262 kb of ram
- 160x144 pixel display
- static linking capable
- 60 fps
- vm runs on SDL2
- written in C and Python
- lots of fun! :smile_cat:

####

**V**irtual machine<br>
**L**anguage<br>
**A**ssembly<br>
**H**ex<br>
**B**inary<br>


## Steps to Build

#### Step 1

Modify the `python3 asm.py conway.asm -s` line in run.sh

```bash
#!/bin/bash

python3 asm.py conway.asm -s
gcc -Og -g -Wall -Wextra -Wpedantic bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin

```

Note that `-s` is a flag for statically-linking all the .asm files in the /asm directory. If you list 1 or more .asm filenames w/o the -s flag, it will only compile those files and start at the first one. If you list 1 or more .asm filenames with the `-s` flag, it will compile _all_ the files in the /asm directory and start with the first one.

| code | meaning |
|:-------|:------|
| `$ python3 asm.py A.asm B.asm C.asm` | Compile A, B and C and start the vm at A.asm |
| `$ python3 asm.py C.asm -s` | Compile all files in /asm and start at top of C.asm |
| `$ python3 asm.py B.asm C.asm -s` | Compile all files in /asm and start at top of B.asm |

#### Step 2

```bash
$ ./run.sh
```

Happy Coding! :tada: :tada: :tada:

---


<!-- For a more educational walkthrough of **VLAHB** checkout the [blog post](http://adamkulidjian.com/vlahb-blog/) -->
