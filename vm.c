#include <stdio.h> 
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <limits.h>
#include <math.h>
#include <time.h>

// global constants
#define ROM_SLOTS 128000
#define RAM_SLOTS 128000
#define STACK_FRAME_SIZE 128
#define STACK_MAX_SIZE 32
#define VRAM_FIRST_INDEX 4100
#define MAX_RAM_VALUE UINT_MAX
#define DEBUG 0

uint32_t rom[ROM_SLOTS];
uint32_t ram[RAM_SLOTS];
int16_t sp;                    // stack pointer
int16_t stack[STACK_MAX_SIZE]; // stack


int init_pc(void)
{
    FILE* file = fopen("start_pc.txt", "r");
    int pc = 0;
    fscanf(file, "%d\n", &pc);
    fclose(file);
    return pc;
}


uint16_t letter_code_to_ram_index(uint16_t letter_code)
{
    switch(letter_code)
    {
        case 1: {
            return 4096;  // U
        }
        case 2: {
            return 4097;  // V
        }
        case 3: {
            return 4098;  // Y
        }
        case 4: {
            return 4099;  // Z
        }
    }
    return -1;
}


void loadPixelsToVram(uint32_t array0[ ],
                      uint32_t array1[ ],
                      uint32_t i,
                      uint32_t j,
                      uint32_t width)
{
    // i: array0 start index
    // j: array1 end index
    //
    // equivalent to `array0[i:i+width] = array1[j:j+width]` in Python
    for(uint32_t x = 0; x < width; x++)
    {
        if((array1[j+x] & 0xFF) == 255)  // check if alpha is 0XFF
        {
            array0[i+x] = array1[j+x];
        }
    }
}


void convert_endianess(void)
{
    for(int32_t i = 0; i < ROM_SLOTS; i++)
    {
        const uint32_t temp = rom[i];
        rom[i] =
            (((temp >> 24) & 0xFF) << 0x00) | (((temp >> 16) & 0xFF) << 0x08) |
            (((temp >>  8) & 0xFF) << 0x10) | (((temp >>  0) & 0xFF) << 0x18);
    }
}


