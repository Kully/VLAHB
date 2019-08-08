#include <stdio.h> 
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <math.h>
#include <time.h>


#define ROM_SLOTS 128000
#define RAM_SLOTS 128000
#define MAX_RAM_VALUE 0XFFFFFFFF  // does this work ?


uint32_t rom[ROM_SLOTS];
uint32_t ram[RAM_SLOTS];
int16_t sp;
int16_t pc;

// seed the random generator
srand(time(NULL));

int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        puts("./a.out file.bin");
        exit(1);
    }

    const int displayScale = 1;  // see vm.py for same const
    const int xres = 800;  // why is this not 160
    const int yres = 640;  // why is this not 120
    SDL_Window* window = SDL_CreateWindow("VLAB VM", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, xres, yres, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STREAMING, xres, yres);
    FILE* fp = fopen(argv[1], "rb");
    fread(rom, sizeof(uint32_t), ROM_SLOTS, fp);
    bool done = false;
    while(!done)
    {
        // const uint32_t cmd = rom[pc + 0];
        // const uint32_t num = rom[pc + 1];
        // const uint16_t lower = (num >>  0) & 0xFFFF;
        // const uint16_t upper = (cmd >> 16) & 0xFFFF;

        const uint32_t word0 = rom[pc + 0];
        const uint32_t word1 = rom[pc + 1];

        const uint16_t word0_first_half = (word0 >> 16) & 0xFFFF;
        const uint16_t word0_second_half = (word0 >> 0) & 0xFFFF;

        const uint16_t word1_first_half = (word1 >> 16) & 0xFFFF;
        const uint16_t word1_second_half = (word1 >> 0) & 0xFFFF;

        // *=====*
        // legend
        // *=====*
        //
        // [0000][0000]
        // [0000][0000]
        //
        // [word0]
        // [word1]
        //
        // [word0_first_half][word0_second_half]
        // [word1_first_half][word1_second_half]

        pc += 2;
        switch(word0_second_half) // Or was it upper?
        {
            case 0x0001:  // GOTO
            {
                pc = word1;
                break;
            }
            case 0x0002:  // DIRECT LOAD
            {
                ram[word0_first_half] = word1;
                break;
            }
            case 0x0003:  // DIRECT ADD
            {
                ram[word0_first_half] += word1
                break;
            }
            case 0x0004:  // DIRECT SUBTRACT
            {
                ram[word0_first_half] -= word1
                break;
            }
            case 0x0005:  // DIRECT MULTIPLY
            {
                ram[word0_first_half] *= word1
                break;
            }
            case 0x0006:  // DIRECT DIVIDE
            {
                ram[word0_first_half] /= word1
                break;
            }
            case 0x0007:  // REGISTER TO REGISTER LOAD
            {
                ram[word0_first_half] = ram[word1]
                break;
            }
            case 0x0008:  // REGISTER TO REGISTER ADD
            {
                ram[word0_first_half] += ram[word1]
                break;
            }
            case 0x0009:  // REGISTER TO REGISTER SUBTRACT
            {
                ram[word0_first_half] -= ram[word1]
                break;
            }
            case 0x000a:  // REGISTER TO REGISTER MULTIPLY
            {
                ram[word0_first_half] *= ram[word1]
                break;
            }
            case 0x000b:  // REGISTER TO REGISTER DIVIDE
            {
                ram[word0_first_half] /= ram[word1]
                break;
            }
            case 0x000c:  // COMPARE REGISTER TO DIRECT
            {
                if(ram[word0_first_half] == word1) {
                    pc += 2
                }
                break;
            }
            case 0x000d:  // COMPARE REGISTER TO REGISTER
            {
                if(ram[word0_first_half] == ram[word1]) {
                    pc += 2
                }
                break;
            }
            case 0x000e:  // CALL
            {
                // Code goes here
                break;
            }
            case 0x000f:  // RETURN
            {
                // Code goes here
                break;
            }
            case 0x0010:  // STRICT LESS THAN REGISTER TO DIRECT a < b
            {
                if(ram[word0_first_half] < word1) {
                    pc += 2
                }
                break;
            }
            case 0x0011:  // STRICT LESS THAN REGISTER TO REGISTER a < b
            {
                if(ram[word0_first_half] < ram[word1]) {
                    pc += 2
                }
                break;
            }
            case 0x0012:  // LESS THAN OR EQUAL REGISTER TO DIRECT a <= b
            {
                if(ram[word0_first_half] <= word1) {
                    pc += 2
                }
                break;
            }
            case 0x0013:  // LESS THAN OR EQUAL REGISTER TO REGISTER a <= b
            {
                if(ram[word0_first_half] <= ram[word1]) {
                    pc += 2
                }
                break;
            }
            case 0x0014:  // STRICT GREATER THAN REGISTER TO DIRECT a > b
            {
                if(ram[word0_first_half] > word1) {
                    pc += 2
                }
                break;
            }
            case 0x0015:  // STRICT GREATER THAN REGISTER TO REGISTER a > b
            {
                if(ram[word0_first_half] > ram[word1]) {
                    pc += 2
                }
                break;
            }
            case 0x0016:  // GREATER THAN OR EQUAL REGISTER TO DIRECT a >= b
            {
                if(ram[word0_first_half] >= word1) {
                    pc += 2
                }
                break;
            }
            case 0x0017:  // GREATER THAN OR EQUAL REGISTER TO REGISTER a >= b
            {
                if(ram[word0_first_half] >= ram[word1]) {
                    pc += 2
                }
                break;
            }
            case 0x0018: // BLIT
            {
                void* raw;
                int32_t pitch;
                SDL_LockTexture(texture, NULL, &raw, &pitch);
                uint32_t* pixels = (uint32_t*) raw;

                for(int y = 0; y < yres; y++)
                for(int x = 0; x < xres; x++)
                    pixels[x + y * xres] = 0x0000FFFF; // Keep it dumb, clear the screen with blue for now.

                SDL_UnlockTexture(texture);
                SDL_RenderCopy(renderer, texture, NULL, NULL);
                SDL_RenderPresent(renderer);
                break;
            }
            case 0x0019:  // DIRECT SQRT
            {
                ram[word0_first_half] = sqrt(double word1);
                break;
            }
            case 0x001a:  // REGISTER TO REGISTER SQRT
            {
                ram[word0_first_half] = sqrt(double ram[word1]);
                break;
            }
            case 0x001b:  // DIRECT SIN
            {
                ram[word0_first_half] = sin(double word1);
                break;
            }
            case 0x001c:  // REGISTER TO REGISTER SIN
            {
                ram[word0_first_half] = sin(double ram[word1]);
                break;
            }
            case 0x001d:  // DIRECT COS
            {
                ram[word0_first_half] = cos(double word1);
                break;
            }
            case 0x001e:  // REGISTER TO REGISTER COS
            {
                ram[word0_first_half] = cos(double ram[word1]);
                break;
            }
            case 0x0020:  // LD R[i:j] R[k]
            {
                // Code goes here
                break;
            }
            case 0x0021:  // LD R[i:j] R[k:l]
            {
                // Code goes here
                break;
            }
            case 0x0022:  // FLOOR
            {
                ram[word1] = double floor(double ram[word1]);
                break;
            }
            case 0x0023:  // CEIL
            {
                ram[word1] = double ceil(double ram[word1]);
                break;
            }
            case 0x0024:  // RAND
            {   
                int random_bit = rand() % 2;
                ram[word1] = random_bit;
                break;
            }
            case 0x0025:  // ARRAY
            {
                int label_idx = word0_first_half;
                

                uint8_t x_sprite = (rom[pc - 1] >> 24) & 0xFF;
                uint8_t y_sprite = (rom[pc - 1] >> 16) & 0XFF;
                uint8_t width_sprite = (rom[pc - 1] >> 8) & 0XFF;
                uint8_t height_sprite = (rom[pc - 1]) & 0xFF;

                // WIP

                break;
            }
            case 0x0100:  // LD R[U] R[V]
            {
                // Code goes here
                break;
            }
            case 0x0101:  // LD R[U:V] R[Y]
            {
                // Code goes here
                break;
            }
            case 0x0102:  // LD R[U:V] R[Y:Z]
            {
                // Code goes here
                break;
            }
            case 0x0103:  // LD R[U:V] R[i]
            {
                // Code goes here
                break;
            }
            case 0x0104:  // LD R[U] R[i]
            {
                // Code goes here
                break;
            }
            case 0x0105:  // LD R[U] i
            {
                // Code goes here
                break;
            }
            case 0x0106:  // LD R[U:V] i
            {
                // Code goes here
                break;
            }
            case 0x0107:  // COMPARE UV TO DIRECT
            {
                // Code goes here
                break;
            }
            case 0xfff0:  // POP
            {
                // Code goes here
                break;
            }
            case 0xfff1:  // PUSH
            {
                // Code goes here
                break;
            }
            case 0xfff2:  // CLEAR
            {
                void* raw;
                int32_t pitch;
                SDL_LockTexture(texture, NULL, &raw, &pitch);
                uint32_t* pixels = (uint32_t*) raw;

                for(int y = 0; y < yres; y++)
                for(int x = 0; x < xres; x++)
                    pixels[x + y * xres] = word1;

                SDL_UnlockTexture(texture);
                SDL_RenderCopy(renderer, texture, NULL, NULL);
                SDL_RenderPresent(renderer);
                break;
            }
            case 0xFFFF:
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
