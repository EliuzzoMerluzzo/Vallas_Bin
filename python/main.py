import random
from arduino.app_utils import *

print("PYTHON_START")


def loop():
    while True:
        Bridge.call("write_ultrasound", 3, random.randint(0, 256))


# See: https://docs.arduino.cc/software/app-lab/tutorials/getting-started/#app-run
App.run(user_loop=loop)