int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        puts("./a.out file_r.bin");
        exit(1);
    }

    const int xres = 160;  // new res 800
    const int yres = 120;  // new res 640
    SDL_Window* window = SDL_CreateWindow("VLAB VM", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, xres, yres, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STREAMING, xres, yres);
    FILE* fp = fopen(argv[1], "rb");
    fread(rom, sizeof(uint32_t), ROM_SLOTS, fp);
    convert_endianess();
    bool done = false;

    // set program counter
    int pc = init_pc();

    while(!done)
    {
        const uint32_t word0 = rom[pc + 0];
        const uint32_t word1 = rom[pc + 1];
        const uint16_t word0_first_half = (word0 >> 16) & 0xFFFF;
        const uint16_t word0_second_half = (word0 >> 0) & 0xFFFF;
#if DEBUG == 1
        printf("word0: 0x%08X\n", word0);
        printf("word1: 0x%08X\n", word1);
        printf("pc: %i\n", pc);
        printf("sp: %i\n", sp);
        printf("stack[0,1,2]: [%i,%i,%i]\n", stack[0],stack[1],stack[2]);
        printf("ram\n");
        printf("    0: %u\n", ram[0]);
        printf("    1: %u\n", ram[1]);
        printf("    2: %u\n", ram[2]);
        printf("    3: %u\n", ram[3]);
        printf("\n\n");
#endif
        pc += 2;
        switch(word0_second_half)
        {
            case 0x0001:  // GOTO //
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
            case 0x0006:  // DIRECT DIVIDE //
            {
                ram[word0_first_half] /= word1;
                break;
            }
            case 0x0007:  // REGISTER TO REGISTER LOAD //
            {
                ram[word0_first_half] = ram[word1];
                break;
            }
            case 0x0008:  // REGISTER TO REGISTER ADD //
            {
                ram[word0_first_half] += ram[word1];
                break;
            }
            case 0x0009:  // REGISTER TO REGISTER SUBTRACT //
            {
                ram[word0_first_half] -= ram[word1];
                break;
            }
            case 0x000a:  // REGISTER TO REGISTER MULTIPLY //
            {
                ram[word0_first_half] *= ram[word1];
                break;
            }
            case 0x000b:  // REGISTER TO REGISTER DIVIDE //
            {
                ram[word0_first_half] /= ram[word1];
                break;
            }
            case 0x000c:  // COMPARE REGISTER TO DIRECT //
            {
                if(ram[word0_first_half] == word1) pc += 2;
                break;
            }
            case 0x000d:  // COMPARE REGISTER TO REGISTER //
            {
                if(ram[word0_first_half] == ram[word1]) pc += 2;
                break;
            }
            case 0x000e:  // CALL (GOTO AND PUSH) //
            {
                stack[sp] = pc;
                int a = STACK_FRAME_SIZE * (0 + sp);
                int b = STACK_FRAME_SIZE * (1 + sp);
                for(int x = 0; x < b; x++) ram[a + x] = ram[0 + x];

                sp += 1;  // increment stack pointer
                pc = word1; // GOTO

                break;
            }
            case 0x000f:  // RETURN (GOTO AND POP) //
            {
                int a = STACK_FRAME_SIZE * (0 + sp);
                int b = STACK_FRAME_SIZE * (1 + sp);
                for(int x = 0; x < b; x++) ram[0 + x] = ram[a + x];

                // pop from stack and assign to pc
                sp -= 1;
                pc = stack[sp];

                break;
            }
            case 0x0010:  // STRICT LESS THAN REGISTER TO DIRECT a < b //
            {
                if(ram[word0_first_half] < word1) pc += 2;
                break;
            }
            case 0x0011:  // STRICT LESS THAN REGISTER TO REGISTER a < b //
            {
                if(ram[word0_first_half] < ram[word1]) pc += 2;
                break;
            }
            case 0x0012:  // LESS THAN OR EQUAL REGISTER TO DIRECT a <= b //
            {
                if(ram[word0_first_half] <= word1) pc += 2;
                break;
            }
            case 0x0013:  // LESS THAN OR EQUAL REGISTER TO REGISTER a <= b //
            {
                if(ram[word0_first_half] <= ram[word1]) pc += 2;
                break;
            }
            case 0x0014:  // STRICT GREATER THAN REGISTER TO DIRECT a > b //
            {
                if(ram[word0_first_half] > word1) pc += 2;
                break;
            }
            case 0x0015:  // STRICT GREATER THAN REGISTER TO REGISTER a > b //
            {
                if(ram[word0_first_half] > ram[word1]) pc += 2;
                break;
            }
            case 0x0016:  // GREATER THAN OR EQUAL REGISTER TO DIRECT a >= b //
            {
                if(ram[word0_first_half] >= word1) pc += 2;
                break;
            }
            case 0x0017:  // GREATER THAN OR EQUAL REGISTER TO REGISTER a >= b //
            {
                if(ram[word0_first_half] >= ram[word1]) pc += 2;
                break;
            }
            case 0x0018:  // BLIT //
            {
                void* raw;
                int32_t pitch;
                SDL_LockTexture(texture, NULL, &raw, &pitch);
                uint32_t* pixels = (uint32_t*) raw;

                for(int y = 0; y < yres; y++)
                for(int x = 0; x < xres; x++)
                    pixels[x + y * xres] = ram[VRAM_FIRST_INDEX + x + y * xres];

                SDL_UnlockTexture(texture);
                SDL_RenderCopy(renderer, texture, NULL, NULL);
                SDL_RenderPresent(renderer);
                break;
            }
            case 0x0019:  // DIRECT SQRT ???
            {
                ram[word0_first_half] = sqrt(word1);
                break;
            }
            case 0x001a:  // REGISTER TO REGISTER SQRT ???
            {
                ram[word0_first_half] = sqrt(ram[word1]);
                break;
            }
            case 0x001b:  // DIRECT SIN ???
            {
                ram[word0_first_half] = sin(word1);
                break;
            }
            case 0x001c:  // REGISTER TO REGISTER SIN ???
            {
                ram[word0_first_half] = sin(ram[word1]);
                break;
            }
            case 0x001d:  // DIRECT COS ???
            {
                ram[word0_first_half] = cos(word1);
                break;
            }
            case 0x001e:  // REGISTER TO REGISTER COS ???
            {
                ram[word0_first_half] = cos(ram[word1]);
                break;
            }
            case 0x0020:  // LD R[i:j] R[k] ???
            {
                uint16_t i = (rom[ pc - 2] >> 16) & 0XFFFF;
                uint16_t j = (rom[ pc - 1] >> 16) & 0XFFFF;
                uint16_t k = (rom[ pc - 1] >> 0) & 0XFFFF;

                for(int x=0; x<(j+1-i); x++) {
                    ram[i + x] = ram[k];
                }

                break;
            }
            case 0x0021:  // LD R[i:j] R[k:l] ???
            {
                // Code goes here - WIP
                break;
            }
            case 0x0022:  // FLOOR ???
            {
                ram[word1] = floor(ram[word1]);
                break;
            }
            case 0x0023:  // CEIL ???
            {
                ram[word1] = ceil(ram[word1]);
                break;
            }
            case 0x0024:  // RAND ???
            {   
                int random_bit = rand() % 2;
                ram[word1] = random_bit;
                break;
            }
            case 0x0025:  // ARRAY
            {
                const uint16_t label_idx = word0_first_half;

                const uint16_t x_sprite = (rom[pc - 1] >> 24) & 0xFF;
                const uint16_t y_sprite = (rom[pc - 1] >> 16) & 0XFF;
                const uint16_t width_sprite = (rom[pc - 1] >> 8) & 0XFF;
                const uint16_t height_sprite = (rom[pc - 1]) & 0xFF;

                const uint16_t vram_idx = 4101 + x_sprite + 160*y_sprite;

                for(int h = 0; h < height_sprite; h++)
                {
                    loadPixelsToVram(ram, rom, vram_idx + (h*160),
                                     label_idx + h*width_sprite,
                                     width_sprite);
                }

                break;
            }
            case 0x0100:  // LD R[U] R[V] //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t j = (word0_first_half >> 8) & 0XF;  // 0j00

                const uint16_t ram_index_i = letter_code_to_ram_index(i);
                const uint16_t ram_index_j = letter_code_to_ram_index(j);

                ram[ram[ram_index_i]] = ram[ram[ram_index_j]];

                break;
            }
            case 0x0101:  // LD R[U:V] R[Y] //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t j = (word0_first_half >> 8) & 0XF;  // 0j00
                const uint16_t k = (word0_first_half >> 4) & 0XF;  // 00k0

                const uint16_t ram_index_i = letter_code_to_ram_index(i);
                const uint16_t ram_index_j = letter_code_to_ram_index(j);
                const uint16_t ram_index_k = letter_code_to_ram_index(k);

                int32_t array_span = ram[ram_index_j] - ram[ram_index_i];

                for(int idx = 0; idx < array_span; idx++)
                {
                    ram[ram[ram_index_i] + idx] = ram[ram[ram_index_k]];    
                }

                break;
            }
            case 0x0102:  // LD R[U:V] R[Y:Z] //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t j = (word0_first_half >> 8) & 0XF;  // 0j00
                const uint16_t k = (word0_first_half >> 4) & 0XF;  // 00k0
                // does not use 000l bit

                const uint16_t ram_index_i = letter_code_to_ram_index(i);
                const uint16_t ram_index_j = letter_code_to_ram_index(j);
                const uint16_t ram_index_k = letter_code_to_ram_index(k);

                int32_t array_span = ram[ram_index_j] - ram[ram_index_i];

                for(int idx = 0; idx < array_span; idx++)
                {
                    ram[ram[ram_index_i] + idx] = ram[ram[ram_index_k] + idx];
                }
                break;
            }
            case 0x0103:  // LD R[U:V] R[k] //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t j = (word0_first_half >> 8) & 0XF;  // 0j00

                const uint16_t ram_index_i = letter_code_to_ram_index(i);
                const uint16_t ram_index_j = letter_code_to_ram_index(j);

                int32_t array_span = ram[ram_index_j] - ram[ram_index_i];

                for(int idx = 0; idx < array_span; idx++)
                {
                    ram[ram[ram_index_i] + idx] = ram[word1];
                }

                break;
            }
            case 0x0104:  // LD R[U] R[i] //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t ram_index_i = letter_code_to_ram_index(i);

                ram[ram[ram_index_i]] = ram[word1];

                break;
            }
            case 0x0105:  // LD R[U] i //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t ram_index_i = letter_code_to_ram_index(i);

                ram[ram[ram_index_i]] = word1;

                break;
            }
            case 0x0106:  // LD R[U:V] i //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t j = (word0_first_half >> 8) & 0XF;  // 0j00

                const uint16_t ram_index_i = letter_code_to_ram_index(i);
                const uint16_t ram_index_j = letter_code_to_ram_index(j);

                int32_t array_span = ram[ram_index_j] - ram[ram_index_i];

                for(int idx = 0; idx < array_span; idx++)
                {
                    ram[ram[ram_index_i] + idx] = word1;
                }


                break;
            }
            case 0x0107:  // COMPARE UV TO DIRECT //
            {
                const uint16_t i = (word0_first_half >> 12) & 0XF; // i000
                const uint16_t ram_index_i = letter_code_to_ram_index(i);

                if(ram[ram[ram_index_i]] == word1) pc += 2;

                break;
            }
            case 0xfff0:  // POP ???
            {
                int a = STACK_FRAME_SIZE * (0 + sp);
                int b = STACK_FRAME_SIZE * (1 + sp);
                for(int x = 0; x < b; x++) ram[0 + x] = ram[a + x];

                // pop from stack and don't change pc
                sp -= 1;
                break;
            }
            case 0xfff1:  // PUSH ???
            {
                stack[sp] = pc;
                int a = STACK_FRAME_SIZE * (0 + sp);
                int b = STACK_FRAME_SIZE * (1 + sp);
                for(int x = 0; x < b; x++) ram[a + x] = ram[0 + x];

                sp += 1;  // increment stack pointer
                break;
            }
            case 0xfff2:  // CLEAR //
            {
                void* raw;
                int32_t pitch;
                SDL_LockTexture(texture, NULL, &raw, &pitch);
                uint32_t* pixels = (uint32_t*) raw;

                for(int y = 0; y < yres; y++)
                {
                    for(int x = 0; x < xres; x++)
                    {
                        ram[VRAM_FIRST_INDEX + x + y * xres] = word1;
                        pixels[x + y * xres] = ram[VRAM_FIRST_INDEX + x + y * xres];
                    }
                }

                SDL_UnlockTexture(texture);
                SDL_RenderCopy(renderer, texture, NULL, NULL);
                SDL_RenderPresent(renderer);

                break;
            }
            case 0Xfff3:  // INPUT //
            {
                ram[word0_first_half] = 0XFFFFFFFF;
                break;
            }
            case 0xffff:
            {
                done = true;
                break;
            }
            default:
            {
                printf("error: caught unknown instruction 0x%04X\n", word0_second_half);
                exit(1);
            }
        }
    }
    fclose(fp);
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyTexture(texture);
}
