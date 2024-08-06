import cv2
import numpy as np


# according to documents, get HSV, then Lower = [H-10, 100, 100], Higher = [H+10, 255, 255]
# hue range is [0,179], saturation range is [0,255], and value range is [0,255]

def get_red_mask(image):
    # Read the image
    # image = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of the red color in the HSV space
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create two masks to cover the red color range
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the masks
    red_mask = cv2.bitwise_or(mask1, mask2)

    return red_mask


def get_black_mask(image):
    # Read the image
    # image = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of the black color in the HSV space
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])

    # Create a mask to cover the black color range
    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)

    return black_mask


def get_brown_mask(image):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of the brown color in the HSV space
    lower_brown = np.array([0, 0, 0])
    upper_brown = np.array([180, 255, 50])

    # Create a mask to cover the brown color range
    brown_mask = cv2.inRange(hsv_image, lower_brown, upper_brown)

