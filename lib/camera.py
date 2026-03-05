import cv2
import numpy as np

# camera constants
WIDTH = 640
HEIGHT = 480
CAMERA_INDEX = 0

# creates a capture device
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


if not cap.isOpened():
    print("Error: Could not open the video source")


def get_image():
    """Captures an image from the Raspbot's camera and converts it to HSV

    Returns:
        numpy array: 2D matrix of HSV values
    """

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read the camera frame")
        return None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # cv2.imshow("image", get_blue_mask(hsv))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return hsv


def get_mask(hsv, max_color):
    """Applies a specific mask to the given image

    Args:
        hsv (numpy array): image in HSV format
        max_color (str): command color with the heighest pixel count

    Returns:
        numpy array: the hsv image after applying a certain mask (fileters the given max_color)
    """

    if max_color == "red":
        return get_red_mask(hsv)
    elif max_color == "green":
        return get_green_mask(hsv)
    elif max_color == "blue":
        return get_blue_mask(hsv)
    else:
        return None


def get_red_mask(hsv):
    """Higlights areas with red color

    Args:
        hsv (numpy array): image in HSV format

    Returns:
        numpy array: the hsv image after filtering red color
    """

    lower_red_1 = np.array([0, 100, 100])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 100, 100])
    upper_red_2 = np.array([180, 255, 255])

    red_mask = cv2.inRange(hsv, lower_red_1, upper_red_1) + cv2.inRange(
        hsv, lower_red_2, upper_red_2
    )

    return red_mask


def get_green_mask(hsv):
    """Higlights areas with green color

    Args:
        hsv (numpy array): image in HSV format

    Returns:
        numpy array: the hsv image after filtering green color
    """

    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    return green_mask


def get_blue_mask(hsv):
    """Higlights areas with blue color

    Args:
        hsv (numpy array): image in HSV format

    Returns:
        numpy array: the hsv image after filtering blue color
    """

    lower_blue = np.array([90, 50, 150])
    upper_blue = np.array([130, 255, 255])

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    return blue_mask


# for testing - draws the average positon on the image
def draw_average_pos(img, majority_color, avg_pos):
    cv2.circle(img, avg_pos, 10, (0, 255, 255), -1)
    cv2.putText(
        img,
        majority_color,
        (10, 25),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (255, 0, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("Circle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows
