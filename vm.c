#include <stdio.h> 
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>

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
    const int xres = 800;
    const int yres = 640;
    SDL_Window* window = SDL_CreateWindow("VLAB VM", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, xres, yres, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STREAMING, xres, yres);
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
            case 0x0018:
            {
                void* raw;
                int32_t pitch;
                SDL_LockTexture(texture, NULL, &raw, &pitch);
                uint32_t* pixels = (uint32_t*) raw;

                for(int x = 0; x < xres; x++)
                for(int y = 0; y < yres; y++)
                    pixels[x + y * xres] = 0x0000FFFF; // Keep it dumb, clear the screen with blue for now.

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
                printf("error: caught unknown instruction 0x%04X\n", lower);
                exit(1);
            }
        }
    }
    fclose(fp);
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyTexture(texture);
}
