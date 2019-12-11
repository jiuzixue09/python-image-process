import time

import cv2


def resize(img, width=680, height=None):
    if isinstance(img, str):
        image = cv2.imread(img)
    else:
        image = img

    if image.shape[1] > width:
        if height is None:
            ratio = (width/image.shape[1])
            height = int(image.shape[0] * ratio)

        resized = cv2.resize(image, (width, height))
    else:
        resized = image

    return resized


def byte_array_image_resize(mat):
    resized = resize(mat)
    file_name = str(int(time.time() * 1000)) + '.jpg'
    cv2.imwrite(file_name, resized)
    return file_name


def image_resize(img, filename, width=680, height=None):
    resized = resize(img, width, height)
    cv2.imwrite(filename, resized)

    return filename

