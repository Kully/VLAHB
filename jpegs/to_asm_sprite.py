import re

import PIL
from PIL import Image
from PIL.Image import core as _imaging

import numpy as np
import time


def int_to_hex(i):
    if re.match(REGEX_HEX, str(i)):
        i = int(i, 16)

    return hex(int(i))[2:]


def rgba_tuple_to_hex(r,g,b,a):
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    if a > 255:
        a = 255

    r_hex = int_to_hex(r).zfill(2)
    g_hex = int_to_hex(g).zfill(2)
    b_hex = int_to_hex(b).zfill(2)
    a_hex = int_to_hex(a).zfill(2)
    return r_hex + g_hex + b_hex + a_hex


# constants
DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 120
VRAM_INDEX_START = 4101
REGEX_HEX = r'0X[0-9a-fA-F]+'

asm_filename = 'jpg.asm'


list_of_images = [
    # 'Capemario1.jpeg',
    # 'Capemario2.jpeg',
    # 'Capemario3.jpeg',
    # 'Capemario4.jpeg',
    'Capemario4_alpha.jpeg',
]


def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
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


asm_script = ''
for idx, image_filename in enumerate(list_of_images):

    pixel_values = get_image(image_filename)
    image_filename_stripped = image_filename.replace('.jpeg', '')
    image_filename_stripped = image_filename_stripped.replace('.', '')

    width_sprite = pixel_values.shape[0]
    height_sprite = pixel_values.shape[1]

    asm_script += '// %s %s' %(width_sprite, height_sprite)
    asm_script += 'SPRITE_%s_%s:\n' %(image_filename_stripped, idx)
    for y in range(height_sprite):
        for x in range(width_sprite):
            r = pixel_values[y][x][0]
            g = pixel_values[y][x][1]
            b = pixel_values[y][x][2]

            color = rgba_tuple_to_hex(r,g,b,255).upper()
            asm_script += '    0X%s\n' %( color )

    asm_script += '\n'


file = open(asm_filename, 'w')
file.write(asm_script)
file.close()
