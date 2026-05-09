# Embedded Systems Project - Group 06

Created a real-time system, using round-robing scheduling, for a robot to engage in certain behaviors when the camera senses an associated command color.

## What the Code Does

This project implements a simple RTOS-style controller for the Yahboom RASPBOT v2 in Python. The program begins with a startup action that rotates the robot 360 degrees to show initialization was successful. After that, it enters a round-robin loop that repeatedly captures a camera frame, counts red, green, and blue command-color pixels, determines which command color is dominant, estimates that object's average image position, and runs the matching robot behavior.

The robot behaviors are:

- `IdleAction`: stop the robot when no command color is detected
- `GreenAction`: rotate the robot body until the green object is centered horizontally in the camera image
- `BlueAction`: move the robot sideways until the blue object is centered horizontally in the camera image
- `RedAction`: rotate the robot about 180 degrees away from the red object
- `TimerCheck`: stop execution after too much idle time for safety

## OpenCV and HSV Filtering

OpenCV is used in `lib/camera.py` to read frames from the RASPBOT camera with `cv2.VideoCapture`. Each frame is converted from BGR color format to HSV color format using `cv2.cvtColor`.

HSV filtering is used because it is easier to isolate colors by hue range than in raw BGR values. The program creates separate masks for red, green, and blue by defining lower and upper HSV bounds and applying `cv2.inRange`. Red uses two HSV ranges because red wraps around the hue scale. Each mask highlights pixels that fall inside that color's threshold range. The code then counts the nonzero pixels in each mask to find the dominant command color, and uses the average position of the matching pixels to estimate where the colored card is located in the image.

## Python Files

- `main.py`: main RTOS-style program. It performs startup, runs the round-robin scheduler, checks the safety timer, counts color pixels, finds the command-color position, and triggers the robot actions.
- `lib/camera.py`: camera and computer-vision helper functions. It opens the camera, captures images, converts frames to HSV, builds red/green/blue masks, and provides helper functions for locating colored regions.
- `lib/movement.py`: movement helper functions for the mecanum-wheel robot. It provides forward, backward, sideways, diagonal, and rotation movement commands, plus stop functions. Provided by Yahboom.
- `lib/raspbot.py`: low-level hardware control library. It sends I2C commands to the RASPBOT controller board for motors, servos, LEDs, and other onboard hardware features. Provided by Yahboom.

## Prerequisite

- Install the latest version of `python` on your system. [Python Download](https://www.python.org/downloads)
- Install `uv` for python package/environment management. [uv Download](https://docs.astral.sh/uv/getting-started/installation/)

## Raspbot Resources

- Raspbot documentation - <https://www.yahboom.net/study/RASPBOT-V2>
- Raspbot sample code - <https://github.com/YahboomTechnology/Raspbot-V2>
- Raspbot Wi-Fi
  - SSID - `Raspbot-group06`
  - Password - `12345678`
- Raspbot IP address - `192.168.1.11`
- Raspbot default user
  - Username - `pi`
  - Password - `yahboom`

## Development Setup (on your computer)

### Clone Repository

- Open a new terminal
- Enter the following commands:
  - `git clone https://github.com/heavydriver/embedded-project.git`
  - `cd embedded-project`

### Setup Environment

- Open a new terminal and `cd` to the `embedded-project` directory
- Enter the following commands:
  - `uv sync`
  - `uv add -r requirements.txt`
  - `.venv\Scripts\activate.bat` (for Windows) <br /> `source .venv/bin/activate` (for Mac/Linux)

### Running the Program

- Open a new terminal and `cd` to the `embedded-project` directory
- Use any one of the following commands:
  - `uv run main.py`
  - `python main.py`

## Raspbot Setup

### Connecting to Raspbot over SSH

- Connect to the `Raspbot-group06` Wi-Fi network (password = `12345678`)
- Open a new terminal
- Enter the following command:
  - `ssh pi@192.168.1.11` (password = `yahboom`)

### Transferring code to Raspbot

#### Option 1 - scp

- Connect to the `Raspbot-group06` WIFI network (password = `12345678`)
- Open a new terminal and `cd` to the `embedded-project` directory
- Enter the following command:
  - `scp ./main.py pi@192.168.1.11:~/embedded-project/main.py` (password = `yahboom`)

#### Option 2 - WinSCP, Commander One, FileZilla

- Connect to the `Raspbot-group06` WIFI network (password = `12345678`)
- Use the following config:
  - Mode/Type - SFTP or FTP
  - IP/Host - `192.168.1.11`
  - Port - `22`
  - Password - `yahboom`
- Navigate to `/home/pi/embedded-project` on the remote file system (Raspbot)
- Copy the `main.py` from you local machine to the remote machine (Raspbot)

### Executing Code on Raspbot

- SSH into Raspbot (see instructions [above](#connecting-to-raspbot-over-ssh))
- Execute the following commands:
  - `sh /home/pi/project_demo/raspbot/killprocess.sh` (only execute once whenever you reboot the Raspbot)
  - `cd ~/embedded-project`
  - `python main.py`

## Git Commands

- Create a new branch with your name - `git checkout -b <your-name>` (remove the angle brackets <, >)

- Make changes to your code, add your changes with `git add .` (adds all new/modified files to staging area)

- Commit your code - `git commit -m "some message"`

- Push your code to GitHub - `git push origin <your-name>`

- Occasionally do `git pull origin main` to sync with the main branch (always `commit` your changes before running a `git pull`)
