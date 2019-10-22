# VLAHB

### How to Build
Ensure filename in run.sh is the name of a file in the /asm directory

```bash
#!/bin/bash

# remove -fsanitize=address to run much faster
python3 asm.py pong.asm std.asm
gcc -Og -g -Wall -Wextra -Wpedantic bin.c && ./a.out hex/file.hex bin/file.bin
gcc -Og -g -Wall -Wextra -Wpedantic vm.c -lSDL2 -lm && ./a.out bin/file.bin
```

then

```bash
$ ./run.sh
```

and you're all set! :tada:

Note about L6 in run.sh