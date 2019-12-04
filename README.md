# VLAHB
_Checkout the [blog post](http://adamkulidjian.com/vlahb-blog/) of _VLAHB_ for an overview of the assembly language_

## Building

### Step 1: Pick which asm files to compile in [run.sh](https://github.com/Kully/VLAHB/blob/master/run.sh#L3)

Note that `-s` is a flag for statically-linking all the .asm files in the /asm directory. If you list 1 or more .asm filenames w/o the -s flag, it will only compile those files and start at the first one. If you list 1 or more .asm filenames with the `-s` flag, it will compile _all_ the files in the /asm directory and start with the first one.

| code | meaning |
|:-------|:------|
| `$ python3 assembler.py A.asm B.asm C.asm` | Compile A, B and C and start the vm at A.asm |
| `$ python3 assembler.py C.asm -s` | Compile all files in /asm and start at top of C.asm |
| `$ python3 assembler.py B.asm C.asm -s` | Compile all files in /asm and start at top of B.asm |

### Step 2: `$ ./run.sh`

<b>Tip:</b> Run `$ xxd -c 4 bin/file.bin` to view the machine code displayed as hex in the terminal.

### Step 3: Write your own games and programs with a brand new assembly langauge called V-ASM! :tada: :tada: :tada:

---

<u>Specs</u>

- virtual machine, assembler/compiler
- 48 opcodes
- 262 kb of ram
- 160x144 pixel display
- static linking capable
- 60 fps
- vm runs on SDL2
- written in C and Python
- lots of fun! :smile_cat:

`V`irtual machine<br>
`L`inker<br>
`A`ssembly<br>
`H`ex<br>
`B`inary<br>
