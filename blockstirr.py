from random import randint
import numpy as np
import numpy.typing as npt


def iteration(p, c, s, input, output, cache, width, height):
    """
    Performs one iteration of the transformation processing one block.

            Parameters:
                    p (int):        block (pixel) size
                    c (int):        trigger level
                    s (int):        step / width
                    n (int):        scans
                    input (array):  input image array
                    output (array): output image array
                    cache (dict):   cache of the current iteration
                    width (int):    image width
                    height (int):   image height

            Returns:
                    input (array):  input image array
                    output (array): output image array
                    cache (dict):   cache of the current iteration
    """

    restart = False

    yrange = np.arange(s * 2, height - p - s, s)
    xrange = np.arange(s * 2, width - p - s, s)
    lcache = cache[(p, s)]

    for y in yrange:
        if restart:
            break
        for x in xrange:
            if not lcache[(y, x)]:
                continue
            sub = input[y : y + p, x : x + p]
            subsum = sub.sum() / 255 / (p * p)
            if subsum <= c:
                output[y + s : y + p - s, x + s : x + p - s] = 0
                input[y - s : y + p + s, x - s : x + p + s] = 255
                cache[(p, s)][(y, x)] = False
                restart = True
                break

    return output, input, cache


def get_cache(p, s, c, width, height, input):
    result = {}

    yrange = np.arange(s * 2, height - p - s, s)
    xrange = np.arange(s * 2, width - p - s, s)

    for y in yrange:
        for x in xrange:
            sub = input[y : y + p, x : x + p]
            subsum = sub.sum() / 255 / (p * p)
            result[(y, x)] = subsum <= c

    return result


def transform(
    input: npt.NDArray,
    iterations: int,
    min_p: int,
    max_p: int,
    min_s: int = 1,
    max_s: int = 3,
) -> npt.NDArray:
    """
    Transform the input array input blocks.

            Parameters:
                    input (numpy.ndarray):  black and white image
                    iterations (int):       number of iterations on the image
                    min_p (int):            minimum block size
                    max_p (int):            maximum block size
                    min_s (int):            minimum spacing around blocks
                    max_s (int):            maximum spacing around blocks

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    """
    width, height = input.shape
    result = np.ones((height, width), dtype=np.uint8) * 255

    cache = {}
    for p in range(min_p, max_p + 1):
        for s in range(min_s, max_s + 1):
            cache[(p, s)] = get_cache(p, s, 0.1, width, height, input)

    for _ in range(iterations):
        result, input, cache = iteration(
            randint(min_p, max_p),
            0.1,
            randint(min_s, max_s),
            input,
            result,
            cache,
            width,
            height,
        )

    return result
