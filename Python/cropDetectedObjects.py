import cv2
import base64
import os
from inference_sdk import InferenceHTTPClient
import supervision as sv
import numpy as np


def crop_detected_objects(image_file, output_dir="cropped_objects"):
    # Initialize the client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="2qLodEpMDdF8DZbeOJBN"
    )

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the image
    image = cv2.imread(image_file)
    if image is None:
        raise ValueError("Image not found or unable to read.")

    # Encode the image if needed
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Run inference on the image
    results = CLIENT.infer(image_base64, model_id="resistor-framer/1")

    # Ensure the results are not empty
    if not results:
        raise ValueError("No results returned from the inference.")

    # Process the results using supervision
    detections = sv.Detections.from_inference(results)

    # Array to store cropped images
    cropped_images = []

    # Crop and save each detected object
    for idx, detection in enumerate(detections):
        # Extract bounding box coordinates, assuming they are in (x1, y1, x2, y2) format
        x1, y1, x2, y2 = map(int, detection[0])

        # Crop the image
        cropped_image = image[y1:y2, x1:x2]
        cropped_images.append(cropped_image)

        # Save the cropped image
        cropped_image_path = os.path.join(output_dir, f"object_{idx}.jpg")
        cv2.imwrite(cropped_image_path, cropped_image)
        print(f"Cropped image saved at: {cropped_image_path}")

    return cropped_images

# Example usage:
# cropped_images = crop_detected_objects("images/3_Resistors.jpg")


def rotate_image_to_align(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detector
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    if lines is None:
        return image, image  # Return the original image if no lines are detected

    # Find the longest line segment
    max_len = 0
    best_line = None
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length > max_len:
            max_len = length
            best_line = (x1, y1, x2, y2)

    if best_line is None:
        print('No best line found')
        return image, image  # Return the original image if no valid line is found

    x1, y1, x2, y2 = best_line
    # Calculate the angle of the line with the horizontal axis
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

    # Draw the best line on the image
    image_with_line = image.copy()
    cv2.line(image_with_line, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Determine the rotation angle to make the line horizontal
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180

    # Rotate the image to align the resistor horizontally
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return image_with_line, rotated_image


def save_images(images, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, image in enumerate(images):
        image_path = os.path.join(folder_path, f'image_{i}.jpg')
        if isinstance(image, np.ndarray):
            cv2.imwrite(image_path, image)
        else:
            print(f"Image {i} is not a valid NumPy array.")
