from lib.movement import *


def main():
    print("Hello from embedded-project!")

    move_forward(100)
    time.sleep(5)
    stop_robot()


if __name__ == "__main__":
    main()
