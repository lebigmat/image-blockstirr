from tqdm import tqdm
import numpy as np
from PIL import Image

import click
import imageio

import blockstirr


def load_image_as_array(filename):
    with Image.open(filename) as im:
        input = np.array(im.convert("F"))
    return input


@click.command()
@click.option("--merge", is_flag=True, help="Merge into animation")
@click.option("--norender", is_flag=True, help="Do not render frames")
@click.option("--frames", default=1, type=int, help="Number of images")
@click.option("--inputname", required=True, type=str, help="Input filename")
@click.option("--outputname", required=True, help="Output filename")
def process(inputname, outputname, frames, merge, norender):
    input_array = load_image_as_array(inputname)
    width, height = input_array.shape

    min_block_size = int(min(width, height) / 50)
    max_block_size = int(min(width, height) / 20)
    min_spacing = 1
    max_spacing = max(1, int(min(width, height) / 150))

    images_filenames = []
    for i in tqdm(range(frames)):
        outfilename = f"{outputname}_{str(i).zfill(2)}.png"
        if not norender:
            output_array = blockstirr.transform(
                np.copy(input_array),
                400,
                min_block_size,
                max_block_size,
                min_spacing,
                max_spacing,
            )
            Image.fromarray(output_array).convert("RGB").save(outfilename)
        if merge:
            images_filenames.append(outfilename)

    if merge:
        images = []
        for image_filename in images_filenames:
            images.append(imageio.imread(image_filename))
        imageio.mimsave(f"{outputname}.gif", images, fps=30)


if __name__ == "__main__":
    process()
