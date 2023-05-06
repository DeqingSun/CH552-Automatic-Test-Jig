from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    try:
        from pynput import keyboard
    except ImportError:
        #nah, no X? just pass
        exit(0)

from pynput import keyboard
from ch559_jig_code import CH559_jig
import time

keyboard_input = ""

def on_press(key):
    global keyboard_input
    try:
        keyboard_input = keyboard_input+(key.char)
    except AttributeError:
        pass

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

pins_and_outputs = [[ch559_jig.PIN_CH552_P30_X,"a"],[ch559_jig.PIN_CH552_P31_X,"Hello"]]

ch559_jig.digital_write(25,True)

time.sleep(0.1)

listener = keyboard.Listener(on_press=on_press)
listener.start()

for pin_and_output in pins_and_outputs:
    pin = pin_and_output[0]
    output = pin_and_output[1]
    ch559_jig.connect_pins(pin,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
    time.sleep(0.1)
    keyboard_input = ""
    ch559_jig.digital_write(25,False)
    time.sleep(0.1)
    ch559_jig.digital_write(25,True)
    time.sleep(0.1)
    if (keyboard_input != output):
        print(f"CH559 keyboard input {keyboard_input} not match output {output}")
        exit(1)

    ch559_jig.disconnect_pins(pin,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)
