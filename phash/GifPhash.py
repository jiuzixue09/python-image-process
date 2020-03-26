from PIL import Image, ImageSequence
import numpy as np


def gif_to_sample_img(image, columns=2, rows=2):
    if columns != rows:
        raise ValueError("columns and rows values must be the same")
    all_frames = ImageSequence.all_frames(image)

    width, height = all_frames[0].size
    total_width = width << 1
    total_height = height << 1
    frame_size = columns * rows

    if image.n_frames >= frame_size:
        frames = [all_frames[int(x)] for x in np.linspace(0, image.n_frames - 1, frame_size)]
    else:
        frames = all_frames
        if len(frames) == columns:
            total_height = height
        else:
            frames.append(all_frames[0])

    new_img = Image.new('L', (total_width, total_height))

    offsets = [(width * c, height * r) for r in range(rows) for c in range(columns)]
    for index, f in enumerate(frames):
        new_img.paste(f, offsets[index])

    return new_img
