#include <stdio.h> 
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define ROM_SLOTS 128000
#define RAM_SLOTS 128000

uint32_t rom[ROM_SLOTS];
uint32_t ram[RAM_SLOTS];
int16_t sp;
int16_t pc;

int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        puts("./a.out file.bin");
        exit(1);
    }
    FILE* fp = fopen(argv[1], "rb");
    fread(rom, sizeof(uint32_t), ROM_SLOTS, fp);
    bool done = false;
    while(!done)
    {
        const uint32_t cmd = rom[pc + 0];
        const uint32_t num = rom[pc + 1];
        const uint16_t lower = (cmd >>  0) & 0xFFFF;
        const uint16_t upper = (cmd >> 16) & 0xFFFF;
        pc += 2;
        switch(lower) // Or was it upper?
        {
            case 0x0001:
            {
                // Code goes here.
                break;
            }
            case 0xFFFF:
            {
                done = true;
                break;
            }
            default:
            {
                printf("error: caught unknown instruction 0x%04X\n", lower);
                exit(1);
            }
        }
    }
    fclose(fp);
}
