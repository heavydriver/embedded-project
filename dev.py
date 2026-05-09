from lib.movement import *
from lib.camera import *
import numpy as np
import time
from datetime import datetime, timedelta

# constants
ROTATE_180_TIME = timedelta(seconds=1.3)  # in seconds
ROTATE_360_TIME = 2.665  # in seconds
MIN_COLOR_THRESHOLD = 5000
MAX_IDLE_TIME = timedelta(seconds=20)  # in seconds
GREEN_ACTION_TOLERANCE = 80  # in pixels
BLUE_ACTION_TOLERANCE = 50  # in pixels


def round_robin():
    start_time = datetime.now()
    last_action_time = start_time

    red_rotation_start_time = None

    while True:
        if timer_check(last_action_time):
            stop_robot()
            break

        img = get_image()
        color_counts = color_counter(img)
        max_color, avg_pos = color_locator(img, color_counts)

        if max_color != None or red_rotation_start_time != None:
            last_action_time = datetime.now()

        if red_rotation_start_time != None:
            red_rotation_start_time = red_action(red_rotation_start_time)
        elif max_color == "green":
            green_action(avg_pos)
        elif max_color == "blue":
            blue_action(avg_pos)
        elif max_color == "red":
            if red_rotation_start_time is None:
                red_rotation_start_time = datetime.now()

            red_rotation_start_time = red_action(red_rotation_start_time)
        else:
            idle_action()

        print(color_counts)

        time.sleep(0.05)


def startup_action():
    rotate_right(40)
    time.sleep(ROTATE_360_TIME)
    stop_robot()


def timer_check(last_action_time):
    if datetime.now() - last_action_time > MAX_IDLE_TIME:
        return True

    return False


def color_counter(image):
    """Counts the number of pixels which match the command colors

    Args:
        image (numpy array): the image from the raspbot camera

    Returns:
        dictionary: command colors and their associated counts
    """

    red_count = int(np.count_nonzero(get_red_mask(image)))
    green_count = int(np.count_nonzero(get_green_mask(image)))
    blue_count = int(np.count_nonzero(get_blue_mask(image)))

    color_counts = {"red": red_count, "green": green_count, "blue": blue_count}

    return color_counts


def color_locator(image, color_counts):
    """Gets the 2D position of the object which has the highest command color count

    Args:
        image (numpy array): the image from the raspbot camera
        color_counts (dictionary): command colors and their associated counts

    Returns:
        str: command color with the highest pixel count
        (int, int): x and y position of the command color object
    """

    max_color = max(color_counts, key=color_counts.get)

    if color_counts[max_color] < MIN_COLOR_THRESHOLD:
        return None, None

    mask = get_mask(image, max_color)

    rows, cols = np.where(mask > 0)

    avg_row = int(np.mean(rows))
    avg_col = int(np.mean(cols))

    # (x, y)
    avg_pos = (avg_col, avg_row)

    # for testing
    # draw_average_pos(image, max_color, avg_pos)

    return max_color, avg_pos


def idle_action():
    stop_robot()


def green_action(p_vector):
    if p_vector is None:
        stop_robot()
        return

    center_x = WIDTH // 2
    dx = p_vector[0] - center_x

    if abs(dx) <= GREEN_ACTION_TOLERANCE:
        stop_robot()
    elif dx > 0:
        rotate_right(10)
    else:
        rotate_left(10)


def blue_action(p_vector):
    if p_vector is None:
        stop_robot()
        return

    center_x = WIDTH // 2
    dx = p_vector[0] - center_x

    if abs(dx) <= BLUE_ACTION_TOLERANCE:
        stop_robot()
    elif dx > 0:
        move_right(20)
    else:
        move_left(20)


def red_action(start_time):
    if datetime.now() - start_time < ROTATE_180_TIME:
        rotate_left(40)
        return start_time
    else:
        stop_robot()
        return None


def camera_test():
    while True:
        image = get_image()
        color_counts = color_counter(image)
        avg_pos = color_locator(image, color_counts)

        print(f"Colors counts: {color_counts}")
        print(f"Average position: {avg_pos}")

        time.sleep(0.05)


def main():
    print("Hello from embedded-project!")

    startup_action()
    round_robin()


if __name__ == "__main__":
    main()
