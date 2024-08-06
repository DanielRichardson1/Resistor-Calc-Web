from matplotlib import pyplot as plt
from colorMask import get_red_mask, get_black_mask

from cropDetectedObjects import crop_detected_objects, rotate_image_to_align, save_images
import cv2
import numpy as np

# Example usage with your existing functions
cropped_images = crop_detected_objects("images/all.JPG")


# reds
# (230, 73, 57) (240, 92, 67) (242, 91, 68) (241, 86, 57) (239, 98, 77)
# Incorrectly classified: pink(165, 72, 98), brown(180, 97, 60)(166, 87, 44)

# blacks
# (29, 24, 11) (37, 49, 43) (89, 95, 74) (44, 40, 24) (46, 35, 22) (36, 31, 9) (56, 53, 35)

count = 0
for image in cropped_images:
    red_mask = get_red_mask(image)
    black_mask = get_black_mask(image)
    red_result = cv2.bitwise_and(image, image, mask=red_mask)
    black_result = cv2.bitwise_and(image, image, mask=black_mask)
    cv2.imwrite(f'images/red{count}.jpg', red_result)
    cv2.imwrite(f'images/black{count}.jpg', black_result)
    count += 1

# RGB -> HSV:

# black (29, 24, 9)
# brown (162, 83, 42) (168, 88, 43)
# red (230, 77, 60)
# orange
# yellow (239, 205, 53)
# green (124, 194, 123) (123, 193, 122)
# blue
# violet (230, 77, 60)
# grey
# white
# gold
# silver

# get RGB, convert to HSV range, ensure no overlapping, test

rgb = {
    'black': np.uint8([[[29, 24, 9]]]),
    'brown': np.uint8([[[162, 83, 42]]]),
    'red': np.uint8([[[230, 77, 60]]]),
    'orange': np.uint8([[[237, 130, 0]]]),
    'yellow': np.uint8([[[239, 205, 53]]]),
    'green': np.uint8([[[124, 194, 123]]]),
    'blue': np.uint8([[[93, 101, 202]]]),
    'violet': np.uint8([[[230, 77, 60]]]),
    'grey': np.uint8([[[193, 193, 193]]]),
    'white': np.uint8([[[248, 250, 236]]])
    # 'gold': (),
    # 'silver': ()
}

hsv = {}
for key, value in rgb.items():
    hsv[key] = cv2.cvtColor(value, cv2.COLOR_RGB2HSV)

for key, value in hsv.items():
    print(f'{key}: {value}')