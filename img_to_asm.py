import PIL
from PIL import Image
from PIL.Image import core as _imaging

from util import rgba_tuple_to_int

import numpy as np

DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 120
PIXEL_MULTIPLIER = 2
VRAM_INDEX_START = 4101

ASM_SCRIPT = ''
ASM_FILENAME = 'asm/img_to_asm.asm'
# image_filename = 'imgs/gustav.jpg'
image_filename = 'imgs/smb2.jpg'

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


pixel_values = get_image(image_filename)

for x in range(  min(len(pixel_values), DISPLAY_WIDTH)  ):
    for y in range(  min(len(pixel_values[0]), DISPLAY_HEIGHT)  ):

        r = pixel_values[y][x][0]
        g = pixel_values[y][x][1]
        b = pixel_values[y][x][2]

        ASM_SCRIPT += 'LD R[%s] %s \n' %(VRAM_INDEX_START + x + y * DISPLAY_WIDTH,
                                         rgba_tuple_to_int(r,g,b,255))


ASM_SCRIPT += 'BLIT\n'
# add infinite loop so I can keep looking at image
ASM_SCRIPT += 'INFINITE_LOOP123:   \nGOTO INFINITE_LOOP123\n'

file = open(ASM_FILENAME, 'w')
file.write(ASM_SCRIPT)
file.close()
