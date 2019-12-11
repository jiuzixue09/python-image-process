import collections
from typing import Dict

import numpy as np
from PIL import Image
from PIL import ImageChops
from scipy.fftpack import dct

from phash.GifPhash import gif_to_sample_img


def trim(im, border):

    bg = Image.new(im.mode, im.size, border)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -50)
    # diff.show()     # show the effect
    # diff = ImageChops.add(diff, diff)
    bbox = diff.getbbox()

    if bbox:
        return im.crop(bbox)
    else:
        # found no content
        raise ValueError("cannot trim; image was empty")


def image_to_hash(img, hash_size=8, highfreq_factor=4, times=1) -> Dict:
    """
    Perceptual Hash computation.

    Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    :param img: a PIL instance
    :param hash_size:
    :param highfreq_factor:
    :param times:
    :return: (state, binary hash code) state 1 means the image was cropped
    """
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    img_size = hash_size * highfreq_factor
    if isinstance(img, Image.Image):
        image = img
    else:
        image = Image.open(img)

    flag = 0
    if image.format == 'GIF' and image.n_frames > 1:
        image = gif_to_sample_img(image)
        flag = 2

    l_image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(l_image)

    dst = dct(dct(pixels, axis=0), axis=1)  # the dct

    bit_string = None
    if flag != 2:
        frequency = count_array_frequency(pixels)
        if (sum([x[1] for x in frequency[0:5]]) / img_size ** 2) > 0.7 and times == 1:
            trim_img = trim(image, image.getpixel((3, 3)))
            # crop_img.save(img.replace('.', '_crop.'), "JPEG")
            # from phash import FigureUtil as fu
            # fu.figure_save(image, trim_img, img.replace('.', '_crop.'))
            if image.size != trim_img.size:
                bit_string = image_to_hash(trim_img, hash_size, highfreq_factor, times + 1)['phash']
                flag = 1

    if not bit_string:
        d = dst[1:hash_size + 1, 1:hash_size + 1]
        avg = np.median(d)
        # bit_string = binary_array_to_binary_str(d > avg)
        bit_string = binary_array_to_binary_str(d > avg)

    return {"phash": bit_string, "flag": flag}


def binary_array_to_binary_str(arr) -> str:
    """
    make a binary string out of a binary array.

    :param arr: binary array
    :return: binary string
    """
    bit_string = ''.join(str(b) for b in 1 * arr.flatten())
    return bit_string


def binary_array_to_hex(arr) -> str:
    """
    make a hex string out of a binary array.

    :param arr: binary array
    :return: hex string
    """
    bit_string = binary_array_to_binary_str(arr)
    width = int(np.ceil(len(bit_string) / 4))
    return '{:0>{width}x}'.format(int(bit_string, 2), width=width)


def hex_to_hash(hexstr):
    hash_size = int(np.sqrt(len(hexstr) * 4))
    binary_array = '{:0>{width}b}'.format(int(hexstr, 16), width=hash_size * hash_size)
    return binary_array


def count_array_frequency(arr):
    return collections.Counter(arr.flatten()).most_common()


def hamming_distance(bit_string1, bit_string2) -> int:
    """
    calculate the Hamming distance between two strings.

    A distance of zero indicates that it is likely a very similar picture (or a variation of the same picture).
    A distance of 5 means a few things may be different, but they are probably still close enough to be similar.
    But a distance of 10 or more? That's probably a very different picture.

    :param bit_string1:
    :param bit_string2:
    :return:
    """
    return sum(c1 != c2 for c1, c2 in zip(bit_string1, bit_string2))
