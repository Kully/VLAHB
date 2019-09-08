import re

import PIL
from PIL import Image
from PIL.Image import core as _imaging

import numpy as np
import time

from util import int_to_hex, rgba_tuple_to_hex, REGEX_HEX

# constants
DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 144
VRAM_INDEX_START = 4101
REGEX_HEX = r'0X[0-9a-fA-F]+'
ASM_FILENAME = 'output.asm'
PATH_TO_IMAGES_DIR = 'imgs_and_gifs/'


list_of_images_and_gifs = [
    'SPRITE_TETRIS_TETROMINO_S_ROT0.jpg',
    'SPRITE_TETRIS_TETROMINO_Z_ROT0.jpg',
    'SPRITE_TETRIS_TETROMINO_Z_ROT1.jpg',
    # 'tetris_layout.jpg',
]


def get_image(image_path, imgScale):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size  # original w, h

    # resize image
    image = image.resize((imgScale * width, imgScale * height), resample=Image.NONE)
    width, height = image.size

    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None

    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values


def convert_list_of_images_and_gifs_to_sprites_in_output_asm(imgScale):
    asm_script = ''
    for idx, image_filename in enumerate(list_of_images_and_gifs):

        # compute array of pixel
        path_to_img = PATH_TO_IMAGES_DIR + image_filename
        pixel_values = get_image(path_to_img, imgScale)

        # remove strange symbols
        image_filename_stripped = image_filename
        for str_to_replace in ['jpg', 'jpeg', '.', '/', '-']:
            image_filename_stripped = image_filename_stripped.replace(
                str_to_replace, ''
            )

        # compute width and height of sprite
        width_sprite = pixel_values.shape[0]
        height_sprite = pixel_values.shape[1]

        # write width and height as //comment about LABEL:
        asm_script += '// %s %s\n' %(width_sprite, height_sprite)
        label_name = '%s_X%s:\n' %(image_filename_stripped, imgScale)
        asm_script += label_name.upper()

        # put all pixels into array
        flattened_array_of_pixels = []
        for x in range(width_sprite):
            # print("x: %r" %x)
            for y in range(height_sprite):
                r = pixel_values[x][y][0]
                g = pixel_values[x][y][1]
                b = pixel_values[x][y][2]

                color = rgba_tuple_to_hex(r,g,b,255).upper()
                # print("    y: %s, %s" %(y, color))

                if color == 'FFFFFFFF':
                    color = 'FFFFFF00'
                asm_script += '    0X%s\n' %(color)

    # TODO: replace with "if LABEL in sprites.asm, replace it there" option
    file = open(ASM_FILENAME, 'w')
    file.write(asm_script)
    file.close()

if __name__ == "__main__":
    convert_list_of_images_and_gifs_to_sprites_in_output_asm(imgScale=8)
